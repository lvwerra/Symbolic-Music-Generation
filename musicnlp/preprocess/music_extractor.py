"""
Since Sun. Jan. 30th, an updated module for music/melody extraction, with a duration-quantized approach

See `melody_extractor` for the old version.
"""

from collections import defaultdict, Counter

from music21.stream import Voice
from music21.duration import Duration

from musicnlp.util import *
from musicnlp.util.music_lib import *
from musicnlp.preprocess import WarnLog


pd.set_option('display.max_columns', None)  # TODO


class MusicExtractor:
    """
    Extract melody and potentially chords from MXL music scores => An 1D polyphonic representation
    """
    def __init__(
            self, precision: int = 5, mode: str = 'melody',
            logger: Union[WarnLog, bool] = None, save_memory=True, verbose=True
    ):
        """
        :param precision: Bar duration quantization, see `melody_extractor.MxlMelodyExtractor`
        :param mode: Extraction mode, one of [`melody`, `full`]
            `melody`: Only melody is extracted
            `full`: Melody and Chord as 2 separate channels extracted TODO
        :param logger: A logger for storing warnings
            If True, a logger is instantiated
        :param save_memory: If true, prior logging warning messages are removed after new encode call
            See `Warning.end_tracking`
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
        self.save_memory = save_memory
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
        parts = list(scr.parts)
        ignore = [(any(p_[drum] for drum in instrs_drum) or is_drum(p_)) for p_ in parts]

        time_sig, tempo = None, None
        for idx, bars in enumerate(zip(*[list(p[Measure]) for p in parts])):  # Bars for all tracks across time
            # Still enumerate the to-be-ignored tracks for getting time signature and tempo
            assert list_is_same_elms([b.number for b in bars]), 'Bar numbers should be the same'

            # Update time signature
            tss = [b[TimeSignature] for b in bars]
            if idx == 0 or any(tss):  # 1st bar must have time signature defined
                assert all(len(t) == 1 for t in tss)
                tss = [next(t) for t in tss]
                assert list_is_same_elms([(ds.numerator, ds.denominator) for ds in tss])
                time_sig = tss[0]

            tempos = [list(b[MetronomeMark]) for b in bars]
            if idx == 0 or any(tempos):
                tempos = [t for t in tempos if len(t) != 0]
                # When multiple tempos, take the mean
                tempos = [MetronomeMark(number=np.array([t.number for t in ts]).mean()) for ts in tempos]
                bpms = [t.number for t in tempos]
                assert list_is_same_elms(bpms)

                tempo = MetronomeMark(number=bpms[0])
            yield [b for ignore, b in zip(ignore, bars) if not ignore], time_sig, tempo

    def log_warn(self, log_d: Dict):
        if self.logger is not None:
            self.logger.update(log_d)

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
        # ic('in quantize', number)
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
        # if number == 50:
        #     ic(notes)
        #     for n in flatten_notes(notes):
        #         ic(n, n.fullName, n.offset, n.duration.quarterLength)
        #     ic([get_overlap(*edge, i) > 0 for edge, i in zip(bin_edges, idxs_note)])
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
        lst = []
        it = iter(bar)
        elm = next(it, None)
        while elm is not None:
            if hasattr(elm, 'fullName') and TUPLET_POSTFIX in elm.fullName:
                tup_str, n_tup = fullname2tuplet_meta(elm.fullName)

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
                if number == 111:
                    ic('in found tuplet', len(elms_tup), tup_str, n_tup)
                    for n in elms_tup:
                        ic(n, n.fullName, n.offset, n.duration.quarterLength)

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
                            self.log_warn(dict(warn_name=warn_nm, bar_num=number, offsets=offsets, durations=durs))
                    idx += 1
                    e_tup = next(it_tup, None)
                # All triple notes with the same `n_tup` are added
                assert tup_added
                if not is_single_tup:
                    assert sum(len(tup) for tup in lst[idx_tup_strt:]) == len(elms_tup)

                    for tup in lst[idx_tup_strt:]:
                        ln = len(tup)
                        if ln != n_tup:
                            self.log_warn(dict(warn_name=WarnLog.InvTupSz, bar_num=number, n_expect=n_tup, n_got=ln))

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
                            self.log_warn(dict(
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
                                n_opns = [len(n) for n in opns if n]
                                if np.prod(n_opns) > 3 ** 9:
                                    # Too much possible cartesian products for later processing to handle
                                    # as it involves sorting
                                    # Cap at a tuplet of 9 consecutive 3-note Chords, beyond this number,
                                    # just treat the bar as wicked
                                    self.log_warn(dict(
                                        warn_name=WarnLog.ExcecTupNote, bar_num=number, note_choices=n_opns
                                    ))
                                    notes_max_pitch = tuple([max(notes, key=note2pitch) for notes in opns])
                                    tups_new.append(notes_max_pitch)
                                else:
                                # if number == 111 and len(opns) == 25:
                                #     ic(len(opns), [len(o) for o in opns])
                                #     ic(tup, len(tup), opns)
                                #     ic(type(bar))
                                #     bar.show()
                                #     exit(1)
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
            self, song: Union[str, Score], exp='mxl', return_duration=False,
    ) -> Union[
        Tuple[Union[Score, List[str], List[int], str]],
        Tuple[Union[Score, List[str], List[int], str], int]
    ]:
        """
        :param song: A music21 Score object, or file path to an MXL file
        :param exp: Export mode, one of ['mxl', 'str', 'id', 'str_join', 'visualize']
            If `mxl`, a music21 Score is returned and written to file
            If `str` or `int`, the corresponding tokens and integer ids are returned as lists
            If `str_join`, the tokens are jointed together
            If `visualize`, a grouped, colorized string is returned, intended for console output
        :param return_duration: If true, the song duration in seconds is also returned
        """
        if self.logger is not None and self.save_memory:
            self.logger.end_tracking()

        if isinstance(song, str):
            song = m21.converter.parse(song)
        song: Score

        title = song.metadata.title
        if title.endswith('.mxl'):
            title = title[:-4]
        self.title = title

        lst_bar_info: List[tuple[tuple[Measure], TimeSignature, MetronomeMark]] = list(MusicExtractor.it_bars(song))
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
        set_ts = set(f'{ts.numerator}/{ts.denominator}' for ts in time_sigs)
        set_tp = set(round(tp.number) for tp in tempos)
        if len(set_ts) > 1:
            self.log_warn(dict(warn_name=WarnLog.MultTimeSig, time_sigs=sorted(set_ts)))
        if len(set_tp) > 1:
            self.log_warn(dict(warn_name=WarnLog.MultTempo, tempos=sorted(set_tp)))
        if not is_common_time_sig(time_sig_mode):
            self.log_warn(dict(
                warn_name=WarnLog.UncomTimeSig, time_sig_expect=COMMON_TIME_SIGS, time_sig_got=time_sig_mode
            ))
        for warn_dict in empty_warns:  # Postpone warning message until after logging song info
            self.log_warn(warn_dict)

        th = 0.95
        n_mode, n_bar = counter_ts[time_sig_mode], len(time_sigs)
        if (n_mode / n_bar) < th:  # Arbitrary threshold; Too much invalid time signature
            self.log_warn(dict(
                warn_name=WarnLog.IncTimeSig, time_sig=time_sig_mode, n_bar_total=n_bar, n_bar_mode=n_mode
            ))

        lst_notes: List[List[Union[Note, Chord, tuple[Note]]]] = []  # TODO: melody only
        i_bar_strt = lst_bars_[0][0].number  # Get number of 1st bar
        # ic(i_bar_strt)
        for i_bar, (bars, time_sig, tempo) in enumerate(lst_bar_info):
            number = bars[0].number - i_bar_strt  # Enforce bar number 0-indexing
            assert number == i_bar
            ic(number)
            # if number == 50:
            #     for b in bars:
            #         b.show()
            if number == 111:
                ic('in bar 111')
            notes = sum((self.expand_bar(b, time_sig, keep_chord=self.mode == 'full', number=number) for b in bars), [])
            if number == 111:
                ic('in bar 111, finished expand bar')

            groups: Dict[float, List[ExtNote]] = defaultdict(list)  # Group notes by starting location
            for n in notes:
                n_ = n[0] if isinstance(n, tuple) else n
                groups[n_.offset].append(n)
            # Sort by pitch then by duration
            if number == 111:
                ic('in bar 111, finished group creation', [len(g) for g in groups.values()])

            def sort_groups(g):
                return {
                    offset: sorted(ns, key=lambda nt: (note2pitch(nt), note2dur(nt)))
                    for offset, ns in g.items()
                }
            groups = sort_groups(groups)
            if number == 111:
                ic('in bar 111, finished group sorting')
            # if number == 1:
            #     ic(groups)
            #     for elm in groups[0]:
            #         if isinstance(elm, tuple):
            #             ic('tuplet')
            #             for e in elm:
            #                 ic(e, e.duration, e.pitch if isinstance(e, Note) else e.name)
            #         else:
            #             ic(elm, elm.duration, elm.pitch if isinstance(elm, Note) else elm.name)

            def get_notes_out(grps) -> List[Union[Note, Chord, tuple[Note]]]:
                # if number == 50:
                #     ic('in new get_notes_out', groups)
                if number == 111:
                    ic('in bar 111, get notes out')
                ns_out = []
                offset_next = 0
                for offset in sorted(grps.keys()):  # Pass through notes in order
                    notes_ = grps[offset]
                    if len(notes_) == 0:  # As a result of removing triplets
                        continue
                    nt = notes_[-1]  # Note with the highest pitch
                    nt_ = nt[-1] if isinstance(nt, tuple) else nt
                    nt_end_offset = nt_.offset + nt_.duration.quarterLength
                    # if number == 50:
                    #     ic(ns_out, nt, offset, offset_next)
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
                                self.log_warn(dict(warn_name=WarnLog.HighPchOvlTup, bar_num=number))
                                return get_notes_out(grps)
                            else:  # Triplet replaces prior note
                                self.log_warn(dict(warn_name=WarnLog.HighPchOvl, bar_num=number))

                                nt_ = nt[0] if isinstance(nt, tuple) else nt
                                # Resulting duration usually non-0, for offset grouping
                                ns_out[-1].duration = dur_last = Duration(quarterLength=nt_.offset - ns_out[-1].offset)
                                assert dur_last.quarterLength >= 0
                                # If it's 0, it's cos a **truncated** note was appended, as makeup
                                if dur_last.quarterLength == 0:
                                    self.log_warn(dict(warn_name=WarnLog.LowPchMakeupRmv, bar_num=number))
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
                                assert d.quarterLength > 0
                                if offset_next in grps:
                                    grps[offset_next].append(nt_)
                                else:
                                    grps[offset_next] = [nt_]
                                grps = sort_groups(grps)
                                self.log_warn(dict(warn_name=WarnLog.LowPchMakeup, bar_num=number))
                                return get_notes_out(grps)
                            # Skip adding tuplets, TODO: can this potentially lead to gaps in the extraction?
                        # Otherwise, skip if later note is lower in pitch and is covered by the prior note duration
                    else:
                        ns_out.append(nt)
                        offset_next = nt_end_offset
                return ns_out
            notes_out = get_notes_out(groups)
            # if number == 2:
            #     ic(notes_out)
            #     exit(1)
            if number == 111:
                ic('in bar 111, finished get_notes_out')
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
                self.log_warn(dict(
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
                assert is_notes_no_overlap(notes_out_)  # The source of overlapping should be inside tuplet
                for tup__ in notes_out:
                    if isinstance(tup__, tuple) and not is_notes_no_overlap(tup__):
                        offsets, durs = notes2offset_duration(tup__)
                        self.log_warn(dict(
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
                self.log_warn(dict(warn_name=WarnLog.NoteNotQuant, bar_num=i_bar, offsets=offsets, durations=durs))
        # Now, triplets fixed to equal duration by `notes2quantized_notes`

        def trip_n_quant2notes(notes_: List[Union[Rest, Note, tuple[Note]]], num_bar: int):
            lst = []
            for nt in notes_:
                # If triplet notes turned out quantized, i.e. durations are in powers of 2, turn to normal notes
                if isinstance(nt, tuple) and any(note_within_prec(n__) for n__ in nt):
                    assert all(note_within_prec(n__) for n__ in nt)  # Should be equivalent
                    lst.extend(nt)
                    offsets_, durs_ = notes2offset_duration(notes)
                    self.log_warn(dict(
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

        if exp == 'mxl':  # TODO: didn't test
            scr_out = make_score(
                title=f'{self.title}, extracted', mode=self.mode, time_sig=ts_mode_str, tempo=mean_tempo,
                lst_note=[list(flatten_notes(notes)) for notes in lst_notes]
            )
            dir_nm = config(f'{DIR_DSET}.mxl-eg.dir_nm_extracted')
            fmt = 'mxl'
            # fmt = 'musicxml'
            # sometimes file-writes via `mxl` couldn't be read by MuseScore
            scr_out.write(fmt=fmt, fp=os.path.join(PATH_BASE, DIR_DSET, dir_nm, f'{title}.{fmt}'), makeNotation=False)
            ret = scr_out
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
                    return log_s(f'{i:>{n_pad}}:', c='y')
                ret = '\n'.join(f'{idx2str(i)} {" ".join(toks)}' for i, toks in enumerate(groups_))
            else:
                toks = sum(groups_, start=[])
                if exp in ['str', 'id']:
                    ret = toks if exp == 'str' else self.vocab.encode(toks)
                else:
                    ret = ' '.join(toks)
        if return_duration:
            return ret, secs


if __name__ == '__main__':
    from icecream import ic

    import musicnlp.util.music as music_util

    def toy_example():
        logger = WarnLog()
        # fnm = get_my_example_songs('Merry Go Round of Life', fmt='MXL')
        # fnm = get_my_example_songs('Shape of You', fmt='MXL')
        # fnm = get_my_example_songs('平凡之路', fmt='MXL')
        fnm = music_util.get_my_example_songs('Canon')
        # fnm = music_util.get_my_example_songs('canonpiano')
        # fnm = music_util.get_my_example_songs('canonroc1')
        ic(fnm)
        mt = MusicExtractor(logger=logger, verbose=True)

        def check_mxl_out():
            mt(fnm, exp='mxl')
            ic(logger.to_df())

        def check_str():
            toks = mt(fnm, exp='str')
            ic(len(toks), toks[:20])

        def check_visualize():
            s = mt(fnm, exp='visualize')
            print(s)

        check_mxl_out()
        # check_str()
        # check_visualize()
    # toy_example()

    def encode_a_few():
        # dnm = 'POP909'
        dnm = 'LMD-cleaned-subset'
        fnms = music_util.get_cleaned_song_paths(dnm, fmt='mxl')[6:]
        # ic(len(fnms), fnms[:5])

        # idx = [idx for idx, fnm in enumerate(fnms) if '恋爱ing' in fnm][0]
        # ic(idx)
        # exit(1)
        logger = WarnLog()
        me = MusicExtractor(logger=logger, verbose=True)
        for i_fl, fnm in enumerate(fnms):
            ic(i_fl)
            me(fnm, exp='mxl')
            # exit(1)
            # s = mt(fnm, exp='visualize')
            # print(s)
    encode_a_few()

    def check_vocabulary():
        vocab = MusicVocabulary()
        ic(vocab.enc, vocab.dec, len(vocab))

        # fnm = eg_songs('Merry Go Round of Life', fmt='MXL')
        # mt = MusicTokenizer()
        # toks = mt(fnm, exp='str')
        # ic(vocab.encode(toks[:20]))
    # check_vocabulary()
