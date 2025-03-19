# MML -> MIDI converter
# Written in hopes of being finally set free of Nin0's purgatory

try:
    import mido
except ImportError:
    mido = None

import random

from revo_snd.engine._snd.OS_SeqPlayer import (
    SEQ_LOCAL_VAR_RANGE,
    SEQ_GLOBAL_VAR_RANGE,
    SEQ_TRACK_VAR_RANGE,

    SEQ_MAX_VAR,
    SEQ_VAR_DEFAULT
)

import brseq
from revo_snd.rseq.mml_instruction import MML, MMLEX
from revo_snd.rseq.mml_parser import Sequence, Cmd
from revo_snd.rseq.note import Note

__GLOBAL_VARS__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR


def _mido_installed() -> None:
    if mido is None:
        raise ImportError(('"mido" is not installed. Please make sure that the "mido" package'
                           ' for Python is installed. Install mido using pip, i.e. "pip install mido"'))


def get_var(idx: int, __local_vars__: list[int], __trk_vars__: list[int]) -> int:
    if idx in SEQ_LOCAL_VAR_RANGE:
        return __local_vars__[idx]
    elif idx in SEQ_GLOBAL_VAR_RANGE:
        return __GLOBAL_VARS__[idx - 16]
    elif idx in SEQ_TRACK_VAR_RANGE:
        return __trk_vars__[idx - 32]
    else:
        raise IndexError(f'Invalid var no {idx} for sequence')


def set_var(idx: int, val: int, __local_vars__: list[int], __trk_vars__: list[int]) -> None:
    if idx in SEQ_LOCAL_VAR_RANGE:
        __local_vars__[idx] = val
    elif idx in SEQ_GLOBAL_VAR_RANGE:
        __GLOBAL_VARS__[idx - 16] = val
    elif idx in SEQ_TRACK_VAR_RANGE:
        __trk_vars__[idx - 32] = val
    else:
        raise IndexError(f'Invalid var no {idx} for sequence')


def compute_prefix_cmd(__c: Cmd, __local_vars__: list[int], __trk_vars__: list[int]) -> int:
    result = 0
    if isinstance(__c.cmd, tuple):
        for __pre in __c.cmd[1:]:
            match __pre:
                case MML.RANDOM:
                    rand_args = __c.args[0]
                    result = random.randint(rand_args[0], rand_args[1])
                case MML.VARIABLE:
                    if isinstance(__c.get_cmd(), MMLEX):
                        result = get_var(__c.args[1], __local_vars__, __trk_vars__)
                    else:
                        result = get_var(__c.args[0], __local_vars__, __trk_vars__)
    else:
        if (__len := len(__c.args)) > 0:
            if __len == 1:
                result = __c.args[0]
            else:
                result = __c.args

    return result


def _parse_seq(seq: Sequence, __local_vars__: list[int]) -> mido.MidiFile:
    __trk_vars__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR

    _midi = mido.MidiFile(type=0, ticks_per_beat=96)
    trk = mido.MidiTrack()
    _midi.tracks.append(trk)

    if len(tempo := seq.get_specific_cmd(MML.TEMPO)) > 0:
        tempo = tempo[0].args[0]
        trk.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo), time=0))

    current_time = 0
    for cmd in seq.cmd_set:
        if isinstance(cmd.cmd, Note):
            velocity, length = compute_prefix_cmd(cmd, __local_vars__, __trk_vars__)
            note = cmd.cmd.value

            trk.append(mido.Message('note_on', note=note, velocity=velocity, time=length - current_time))
            trk.append(mido.Message('note_off', note=note, velocity=0, time=length))

        match cmd.cmd:
            case MML.PRG:
                trk.append(mido.Message('program_change', program=cmd.args[0]))

    return _midi


class Midi:
    def __init__(self, rseq: brseq.BRSEQ) -> None:
        self._sequences = rseq._seq_data
        self._parse()

    def _parse(self) -> None:
        _mido_installed()

        __local_vars__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR
        midis = []

        for seq in self._sequences.values():
            midis.append(_parse_seq(seq, __local_vars__))


with open(r'C:\Users\oguy\Desktop\nin0_is_doubting_me.brseq', 'rb') as file:
    rseq = brseq.BRSEQ(file)
    # print(rseq['SE_PLY_THROW_FIRE'].pretty_string())
    midi = Midi(rseq)
