import dataclasses
import random
from collections import namedtuple
from typing import BinaryIO

import revo_snd.engine.OS as OS
from revo_snd.engine.OS import clamp, unpack_singleton_value
from revo_snd.rbnk.brbnk import BRBNK, WavDataLocationType, InstParam

from revo_snd.rseq.brseq import BRSEQ
from revo_snd.rseq.mml_parser import Cmd, Sequence
from revo_snd.rseq.mml_instruction import (MML, MMLEX)
from revo_snd.rseq.note import Note

from revo_snd.rwar.brwar import BRWAR
from revo_snd.rwav.brwav import BRWAV

SEQ_BASE_NOTE              = 60  # cn4 is the default value

SEQ_DEFAULT_TEMPO          = 120
SEQ_DEFAULT_TIME_BASE      = 48

SEQ_MAX_STACK_DEPTH        = 3

SEQ_VAR_DEFAULT            = -1
SEQ_MAX_VAR                = 16
SEQ_LOCAL_VAR_RANGE        = range(0, 16)
SEQ_GLOBAL_VAR_RANGE       = range(16, 32)
SEQ_TRACK_VAR_RANGE        = range(32, 48)

SEQ_MAX_PRG                = 0xFFFF
SEQ_MOD_DEPTH_CONST        = 128.0
SEQ_MOD_SPEED_CONST        = 0.390625
SEQ_SWEEP_PITCH_CONST      = 64.0
SEQ_DAMPER_CONST           = 64
SEQ_LPF_CUTOFF_INT_CONST   = 64
SEQ_LPF_CUTOFF_FLOAT_CONST = 64.0
SEQ_BIQUAD_VAL_CONST       = 127.0

# Global Variable table, shared between all BRSEQ files
__GLOBAL_VARS__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR
__CALL_DEPTH__ = 0

# skeletal "sound handle" for an individual BRSEQ
#     rseq           : The BRSEQ attached to this handle
#     __LOCAL_VARS__ : Variable list shared between all tracks inside the BRSEQ
__OS_SeqHandle = namedtuple('__OS_SeqHandle', ['rseq'])
__OS_SeqHandles__ = {}


@dataclasses.dataclass
class __OS_SeqHandle:
    rseq: BRSEQ

    def __init__(self, rseq: BRSEQ) -> None:
        self.rseq = rseq
        self.__LOCAL_VARS__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR


def __OS_CreateSeqHandle(brseq: BRSEQ) -> __OS_SeqHandle:
    global __OS_SeqHandles__
    if brseq in __OS_SeqHandles__:
        return __OS_SeqHandles__[brseq]

    snd_handle = __OS_SeqHandle(brseq)
    __OS_SeqHandles__[brseq] = snd_handle

    return snd_handle


def OS_SeqHandle_Play2(brsar: BinaryIO, brseq: BRSEQ, seq_name: str, brbnk: BRBNK, brwar: BRWAR) -> (BRWAV | list[BRWAV]):
    """
    Fast version of OS_SeqHandle_Play. The result will be as if all variations of
    the given sequence would have been played in a real environment. This function
    does not play the sequence itself but rather fetches all sample data for the
    specified sequence in accordance to the given BRBNK.

    :param brsar:    The binary data stream for the BRSAR.
    :param brseq:    The sequence file.
    :param seq_name: The name of the sequence to play.
    :param brbnk:    The BRBNK with the instrument data.
    :param brwar:    The BRWAR the BRBNK uses.
    :return: all used BRWAV files/samples in a list.
    """

    if brsar is None or brseq is None or brbnk is None or brwar is None:
        raise ValueError((f'Received following data: {[type(brsar), type(brseq), type(seq_name), type(brbnk), type(brwar)]}\n'
                         '\t\t\tCannot have None values for sound playback!\n'))

    already_computed = []

    def get_all_callees(__seq: (str | int)) -> (list[Sequence] | None):
        if __seq in already_computed:
            return None

        already_computed.append(__seq)
        __caller = brseq[__seq]

        callees = []
        for callee in __caller.calling:
            if isinstance(callee, int) and callee == __caller.start_offset:
                break

            try:
                callees.append(brseq[callee])
                if (__tmp := get_all_callees(callee)) is not None:
                    callees += __tmp
            except IndexError:
                # Seems to be a jump in a sequence itself
                # see mml_parser for more thorough explanation
                continue

        return callees

    # Main sequence
    seq = brseq[seq_name]
    calling = get_all_callees(seq_name)

    call_stack = list(dict.fromkeys([seq] + calling))
    samples = []

    def get_wav(__inst_data: InstParam) -> (BRWAV | None):
        if __inst_data is None:
            return None

        match __inst_data.wav_dat_loc_type:
            case WavDataLocationType.INDEX:
                return brwar[__inst_data.wav_no]
            case WavDataLocationType.ADDRESS:
                brsar.seek(__inst_data.wav_no)
                return BRWAV(brsar)
            case WavDataLocationType.CALLBACK | _:
                print(f'No implementation for wav_data_loc_type={__inst_data.wav_dat_loc_type}')

    for caller in call_stack:
        for cmd in caller.cmd_set:
            if isinstance(cmd.get_cmd(), MML) and cmd.get_cmd() == MML.PRG:
                prg = cmd.args[0]
                if isinstance(prg, tuple):
                    inst_data = []
                    for i in prg:
                        data = brbnk.get_inst_param_direct(i)
                        if isinstance(data, list):
                            inst_data += data
                        else:
                            inst_data.append(data)
                else:
                    inst_data = brbnk.get_inst_param_direct(cmd.args[0])

                if isinstance(inst_data, list):
                    [samples.append(get_wav(i)) for i in inst_data]
                else:
                    samples.append(get_wav(inst_data))

    return samples


def OS_SeqHandle_Play(brseq: BRSEQ, seq_name: (str | int), *, disable_random_values: bool = False) -> tuple[list, list]:
    """
    Generates an output for the specified track in the provided BRSEQ file
    and returns all generated sounds and calls to program changes
    (PRG x instruction invocations).

    The return value will either be a tuple containing the PRG command and
    the produced note, or a list of all invocations of the PRG command and
    all played sounds, i.e:

    ([prg 1, prg2, [prg 76, prg 3, [prg 1]]], [cn4, dn4, as1])

    The maximum call stack depth is limited to 3 (according to Nintendo's
    own SeqPlayer). This means, this function will never recursively call itself
    more than 3 times, if so, an exception will be raised.

    Every recursive call alongside its generated output will be stored
    in a sub list inside the main list (see example above). If there is only
    a single output, it will be not stored inside a list, i.e.:

    (prg 1, [cn4, as2])

    The output generated by this function is used to help determine, which
    sound inside a range region may be played. The main factors are the
    called programm (PRG x) which references the instrument data inside the
    respective bank file, and the (probably) produces note. There is no guarantee
    that the produced output for the notes is exactly what the Wii would produce
    for the given track. It is rather an approximation for the program's sake.

    :param brseq: A valid BRSEQ file.
    :param seq_name: The name of the track to play.
    :param disable_random_values: Flag whether random values should be generated or not. This flag should be
                                  used with caution, as the produced result may yield unintended side effects.
                                  If this flag is set, instead of the random value, the following number will be used:
                                  may 'a' be the lower bound and 'b' the upper bound for a random number, then the
                                  following number will be used: (a + b) // 2

    :return: the generated output.
    """
    if brseq is None:
        raise ValueError('OS_SeqPlayer_Error: BRSEQ file is None')
    if isinstance(seq_name, int) and seq_name < 0:
        raise IndexError('OS_SeqPlayer_Error: Tried to play a track with a negative offset')

    global __CALL_DEPTH__
    global __GLOBAL_VARS__

    if __CALL_DEPTH__ >= SEQ_MAX_STACK_DEPTH:
        raise OverflowError('Reached maximum call stack depth in BRSEQ! Cannot make any further calls!')
    else:
        __CALL_DEPTH__ += 1

    # Each track may hold its own variables
    __TRACK_VARS__ = [SEQ_VAR_DEFAULT] * SEQ_MAX_VAR

    __PLAYED_NOTES__ = []
    __PRG_CALLS__ = []

    __TRANSPOSE__ = 0
    __CMP_FLAG__ = False

    snd_handle = __OS_CreateSeqHandle(brseq)  # get or create the SeqSound Handle
    track = snd_handle.rseq[seq_name]  # load the track

    def create_pseudo_rand_int(a: int, b: int) -> int:
        if disable_random_values:
            if a >= b:
                raise ValueError('OS_SeqPlayer_Error: FATAL ERROR FOR create_pseudo_rand_int')

            if b == 1:
                return 1

            return (a + b) // 2

        return random.randint(a, b)

    def get_var(idx: int) -> int:
        if idx in SEQ_LOCAL_VAR_RANGE:
            return snd_handle.__LOCAL_VARS__[idx]
        elif idx in SEQ_GLOBAL_VAR_RANGE:
            return __GLOBAL_VARS__[idx - 16]
        elif idx in SEQ_TRACK_VAR_RANGE:
            return __TRACK_VARS__[idx - 32]
        else:
            raise IndexError(f'Invalid var no {idx} for sequence {seq_name}')

    def set_var(idx: int, val: int) -> None:
        if idx in SEQ_LOCAL_VAR_RANGE:
            snd_handle.__LOCAL_VARS__[idx] = val
        elif idx in SEQ_GLOBAL_VAR_RANGE:
            __GLOBAL_VARS__[idx - 16] = val
        elif idx in SEQ_TRACK_VAR_RANGE:
            __TRACK_VARS__[idx - 32] = val
        else:
            raise IndexError(f'Invalid var no {idx} for sequence {seq_name}')

    def compute_prefix_cmd(__c: Cmd) -> int | tuple:
        result = 0
        if isinstance(__c.cmd, tuple):
            for __pre in __c.cmd[1:]:
                match __pre:
                    case MML.RANDOM:
                        rand_args = __c.args[0]
                        result = create_pseudo_rand_int(rand_args[0], rand_args[1])
                    case MML.VARIABLE:
                        if type(cmd.get_cmd()) == MMLEX:
                            result = get_var(__c.args[1])
                        else:
                            result = get_var(__c.args[0])
        else:
            result = __c.args[0]

        return result

    played_note = (-1, -1)
    for cmd in track.cmd_set:
        if isinstance(cmd.cmd, tuple) and cmd.cmd[-1] == MML.IF and not __CMP_FLAG__:
            continue

        # We get a note, so we just "play" it
        if type(note := cmd.get_cmd()) == Note:
            if played_note[0] != -1:
                __PLAYED_NOTES__.append(played_note)

            played_note = (clamp(note.value + __TRANSPOSE__, 0, 127), cmd.args[0])
        elif type(mml := cmd.get_cmd()) == MML:
            match mml:
                case MML.PRG:
                    if cmd.args[0] >= SEQ_MAX_PRG:
                        raise ValueError(f'Too large program no {cmd.args[0]} for sequence {seq_name}')
                    __PRG_CALLS__.append(cmd.args[0])
                case MML.TRANSPOSE:
                    __TRANSPOSE__ = compute_prefix_cmd(cmd)
                case MML.JUMP | MML.CALL:
                    target = brseq[cmd.args[0]]
                    name = OS.is_not_none_then_orElse(target.label, target.label.name, target.start_offset)

                    prg_calls, played_notes = OS_SeqHandle_Play(brseq, name,
                                                                disable_random_values=disable_random_values)

                    __PRG_CALLS__.append(prg_calls)
                    __PLAYED_NOTES__.append(played_notes)
                case MML.FIN:
                    break
                case _:
                    continue
        else:
            match cmd.get_cmd():
                case MMLEX.SETVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], cmd.args[1])
                case MMLEX.ADDVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) + get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) + create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) + cmd.args[1])
                case MMLEX.SUBVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) - get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) - create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) - cmd.args[1])
                case MMLEX.MULVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) * get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) * create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) * cmd.args[1])
                case MMLEX.DIVVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) // get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) // create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) // cmd.args[1])
                case MMLEX.SHIFTVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        shift_by = get_var(cmd.args[1])
                        if shift_by < 0:
                            set_var(cmd.args[0], get_var(cmd.args[0]) >> shift_by)
                        else:
                            set_var(cmd.args[0], get_var(cmd.args[0]) << shift_by)
                    elif cmd.prefix1 == MML.RANDOM:
                        shift_by = create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])

                        if shift_by < 0:
                            set_var(cmd.args[0], get_var(cmd.args[0]) >> shift_by)
                        else:
                            set_var(cmd.args[0], get_var(cmd.args[0]) << shift_by)
                    else:
                        shift_by = cmd.args[1]

                        if shift_by < 0:
                            set_var(cmd.args[0], get_var(cmd.args[0]) >> shift_by)
                        else:
                            set_var(cmd.args[0], get_var(cmd.args[0]) << shift_by)
                case MMLEX.RANDVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        bound = get_var(cmd.args[1])
                        if bound < 0:
                            set_var(cmd.args[0], create_pseudo_rand_int(bound, 0))
                        else:
                            set_var(cmd.args[0], create_pseudo_rand_int(0, bound))
                        # set_var(cmd.args[0], bound)
                    elif cmd.prefix1 == MML.RANDOM:
                        bound = create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])

                        # set_var(cmd.args[0], bound)
                        if bound < 0:
                            set_var(cmd.args[0], create_pseudo_rand_int(bound, 0))
                        else:
                            set_var(cmd.args[0], create_pseudo_rand_int(0, bound))
                    else:
                        bound = cmd.args[1]

                        # set_var(cmd.args[0], bound)
                        if bound < 0:
                            set_var(cmd.args[0], create_pseudo_rand_int(bound, 0))
                        else:
                            set_var(cmd.args[0], create_pseudo_rand_int(0, bound))
                case MMLEX.ANDVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) & get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) & create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) & cmd.args[1])
                case MMLEX.ORVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) | get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) | create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) | cmd.args[1])
                case MMLEX.XORVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) ^ get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) ^ create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) ^ cmd.args[1])
                case MMLEX.NOTVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], ~get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], ~create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], ~cmd.args[1])
                case MMLEX.MODVAR:
                    if cmd.prefix1 == MML.VARIABLE:
                        set_var(cmd.args[0], get_var(cmd.args[0]) % get_var(cmd.args[1]))
                    elif cmd.prefix1 == MML.RANDOM:
                        set_var(cmd.args[0], get_var(cmd.args[0]) % create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1]))
                    else:
                        set_var(cmd.args[0], get_var(cmd.args[0]) % cmd.args[1])
                # cmp instructions
                case MMLEX.CMP_EQ:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) == get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) == create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) == cmd.args[1]
                case MMLEX.CMP_GE:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) >= get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) >= create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) >= cmd.args[1]
                case MMLEX.CMP_GT:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) > get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) > create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) > cmd.args[1]
                case MMLEX.CMP_LE:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) <= get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) <= create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) <= cmd.args[1]
                case MMLEX.CMP_LT:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) < get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) < create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) < cmd.args[1]
                case MMLEX.CMP_NE:
                    if cmd.prefix1 == MML.VARIABLE:
                        __CMP_FLAG__ = get_var(cmd.args[0]) != get_var(cmd.args[1])
                    elif cmd.prefix1 == MML.RANDOM:
                        __CMP_FLAG__ = get_var(cmd.args[0]) != create_pseudo_rand_int(cmd.args[1][0], cmd.args[1][1])
                    else:
                        __CMP_FLAG__ = get_var(cmd.args[0]) != cmd.args[1]

    if played_note[0] > -1:
        __PLAYED_NOTES__.append(played_note)

    __CALL_DEPTH__ -= 1
    return unpack_singleton_value(__PRG_CALLS__), unpack_singleton_value(__PLAYED_NOTES__)
