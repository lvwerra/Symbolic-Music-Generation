from torch.utils.tensorboard import SummaryWriter
from transformers import Trainer, TrainingArguments, TrainerCallback
import datasets

from musicnlp.util.util import *


PT_LOSS_PAD = -100  # Pytorch indicator value for ignoring loss, used in huggingface for padding tokens


def _pretty_single(key: str, val, ref: Dict = None):
    if key in ['step', 'epoch']:
        k = next(iter(k for k in ref.keys() if key in k))
        lim = ref[k]
        assert isinstance(val, (int, float))
        len_lim = len(str(lim))
        if isinstance(val, int):
            s_val = f'{val:>{len_lim}}'
        else:
            fmt = f'%{len_lim+4}.3f'
            s_val = fmt % val
        return f'{s_val}/{lim}'  # Pad integer
    elif 'loss' in key:
        return f'{round(val, 4):7.4f}'
    elif any(k in key for k in ('acc', 'recall', 'auc')):
        def _single(v):
            return f'{round(v * 100, 2):6.2f}' if v is not None else '-'

        if isinstance(val, list):
            return [_single(v) for v in val]
        elif isinstance(val, dict):
            return {k: _single(v) for k, v in val.items()}
        else:
            return _single(val)
    elif 'learning_rate' in key or 'lr' in key:
        return f'{round(val, 7):.3e}'
    else:
        return val


def pretty_log_dict(d_log: Dict, ref: Dict = None):
    return {k: _pretty_single(k, v, ref=ref) for k, v in d_log.items()}


def meta2fnm_meta(meta: Dict) -> Dict:
    if not hasattr(meta2fnm_meta, 'd_key'):
        meta2fnm_meta.d_key = {
            'model name': 'nm', 'max length': 'l', 'axial_pos_shape': 'ax_pos_sp',
            'hidden_size': 'hd_sz', 'ff_size': 'ff_sz',
            'n_layer': 'n_l', 'attn_layers': 'attn', 'attention_shape': 'attn_sh',
            'parameter_count': 'n_param'
        }
    return OrderedDict((meta2fnm_meta.d_key[k_], v) for k_, v in meta.items())


class MyTrainer(Trainer):
    def __init__(self, clm_acc_logging=True, model_meta: Dict = None, my_args: Dict = None, **kwargs):
        super().__init__(**kwargs)
        self.clm_acc_logging = clm_acc_logging
        self.model_meta = model_meta
        self.model_meta['parameter_count'] = get_model_num_trainable_parameter(self.model)
        self.name = self.model.__class__.__qualname__

        self.my_args = my_args
        self.post_init()

    def post_init(self):
        callbacks = self.callback_handler.callbacks
        # When tqdm disabled, Trainer adds a PrinterCallback, replace that with my own
        self.callback_handler.callbacks = [
            c for c in callbacks if str(c.__class__) != "<class 'transformers.trainer_callback.PrinterCallback'>"
        ]
        callback_cls = ColoredPrinterCallbackForClm if self.clm_acc_logging else ColoredPrinterCallback
        if not self.clm_acc_logging:
            raise NotImplementedError('on-CLM task logging not updated')
        self.add_callback(callback_cls(name=self.name, parent_trainer=self))

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
        # don't need to calculate NTP acc here for eval, see `compute_ntp_acc`
        if self.is_in_train and self.clm_acc_logging and 'labels' in inputs:
            preds = outputs.logits.detach().argmax(axis=-1)
            labels_ = inputs['labels'].detach()
            # CLM, predicting the next token given current, so shift
            preds, labels_ = preds[:, :-1], labels_[:, 1:]
            msk_not_pad = labels_ != PT_LOSS_PAD  # Consider only the actual tokens for accuracy
            preds_non_pad, labels_non_pad = preds[msk_not_pad], labels_[msk_not_pad]
            matches: torch.Tensor = (preds_non_pad == labels_non_pad)
            # next-token-prediction task
            ntp_acc_meta = dict(matched=matches.sum().item(), total=preds_non_pad.numel())
            d_log = dict(src='compute_loss', ntp_acc_meta=ntp_acc_meta)
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
        n_data = len(dset_tr_)
        self.n_step = max(math.ceil(len(dset_tr_) / self.bsz), 1) * n_ep  # #step/epoch at least 1
        self.train_meta = OrderedDict([
            ('#data', n_data), ('batch shape', (self.bsz, seq_max_len)),
            ('#epochs', n_ep), ('#steps', self.n_step), ('learning rate', lr),
        ])

        self.output_dir = self.trainer.args.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.save_time = self.output_dir.split(os.sep)[-1]  # expect last dir name as time stamp
        meta = meta2fnm_meta(self.trainer.model_meta)
        self.log_fnm = f'md={log_dict_p(meta)}, n={n_data}, a={lr}, bsz={self.bsz}, n_ep={n_ep}'

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
            self.writer = SummaryWriter(os.path.join(self.output_dir, f'tb - {self.log_fnm}'))

        conf = self.trainer.model.config.to_dict()
        train_args = self.trainer.args.to_dict()
        meta = self.trainer.model_meta
        self.logger.info(f'Training started with model {log_dict(meta)}, {log_dict_pg(conf)} '
                         f'on {log_dict(self.train_meta)} with training args {log_dict_pg(train_args)} '
                         f'and my training args {log_dict(self.trainer.my_args)}... ')
        self.logger_fl.info(f'Training started with with model {log_dict_nc(meta)}, {log_dict_id(conf)} '
                            f'on {log_dict_nc(self.train_meta)} with training args {log_dict_id(train_args)} '
                            f'and my training args {log_dict_nc(self.trainer.my_args)}... ')
        self.t_strt = datetime.datetime.now()

    def on_train_end(self, args: TrainingArguments, state, control, **kwargs):
        self.t_end = datetime.datetime.now()
        t = fmt_dt(self.t_end - self.t_strt)
        self.logger.info(f'Training completed in {logi(t)} ')
        self.logger_fl.info(f'Training completed in {t} ')
        self.mode = 'eval'

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

                    # out_console, out_write = self.out_dict2str(logs, return_wo_color=True)  # TODO: didn't test
                    logs = pretty_log_dict(logs, ref=self.train_meta)
                    self.logger.info(log_dict(logs))
                    self.logger_fl.info(log_dict_nc(logs))
                else:
                    self.logger.info(log_dict(logs))
                    self.logger_fl.info(log_dict(logs, with_color=False))
            else:
                self.logger.info(logs)
                self.logger_fl.info(logs)


def compute_ntp_acc(eval_pred):
    """
    :param eval_pred: 2-tuple of (greedy prediction **ids**, labels)

    Will be the outputs on eval dataset, see `Trainer.compute_metrics`
    """
    if not hasattr(compute_ntp_acc, 'metric'):
        compute_ntp_acc.acc = datasets.load_metric('accuracy')
    predictions, labels = eval_pred
    predictions = predictions.argmax(axis=-1)
    predictions, labels = predictions[:, :-1], labels[:, 1:]  # For CLM
    labels, predictions = labels.flatten(), predictions.flatten()
    msk_non_pad = (labels != PT_LOSS_PAD)
    labels, predictions = labels[msk_non_pad], predictions[msk_non_pad]
    d_metric = compute_ntp_acc.acc.compute(predictions=predictions, references=labels)
    assert 'accuracy' in d_metric
    d_metric['ntp_acc'] = d_metric.pop('accuracy')
    return d_metric


no_prefix = ['epoch', 'step']


def add_prefix(key: str) -> bool:
    return key not in no_prefix


class ColoredPrinterCallbackForClm(ColoredPrinterCallback):
    """
    Additionally log next-token-prediction accuracy
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.out_dict = None  # For passing NTP accuracy in training steps

    def _log(self, d_log, mode='train', to_console=True):
        modes = ["train", "eval"]
        assert mode in ['train', 'eval'], f'Unexpected mode: expect one of {logi(modes)}, got {logi(mode)}'
        d_log_write = {f'{mode}/{k}' if add_prefix(k) else k: v for k, v in d_log.items()}
        d_log_write = pretty_log_dict(d_log_write, ref=self.train_meta)
        if to_console:
            self.logger.info(log_dict(d_log_write))
        self.logger_fl.info(log_dict_nc(d_log_write))

        step = d_log.get('step') if mode == 'train' else d_log.get('epoch')
        for k, v in d_log.items():
            if add_prefix(k):
                self.writer.add_scalar(tag=f'{mode}/{k}', scalar_value=v, global_step=step)

    def on_log(self, args, state, control, logs=None, **kwargs):
        if state.is_local_process_zero:
            if 'src' in logs and logs['src'] == 'compute_loss':
                del logs['src']
                self.out_dict = logs
            else:
                # Heuristics on the training step updates, see `Trainer._maybe_log_save_evaluate`
                if self.mode == 'train' and all('runtime' not in k for k in logs):
                    step = state.global_step
                    assert logs['epoch'] == round(state.epoch, 2)
                    n_ep = state.epoch  # The one originally is rounded, see `Trainer.log`
                    loss, lr = logs['loss'], logs['learning_rate']
                    assert self.out_dict is not None
                    ntp_acc_meta = self.out_dict['ntp_acc_meta']
                    # TODO: Potentially support gradient accumulation
                    # ntp_acc_meta = {k: sum(v for v in d[k]) for k, d in ntp_acc_meta.items()}
                    # ic(ntp_acc_meta)
                    ntp_acc = ntp_acc_meta['matched'] / ntp_acc_meta['total']

                    self.out_dict = OrderedDict([
                        ('step', step), ('epoch', n_ep), ('learning_rate', lr),
                        ('loss', loss), ('ntp_acc', ntp_acc)
                    ])

                    # `should_log` in Trainer just prevents the `on_log` call, I only filter console logging
                    should_log = False
                    my_log_strat = self.trainer.my_args.get('logging_strategy', 'steps')
                    if my_log_strat == 'steps':
                        should_log = True
                    elif my_log_strat == 'epoch' and step % self.trainer.my_args['steps_per_epoch'] == 0:
                        should_log = True
                    self._log(self.out_dict, mode='train', to_console=should_log)
                elif 'eval_loss' in logs:  # `Trainer.is_in_train` is not False so can't use
                    loss, ntp_acc = logs['eval_loss'], logs['eval_ntp_acc']
                    # Log eval on an epoch-level
                    # Evaluation finished during training; TODO: didn't verify other positive cases
                    n_ep = state.epoch
                    assert n_ep.is_integer()
                    d_log = dict(step=state.global_step, epoch=int(n_ep), loss=loss, ntp_acc=ntp_acc)
                    self._log(d_log, mode='eval', to_console=True)
                else:
                    self.logger.info(log_dict(logs))
                    self.logger_fl.info(log_dict_nc(logs))


class ClmAccCallback(ColoredPrinterCallback):
    """
    Logs training batch accuracy during CLM training

    Needs the **prediction logits** returned
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.out_dict_tr = None
        self.k_acc = 'ntp_acc'

    def on_log(self, args, state, control, logs=None, **kwargs):
        def acc_stats2dict(out_dict: Dict, prefix: str) -> Dict:
            """
            Convert `acc_meta`, `classification_acc_meta` dict to stats for logging
            """
            stats_acc: pd.Series = pd.DataFrame(out_dict[self.k_acc]).sum(axis=0)
            return {f'{prefix}_acc': stats_acc.n_acc / stats_acc.n_total}

        if self.mode == 'train':
            step = state.global_step
            assert not self.trainer.args.do_eval  # TODO: Not supported
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
                self.logger.info(pretty_log_dict(self.out_dict_tr))
                self.out_dict_tr = None  # Rest for next global step
            elif any('runtime' in k for k in logs.keys()):
                self.logger.info(log_dict(logs) if isinstance(logs, dict) else logs)
            else:
                print('unhandled case', logs)
                exit(1)
        else:
            if 'src' not in logs:  # Skip custom compute_loss logging
                super().on_log(args, state, control, logs, **kwargs)
