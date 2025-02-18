"""
Given a piece in musicxml format, return the key of the piece
 using the Krumhansl-Schmuckler key-finding algorithm.
 TODO:What if there are some other good algos?
 It still would not realize all 24 keys!(only 12)
 """
from typing import List, Tuple, Dict, Union

import numpy as np
import music21 as m21

from stefutil import *
from musicnlp.util.music_lib import *
from musicnlp.vocab import Key, enum2key_str


__all__ = ['KeyFinder', 'ScaleDegreeFinder']


# Tuple of key and (un-normalized) confidence score
Keys = Tuple[List[str], List[str]]
KeysDict = Dict[Union[Key, str], float]


def get_durations(s) -> np.array:
    """
    :param: s: a music21.Stream object that stores the piece without drums
    :return: a np list of total durations for each pitch class in quarterLength.
    P.S. So kind of normalized version?
    """
    # flatten, then filter all the notes
    result = np.zeros(12)
    # for n in s.flatten().flatten().notesAndRests:
    #     length = n.quarterLength
    #     if n.isChord:
    #         for m in n.pitchClasses:
    #             result[m] += length
    #     elif not n.isRest:
    #         result[n.pitch.pitchClass] += length
    for n in s.recurse():
        if isinstance(n, Note):
            result[n.pitch.pitchClass] += n.quarterLength
        elif isinstance(n, Chord):
            for m in n.pitchClasses:
                result[m] += n.quarterLength
    return result


class KeyFinder:
    """
    Given a MusicXML file, find the key of those pieces.
    TODO: Do I need to find all modulated keys?
    """

    def __init__(self, song: Union[str, Score]):
        """
        :param song: a Music21 Score object or path to a music file
        """
        self.piece: Score = m21.converter.parse(song) if isinstance(song, str) else song

        # remove all the percussion in this piece
        parts_drum = filter(lambda p_: is_drum_track(p_), self.piece.parts)
        for pd in parts_drum:
            self.piece.remove(pd)

        # major and minor profile, see http://rnhart.net/articles/key-finding/
        self.prof = np.array([[0.748, 0.06, 0.488, 0.082, 0.67, 0.46, 0.096, 0.715, 0.104, 0.366, 0.057, 0.4],
                              [0.712, 0.084, 0.474, 0.618, 0.049, 0.46, 0.105, 0.747, 0.404, 0.067, 0.133, 0.33]])

        # diatonic key naming convention, see 'Circle of Fifth'.
        self.conv_major = {
            'C': 'C',
            'F': 'F',
            'A#': 'Bb',
            'D#': 'Eb',
            'G#': 'Ab',
            'C#': 'Db',
            'F#': 'Gb',
            'B': 'B',
            'E': 'E',
            'A': 'A',
            'D': 'D',
            'G': 'G'
        }
        self.conv_minor = {
            'A': 'A',
            'D': 'D',
            'G': 'G',
            'C': 'C',
            'F': 'F',
            'A#': 'Bb',
            'D#': 'Eb',
            'G#': 'G#',
            'C#': 'C#',
            'F#': 'F#',
            'B': 'B',
            'E': 'E'
        }

    # @eye
    def __call__(self, return_type: str = 'list') -> Union[Keys, KeysDict]:
        """
        return: 2 arrays that contains the best k candidates for major and minor respectively
        of the piece as a string.
        The string format would be [keyName]+Major/Minor.
        All keys with accidental signs are marked as sharp, which would equate 'A#' to 'Bb'.
        Then be transformed to more conventional enharmonic reading. e.g. 'A#' to 'Bb'..

        :param return_type: One of ['list', 'enum', 'dict']
            If 'list', returns 2-tuple list of tuples of (key, confidence) for major and minor respectively
            If 'enum' or `dict`, returns dict of {Key: confidence} where the key is either `Key` or `str` respectively
        """
        ca(key_type=return_type)
        # tonality = ['Major', 'Minor']
        pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        durations = get_durations(self.piece)
        # initialize results for all 24 possible coefficients
        corrcoef_mat = np.empty((2, 12))
        for k in range(2):
            for i in range(12):
                # linear correlation: https://realpython.com/numpy-scipy-pandas-correlation-python/#linear-correlation
                # also remember to rotate the weight matrix couple times
                corrcoef_mat[k, i] = np.corrcoef(np.roll(self.prof[k], i), durations)[1][0]
        # mic(corrcoef_mat)
        best_val_maj = np.max(corrcoef_mat[0])
        best_val_min = np.max(corrcoef_mat[1])
        # fuzzy search
        close_ma = len(corrcoef_mat[0][corrcoef_mat[0] >= best_val_maj * 0.8])
        close_mi = len(corrcoef_mat[1][corrcoef_mat[1] >= best_val_min * 0.7])
        best_maj_keys = (np.argsort(corrcoef_mat[0]))[-close_ma:]
        best_min_keys = (np.argsort(corrcoef_mat[1]))[-close_mi:]
        # convert candidates to string in convention format(circle of fifth).
        maj_keys_result = [(f'{self.conv_major[pitches[tonic]]}Major', corrcoef_mat[0][tonic]) for (_, tonic) in
                           [divmod(i, 12) for i in best_maj_keys]]
        min_keys_result = [(f'{self.conv_minor[pitches[tonic]]}Minor', corrcoef_mat[1][tonic]) for (_, tonic) in
                           [divmod(i, 12) for i in best_min_keys]]
        #
        if return_type == 'list':
            return [k for k, c in maj_keys_result], [k for k, c in min_keys_result]
        else:
            return KeyFinder._key_tup2dict(maj_keys_result, return_type=return_type) | \
                   KeyFinder._key_tup2dict(min_keys_result, return_type=return_type)

    @staticmethod
    def _key_tup2dict(key_tup: List[Tuple[str, float]], return_type: str = 'enum') -> KeysDict:
        return {(Key.from_str(k_) if return_type == 'enum' else k_): v for k_, v in dict(key_tup).items()}

    #
    # def alt_find(self):
    #     a = m21.analysis.discrete.TemperleyKostkaPayne(self.piece)
    #     print(a.getSolution(self.piece))
    #     return m21.analysis.discrete.TemperleyKostkaPayne(self.piece)

    def check_notes(self, k):
        """
        There are 3 kinds of common dissonance in classical period:
        1. modal mixture
        2. Secondary dominant
        3. Neapolitan chord in minor
        Here we will only consider the first two case since the 3rd has been deprecated by modern music.
        TODO: It is very tricky to do such analysis, need to talk with group.
        """
        pass

    def get_scale_degrees(self, k, n):
        """
        Return an array of diatonic notes regardless of  from 1-7 given an array of midi pitch names (0-128) and a key, indicated with a
        name (C, D, etc).
        :param k: A string that represents the key without indicating major or minor.
                n: An array of midi notes (pitch names).
        :return: An array of diatonic scale degrees in key.
        """
        # Note names according to their pitch.
        ref = {
            'C': 0,
            'C#': 1,
            'Db': 1,
            'D': 2,
            'D#': 3,
            'Eb': 3,
            'E': 4,
            'F': 5,
            'F#': 6,
            'Gb': 6,
            'G': 7,
            'G#': 8,
            'Ab': 8,
            'A': 9,
            'A#': 10,
            'Bb': 10,
            'B': 11,
        }
        # get pitch class for each note
        pc = n % 12


class ScaleDegreeFinder:
    t0_degrees = dict(
        C=0,
        D=1,
        E=2,
        F=3,
        G=4,
        A=5,
        B=6
    )

    def __init__(self, song: Union[str, Score] = None):
        self.piece: Score = m21.converter.parse(song) if isinstance(song, str) else song

    def __call__(self, keys: Keys = None):
        """
        :param keys: tuple of 2 lists, each contains major keys candidates and minor keys candidates ([XMajor],[YMinor])
        :return: a dictionary of s in scale degrees of given key in k represented in tuple where each tuple has
            (pitch class/pitch, scale degrees)
                ..note:: they do not have any octave values!

        ..note:: the notion of transposition group has been abused here and forced to adapt to enharmonic scale

        ..note:: Rest notes ignored
        """
        # make a dictionary with group T0 in scale degrees
        # Set e in T0 group, in this case it will be C
        keys = keys[0] + keys[1]
        mic(keys)

        lst_pch_n_degs = []  # to store all scale degrees in T0
        for n in self.piece.flatten().flatten().notesAndRests:
            if n.isChord:
                for p in n.pitches:
                    lst_pch_n_degs.append((p.midi, ScaleDegreeFinder.t0_degrees[p.step]))
            elif not n.isRest:
                n: Note
                lst_pch_n_degs.append((n.pitch.midi, ScaleDegreeFinder.t0_degrees[n.pitch.step]))
        # now shift to T1 and adjust the scale degree accordingly with major and minor
        ret = {}
        for key in keys:
            step = key[0]
            # mod7 plus 1 just to make it align with our scale degrees value convention (1-7)
            ret[key] = [(pch, (deg - ScaleDegreeFinder.t0_degrees[step]) % 7 + 1) for pch, deg in lst_pch_n_degs]
        return ret

    @staticmethod
    def map_single(note: Union[SNote, str], key: Union[Key, str]) -> int:
        """
        Map a note object to its scale degree in [1-7]

        .. note:: Intended that the note object is part of the Music21 piece passed in,
            otherwise, it's the user's responsibility to make sure the `step` of the note is correct
        """
        if isinstance(note, Rest):  # Rest notes don't have a scale degree
            return 0
        elif isinstance(note, (str, Note)):
            step = note.pitch.step if isinstance(note, Note) else note
            deg = ScaleDegreeFinder.t0_degrees[step]
            if isinstance(key, Key):
                key = enum2key_str[key]
            return (deg - ScaleDegreeFinder.t0_degrees[key[0]]) % 7 + 1
        elif isinstance(note, Chord):
            raise NotImplementedError(f'Scale degree for Chord notes?')


def main(path: str):
    kf = KeyFinder(path)
    keys = kf()

    sdf = ScaleDegreeFinder(song=kf.piece)
    mic(sdf(keys))


if __name__ == '__main__':
    from tqdm import tqdm
    import musicnlp.util.music as music_util

    def check_get_key():
        path = music_util.get_my_example_songs('Merry Go Round of Life', fmt='MXL')
        mic(path)
        kf = KeyFinder(path)
        mic(kf(return_type='enum'))
    # check_get_key()

    def check_deprecated_scale_deg():
        path = music_util.get_my_example_songs('Merry Go Round of Life', fmt='MXL')
        kf = KeyFinder(path)
        keys_dep_maj, keys_dep_min = kf()
        mic(keys_dep_maj, keys_dep_min)

        sdf = ScaleDegreeFinder(song=kf.piece)
        mic(sdf((keys_dep_maj, keys_dep_min)))
    # check_deprecated_scale_deg()

    def carson_dev():
        path = '/Users/carsonzhang/Documents/Projects/Rada/midi/Merry-Go-Round-of-Life.musicxml'
        main(path)
    # carson_dev()

    def check_key_finder_terminates():
        """
        Make sure calling KeyFinder on any song in the dataset terminates properly, and at least 1 key returned
        """
        dnm = 'POP909'
        fnms = music_util.get_converted_song_paths(dnm, fmt='mxl')
        # fnms = fnms[:20]  # TODO: debugging
        # for fnm in tqdm(fnms):
        #     keys = KeyFinder(fnm).find_key(return_type='enum')
        #     assert len(keys) > 0
        nm = 'Test Key Finder'
        logger = get_logger(nm)
        pbar = tqdm(total=len(fnms), desc=nm, unit='song')

        def call_single(fl_nm: str):
            try:
                keys = KeyFinder(fl_nm)(return_type='enum')
                assert len(keys) > 0
                pbar.update(1)
            except Exception as e:
                logger.error(f'Failed to find key for {pl.i(fl_nm)}, {pl.i(e)}')  # Abruptly stop the process
                raise ValueError(f'Failed to find key for {pl.i(fl_nm)}')

        def batched_map(fnms_, s, e):
            return [call_single(fnms_[i]) for i in range(s, e)]
        batched_conc_map(batched_map, fnms, batch_size=32)
    # check_key_finder_terminates()
    # profile_runtime(check_key_finder_terminates)

    def check_scale_degree_map():
        import pandas as pd

        from musicnlp.vocab import MusicVocabulary, key_enum2tuple

        vocab = MusicVocabulary()
        notes = [Rest()]
        for i in range(128):
            notes.append(Note(pitch=Pitch(midi=i)))

        sdf = ScaleDegreeFinder()  # for the sake of sanity check, just pick arbitrary song

        rows = []
        for n in notes:
            row = dict(str=str(n), pitch=vocab.note2pitch_str(n))
            for key, (flag, key_str) in key_enum2tuple.items():
                row[key_str] = sdf.map_single(n, key)
            rows.append(row)
        df = pd.DataFrame(rows)
        pd.set_option('display.max_rows', None)
        mic(df)
    check_scale_degree_map()
