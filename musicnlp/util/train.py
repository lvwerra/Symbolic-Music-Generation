import torch
from torch.utils.tensorboard import SummaryWriter
from transformers import Trainer, TrainingArguments, TrainerCallback

from .util import *
from .model import config2model_size


PT_LOSS_PAD = -100  # Pytorch indicator value for ignoring loss, used in huggingface for padding tokens


class MyTrainer(Trainer):
    def __init__(self, clm_acc_logging=True, **kwargs):
        super().__init__(**kwargs)
        self.clm_acc_logging = clm_acc_logging
        self.name = self.model.__class__.__qualname__
        self.post_init()

    def post_init(self):
        callbacks = self.callback_handler.callbacks
        # When tqdm disabled, Trainer adds a PrinterCallback, replace that with my own
        self.callback_handler.callbacks = [
            c for c in callbacks if str(c.__class__) != "<class 'transformers.trainer_callback.PrinterCallback'>"
        ]
        if self.clm_acc_logging:
            self.add_callback(ClmAccCallback(parent_trainer=self))
        else:
            self.add_callback(ColoredPrinterCallback(name=self.name, parent_trainer=self))

    def compute_loss(self, model, inputs, return_outputs=False):
        """
        Override `Trainer.compute_loss` for logging accuracy
            - Note that both training and validation calls `compute_loss`
                => Further logic needs to determine accuracy for which dataset

        Modified from https://discuss.huggingface.co/t/metrics-for-training-set-in-trainer/2461/4?u=stefanh
        """
        if self.label_smoother is not None and "labels" in inputs:
            labels = inputs.pop("labels")
        else:
            labels = None
        outputs = model(**inputs)

        # ========================== Begin of added ==========================
        inputs: Dict[str, torch.Tensor]
        if self.clm_acc_logging and 'labels' in inputs:
            from icecream import ic
            # ic(outputs)
            ic(outputs.logits)  # TODO
            preds = outputs.logits.detach().argmax(axis=-1)
            labels_ = inputs['labels'].detach()
            # CLM, predicting the next token given current, so shift
            preds, labels_ = preds[:, :-1], labels_[:, 1:]
            mask_non_pad = labels_ != PT_LOSS_PAD  # Consider only the actual tokens for accuracy
            preds_non_pad, labels_non_pad = preds[mask_non_pad], labels_[mask_non_pad]
            matches: torch.Tensor = (preds_non_pad == labels_non_pad)
            d_log = dict(src='compute_loss', acc_meta=dict(n_acc=matches.sum().item(), n_total=preds_non_pad.numel()))
            self.log(d_log)
        # ========================== End of added ==========================

        # Save past state if it exists
        # TODO: this needs to be fixed and made cleaner later.
        if self.args.past_index >= 0:
            self._past = outputs[self.args.past_index]

        if labels is not None:
            loss = self.label_smoother(outputs, labels)
        else:
            # We don't use .loss here since the model may return tuples instead of
            # ModelOutput.
            loss = outputs["loss"] if isinstance(outputs, dict) else outputs[0]

        return (loss, outputs) if return_outputs else loss


class ColoredPrinterCallback(TrainerCallback):
    """
    Supports colored terminal output, logging file write, data sent to tensorboard for plotting

    Evaluation during training **not supported**
    """
    def __init__(self, name: str = None, parent_trainer: MyTrainer = None, report2tb: bool = True):
        self.mode = 'eval'
        self.t_strt, self.t_end = None, None

        self.trainer = parent_trainer
        args, dset_tr_, md_, tokzer = (
            getattr(parent_trainer, k) for k in ['args', 'train_dataset', 'model', 'tokenizer']
        )
        lr, n_ep = args.learning_rate, args.num_train_epochs
        self.bsz = args.per_device_train_batch_size * args.gradient_accumulation_steps
        seq_max_len = len(dset_tr_[0]['input_ids'])
        n_data, md_sz = len(dset_tr_), config2model_size(md_.config)
        self.n_step = max(math.ceil(len(dset_tr_) // self.bsz), 1) * n_ep  # #step/epoch at least 1
        self.train_meta = OrderedDict([
            ('#data', n_data), ('model size', md_sz),
            ('learning rate', lr), ('batch shape', (self.bsz, seq_max_len)), ('#epochs', n_ep), ('#steps', self.n_step)
        ])

        # self.save_time = now(for_path=True)
        self.output_dir = self.trainer.args.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.save_time = self.output_dir.split(os.sep)[-1]  # expect last dir name as time stamp
        self.log_fnm = f'{name}, n={n_data}, l={md_sz}, a={lr}, bsz={self.bsz}, n_ep={n_ep}'

        if name is None:
            name = 'MyTrainer'
        self.name = f'{name} Training'
        self.logger, self.logger_fl, self.writer = None, None, None
        self.report2tb = report2tb

    def on_train_begin(self, args: TrainingArguments, state, control, **kwargs):
        self.mode = 'train'

        self.logger = get_logger(self.name)
        self.logger_fl = get_logger(
            name=self.name, typ='file-write', file_path=os.path.join(self.output_dir, f'{self.log_fnm}.log')
        )
        if self.report2tb:
            self.writer = SummaryWriter(os.path.join(self.output_dir, 'tb_log'))

        conf = self.trainer.model.config.to_dict()
        train_args = self.trainer.args.to_dict()
        self.logger.info(f'Training started with model {log_dict_pg(conf)} on {log_dict_pg(self.train_meta)} '
                         f'with training args {log_dict_pg(train_args)}... ')
        self.logger_fl.info(f'Training started with with model {log_dict_id(conf)} on {log_dict_nc(self.train_meta)} '
                            f'with training args {log_dict_id(train_args)}... ')

        self.t_strt = datetime.datetime.now()

    def on_train_end(self, args: TrainingArguments, state, control, **kwargs):
        self.t_end = datetime.datetime.now()
        t = fmt_dt(self.t_end - self.t_strt)
        self.logger.info(f'Training completed in {logi(t)} ')
        self.logger_fl.info(f'Training completed in {t} ')
        self.mode = 'eval'

    def out_dict2str(self, d: Dict, return_wo_color: bool = False):
        keys_ = [
            'step', 'epoch', 'train_loss', 'eval_loss', 'train_acc', 'eval_acc', 'learning_rate'
        ]
        fmt = [
            f':>{len(str(self.n_step))}', f':{len(str(self.trainer.args.num_train_epochs))+4}.3f',
            ':7.4f', ':7.4f', ':6.2f', ':6.2f', ':.2e'
        ]
        s_fmts = [f'{{{k}{fmt_}}}' for k, fmt_ in zip(keys_, fmt)]  # Enforce ordering

        d = {k: (
                ('loss' in k and round(v, 4)) or
                ('acc' in k and round(v * 100, 4)) or
                ('learning_rate' in k and round(v, 6)) or
                v
        ) for k, v in d.items()
        }
        s_outs = [(k, fmt_.format(**{k: d[k]})) for fmt_, k in zip(s_fmts, keys_) if k in d]
        out_ = ', '.join(f'{k}={logi(s)}' for (k, s) in s_outs)
        if return_wo_color:
            out_ = out_, ', '.join(f'{k}={s}' for (k, s) in s_outs)
        return out_

    def on_log(self, args, state, control, logs=None, **kwargs):
        if state.is_local_process_zero:
            if isinstance(logs, dict):
                # Heuristics on the training step updates, see `Trainer._maybe_log_save_evaluate`
                if self.mode == 'train' and all('runtime' not in k for k in logs):
                    logs['step'] = step = state.global_step
                    assert logs['epoch'] == round(state.epoch, 2)
                    logs['epoch'] = state.epoch  # The one originally is rounded, see `Trainer.log`
                    # Trainer internal uses `loss`, instead of `train_loss`
                    logs['train_loss'] = loss = logs.pop('loss', None)
                    assert loss is not None
                    lr = logs['learning_rate']
                    self.writer.add_scalar('Train/loss', loss, step)
                    self.writer.add_scalar('Train/learning_rate', lr, step)

                    out_console, out_write = self.out_dict2str(logs, return_wo_color=True)
                    self.logger.info(out_console)
                    self.logger_fl.info(out_write)
                else:
                    self.logger.info(log_dict(logs))
                    self.logger_fl.info(log_dict(logs, with_color=False))
            else:
                self.logger.info(logs)
                self.logger_fl.info(logs)


class ClmAccCallback(ColoredPrinterCallback):
    """
    Logs training batch accuracy during CLM training

    Needs the **prediction logits** returned
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.out_dict_tr = None
        self.k_acc = 'acc_meta'

    def on_log(self, args, state, control, logs=None, **kwargs):
        def acc_stats2dict(out_dict: Dict, prefix: str) -> Dict:
            """
            Convert `acc_meta`, `classification_acc_meta` dict to stats for logging
            """
            stats_acc: pd.Series = pd.DataFrame(out_dict[self.k_acc]).sum(axis=0)
            return {f'{prefix}_acc': stats_acc.n_acc / stats_acc.n_total}

        if self.mode == 'train':
            step = state.global_step
            assert not self.trainer.do_eval  # TODO: Not supported
            if 'src' in logs and logs['src'] == 'compute_loss':
                # For gradient_accumulation, many batches of `compute_loss` may be called
                # before going into train logging
                if self.out_dict_tr is None:
                    n_ep = logs['epoch']
                    self.out_dict_tr = {'step': step, 'epoch': n_ep, self.k_acc: [logs[self.k_acc]]}
                else:  # Later batch in the same gradient accumulation
                    step_, n_ep = self.out_dict_tr['step'], self.out_dict_tr['epoch']
                    n_ep_ = logs['epoch']
                    assert step_ == step and n_ep_ == n_ep
                    self.out_dict_tr[self.k_acc].append(logs[self.k_acc])
            elif 'loss' in logs:  # The Trainer default training loss logging
                # Take the averaging by parent `Trainer` for granted
                self.out_dict_tr.update(acc_stats2dict(self.out_dict_tr, prefix='train'))
                del self.out_dict_tr[self.k_acc]
                self.out_dict_tr['learning_rate'] = logs['learning_rate']
                self.out_dict_tr['train_loss'] = logs['loss']
                self.logger.info(self.out_dict2str(self.out_dict_tr))
                self.out_dict_tr = None  # Rest for next global step
            elif any('runtime' in k for k in logs.keys()):
                self.logger.info(log_dict(logs) if isinstance(logs, dict) else logs)
            else:
                print('unhandled case', logs)
                exit(1)
        else:
            if 'src' not in logs:  # Skip custom compute_loss logging
                super().on_log(args, state, control, logs, **kwargs)
