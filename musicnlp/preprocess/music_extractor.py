"""
Since Sun. Jan. 30th, an updated module for music/melody extraction, with a duration-quantized approach

See `melody_extractor` for the old version.
"""

import itertools
from copy import deepcopy
from typing import Iterator
from warnings import warn
from fractions import Fraction
from collections import defaultdict

from music21.stream import Score, Measure, Voice
from music21.meter import TimeSignature
from music21.tempo import MetronomeMark
from music21.note import Rest, Note
from music21.chord import Chord
from music21.duration import Duration

from musicnlp.util import *


def expand_bar(bar: Union[Measure, Voice], keep_chord=False, number=None) -> List[Union[tuple[Note], Rest, Note]]:
    """
    Expand elements in a bar into individual notes, no order is enforced

    :param bar: A music21 measure to expand
    :param keep_chord: If true, `Chord`s are not expanded
    :param number: For passing bar number recursively to Voice 

    .. note:: Triplets (potentially any n-plets) are grouped; `Voice`s are expanded
    """
    if not hasattr(expand_bar, 'post'):
        expand_bar.post = 'plet'  # Postfix for all tuplets, e.g. `Triplet`, `Quintuplet`
    if not hasattr(expand_bar, 'post2tup'):
        expand_bar.pref2n = dict(  # Tuplet prefix to the expected number of notes
            Tri=3,
            Quintu=5,
            Nonu=9
        )
    post = expand_bar.post

    lst = []
    it = iter(bar)
    elm = next(it, None)
    while elm is not None:
        if hasattr(elm, 'fullName') and post in elm.fullName:
            pref = elm.fullName[:elm.fullName.find(post)].split()[-1]
            tup = f'{pref}{post}'
            if pref in expand_bar.pref2n:
                n_tup = expand_bar.pref2n[pref]
            else:
                assert pref == 'Tu'  # A generic case, music21 processing, different from that of MuseScore
                # e.g. 'C in octave 1 Dotted 32nd Tuplet of 9/8ths (1/6 QL) Note' makes 9 notes in tuplet
                words = elm.fullName.split()
                word_n_tup = words[words.index(tup)+2]
                n_tup = int(word_n_tup[:word_n_tup.find('/')])
            elms_tup: List[Note] = [elm]
            elm_ = next(it, None)
            while elm_ is not None and tup in elm_.fullName:  # Look for all elements of the same `n_tup`
                elms_tup.append(elm_)
                elm_ = next(it, None)  # Peeked 1 ahead

            # Consecutive tuplet notes => (potentially multiple) groups
            it_tup = iter(elms_tup)
            e_tup = next(it_tup, None)
            dur: Union[Fraction, float] = 0
            idx, idx_prev, idx_last = 0, 0, len(elms_tup)-1
            n_tup_curr = 0
            trip_added = False
            idx_tup_strt = len(lst)

            def check_wrong_n_tup():
                ln = len(lst[-1])
                if ln != n_tup:
                    warn(f'Invalid {tup}: {tup} with invalid number of notes added at bar#{number}'
                         f' - expect {n_tup}, got {ln}')

            while e_tup is not None:  # MIDI & MuseScore transcription quality, e.g. A triplet may not contain 3 notes
                dur += e_tup.duration.quarterLength
                n_tup_curr += 1
                # TODO: generalize beat/tuplet duration checking logic, might involve time signature
                # Enforce a tuplet must have at least `n_tup` notes
                # Duration ends as a beat; Heuristic for end of tuplet group
                if n_tup_curr >= n_tup and dur.denominator == 1:
                    lst.append(tuple(elms_tup[idx_prev:idx+1]))
                    trip_added = True

                    # Prep for next tuplet
                    idx_prev = idx+1
                    n_tup_curr = 0
                    dur = 0

                    if idx == idx_last:  # Postpone warning later, see below
                        check_wrong_n_tup()
                # Processed til last element, last tuplet group not enough elements
                if idx == idx_last and n_tup_curr < n_tup:
                    assert trip_added
                    assert dur.denominator == 1
                    lst[-1] = lst[-1] + tuple(elms_tup[idx_prev:])  # Join the prior tuplet group
                    check_wrong_n_tup()
                idx += 1
                e_tup = next(it_tup, None)
            # All triple notes with the same `n_tup` are added
            assert sum(len(tup) for tup in lst[idx_tup_strt:]) == len(elms_tup)
            if not keep_chord:
                tups_new = []
                has_chord = False
                for i in range(idx_tup_strt, len(lst)):  # Ensure all tuplet groups contain no Chord
                    tup = lst[i]
                    # Bad transcription quality => Keep all possible tuplet combinations
                    # Expect to be the same
                    if any(isinstance(n, Chord) for n in tup):
                        has_chord = True
                        opns = [tuple(n.notes) if isinstance(n, Chord) else (n,) for n in tup]
                        tups_new.extend(list(itertools.product(*opns)))
                if has_chord:  # Update prior triplet groups
                    lst = lst[:idx_tup_strt] + tups_new

            if not trip_added:
                ic('triplet not added')
                exit(1)

            elm = elm_
            # exit(1)
            continue  # Skip `next` for peeked 1 step ahead
        elif isinstance(elm, (Note, Rest)):
            lst.append(elm)
        elif isinstance(elm, Chord):
            if keep_chord:
                lst.append(elm)
            else:
                notes = deepcopy(elm.notes)
                for n in notes:
                    n.offset += elm.offset  # Shift offset in the scope of bar
                lst.extend(notes)
        else:
            if not isinstance(elm, (  # Ensure all relevant types are considered
                TimeSignature, MetronomeMark, Voice,
                m21.layout.LayoutBase, m21.clef.Clef, m21.key.KeySignature, m21.bar.Barline
            )):
                ic(elm)
                print('unexpected type')
                exit(1)
        elm = next(it, None)
    if bar.hasVoices():  # Join all voices to notes
        lst.extend(join_its(expand_bar(v, number=bar.number) for v in bar.voices))
    return lst


class MusicExtractor:
    """
    Extract melody and potentially chords from MXL music scores => An 1D polyphonic representation
    """
    def __init__(self, scr: Union[str, Score], precision: int = 5, mode: str = 'melody'):
        """
        :param scr: A music21 Score object, or file path to an MXL file
        :param precision: Bar duration quantization, see `melody_extractor.MxlMelodyExtractor`
        :param mode: Extraction mode, one of [`melody`, `full`]
            `melody`: Only melody is extracted
            `full`: Melody and Chord as 2 separate channels extracted TODO
        """
        if isinstance(scr, str):
            self.scr = m21.converter.parse(scr)
        else:
            self.scr = scr
        self.scr: Score

        self.prec = precision
        self.mode = mode

    @staticmethod
    def it_bars(scr: Score) -> Iterator[tuple[Measure, TimeSignature, MetronomeMark]]:
        """
        Unroll a score by time, with the time signatures of each bar
        """
        time_sig, tempo = None, None
        for idx, bars in enumerate(zip(*[list(p[Measure]) for p in scr.parts])):  # Bars for all tracks across time
            assert_list_same_elms([b.number for b in bars])  # Bar numbers should be the same

            # Update time signature
            tss = [b[TimeSignature] for b in bars]
            if idx == 0 or any(tss):  # 1st bar must have time signature defined
                assert all(len(t) == 1 for t in tss)
                tss = [next(t) for t in tss]
                assert_list_same_elms([(ds.numerator, ds.denominator) for ds in tss])
                time_sig = tss[0]

            tempos = [b[MetronomeMark] for b in bars]
            if idx == 0 or any(tempos):
                tempos = [t for t in tempos if len(t) != 0]
                # When multiple tempos, take the mean
                tempos = [MetronomeMark(number=np.array([t.number for t in ts]).mean()) for ts in tempos]
                bpms = [t.number for t in tempos]
                assert_list_same_elms(bpms)

                tempo = MetronomeMark(number=bpms[0])
            yield bars, time_sig, tempo

    def __call__(self, exp='mxl'):
        scr = deepcopy(self.scr)

        for bars, time_sig, tempo in MusicExtractor.it_bars(scr):
            number = bars[0].number
            ic(number)
            # if number == 164:
            #     for b in bars:
            #         b.show()
            n_slots_per_beat, n_slots = time_sig2n_slots(time_sig, self.prec)
            notes = sum((expand_bar(b, keep_chord=self.mode == 'full') for b in bars), [])

            def note2pitch(note):
                if isinstance(note, tuple):  # Triplet, return average pitch
                    # Duration for each note not necessarily same duration, for transcription quality
                    fs, durs = zip(*[(note2pitch(n__), n__.duration.quarterLength) for n__ in note])
                    # ic(fs, durs, np.average(fs, weights=durs))
                    return np.average(fs, weights=durs)
                    # return sum(n__.pitch.frequency for n__ in note) / len(note)
                elif isinstance(note, Note):
                    return note.pitch.frequency
                else:
                    assert isinstance(note, Rest)
                    return 0  # `Rest` given pitch frequency of 0

            groups = defaultdict(list)  # Group notes by starting location
            for n in notes:
                n_ = n[-1] if isinstance(n, tuple) else n
                groups[n_.offset].append(n)
            groups = {offset: sorted(ns, key=note2pitch) for offset, ns in groups.items()}

            def get_notes_out() -> List[Union[tuple[Note], Note, Chord]]:
                ns_out = []
                offset_next = 0
                for offset in sorted(groups.keys()):  # Pass through notes in order
                    notes_ = groups[offset]
                    nt = notes_[-1]
                    if offset < offset_next:
                        if note2pitch(nt) > note2pitch(ns_out[-1]):
                            # Offset would closely line up across tracks, expect this to be less frequent
                            warn(f'High pitch overlap: later overlapping note with higher pitch observed '
                                 f'at bar#{number} - prior note truncated')
                            # Definitely non-0 for offset grouping
                            if number == 73:
                                ic(nt, ns_out[-1])
                            if isinstance(ns_out[-1], tuple):  # TODO: recomputing notes, if triplet is overlapping
                                ic('triplet being truncated')
                                exit(1)
                            else:  # Triplet replaces pr..           ior note, which is definitely non triplet
                                nt_ = nt[0] if isinstance(nt, tuple) else nt
                                ns_out[-1].duration = Duration(quarterLength=nt_.offset - ns_out[-1].offset)
                        else:  # Skip if later note is lower in pitch
                            continue
                    ns_out.append(nt)  # Note with the highest pitch
                    nt_ = nt[-1] if isinstance(nt, tuple) else nt
                    offset_next = nt_.offset + nt_.duration.quarterLength
                return ns_out
            notes_out = get_notes_out()
            assert_notes_no_overlap(notes_out)  # Ensure notes cover the entire bar
            n_last = notes_out[-1]
            n_last = n_last[-1] if isinstance(n_last, tuple) else n_last
            assert (n_last.offset + n_last.duration.quarterLength) == (time_sig.numerator / time_sig.denominator * 4)

        composer = PKG_NM
        scr.metadata.composer = composer


if __name__ == '__main__':
    from icecream import ic

    def toy_example():
        fnm = eg_songs('Merry Go Round of Life', fmt='MXL')
        # fnm = eg_songs('Shape of You', fmt='MXL')
        ic(fnm)
        me = MusicExtractor(fnm)
        me(exp='mxl')
    toy_example()
