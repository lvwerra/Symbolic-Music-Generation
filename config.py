import os

from icecream import ic

from util import *


d_allie = dict(
    dir_nm='Allie-Chord-Embedding',
    nm='Allie-Chord-Embedding',
    nm_data='full_song_objects.pickle'
)
fnm = f'../datasets/{d_allie["dir_nm"]}/{d_allie["nm_data"]}'
d_allie['n_entry'] = len(read_pickle(fnm)[0])


def get_tokenizer():
    # should be a one-to-one map
    n_special = 2 ** 7
    half = n_special / 2
    encoder = {
        '[SEP]': 0,  # Bar separation
        '[TRIP]': 1,  # Last quarter encoding for triplets
        '[REST]': int(half)
    }
    vocab_special = list(encoder.keys())
    # pitch midi follows after `n_special`
    encoder.update({pitch: pitch+n_special for pitch in range(2**7)})  # Per MIDI spec
    # ic(vocab_enc)
    decoder = {v: k for k, v in encoder.items()}
    # ic(vocab_dec)
    return dict(
        n_special_token=n_special,
        vocab_special=vocab_special,
        encoder=encoder,
        decoder=decoder
    )


config = {
    DIR_DSET: dict(
        Allie_Chords=d_allie,
        LMD_matched=dict(
            nm='The Lakh MIDI Dataset, Matched',
            dir_nm='Lakh-MIDI-Dataset/LMD-Matched',
        ),
        LMD_Aligned=dict(
            nm='The Lakh MIDI Dataset, Aligned',
            dir_nm='Lakh-MIDI-Dataset/LMD-Aligned',
        ),
        LMD_Cleaned=dict(
            nm='The Lakh MIDI Dataset, Cleaned',
            dir_nm='Lakh-MIDI-Dataset/LMD-Cleaned',
            song_fmt='**/*.mid',
            song_fmt_exp='**/*.mxl'
        ),
        MIDI_EG=dict(
            nm='Some hand-selected MIDI samples',
            dir_nm='MIDI-eg',
            song_fmt='*.mid'
        ),
        MXL_EG=dict(
            nm='Some hand-selected MXL samples',
            dir_nm='MXL-eg',
            song_fmt='*.mxl',
        ),
        POP909=dict(
            nm='POP909 Dataset for Music Arrangement Generation',
            dir_nm='POP909',
            song_fmt='*.mid',
            song_fmt_exp='*.mxl'
        )
    ),
    'Melody-Extraction': dict(
        tokenizer=get_tokenizer(),
        output=dict(
            BPM=120
        )
    )
}


for k in keys(config[DIR_DSET]):    # Accommodate other OS
    k = f'{DIR_DSET}.{k}'
    val = get(config, k)
    if k[k.rfind('.')+1:] == 'dir_nm':
        set_(config, k, os.path.join(*val.split('/')))


if __name__ == '__main__':
    import json
    from data_path import *

    fl_nm = 'config.json'
    ic(config)
    print(config)
    open(fl_nm, 'a').close()  # Create file in OS
    with open(f'{PATH_BASE}/{DIR_PROJ}/{fl_nm}', 'w') as f:
        json.dump(config, f, indent=4)

