"""
Since Sun. Jan. 30th, an updated module for music/melody extraction, with a duration-quantized approach

See `melody_extractor` for the old version.
"""

import sys
import functools
from collections import defaultdict, Counter

from music21.stream import Score, Measure, Voice
from music21.tempo import MetronomeMark
from music21.duration import Duration
from music21.pitch import Pitch

from musicnlp.util import *


pd.set_option('display.max_columns', None)  # TODO


class WarnLog:
    """
    Keeps track of warnings in music extraction

    JSON-serializable
    """
    InvTupSz, TupNoteOvl = 'Invalid Tuplet Size', 'Tuplet Notes Overlap'
    # InvTupNt = 'Invalid Tuplet Notes'
    InvTupDur, InvTupDurSv = 'Invalid Tuplet Durations', 'Invalid Tuplet Durations, Severe'
    RestInTup = 'Rest in Tuplet'
    HighPchOvl, HighPchOvlTup = 'Higher Pitch Overlap', 'Higher Pitch Overlap with Triplet'
    LowPchMakeup, LowPchMakeupRmv = 'Lower Pitch Makeup', 'Lower Pitch Makeup Removed'
    IncTimeSig, UncomTimeSig = 'Inconsistent Time Signatures', 'Uncommon Time Signature'
    NoteNotQuant, TupNoteQuant = 'Notes Beyond Quantization', 'Tuplet Notes Quantizable'
    InvBarDur = 'Invalid Bar Notes Duration'
    EmptyStrt, EmptyEnd = 'Beginning Empty Bars', 'Ending Empty Bars'
    T_WN = [  # Warning types
        InvTupSz, TupNoteOvl,
        InvTupDur, InvTupDurSv,
        # InvTupNt,
        RestInTup,
        HighPchOvl, HighPchOvlTup,
        LowPchMakeup, LowPchMakeupRmv,
        IncTimeSig, UncomTimeSig,
        NoteNotQuant, TupNoteQuant,
        InvBarDur,
        EmptyStrt, EmptyEnd
    ]

    def __init__(self, name=f'{PKG_NM} Music Extraction', verbose=True):
        self.warnings: List[Dict] = []
        self.idx_track = None
        self.args_func = None
        self.verbose = verbose

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stream=sys.stdout)  # For my own coloring
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(MyFormatter())
        self.logger.addHandler(handler)

        MyTheme.set_color_type('sty')  # Defaults warning color to `yellow`
        self.yellow = MyTheme.yellow

    @staticmethod
    def warn_nm2str_tpl(warn_nm) -> str:
        # Map Warning to string output
        if warn_nm in [WarnLog.InvTupDur, WarnLog.InvTupDurSv]:
            msg = '{warn_name}: Tuplet durations don\'t sum up to 8th notes ' \
                  'at bar#{bar_num}, with offsets: {offsets}, durations: {durations} ' \
                  '- note durations distributed, and cropped to bar length if necessary'
        elif warn_nm == WarnLog.InvTupSz:
            msg = '{warn_name}: Tuplet with invalid number of notes added ' \
                  'at bar#{bar_num} - expect {n_expect}, got {n_got}'
        # elif nm == WarnLog.InvTupNt:
        #     msg = '{warn_name}: Tuplet with overlapping notes added at bar#{bar_num}, ' \
        #           'with offsets: {offsets}, durations: {durs} - notes are cut off'
        elif warn_nm == WarnLog.RestInTup:
            msg = '{warn_name}: Rest Notes observed in tuplet group at bar#{bar_num}' \
                  ' - total note {n_note}, rest count {n_rest}'
        elif warn_nm == WarnLog.UncomTimeSig:
            msg = '{warn_name}: Time Signature is uncommon' \
                  ' - Expect one of: {time_sig_expect}, got {time_sig_got}'
        elif warn_nm == WarnLog.IncTimeSig:
            msg = '{warn_name}: ratio of mode time signature below {th}' \
                  ' - #mode {n_mode}, #total {n_bar}'
        elif warn_nm == WarnLog.HighPchOvlTup:
            msg = '{warn_name}: Higher pitch observed at bar#{bar_num}' \
                  ' - triplet truncated'
        elif warn_nm == WarnLog.HighPchOvl:
            msg = '{warn_name}: Later overlapping note with higher pitch observed ' \
                  'at bar#{bar_num} - prior note truncated'
        elif warn_nm == WarnLog.LowPchMakeup:
            msg = '{warn_name}: Later overlapping note with lower pitch but longer ending time observed ' \
                  'at bar#{bar_num} - truncated note appended'
        elif warn_nm == WarnLog.LowPchMakeupRmv:
            msg = '{warn_name}: Previously-added, truncated, lower-pitch makeup note overridden ' \
                  'by higher pitch note at bar#{bar_num} - makeup note removed'
        elif warn_nm == WarnLog.InvBarDur:
            msg = '{warn_name}: Note duration don\'t add up to bar max duration at bar#{bar_num}'
        elif warn_nm == WarnLog.TupNoteOvl:
            msg = '{warn_name}: Notes inside tuplet group are overlapping at bar#{bar_num} ' \
                  '- Note durations will be equally distributed'
        elif warn_nm == WarnLog.NoteNotQuant:
            msg = '{warn_name}: Note durations smaller than quantized slot at bar#{bar_num} ' \
                  '- Note durations approximated'
        elif warn_nm == WarnLog.EmptyStrt:
            msg = '{warn_name}: Empty bars observed at start of song in range: {bar_range}'
        elif warn_nm == WarnLog.EmptyEnd:
            msg = '{warn_name}: Empty bars observed at end of song in range: {bar_range}'
        else:
            assert warn_nm == WarnLog.TupNoteQuant
            msg = '{warn_name}: Tuplet notes of equal duration is quantizable at bar#{bar_num}' \
                  f' - Tuplet notes converted to normal notes'
        return msg

    def update(self, warn_: Dict):
        """
        :param warn_: Dictionary object specifying warning information
            nm: Warning name
            args - Dict: Metadata for the warning
            id: Warning entry id
            timestamp: Logging timestamp
        """
        assert 'warn_name' in warn_
        nm, args = warn_['warn_name'], warn_

        assert nm in WarnLog.T_WN
        if nm == WarnLog.InvTupSz:
            assert all(k in args for k in ['bar_num', 'n_expect', 'n_got'])
        elif nm in [
            # WarnLog.InvTupNt,
            WarnLog.InvTupDur, WarnLog.InvTupDurSv,
            WarnLog.NoteNotQuant, WarnLog.TupNoteQuant, WarnLog.TupNoteOvl,
            WarnLog.InvBarDur
        ]:
            assert all(k in args for k in ['bar_num', 'offsets', 'durations'])
            if nm == WarnLog.InvBarDur:
                assert 'time_sig' in args
        elif nm == WarnLog.RestInTup:
            assert all(k in args for k in ['bar_num', 'n_rest', 'n_note'])

        elif nm in [WarnLog.HighPchOvl, WarnLog.HighPchOvlTup, WarnLog.LowPchMakeup, WarnLog.LowPchMakeupRmv]:
            assert 'bar_num' in args
        elif nm == WarnLog.UncomTimeSig:
            assert 'time_sig_expect' in args and 'time_sig_got' in args
        elif nm in [WarnLog.EmptyStrt, WarnLog.EmptyEnd]:
            assert 'bar_range' in args
        else:
            assert nm == WarnLog.IncTimeSig
            assert all(k in args for k in ['time_sig', 'n_bar_total', 'n_bar_mode'])
        if self.args_func is not None:
            warn_ = self.args_func() | warn_

        if self.verbose:
            warn_out = {k: logi(v)+self.yellow for k, v in warn_.items()}
            warn_out['warn_name'] = sty.ef.bold + self.yellow + warn_out['warn_name']
            self.logger.warning((WarnLog.warn_nm2str_tpl(nm) + MyFormatter.RESET).format(**warn_out))
        self.warnings.append(warn_)

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.warnings)  # TODO: change column names?
        return df

    def start_tracking(self, args_func: Callable[[], Dict] = None):
        """
        Start tracking warnings added after the call

        :args_func: A function that returns a dictionary of metadata, merged to each `update` call
        """
        self.idx_track = len(self.warnings)
        self.args_func = args_func

    def tracked(self, summary=True) -> Union[str, List[Dict]]:
        """
        Statistics of warnings since tracking started
        """
        if summary:
            counts = Counter(w['warn_name'] for w in self.warnings[self.idx_track:])
            return ', '.join((f'{logi(k)}: {logi(v)}' for k, v in counts.items()))
        else:
            return self.warnings[self.idx_track:]


class MusicVocabulary:
    """
    Stores mapping between string tokens and integer ids
    & support the conversion, from relevant `music21` objects to [`str`, `int] conversion
    """
    SPEC_TOKS = dict(
        sep='_',  # Separation
        rest='r',
        prefix_pitch='p',
        prefix_duration='d',
        start_of_tuplet='<tup>',
        end_of_tuplet='</tup>',
        start_of_bar='<bar>',
        end_of_song='</s>',
        prefix_time_sig='TimeSig',
        prefix_tempo='Tempo'
    )
    # Uncommon Time Signatures in music theory, but empirically seen in MIDI data
    UNCOM_TSS: List[TsTup] = [(1, 4)]

    def __init__(self, prec: int = 5, color: bool = False):
        """
        :param prec: See `MusicTokenizer`
        :param color: If True, string outputs are colorized
            Update individual coloring of subsequent tokens via `__getitem__`
        """
        self.prec = prec
        self.color = color

        specs = MusicVocabulary.SPEC_TOKS  # Syntactic sugar
        sep = specs['sep']
        self.cache = dict(  # Common intermediary substrings
            pref_dur=specs['prefix_duration']+sep,
            pref_pch=specs['prefix_pitch']+sep,
            pref_time_sig=specs['prefix_time_sig']+sep,
            pref_tempo=specs['prefix_tempo']+sep,
            bot=self.__getitem__('start_of_tuplet'),
            eot=self.__getitem__('end_of_tuplet')
        )
        self.cache['rest'] = self.cache['pref_pch'] + specs['rest']

        def elm2str(elm):
            return self.__call__(elm, color=False, return_int=False)
        self.n_slots = OrderedDict([  # Reserved slots for each token category
            ('special', 32),
            ('time_sig', 32),  # A few common time signatures only
            ('tempo', 256),  # Usually range from 20+ to 200+
            # 128 pitches in MIDI representation; TODO: with music-theory, mod-7 scale, may increase
            ('pitch', 256),
            ('duration', 256)  # Depends on quantization
        ])

        def rev(time_sig):
            return tuple(reversed(time_sig))  # Syntactic sugar
        tss = [elm2str(rev(ts))[0] for ts in sorted(rev(ts) for ts in COMMON_TIME_SIGS + MusicVocabulary.UNCOM_TSS)]
        tempos = [elm2str(tp)[0] for tp in range(20, 220)]  # Expected normal song ranges
        pitches = [self.cache['rest']] + [self._note2pch_str(Pitch(midi=i)) for i in range(128)]

        def get_durations():
            bound = 6  # Support duration up to **6** in terms of `quarterLength`
            dur_slot = 4 / 2**self.prec  # for durations in quarterLength; TODO: support for longer duration needed?
            return [self._note2dur_str((i + 1) * dur_slot) for i in range(math.ceil(bound / dur_slot))]

        self.toks: Dict[str, List[str]] = dict(
            special=[specs[k] for k in ('end_of_song', 'start_of_bar', 'start_of_tuplet', 'end_of_tuplet')],
            time_sig=tss,
            tempo=tempos,
            pitch=pitches,
            duration=get_durations()
        )
        slot_offsets = [0] + list(itertools.accumulate(self.n_slots.values()))
        self.enc: Dict[str, int] = functools.reduce(lambda a, b: a | b, (
            {tok: id_+slot_offsets[i] for id_, tok in enumerate(self.toks[k])} for i, k in enumerate(self.n_slots)
        ))
        self.dec = {v: k for k, v in self.enc.items()}
        assert len(self.enc) == len(self.dec)  # Sanity check: no id collision

    @property
    def size(self):
        return len(self.enc)

    def _colorize_spec(self, s: str, color: bool = None) -> str:
        c = self.color if color is None else color
        return logs(s, c='m') if c else s

    def __getitem__(self, k: str) -> str:
        """
        Index into the special tokens
        """
        return self._colorize_spec(MusicVocabulary.SPEC_TOKS[k])

    def __call__(
            self, elm: Union[
                Note, Rest, tuple[Note],
                Union[TimeSignature, tuple[int, int]],
                Union[MetronomeMark, int]
            ],
            color: bool = None,
            return_int: bool = False  # TODO
    ) -> Union[List[str], List[int]]:  # TODO: Support chords?
        """
        Convert music21 element to string or int

        :param elm: A relevant token in melody extraction
        :param color: If given, overrides coloring for current call
        :param return_int: If true, integer ids are returned
        :return List of strings of the converted tokens
        """
        c = self.color if color is None else color

        def colorize(s):
            return self._colorize_spec(s, color=c)

        if isinstance(elm, TimeSignature) or (isinstance(elm, tuple) and isinstance(elm[0], int)):  # Time Signature
            if isinstance(elm, TimeSignature):
                top, bot = elm.numerator, elm.denominator
            else:
                top, bot = elm
            return [colorize(self.cache['pref_time_sig']+f'{top}/{bot}')]
        elif isinstance(elm, (int, MetronomeMark)):  # Tempo
            if isinstance(elm, MetronomeMark):
                elm = elm.number
            return [colorize(self.cache['pref_tempo']+str(elm))]
        elif isinstance(elm, Rest):
            r = self.cache['rest']
            return [logs(r, c='b') if color else r, self._note2dur_str(elm)]
        elif isinstance(elm, Note):
            return [self._note2pch_str(elm), self._note2dur_str(elm)]
        elif isinstance(elm, tuple):
            # Sum duration for all tuplets
            bot, eot = self.cache['bot'], self.cache['eot']
            return [colorize(bot)] + [
                (self._note2pch_str(e)) for e in elm
            ] + [self._note2dur_str(elm)] + [colorize(eot)]
        else:  # TODO: chords
            ic('other element type', elm)
            exit(1)

    def _note2dur_str(
            self, e: Union[
                Rest, Note, tuple[Note],
                Fraction, float, int
            ]) -> str:
        """
        :param e: A note, tuplet, or a numeric representing duration
        """
        # If a float, expect multiple of powers of 2
        dur = Fraction(e if isinstance(e, (Fraction, float, int)) else note2dur(e))
        if dur.denominator == 1:
            s = f'{self.cache["pref_dur"]}{dur.numerator}'
        else:
            s = f'{self.cache["pref_dur"]}{dur.numerator}/{dur.denominator}'
        return logs(s, c='g') if self.color else s

    def _note2pch_str(self, note: Union[Note, Rest, Pitch]) -> str:
        """
        :param note: A note, tuplet, or a music21.pitch.Pitch
        """
        def pch2step(p: Pitch) -> int:
            """
            Naive mapping to the physical, mod-12 pitch frequency, in [1-12]
            """
            return (p.midi % 12) + 1
        if isinstance(note, Rest):
            s = self.cache["rest"]
        else:
            pitch = note.pitch if isinstance(note, Note) else note
            # `pitch.name` follows certain scale by music21 default, may cause confusion
            s = f'{self.cache["pref_pch"]}{pch2step(pitch)}/{pitch.octave}'
        return logs(s, c='b') if self.color else s

    def encode(self, s: Union[str, List[str], List[List[str]]]) -> Union[int, List[int], List[List[int]]]:
        """
        Convert string token to integer id
        """
        if isinstance(s, List) and isinstance(s[0], List):
            return list(conc_map(self.encode, s))
        elif isinstance(s, List):
            return [self.enc[s_] for s_ in s]
        else:
            return self.enc[s]

    def decode(self, id_: Union[int, List[int], List[List[int]]]) -> Union[str, List[str], List[List[str]]]:
        """
        Reverse function of `str2id`
        """
        if isinstance(id_, List) and isinstance(id_[0], List):
            return list(conc_map(self.decode, id_))
        elif isinstance(id_, List):
            return [self.dec[i_] for i_ in id_]
        else:
            return self.dec[id_]


class MusicTokenizer:
    """
    Extract melody and potentially chords from MXL music scores => An 1D polyphonic representation
    """
    def __init__(self, precision: int = 5, mode: str = 'melody', logger: Union[WarnLog, bool] = None, verbose=True):
        """
        :param precision: Bar duration quantization, see `melody_extractor.MxlMelodyExtractor`
        :param mode: Extraction mode, one of [`melody`, `full`]
            `melody`: Only melody is extracted
            `full`: Melody and Chord as 2 separate channels extracted TODO
        :param logger: A logger for storing warnings
            If True, a logger is instantiated
        :param verbose: If true, process is logged, including statistics of score and warnings
        """
        self.title = None  # Current score title

        self.prec = precision
        self.mode = mode

        self.logger: WarnLog
        if logger:
            self.logger = logger if isinstance(logger, WarnLog) else WarnLog(verbose=verbose)
            self.logger.verbose = verbose
        else:
            self.logger = None
        self.verbose = verbose

        self.vocab = MusicVocabulary(precision)

    @staticmethod
    def it_bars(scr: Score) -> Iterator[Tuple[Tuple[Measure], TimeSignature, MetronomeMark]]:
        """
        Unroll a score by time, with the time signatures of each bar
        """
        # Remove drum tracks
        def is_drum(part):
            """
            :return: True if `part` contains *only* `Unpitched`
            """
            return list(part[m21.note.Unpitched]) and not list(part[m21.note.Note])
        instrs_drum = [
            m21.instrument.BassDrum,
            m21.instrument.BongoDrums,
            m21.instrument.CongaDrum,
            m21.instrument.SnareDrum,
            m21.instrument.SteelDrum,
            m21.instrument.TenorDrum,
        ]
        parts = [p_ for p_ in scr.parts if not (any(p_[drum] for drum in instrs_drum) or is_drum(p_))]

        time_sig, tempo = None, None
        for idx, bars in enumerate(zip(*[list(p[Measure]) for p in parts])):  # Bars for all tracks across time
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

    def my_log_warn(self, log_dict: Dict):
        if self.logger is not None:
            self.logger.update(log_dict)

    def dur_within_prec(self, dur: Union[float, Fraction]) -> bool:
        return is_int(dur / 4 / (2**-self.prec))

    def notes2quantized_notes(
            self, notes: List[ExtNote], time_sig: TimeSignature, number: int = None
    ) -> List[ExtNote]:
        """
        Approximate notes to the quantization `prec`, by taking the note with majority duration

        .. note:: Notes all have 0 offsets, in the output order

        Expect tuplets to be fully quantized before call - intended for triplets to be untouched after call
        """
        ic('in quantize', number)
        dur_slot = 4 * 2**-self.prec  # In quarter length
        dur_bar = (time_sig.numerator/time_sig.denominator*4)
        n_slots = dur_bar / dur_slot
        assert n_slots.is_integer()
        n_slots = int(n_slots)
        bin_edges = [(i*dur_slot, (i+1)*dur_slot) for i in range(n_slots)]  # All info indexed by note order

        def note2range(note):
            if isinstance(note, tuple):
                strt, end = note[0], note[-1]
                return strt.offset, end.offset + end.duration.quarterLength
            else:
                return note.offset, note.offset + note.duration.quarterLength

        notes_ranges = [note2range(n) for n in notes]
        n_notes = len(notes)

        def get_overlap(low, high, idx_note):
            return min(high, notes_ranges[idx_note][1]) - max(low, notes_ranges[idx_note][0])

        def assign_max_note_idx(low, high, options: Iterable[int]):
            """
            :param low: Lower bound of bin range
            :param high: Upperbound bound of bin range
            :param options: Note candidate indices
            """
            return max(options, key=lambda i: get_overlap(low, high, i))
        idxs_note = [assign_max_note_idx(*edge, range(n_notes)) for edge in bin_edges]
        offset = 0
        notes_out = []
        for i, n in compress(idxs_note):
            # If tuplet case, total duration must've been within quantization before this `notes2quantized_notes` call,
            # see `expand_bar`
            nt = note2note_cleaned(notes[i], q_len=n*dur_slot)
            if isinstance(nt, tuple):
                dur_ea = quarter_len2fraction(n*dur_slot) / len(nt)
                note_tups_out = []
                for i_, nt_tup in enumerate(nt):
                    nt_tup.offset = offset + dur_ea * i_
                    note_tups_out.append(nt_tup)
                notes_out.append(tuple(note_tups_out))
            else:
                nt.offset = offset  # Unroll the offsets
                notes_out.append(nt)
            offset += note2dur(nt)

        # def sanity_check():
        #     for n in notes:
        #         ic('ori', n.duration.quarterLength)
        #     for n in notes_out:
        #         ic('quant', n.duration.quarterLength)
        #     bar_ori = Measure()
        #     bar_ori.append(notes)
        #     bar_quant = Measure()
        #     bar_quant.append(notes_out)
        #     bar_ori.show()
        #     bar_quant.show()

        assert is_notes_no_overlap(notes_out)  # Sanity check
        assert sum(note2dur(n) for n in notes_out) == dur_bar
        if number == 50:
            ic(notes)
            for n in flatten_notes(notes):
                ic(n, n.fullName, n.offset, n.duration.quarterLength)
            ic([get_overlap(*edge, i) > 0 for edge, i in zip(bin_edges, idxs_note)])
        assert all((get_overlap(*edge, i) > 0) for edge, i in zip(bin_edges, idxs_note))
        return notes_out

    def expand_bar(
            self, bar: Union[Measure, Voice], time_sig: TimeSignature, keep_chord=False, number=None
    ) -> List[ExtNote]:
        """
        Expand elements in a bar into individual notes, no order is enforced

        :param bar: A music21 measure to expand
        :param time_sig: Time signature of the bar
        :param keep_chord: If true, `Chord`s are not expanded
        :param number: For passing bar number recursively to Voice

        .. note:: Triplets (potentially any n-plets) are grouped; `Voice`s are expanded
        """
        # if number == 109:
        #     ic('in expand bar')
        #     for n in bar:
        #         if not isinstance(n, (Voice, m21.layout.LayoutBase, m21.clef.Clef)):
        #             ic(n, n.fullName, n.offset, n.duration.quarterLength)

        if not hasattr(MusicTokenizer, 'post'):
            MusicTokenizer.post = 'plet'  # Postfix for all tuplets, e.g. `Triplet`, `Quintuplet`
        if not hasattr(MusicTokenizer, 'post2tup'):
            MusicTokenizer.pref2n = dict(  # Tuplet prefix => expected number of notes
                Tri=3,
                Quintu=5,
                Nonu=9
            )
        post = MusicTokenizer.post

        lst = []
        it = iter(bar)
        elm = next(it, None)
        while elm is not None:
            if hasattr(elm, 'fullName') and post in elm.fullName:
                pref = elm.fullName[:elm.fullName.find(post)].split()[-1]
                tup_str: str = f'{pref}{post}'
                if pref in MusicTokenizer.pref2n:
                    n_tup = MusicTokenizer.pref2n[pref]
                else:
                    assert pref == 'Tu'  # A generic case, music21 processing, different from that of MuseScore
                    # e.g. 'C in octave 1 Dotted 32nd Tuplet of 9/8ths (1/6 QL) Note' makes 9 notes in tuplet
                    words = elm.fullName.split()
                    word_n_tup = words[words.index(tup_str)+2]
                    n_tup = int(word_n_tup[:word_n_tup.find('/')])

                elms_tup: List[Union[Rest, Note, Chord]] = [elm]
                elm_ = next(it, None)
                while elm_ is not None:
                    # For poor transcription quality, skip over non-note elements in the middle
                    if isinstance(elm_, (m21.clef.Clef, MetronomeMark, m21.bar.Barline)):
                        elm_ = next(it, None)
                    elif tup_str in elm_.fullName:  # Look for all elements of the same `n_tup`
                        elms_tup.append(elm_)
                        elm_ = next(it, None)  # Peeked 1 ahead
                    else:  # Finished looking for all tuplets
                        break
                # if number == 389:
                #     ic('in found tuplet', elms_tup)
                #     for n in elms_tup:
                #         ic(n, n.fullName, n.offset, n.duration.quarterLength)

                # Consecutive tuplet notes => (potentially multiple) groups
                it_tup = iter(elms_tup)
                e_tup = next(it_tup, None)
                dur: Union[Fraction, float] = 0
                idx, idx_next_strt, idx_last = 0, 0, len(elms_tup)-1
                n_tup_curr = 0
                tup_added = False
                idx_tup_strt = len(lst)
                is_single_tup = False  # Edge case, see below

                # MIDI & MuseScore transcription quality, e.g. A triplet may not contain 3 notes
                while e_tup is not None:
                    dur += e_tup.duration.quarterLength
                    n_tup_curr += 1
                    # Enforce a tuplet must have at least `n_tup` notes
                    # Duration for a (normal) tuplet must be multiples of 8th note; Heuristic for end of tuplet group
                    if n_tup_curr >= n_tup and is_8th(dur):
                        lst.append(tuple(elms_tup[idx_next_strt:idx+1]))
                        tup_added = True

                        # Prep for next tuplet
                        idx_next_strt = idx+1
                        n_tup_curr = 0
                        dur = 0

                    if idx == idx_last:  # Processed til last element, make sure all tuplet notes are added
                        if len(elms_tup) == 1:  # Poor processing, edge case
                            note = elms_tup[0]  # As if single note with weird duration
                            lst.append(note)
                            tup_added, is_single_tup = True, True
                            e_tup = None
                            continue  # Break out since done processing this tuplet group

                        if is_8th(dur) and n_tup_curr < n_tup:  # Last tuplet group not enough elements
                            if tup_added:  # Join the prior tuplet group if possible
                                lst[-1] = lst[-1] + tuple(elms_tup[idx_next_strt:])
                            else:  # Number of tuplet notes not enough, create new tuplet anyway
                                tup_added = True
                                lst.append(tuple(elms_tup[idx_next_strt:]))
                        else:  # Resort to the erroneous case only til the end
                            # Must be that duration of all triplet elements don't sum up to an 8th note in quarterLength
                            assert not is_8th(dur)  # Add such tuplet notes anyway, set a valid quantized length
                            warn_nm = WarnLog.InvTupDur
                            offsets, durs = notes2offset_duration(elms_tup[idx_next_strt:])
                            if not self.dur_within_prec(dur):  # Enforce it by changing the durations
                                warn_nm = WarnLog.InvTupDurSv

                                def round_by_factor(num, fact):
                                    return round(num / fact) * fact
                                # Round to quantization duration; Crop by bar max duration
                                dur = min(
                                    round_by_factor(dur, 2**-self.prec), time_sig.numerator/time_sig.denominator*4
                                )
                                n_tup_last = len(elms_tup[idx_next_strt:])
                                dur_ea = dur / n_tup_last
                                strt = elms_tup[idx_next_strt].offset
                                for i in range(idx_next_strt, idx_next_strt+n_tup_last):
                                    elms_tup[i].offset = strt
                                    dur_ = m21.duration.Duration(quarterLength=dur_ea)
                                    elms_tup[i].duration = dur_
                                    if isinstance(elms_tup[i], Chord):
                                        cd = elms_tup[i]
                                        for i_n in range(len(cd.notes)):  # Broadcast duration to notes inside
                                            elms_tup[i].notes[i_n].duration = dur_
                                    strt += dur_ea
                            lst.append(tuple(elms_tup[idx_next_strt:]))
                            tup_added = True
                            self.my_log_warn(dict(warn_name=warn_nm, bar_num=number, offsets=offsets, durations=durs))
                    idx += 1
                    e_tup = next(it_tup, None)
                # All triple notes with the same `n_tup` are added
                assert tup_added
                if not is_single_tup:
                    assert sum(len(tup) for tup in lst[idx_tup_strt:]) == len(elms_tup)

                    for tup in lst[idx_tup_strt:]:
                        ln = len(tup)
                        if ln != n_tup:
                            self.my_log_warn(dict(warn_name=WarnLog.InvTupSz, bar_num=number, n_expect=n_tup, n_got=ln))

                    for tup in lst[idx_tup_strt:]:  # Enforce no overlap in each triplet group
                        tup: tuple[Union[Note, Rest]]
                        if not is_notes_no_overlap(tup):
                            pass
                            # TODO: Left as is since code didn't seem to reach here ever
                            # offsets, durs = notes2offset_duration(tup)
                            # self.my_log_warn(dict(
                            #     warn_name=WarnLog.InvTupNt, bar_num=number, offsets=offsets, durations=durs
                            # ))
                            # it_n = iter(tup)
                            # nt = next(it_n)
                            # end = nt.offset + nt.duration.quarterLength
                            # tup_new = [nt]
                            # bar.show()
                            exit(1)
                            # while nt is not None:
                    for tup in lst[idx_tup_strt:]:
                        n_rest = sum(isinstance(n, Rest) for n in tup)
                        if n_rest != 0:
                            self.my_log_warn(dict(
                                warn_name=WarnLog.RestInTup, bar_num=number, n_rest=n_rest, n_note=len(tup)
                            ))

                    if not keep_chord:
                        tups_new = []
                        has_chord = False
                        for i in range(idx_tup_strt, len(lst)):  # Ensure all tuplet groups contain no Chord
                            tup = lst[i]
                            # Bad transcription quality => Keep all possible tuplet combinations
                            # Expect to be the same
                            if any(isinstance(n, Chord) for n in tup):
                                def chord2notes(c):
                                    notes_ = list(c.notes)
                                    for i_ in range(len(notes_)):  # Offsets for notes in chords are 0, restore them
                                        notes_[i_].offset = c.offset
                                    return notes_
                                has_chord = True
                                opns = [chord2notes(n) if isinstance(n, Chord) else (n,) for n in tup]
                                tups_new.extend(list(itertools.product(*opns)))
                        if has_chord:  # Replace prior triplet groups
                            lst = lst[:idx_tup_strt] + tups_new
                elm = elm_
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
            lst.extend(join_its(self.expand_bar(v, time_sig, number=number) for v in bar.voices))
        return lst

    def __call__(
            self, scr: Union[str, Score], exp='mxl'
    ) -> Union[Score, List[str], List[int], str]:
        """
        :param scr: A music21 Score object, or file path to an MXL file
        :param exp: Export mode, one of ['mxl', 'str', 'id', 'str_join', 'visualize']
            If `mxl`, a music21 Score is returned and written to file
            If `str` or `int`, the corresponding tokens and integer ids are returned as lists
            If `str_join`, the tokens are jointed together
            If `visualize`, a grouped, colorized string is returned, intended for console output
        """
        if isinstance(scr, str):
            scr = m21.converter.parse(scr)
        scr: Score

        title = scr.metadata.title
        if title.endswith('.mxl'):
            title = title[:-4]
        self.title = title

        lst_bar_info: List[tuple[tuple[Measure], TimeSignature, MetronomeMark]] = list(MusicTokenizer.it_bars(scr))
        n_bars_ori = len(lst_bar_info)  # Subject to change, see below

        # Crop out empty bars at both ends to reduce token length
        def is_empty_bars(bars: tuple[Measure]):
            def bar2elms(b: Measure):
                def stream2elms(stm: Union[Measure, Voice]):
                    return list(join_its((stm[Note], stm[Rest], stm[Chord])))  # Get all relevant notes
                elms = stream2elms(b)
                if b.hasVoices():
                    elms += sum((stream2elms(v) for v in b.voices), start=[])
                return elms
            return all(all(isinstance(e, Rest) for e in bar2elms(b)) for b in bars)
        empty_warns = []
        idx = 0
        while is_empty_bars(lst_bar_info[idx][0]):
            idx += 1
        idx_strt_last_empty = idx-1
        if idx_strt_last_empty != -1:  # 2-tuple, 0-indexed, inclusive on both ends
            empty_warns.append(dict(warn_name=WarnLog.EmptyStrt, bar_range=(0, idx_strt_last_empty)))

        idx = n_bars_ori-1
        while is_empty_bars(lst_bar_info[idx][0]):
            idx -= 1
        idx_end_1st_empty = idx+1
        if idx_end_1st_empty != n_bars_ori:
            empty_warns.append(dict(warn_name=WarnLog.EmptyEnd, bar_range=(idx_end_1st_empty, n_bars_ori-1)))
        lst_bar_info = lst_bar_info[idx_strt_last_empty+1:idx_end_1st_empty]

        lst_bars_, time_sigs, tempos = zip(*(
            (bars, time_sig, tempo) for bars, time_sig, tempo in lst_bar_info
        ))
        # Pick 1st bar arbitrarily
        secs = round(sum(t.durationToSeconds(bars[0].duration) for t, bars in zip(tempos, lst_bars_)))
        mean_tempo = round(np.array([t.number for t in tempos]).mean())  # To the closest integer
        counter_ts = Counter((ts.numerator, ts.denominator) for ts in time_sigs)
        time_sig_mode = max(counter_ts, key=counter_ts.get)
        ts_mode_str = f'{time_sig_mode[0]}/{time_sig_mode[1]}'
        if self.verbose:
            log(f'Tokenizing music {logi(self.title)}'
                f' - Time Signature: {logi(ts_mode_str)}, avg Tempo: {logi(mean_tempo)}, '
                f'{logi(len(lst_bars_))} bars with Duration: {logi(sec2mmss(secs))}...')
            if self.logger is not None:
                self.logger.start_tracking(args_func=lambda: dict(id=self.title, timestamp=now()))
        if not is_common_time_sig(time_sig_mode):
            self.my_log_warn(dict(
                warn_name=WarnLog.UncomTimeSig, time_sig_expect=COMMON_TIME_SIGS, time_sig_got=time_sig_mode
            ))
        for warn_dict in empty_warns:  # Postpone warning message until after logging song info
            self.my_log_warn(warn_dict)

        th = 0.95
        n_mode, n_bar = counter_ts[time_sig_mode], len(time_sigs)
        if (n_mode / n_bar) < th:  # Arbitrary threshold; Too much invalid time signature
            self.my_log_warn(dict(
                warn_name=WarnLog.IncTimeSig, time_sig=time_sig_mode, n_bar_total=n_bar, n_bar_mode=n_mode
            ))

        lst_notes: List[List[Union[Note, Chord, tuple[Note]]]] = []  # TODO: melody only
        i_bar_strt = lst_bars_[0][0].number  # Get number of 1st bar
        ic(i_bar_strt)
        for i_bar, (bars, time_sig, tempo) in enumerate(lst_bar_info):
            number = bars[0].number - i_bar_strt  # Enforce bar number 0-indexing
            assert number == i_bar
            ic(number)
            # if number == 50:
            #     for b in bars:
            #         b.show()
            notes = sum((self.expand_bar(b, time_sig, keep_chord=self.mode == 'full', number=number) for b in bars), [])

            groups: Dict[float, List[ExtNote]] = defaultdict(list)  # Group notes by starting location
            for n in notes:
                n_ = n[0] if isinstance(n, tuple) else n
                groups[n_.offset].append(n)
            # Sort by pitch then by duration

            def sort_groups(g):
                return {
                    offset: sorted(ns, key=lambda nt: (note2pitch(nt), note2dur(nt)))
                    for offset, ns in g.items()
                }
            groups = sort_groups(groups)
            # if number == 23:
            #     ic(groups)

            def get_notes_out(grps) -> List[Union[Note, Chord, tuple[Note]]]:
                if number == 50:
                    ic('in new get_notes_out', groups)
                ns_out = []
                offset_next = 0
                for offset in sorted(grps.keys()):  # Pass through notes in order
                    notes_ = grps[offset]
                    if len(notes_) == 0:  # As a result of removing triplets
                        continue
                    nt = notes_[-1]  # Note with the highest pitch
                    nt_ = nt[-1] if isinstance(nt, tuple) else nt
                    nt_end_offset = nt_.offset + nt_.duration.quarterLength
                    if number == 50:
                        ic(ns_out, nt, offset, offset_next)
                    eps = 1e-3
                    # For difference between floating point and Fraction on real small duration edge cases
                    # See below for another instance
                    if offset_next-offset > eps:
                        # Tuplet notes not normalized at this point, remain faithful to the weighted average pitch
                        if note2pitch(nt) > note2pitch(ns_out[-1]):
                            # Offset would closely line up across tracks, expect this to be less frequent
                            if isinstance(ns_out[-1], tuple):  # triplet being truncated => Remove triplet, start over
                                # The triplet must've been the last note added, and it's joint offset is known
                                del grps[ns_out[-1][0].offset][-1]
                                self.my_log_warn(dict(warn_name=WarnLog.HighPchOvlTup, bar_num=number))
                                return get_notes_out(grps)
                            else:  # Triplet replaces prior note
                                self.my_log_warn(dict(warn_name=WarnLog.HighPchOvl, bar_num=number))

                                nt_ = nt[0] if isinstance(nt, tuple) else nt
                                # Resulting duration usually non-0, for offset grouping
                                ns_out[-1].duration = dur_last = Duration(quarterLength=nt_.offset - ns_out[-1].offset)
                                assert dur_last.quarterLength >= 0
                                # If it's 0, it's cos a **truncated** note was appended, as makeup
                                if dur_last.quarterLength == 0:
                                    self.my_log_warn(dict(warn_name=WarnLog.LowPchMakeupRmv, bar_num=number))
                            ns_out.append(nt)
                            offset_next = nt_end_offset
                        # Later note has smaller pitch, but ends later than the last note
                        # Truncate the note, add it into later group for consideration
                        elif (nt_end_offset-offset_next) > eps:
                            if not isinstance(nt, tuple):
                                # Move the truncated note to later group, restart
                                del grps[offset][-1]
                                nt_ = note2note_cleaned(nt)
                                nt_.offset = offset_next
                                nt_.duration = d = Duration(quarterLength=nt_end_offset-offset_next)
                                ic(nt.duration.quarterLength, nt_end_offset, offset_next, d.quarterLength)
                                assert d.quarterLength > 0
                                if offset_next in grps:
                                    grps[offset_next].append(nt_)
                                else:
                                    grps[offset_next] = [nt_]
                                grps = sort_groups(grps)
                                self.my_log_warn(dict(warn_name=WarnLog.LowPchMakeup, bar_num=number))
                                return get_notes_out(grps)
                            # Skip adding tuplets, TODO: can this potentially lead to gaps in the extraction?
                        # Otherwise, skip if later note is lower in pitch and is covered by the prior note duration
                    else:
                        ns_out.append(nt)
                        offset_next = nt_end_offset
                return ns_out
            notes_out = get_notes_out(groups)
            # For poor transcription quality, postpone `is_valid_bar_notes` *assertion* until after quantization,
            # since empirically observe notes don't sum to bar duration,
            #   e.g. tiny-duration notes shifts all subsequent notes
            #     n: <music21.note.Rest inexpressible>
            #     n.fullName: 'Inexpressible Rest'
            #     n.offset: 2.0
            #     n.duration.quarterLength: Fraction(1, 480)
            dur_bar = time_sig.numerator / time_sig.denominator * 4
            if not math.isclose(sum(n.duration.quarterLength for n in flatten_notes(notes_out)), dur_bar, abs_tol=1e-6):
                offsets, durs = notes2offset_duration(notes_out)
                self.my_log_warn(dict(
                    warn_name=WarnLog.InvBarDur, bar_num=number, offsets=offsets, durations=durs, time_sig=time_sig
                ))
            if not is_notes_no_overlap(notes_out):
                # Convert tuplet to single note by duration, pitch doesn't matter, prep for overlap check
                def tup2note(t: tuple[Note]):
                    note = Note()
                    note.offset = min(note_.offset for note_ in t)
                    q_len_max = max(note_.offset + note_.duration.quarterLength for note_ in t) - note.offset
                    note.duration = Duration(quarterLength=q_len_max)
                    return note
                notes_out_ = [tup2note(n) if isinstance(n, tuple) else n for n in notes_out]  # Temporary, for checking
                # if number == 23:
                #     ic('original notes', notes_out)
                #     for n in flatten_notes(notes_out):
                #         ic(n, n.fullName, n.offset, n.duration.quarterLength)
                #     ic('tuplet converted notes', notes_out_)
                #     for n in notes_out_:
                #         ic(n, n.fullName, n.offset, n.duration.quarterLength)
                assert is_notes_no_overlap(notes_out_)  # The source of overlapping should be inside tuplet
                for tup__ in notes_out:
                    if isinstance(tup__, tuple) and not is_notes_no_overlap(tup__):
                        offsets, durs = notes2offset_duration(tup__)
                        self.my_log_warn(dict(
                            warn_name=WarnLog.TupNoteOvl, bar_num=number, offsets=offsets, durations=durs
                        ))
            lst_notes.append([note2note_cleaned(n) for n in notes_out])

        # Enforce quantization
        dur_slot = 4 / 2**self.prec  # quarterLength by quantization precision

        def note_within_prec(note):
            return (note2dur(note) / dur_slot).is_integer()

        def notes_within_prec(notes_):
            return all(note_within_prec(n__) for n__ in notes_)
        for i_bar, (notes, time_sig) in enumerate(zip(lst_notes, time_sigs)):
            if not notes_within_prec(notes):
                lst_notes[i_bar] = self.notes2quantized_notes(notes, time_sig, number=i_bar)
                assert notes_within_prec(lst_notes[i_bar])  # Sanity check implementation
                offsets, durs = notes2offset_duration(notes)
                self.my_log_warn(dict(warn_name=WarnLog.NoteNotQuant, bar_num=i_bar, offsets=offsets, durations=durs))
        # Now, triplets fixed to equal duration by `notes2quantized_notes`

        def trip_n_quant2notes(notes_: List[Union[Rest, Note, tuple[Note]]], num_bar: int):
            lst = []
            for nt in notes_:
                # If triplet notes turned out quantized, i.e. durations are in powers of 2, turn to normal notes
                if isinstance(nt, tuple) and any(note_within_prec(n__) for n__ in nt):
                    assert all(note_within_prec(n__) for n__ in nt)  # Should be equivalent
                    lst.extend(nt)
                    offsets_, durs_ = notes2offset_duration(notes)
                    self.my_log_warn(dict(
                        warn_name=WarnLog.TupNoteQuant, bar_num=num_bar, offsets=offsets_, durations=durs_
                    ))
                else:
                    lst.append(nt)
            return lst
        lst_notes = [trip_n_quant2notes(notes, num_bar=i) for i, notes in enumerate(lst_notes)]
        for notes, time_sig in zip(lst_notes, time_sigs):  # Final check before output
            is_valid_bar_notes(notes, time_sig)
        if self.verbose and self.logger is not None:
            log(f'Encoding {logi(self.title)} completed - Observed warnings {{{self.logger.tracked()}}}')

        if exp == 'mxl':
            scr_out = Score()
            scr_out.insert(m21.metadata.Metadata())
            post = 'Melody only' if self.mode == 'melody' else 'Melody & Chord'
            title = f'{self.title}, {post}'
            scr_out.metadata.title = title
            scr_out.metadata.composer = PKG_NM

            part_nm = 'Melody, Ch#1'  # TODO: a 2nd chord part
            part = m21.stream.Part(partName=part_nm)
            part.partName = part_nm
            instr = m21.instrument.Piano()
            part.append(instr)

            lst_bars = []
            for i, notes in enumerate(lst_notes):
                bar = Measure(number=i)  # Original bar number may not start from 0
                bar.append(list(flatten_notes(notes)))
                lst_bars.append(bar)
            part.append(lst_bars)

            bar0 = part.measure(0)  # Insert metadata into 1st bar
            bar0.insert(MetronomeMark(number=mean_tempo))
            bar0.insert(TimeSignature(ts_mode_str))

            dir_nm = config(f'{DIR_DSET}.MXL_EG.dir_nm')
            dir_nm = f'{dir_nm}_out'
            scr_out.append(part)
            scr_out.write(fmt='mxl', fp=os.path.join(PATH_BASE, DIR_DSET, dir_nm, f'{title}.mxl'))
            return scr_out
        else:
            assert exp in ['str', 'id', 'visualize', 'str_join']
            color = exp == 'visualize'
            self.vocab.color = color

            def e2s(elm):  # Syntactic sugar
                return self.vocab(elm, color=color)

            groups_: List[List[str]] = [
                [*e2s(time_sig_mode), *e2s(mean_tempo)],
                *(([self.vocab['start_of_bar']] + sum([e2s(n) for n in notes], start=[])) for notes in lst_notes),
                [self.vocab['end_of_song']]
            ]  # TODO: adding Chords as 2nd part?
            if exp == 'visualize':
                n_pad = len(str(len(groups_)))

                def idx2str(i):
                    return logs(f'{i:>{n_pad}}:', c='y')
                return '\n'.join(f'{idx2str(i)} {" ".join(toks)}' for i, toks in enumerate(groups_))
            else:
                toks = sum(groups_, start=[])
                if exp in ['str', 'id']:
                    return toks if exp == 'str' else self.vocab.encode(toks)
                else:
                    return ' '.join(toks)


if __name__ == '__main__':
    from icecream import ic

    def toy_example():
        logger = WarnLog()
        fnm = eg_songs('Merry Go Round of Life', fmt='MXL')
        # fnm = eg_songs('Shape of You', fmt='MXL')
        # fnm = eg_songs('平凡之路', fmt='MXL')
        ic(fnm)
        mt = MusicTokenizer(logger=logger, verbose=True)

        def check_mxl_out():
            mt(fnm, exp='mxl')
            ic(logger.to_df())

        def check_str():
            toks = mt(fnm, exp='str')
            ic(len(toks), toks[:20])

        def check_visualize():
            s = mt(fnm, exp='visualize')
            print(s)

        # check_mxl_out()
        # check_str()
        check_visualize()
    # toy_example()

    def encode_a_few():
        dnm = 'POP909'
        fnms = fl_nms(dnm, k='song_fmt_exp')
        # ic(fnms[:20])

        # idx = [idx for idx, fnm in enumerate(fnms) if '恋爱ing' in fnm][0]
        # ic(idx)
        # exit(1)
        logger = WarnLog()
        mt = MusicTokenizer(logger=logger, verbose=True)
        for i_fl, fnm in enumerate(fnms[637:]):
            ic(i_fl)
            mt(fnm, exp='mxl')

            # s = mt(fnm, exp='visualize')
            # print(s)
    encode_a_few()

    def check_vocabulary():
        vocab = MusicVocabulary()
        ic(vocab.enc, vocab.size)

        fnm = eg_songs('Merry Go Round of Life', fmt='MXL')
        mt = MusicTokenizer()
        toks = mt(fnm, exp='str')
        ic(vocab.encode(toks[:20]))
    # check_vocabulary()

