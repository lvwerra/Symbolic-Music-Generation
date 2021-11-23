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
        MIDI_EG=dict(
            nm='Some hand-selected MIDI samples',
            dir_nm='MIDI-eg',
            fmt_midi='*.mid'
        )
    )
}


for k in keys(config):    # Accommodate other OS
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

