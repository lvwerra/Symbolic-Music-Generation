import os
import re
import glob
import json
import pickle
import pathlib
import logging
import datetime
import itertools
import concurrent.futures
from typing import Tuple, List, Dict
from typing import Iterable, Callable, TypeVar, Union

from functools import reduce
from collections import OrderedDict

import sty
import colorama
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from musicnlp.util.data_path import PATH_BASE, DIR_PROJ, PKG_NM, DIR_DSET, DIR_MDL


pd.set_option('expand_frame_repr', False)
pd.set_option('display.precision', 2)
pd.set_option('max_colwidth', 40)

plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['figure.figsize'] = (16, 9)
sns.set_style('darkgrid')

nan = float('nan')


def flatten(lsts):
    """ Flatten list of [list of elements] to list of elements """
    return sum(lsts, [])


def clip(val, vmin, vmax):
    return max(min(val, vmax), vmin)


def np_index(arr, idx):
    return np.where(arr == idx)[0][0]


def vars_(obj, include_private=False):
    """
    :return: A variant of `vars` that returns all properties and corresponding values in `dir`, except the
    generic ones that begins with `_`
    """
    def is_relevant():
        if include_private:
            return lambda a: not a.startswith('__')
        else:
            return lambda a: not a.startswith('__') and not a.startswith('_')
    attrs = filter(is_relevant(), dir(obj))
    return {a: getattr(obj, a) for a in attrs}


def read_pickle(fnm):
    objects = []
    with (open(fnm, 'rb')) as f:
        while True:
            try:
                objects.append(pickle.load(f))
            except EOFError:
                break
    return objects


def get(dic, ks):
    """
    :param dic: Potentially multi-level dictionary
    :param ks: Potentially `.`-separated keys
    """
    ks = ks.split('.')
    return reduce(lambda acc, elm: acc[elm], ks, dic)


def set_(dic, ks, val):
    ks = ks.split('.')
    node = reduce(lambda acc, elm: acc[elm], ks[:-1], dic)
    node[ks[-1]] = val


def keys(dic, prefix=''):
    """
    :return: Generator for all potentially-nested keys
    """
    def _full(k_):
        return k_ if prefix == '' else f'{prefix}.{k_}'
    for k, v in dic.items():
        if isinstance(v, dict):
            for k__ in keys(v, prefix=_full(k)):
                yield k__
        else:
            yield _full(k)


PATH_CONF = os.path.join(PATH_BASE, DIR_PROJ, PKG_NM, 'util', 'config.json')


def config(attr, force_update=False):
    """
    Retrieves the queried attribute value from the config file.

    Loads the config file on first call.
    """
    if not hasattr(config, 'config'):
        with open(PATH_CONF, 'r') as f:
            config.config = json.load(f)
    if force_update:
        # For colab re-running; TODO: pretty ugly
        d_my = config.config['datasets']['my']
        config.config['path-export'] = os.path.join(PATH_BASE, DIR_DSET, d_my['dir_nm'])
        with open(PATH_CONF, 'w') as f_:
            json.dump(config.config, f_, indent=4)
    return get(config.config, attr)


def now(as_str=True, sep=':'):
    d = datetime.datetime.now()
    return d.strftime(f'%Y-%m-%d %H{sep}%M{sep}%S') if as_str else d  # Considering file output path


def fmt_dt(secs: Union[int, float, datetime.timedelta]):
    if isinstance(secs, datetime.timedelta):
        secs = secs.seconds + (secs.microseconds/1e6)
    if secs >= 86400:
        d = secs // 86400  # // floor division
        return f'{round(d)}d{fmt_dt(secs-d*86400)}'
    elif secs >= 3600:
        h = secs // 3600
        return f'{round(h)}h{fmt_dt(secs-h*3600)}'
    elif secs >= 60:
        m = secs // 60
        return f'{round(m)}m{fmt_dt(secs-m*60)}'
    else:
        return f'{round(secs)}s'


def sec2mmss(sec: int) -> str:
    return str(datetime.timedelta(seconds=sec))[2:]


T = TypeVar('T')
K = TypeVar('K')


def compress(lst: List[T]) -> List[Tuple[T, int]]:
    """
    :return: A compressed version of `lst`, as 2-tuple containing the occurrence counts
    """
    if not lst:
        return []
    return ([(lst[0], len(list(itertools.takewhile(lambda elm: elm == lst[0], lst))))]
            + compress(list(itertools.dropwhile(lambda elm: elm == lst[0], lst))))


def split(lst: List[T], call: Callable[[T], bool]) -> List[List[T]]:
    """
    :return: Split a list by locations of elements satisfying a condition
    """
    return [list(g) for k, g in itertools.groupby(lst, call) if k]


def join_its(its: Iterable[Iterable[T]]) -> Iterable[T]:
    out = itertools.chain()
    for it in its:
        out = itertools.chain(out, it)
    return out


def conc_map(fn: Callable[[T], K], it: Iterable[T]) -> Iterable[K]:
    """
    Wrapper for `concurrent.futures.map`

    :param fn: A function
    :param it: A list of elements
    :return: Iterator of `lst` elements mapped by `fn` with concurrency
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.map(fn, it)


def log(s, c: str = 'log', c_time='green', as_str=False):
    """
    Prints `s` to console with color `c`
    """
    if not hasattr(log, 'reset'):
        log.reset = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
    if not hasattr(log, 'd'):
        log.d = dict(
            log='',
            warn=colorama.Fore.YELLOW,
            error=colorama.Fore.RED,
            err=colorama.Fore.RED,
            success=colorama.Fore.GREEN,
            suc=colorama.Fore.GREEN,
            info=colorama.Fore.BLUE,
            i=colorama.Fore.BLUE,
            w=colorama.Fore.RED,

            y=colorama.Fore.YELLOW,
            yellow=colorama.Fore.YELLOW,
            red=colorama.Fore.RED,
            r=colorama.Fore.RED,
            green=colorama.Fore.GREEN,
            g=colorama.Fore.GREEN,
            blue=colorama.Fore.BLUE,
            b=colorama.Fore.BLUE,

            m=colorama.Fore.MAGENTA
        )
    if c in log.d:
        c = log.d[c]
    if as_str:
        return f'{c}{s}{log.reset}'
    else:
        print(f'{c}{log(now(), c=c_time, as_str=True)}| {s}{log.reset}')


def log_s(s, c):
    return log(s, c=c, as_str=True)


def logi(s):
    """
    Syntactic sugar for logging `info` as string
    """
    return log_s(s, c='i')


def log_dict(d: Dict = None, with_color=True, **kwargs) -> str:
    """
    Syntactic sugar for logging dict with coloring for console output
    """
    if d is None:
        d = kwargs
    pairs = (f'{k}: {logi(v) if with_color else v}' for k, v in d.items())
    pref = log_s('{', c='m') if with_color else '{'
    post = log_s('}', c='m') if with_color else '}'
    return pref + ', '.join(pairs) + post


def hex2rgb(hx: str) -> Union[Tuple[int], Tuple[float]]:
    # Modified from https://stackoverflow.com/a/62083599/10732321
    if not hasattr(hex2rgb, 'regex'):
        hex2rgb.regex = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$')
    m = hex2rgb.regex.match(hx)
    assert m is not None
    if len(hx) <= 4:
        return tuple(int(hx[i]*2, 16) for i in range(1, 4))
    else:
        return tuple(int(hx[i:i+2], 16) for i in range(1, 7, 2))


class MyTheme:
    """
    Theme based on `sty` and `Atom OneDark`
    """
    COLORS = OrderedDict([
        ('yellow', 'E5C07B'),
        ('green', '00BA8E'),
        ('blue', '61AFEF'),
        ('cyan', '2AA198'),
        ('red', 'E06C75'),
        ('purple', 'C678DD')
    ])
    yellow, green, blue, cyan, red, purple = (
        hex2rgb(f'#{h}') for h in ['E5C07B', '00BA8E', '61AFEF', '2AA198', 'E06C75', 'C678DD']
    )

    @staticmethod
    def set_color_type(t: str):
        """
        Sets the class attribute accordingly

        :param t: One of ['rgb`, `sty`]
            If `rgb`: 3-tuple of rgb values
            If `sty`: String for terminal styling prefix
        """
        for color, hex_ in MyTheme.COLORS.items():
            val = hex2rgb(f'#{hex_}')  # For `rgb`
            if t == 'sty':
                setattr(sty.fg, color, sty.Style(sty.RgbFg(*val)))
                val = getattr(sty.fg, color)
            setattr(MyTheme, color, val)


class MyFormatter(logging.Formatter):
    """
    Modified from https://stackoverflow.com/a/56944256/10732321

    Default styling: Time in green, metadata indicates severity, plain log message
    """
    RESET = sty.rs.fg + sty.rs.bg + sty.rs.ef

    MyTheme.set_color_type('sty')
    yellow, green, blue, cyan, red, purple = (
        MyTheme.yellow, MyTheme.green, MyTheme.blue, MyTheme.cyan, MyTheme.red, MyTheme.purple
    )

    KW_TIME = '%(asctime)s'
    KW_MSG = '%(message)s'
    KW_LINENO = '%(lineno)d'
    KW_FNM = '%(filename)s'
    KW_FUNCNM = '%(funcName)s'
    KW_NAME = '%(name)s'

    DEBUG = INFO = BASE = RESET
    WARN, ERR, CRIT = yellow, red, purple
    CRIT += sty.Style(sty.ef.bold)

    LVL_MAP = {  # level => (abbreviation, style)
        logging.DEBUG: ('DBG', DEBUG),
        logging.INFO: ('INFO', INFO),
        logging.WARNING: ('WARN', WARN),
        logging.ERROR: ('ERR', ERR),
        logging.CRITICAL: ('CRIT', CRIT)
    }

    def __init__(self, with_color=True, color_time=green):
        super().__init__()
        self.with_color = with_color

        sty_kw, reset = MyFormatter.blue, MyFormatter.RESET
        color_time = f'{color_time}{MyFormatter.KW_TIME}{sty_kw}| {reset}'

        def args2fmt(args_):
            if self.with_color:
                return color_time + self.fmt_meta(*args_) + f'{sty_kw} - {reset}{MyFormatter.KW_MSG}' + reset
            else:
                return f'{MyFormatter.KW_TIME}| {self.fmt_meta(*args_)} - {MyFormatter.KW_MSG}'

        self.formats = {level: args2fmt(args) for level, args in MyFormatter.LVL_MAP.items()}
        self.formatter = {
            lv: logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S') for lv, fmt in self.formats.items()
        }

    def fmt_meta(self, meta_abv, meta_style=None):
        if self.with_color:
            return f'{MyFormatter.purple}[{MyFormatter.KW_NAME}]' \
               f'{MyFormatter.blue}::{MyFormatter.purple}{MyFormatter.KW_FUNCNM}' \
               f'{MyFormatter.blue}::{MyFormatter.purple}{MyFormatter.KW_FNM}' \
               f'{MyFormatter.blue}:{MyFormatter.purple}{MyFormatter.KW_LINENO}' \
               f'{MyFormatter.blue}, {meta_style}{meta_abv}{MyFormatter.RESET}'
        else:
            return f'[{MyFormatter.KW_NAME}] {MyFormatter.KW_FUNCNM}::{MyFormatter.KW_FNM}' \
                   f':{MyFormatter.KW_LINENO}, {meta_abv}'

    def format(self, entry):
        return self.formatter[entry.levelno].format(entry)


def assert_list_same_elms(lst: List[T]):
    assert all(l == lst[0] for l in lst)


def eg_songs(k=None, pretty=False, fmt='MIDI'):
    """
    :return: A list of or single MIDI file path
    """
    dnm = f'{fmt}_EG'
    d_dset = config(f'{DIR_DSET}.{dnm}')
    dir_nm = d_dset['dir_nm']
    path = f'{PATH_BASE}/{DIR_DSET}/{dir_nm}'
    mids = sorted(glob.iglob(f'{path}/{d_dset["song_fmt"]}', recursive=True))
    if k:
        if type(k) is int:
            return mids[k]
        else:  # Expect str
            return next(filter(lambda p: p.find(k) != -1, mids))
    else:
        return [p[p.find(dir_nm):] for p in mids] if pretty else mids


def fl_nms(dnm, k='song_fmt') -> List[str]:
    """
    :return: List of music file paths
    """
    if not hasattr(fl_nms, 'd_dsets'):
        fl_nms.d_dsets = config('datasets')
    d_dset = fl_nms.d_dsets[dnm]
    return sorted(
        glob.iglob(os.path.join(PATH_BASE, DIR_DSET, d_dset['dir_nm'], d_dset[k]), recursive=True)
    )


def stem(path, ext=False):
    """
    :param path: A potentially full path to a file
    :param ext: If True, file extensions is preserved
    :return: The file name, without parent directories
    """
    return os.path.basename(path) if ext else pathlib.Path(path).stem


def get_extracted_song_eg(
        fnm='musicnlp music extraction, dnm=POP909, n=909, mode=melody, 2022-02-25 20-59-06',
        dir_=config('path-export')
) -> str:
    with open(os.path.join(dir_, f'{fnm}.json')) as f:
        text = json.load(f)['music'][0]['text']
    return text


if __name__ == '__main__':
    from icecream import ic

    # ic(config('Melody-Extraction.tokenizer'))

    def check_compress():
        arr = [
            202, 202, 202, 202, 203, 203, 203, 203, 202, 202, 202, 202, 203,
            203, 203, 203, 202, 202, 202, 202, 203, 203, 203, 203
        ]
        ic(compress(arr))
    # check_compress()

    def check_fl_nms():
        dnm = 'POP909'
        fnms = fl_nms(dnm)
        ic(len(fnms), fnms[:20])
        fnms = fl_nms(dnm, k='song_fmt_exp')
        ic(len(fnms), fnms[:20])
    # check_fl_nms()

    def setup_pop909():
        from shutil import copyfile
        from tqdm import trange
        dnm = 'POP909'
        path = os.path.join(PATH_BASE, DIR_DSET, 'POP909-Dataset', dnm)
        path_exp = os.path.join(PATH_BASE, DIR_DSET, dnm)
        os.makedirs(path_exp, exist_ok=True)

        df = pd.read_excel(os.path.join(path, 'index.xlsx'))
        paths = sorted(glob.iglob(os.path.join(path, '*/*.mid'), recursive=True))
        for i in trange(len(paths)):
            p = paths[i]
            rec = df.iloc[i, :]
            fnm = f'{rec["artist"]} - {rec["name"]}.mid'
            copyfile(p, os.path.join(path_exp, fnm))
    # setup_pop909()

    # ic(quarter_len2fraction(1.25), quarter_len2fraction(0.875))

    # ic(hex2rgb('#E5C0FB'))

    def check_logging():
        ic(colorama.Fore.YELLOW)
        ic(now())
        ic()
        print('normal str')

        logger = logging.getLogger('Test Logger')
        logger.setLevel(logging.DEBUG)

        import sys
        ch = logging.StreamHandler(stream=sys.stdout)  # For my own coloring
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(MyFormatter())
        logger.addHandler(ch)

        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.critical("critical message")

        res = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
        msg = colorama.Fore.YELLOW + 'my msg' + res
        logger.critical(msg)
    check_logging()

