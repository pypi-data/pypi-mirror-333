# Attempts no. 300.064 on building a BRSEQ parser
# which fits our purpose

# The ONLY thing this parser does not do, what others to
# is showing you exactly WHERE a jump/opentrack/call goes
# when the offset is inside a sequence (so not the start offset),
# i.e.
#
# dummy:
#   prg 25
#   cn5 100, 2  <--- jump back here
#   wait 12
#   gn5 80, 2
#   wait 12
#   jump 0x13
#   fin
#
# The pretty print will not tell you, that it goes to exactly
# that position. The pretty print is NOT meant for exactly dumping it,
# just a rough preview. This might be changed in the future.

import dataclasses
import enum
import struct
from collections.abc import Iterable
from typing import BinaryIO, Any

from revo_snd.rseq.mml_instruction import MML, MMLEX
from revo_snd.rseq.note import Note, NOTE_MASK


class Cmd:
    def __init__(self, cmd: (MML | MMLEX | Note | list[...]), args: list) -> None:
        self.cmd = cmd
        self.args = args

        self.prefix1 = None
        self.prefix2 = None
        self.if_flag = False

        if isinstance(cmd, tuple):
            if len(cmd) == 4:
                self.prefix1, self.prefix2, self.if_flag = cmd[1], cmd[2], True
            elif len(cmd) == 3:
                self.prefix1, self.prefix2 = cmd[1], cmd[2]
            elif len(cmd) == 2:
                self.prefix1 = cmd[1]

    def get_cmd(self) -> (MML | MMLEX | Note):
        return self.cmd[0] if isinstance(self.cmd, tuple) else self.cmd

    def has_prefix_cmd(self) -> bool:
        return self.if_flag or self.prefix1 is not None or self.prefix2 is not None

    def __str__(self) -> str:
        return f'RSEQCmd<{self.cmd} {self.args}>'

    def __repr__(self) -> str:
        return self.__str__()


@dataclasses.dataclass
class Sequence:
    label: Any
    cmd_set: list[Cmd]
    end_offset: int
    calling: list
    # start_offset: int <----- getting monkey patched in during parsing

    def __hash__(self) -> int:
        return hash((
            self.label,
            tuple(self.cmd_set),
            self.end_offset,
            tuple(self.calling)
        ))

    def get_specific_cmd(self, opcode: (MML | MMLEX | Note)) -> list[Cmd]:
        return [cmd for cmd in self.cmd_set if cmd.cmd == opcode]

    def pretty_string(self) -> str:
        lines = []

        label_name = f'__anonymous_0x{self.start_offset:X}' if self.label is None else self.label.name
        lines.append(f"{label_name}:")

        for cmd in self.cmd_set:
            args = cmd.args
            cmd_name = ""

            if isinstance(cmd.cmd, Iterable):
                __l = []
                for __c in cmd.cmd:
                    match __c:
                        case MML.IF:
                            __l.append("_if")
                        case MML.RANDOM:
                            __l.append("_r")
                        case MML.VARIABLE:
                            __l.append("_v")
                        case MML.TIME:
                            __l.append("_t")
                        case MML.TIME_RANDOM:
                            __l.append("_tr")
                        case MML.TIME_VARIABLE:
                            __l.append("_tv")
                        case _:
                            __l.append(str(__c))
                cmd_name = "".join(__l)
            else:
                cmd_name = str(cmd.get_cmd())

            match cmd.get_cmd():
                case MML.ALLOC_TRACK:
                    val = args[0] if args else 0
                    bit_str = format(val, "016b")
                    line = f"    {MML.ALLOC_TRACK} {bit_str}"
                case MML.JUMP | MML.CALL:
                    line = f"    {cmd_name} 0x{args[0]:X}"
                case MML.OPEN_TRACK:
                    line = f"    {cmd_name} {args[0]}, 0x{args[1]:X}"
                case MML.MONOPHONIC:
                    is_off = "off" if args[0] == 0 else "on"
                    line = f"    {MML.MONOPHONIC}_{is_off}"
                case MML.NOTE_WAIT:
                    is_off = "off" if args[0] == 0 else "on"
                    line = f"    {MML.NOTE_WAIT}_{is_off}"
                case MML.DAMPER:
                    is_off = "off" if args[0] == 0 else "on"
                    line = f"    {MML.DAMPER}_{is_off}"
                case MML.TIE:
                    is_off = "off" if args[0] == 0 else "on"
                    line = f"    {MML.TIME}_{is_off}"
                case MML.PORTA:
                    is_off = "off" if args[0] == 0 else "on"
                    line = f"    {MML.PORTA}_{is_off}"
                case _:
                    if args:
                        # Format like: "open_track, 1, 1152"
                        line = f"    {cmd_name} {', '.join(map(str, args))}"
                    else:
                        # No args case, just the command name
                        line = f"    {cmd_name}"

            lines.append(line)

        # Join all lines with newlines
        return "\n".join(lines)


class SeqArgType(enum.Enum):
    NONE = 0
    U8 = 1
    S16 = 2
    VAR_LEN = 3
    RANDOM = 4
    VARIABLE = 5


_R_APPLICABLE = [MML.WAIT, MML.PRG, MML.TEMPO, MML.VOLUME, MML.VOLUME2, MML.MAIN_VOLUME, MML.PITCH_BEND, MML.PAN,
                 MML.TRANSPOSE, MML.PORTA_TIME, MML.SWEEP_PITCH, MML.MOD_DEPTH, MML.MOD_SPEED, MML.ATTACK,
                 MML.DECAY, MML.SUSTAIN, MML.RELEASE, MML.MOD_DELAY, MML.LOOP_START, MML.MUTE,
                 *[e for e in MMLEX]]

_V_APPLICABLE = [MML.WAIT, MML.PRG, MML.TEMPO, MML.VOLUME, MML.VOLUME2, MML.MAIN_VOLUME, MML.PITCH_BEND, MML.PAN,
                 MML.TRANSPOSE, MML.PORTA_TIME, MML.SWEEP_PITCH, MML.MOD_DEPTH, MML.MOD_SPEED,
                 MML.ATTACK, MML.DECAY, MML.SUSTAIN, MML.RELEASE, MML.MOD_DELAY, MML.LOOP_START, MML.MUTE,
                 *[e for e in MMLEX]]


def _is_r_applicable(cmd: (MML | MMLEX)) -> bool:
    return cmd in _R_APPLICABLE


def _is_v_applicable(cmd: (MML | MMLEX)) -> bool:
    return cmd in _V_APPLICABLE


def _is_prefix_applicable(cmd: (MML | MMLEX)) -> bool:
    return _is_v_applicable(cmd) or _is_r_applicable(cmd)


class MML_Parser:
    def __init__(self, data: BinaryIO, labels: list[...], data_base_offset: int) -> None:
        self._data = data
        self._labels = labels
        self._data_off = data_base_offset

        # self._offsets = [__l.data_off for __l in self._labels]
        # self._tbl: dict[(str | int), ...] = {}

    def _read_byte(self) -> int:
        return struct.unpack('>B', self._data.read(1))[0]

    def _read_sbyte(self) -> int:
        return struct.unpack('>b', self._data.read(1))[0]

    def _read_short(self) -> int:
        return struct.unpack('>H', self._data.read(2))[0]

    def _read_sshort(self) -> int:
        return struct.unpack('>h', self._data.read(2))[0]

    def _read24(self) -> int:
        ret = self._read_byte()
        ret <<= 8
        ret |= self._read_byte()
        ret <<= 8
        ret |= self._read_byte()
        return ret

    def _read_var_length(self, limit=-1) -> int:
        tmp = self._read_byte()
        val = tmp & 0x7F
        __read = 1
        while (tmp & 0x80) and (limit == -1 or __read < limit):
            val <<= 7
            tmp = self._read_byte()
            __read += 1
            val |= tmp & 0x7F
        return val

    def _read_arg(self, arg_type: SeqArgType):
        val = 0

        match arg_type:
            case SeqArgType.U8:
                val = self._read_byte()
            case SeqArgType.S16:
                val = self._read_sshort()
            case SeqArgType.VAR_LEN:
                val = self._read_var_length()
            case SeqArgType.RANDOM:
                val = (self._read_sshort(), self._read_sshort())
            case SeqArgType.VARIABLE:
                val = self._read_byte()

        return val

    def _get_named_label(self, offset: int) -> ...:
        for __l in self._labels:
            if (__l.data_off + self._data_off) == offset:
                return __l
        return None

    def _is_named_label(self, offset: int) -> bool:
        return self._get_named_label(offset) is not None

    def _get_next_bigger_named_label(self, offset: int):
        for label in self._labels:
            if (label.data_off + self._data_off) > offset:
                return label
        return None

    def _get_previous_named_label(self, offset: int):
        prev_label = None
        for label in self._labels:
            label_offset = label.data_off + self._data_off
            if label_offset < offset:
                prev_label = label
            else:
                break
        return prev_label

    #################################################################
    # --------------------  DECODING FUNCTIONS -------------------- #
    #################################################################
    def parse(self) -> dict[(str | int), Sequence]:
        parsing_table = {}     # label_name    : (label, cmd_seq)
        anonymous_labels = {}  # target_offset : caller

        already_computed = {}

        def named_label_or_default(__o: int) -> ...:
            __r = self._get_named_label(__o)
            return __r if __r is not None else __o

        for __l in self._labels:
            # if __l.data_off in self._tbl:
            #    continue

            if __l.data_off in already_computed:
                __seq = already_computed[__l.data_off]
                __cpy = Sequence(label=__l, end_offset=__seq.end_offset, cmd_set=__seq.cmd_set, calling=__seq.calling)
                __cpy.start_offset = __seq.start_offset
                parsing_table[__l.name] = __cpy
                continue

            self._data.seek(self._data_off + __l.data_off)
            cmd_seq = []
            calling = []

            while True:
                cmd = self.decode_cmd()
                cmd_seq.append(cmd)

                if cmd.get_cmd() == MML.JUMP or cmd.get_cmd() == MML.CALL:
                    off = cmd.args[0]
                    if off != __l.data_off:
                        calling.append(named_label_or_default(off))
                        if not self._is_named_label(off):
                            anonymous_labels[off] = __l

                if cmd.get_cmd() == MML.OPEN_TRACK:
                    off = cmd.args[1]
                    if off != __l.data_off:
                        calling.append(named_label_or_default(off))
                        if not self._is_named_label(off):
                            anonymous_labels[off] = __l

                if cmd.get_cmd() == MML.FIN or self._is_named_label(self._data.tell()):
                    break
            __seq = Sequence(__l, cmd_seq, self._data.tell() - 1, calling)
            __seq.start_offset = __l.data_off
            parsing_table[__l.name] = __seq
            already_computed[__l.data_off] = __seq

        for off, caller in anonymous_labels.items():
            # print('Currently parsing anonymous sequence at relative offset',
            #      hex(off), 'absolute offset =', hex(off + self._data_off), 'called by', caller.name)
            # print('Next named label would be', self._get_next_bigger_named_label(off + self._data_off))

            # There can't be an anonymous label which is also a named label
            if off in already_computed:
                continue

            seq_off = self._data_off + off
            caller = parsing_table[caller.name]

            # There is the possibility, that a jump or call offset is
            # just going BACKWARDS inside a given sequence, i.e.
            # dummy:
            #   prg 25
            #   cn5 100, 2  <--- jump back here
            #   wait 12
            #   gn5 80, 2
            #   wait 12
            #   jump 0x13
            #   fin
            # In this case, we just skip parsing it altogether because
            # we already parsed it in the named label itself.
            if seq_off < caller.end_offset:
                continue

            cmd_seq = []
            calling = []

            self._data.seek(seq_off)
            while not self._is_named_label(self._data.tell()):
                cmd = self.decode_cmd()
                cmd_seq.append(cmd)

                if cmd.get_cmd() == MML.JUMP or cmd.get_cmd() == MML.CALL:
                    __o = cmd.args[0]
                    if off != __o:
                        calling.append(named_label_or_default(__o))

                if cmd.get_cmd() == MML.OPEN_TRACK:
                    __o = cmd.args[1]
                    if off != __o:
                        calling.append(named_label_or_default(__o))

                if cmd.get_cmd() == MML.FIN:
                    break

            __seq = Sequence(None, cmd_seq, self._data.tell() - 1, calling)
            __seq.start_offset = off
            parsing_table[off] = __seq
            already_computed[off] = __seq

        return parsing_table

    if_flag = False  # Python doing me dirty at this point
    use_arg_type = False

    arg_type1 = SeqArgType.NONE
    arg_type2 = SeqArgType.NONE
    prefix = None
    prefix2 = None

    def decode_cmd(self) -> Cmd:
        self.if_flag = False

        self.arg_type1 = SeqArgType.NONE
        self.arg_type2 = SeqArgType.NONE

        self.use_arg_type = False

        self.prefix = None
        self.prefix2 = None
        b = self._read_byte()

        # Process prefix
        if b == MML.IF:
            b = self._read_byte()
            self.if_flag = True

        if b == MML.TIME:
            self.prefix2 = MML.TIME
            b = self._read_byte()
            self.arg_type2 = SeqArgType.S16
        elif b == MML.TIME_RANDOM:
            self.prefix2 = MML.TIME_RANDOM
            b = self._read_byte()
            self.arg_type2 = SeqArgType.RANDOM
        elif b == MML.TIME_VARIABLE:
            self.prefix2 = MML.TIME_VARIABLE
            b = self._read_byte()
            self.arg_type2 = SeqArgType.VARIABLE

        if b == MML.RANDOM:
            self.prefix = MML.RANDOM
            b = self._read_byte()
            self.arg_type1 = SeqArgType.RANDOM
            self.use_arg_type = True
        elif b == MML.VARIABLE:
            self.prefix = MML.VARIABLE
            b = self._read_byte()
            self.arg_type1 = SeqArgType.VARIABLE
            self.use_arg_type = True

        def wrap_if(__cmd: (MML | MMLEX | Note)) -> ...:
            if self.if_flag:
                return __cmd, MML.IF

            return __cmd

        def compute_prefix(__cmd: MML | MMLEX | Note) -> Cmd:
            args = []
            prefixes = []

            if self.arg_type1 != SeqArgType.NONE:
                args.append(self._read_arg(self.arg_type1))
                prefixes.append(self.prefix)

            if self.arg_type2 != SeqArgType.NONE:
                args.append(self._read_arg(self.arg_type2))
                prefixes.append(self.prefix2)

            return Cmd((__cmd, *prefixes, MML.IF), args) if self.if_flag else Cmd((__cmd, *prefixes), args)

        # process notes
        if (b & NOTE_MASK) == 0:
            velocity = self._read_byte()
            if self.use_arg_type:
                return compute_prefix(Note(b))

            length = self._read_var_length()
            if self.arg_type2 != SeqArgType.NONE:
                cmd = compute_prefix(Note(b))
                cmd.args.insert(0, length)
                return cmd

            return Cmd(wrap_if(Note(b)), [velocity, length])

        match b:
            case MML.PRG | MML.WAIT:
                if self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                    return compute_prefix(MML(b))

                arg = self._read_var_length()
                if self.arg_type2 != SeqArgType.NONE:
                    cmd = compute_prefix(MML(b))
                    cmd.args.insert(0, arg)
                    return cmd
                return Cmd(wrap_if(MML(b)), [arg])
            case MML.FIN | MML.RET | MML.LOOP_END:
                return Cmd(MML(b), [])
            case MML.OPEN_TRACK:
                arg1 = self._read_byte()
                arg2 = self._read24()

                return Cmd(MML.OPEN_TRACK, [arg1, arg2])
            case MML.JUMP | MML.CALL:
                arg24 = self._read24()
                return Cmd(wrap_if(MML(b)), [arg24])
            case MML.MOD_DELAY | MML.TEMPO | MML.ALLOC_TRACK:
                if _is_prefix_applicable(MML(b)) and self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                    return compute_prefix(MML(b))

                arg16 = self._read_short()
                if _is_prefix_applicable(MML(b)) and self.arg_type2 != SeqArgType.NONE:
                    cmd = compute_prefix(MML(b))
                    cmd.args.insert(0, arg16)
                    return cmd

                return Cmd(wrap_if(MML(b)), [arg16])
            case MML.SWEEP_PITCH:
                if self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                    return compute_prefix(MML(b))

                arg16 = self._read_sshort()
                if self.arg_type2 != SeqArgType.NONE:
                    cmd = compute_prefix(MML.SWEEP_PITCH)
                    cmd.args.insert(0, arg16)
                    return cmd

                return Cmd(wrap_if(MML.SWEEP_PITCH), [arg16])
            case MML.ENV_HOLD | MML.TRANSPOSE | MML.PITCH_BEND | MML.ATTACK | MML.DECAY | MML.SUSTAIN | MML.RELEASE:
                if _is_prefix_applicable(MML(b)) and self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                    return compute_prefix(MML(b))

                arg = self._read_sbyte()
                if _is_prefix_applicable(MML(b)) and self.arg_type2 != SeqArgType.NONE:
                    cmd = compute_prefix(MML(b))
                    cmd.args.insert(0, arg)
                    return cmd

                return Cmd(wrap_if(MML(b)), [arg])
            case _:
                if b == MML.EX_COMMAND:
                    ex_cmd = self._read_byte()

                    match ex_cmd:
                        case MMLEX.USERPROC:
                            if self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                                return compute_prefix(MMLEX.USERPROC)

                            arg16 = self._read_short()
                            if self.use_arg_type:
                                cmd = compute_prefix(MMLEX.USERPROC)
                                cmd.args.insert(0, arg16)
                                return cmd

                            return Cmd(wrap_if(MMLEX.USERPROC), [arg16])
                        case _:
                            arg = self._read_byte()
                            if self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                                cmd_set = compute_prefix(MMLEX(ex_cmd))
                                cmd_set.args.insert(0, arg)

                                return cmd_set

                            arg16 = self._read_sshort()
                            if self.arg_type2 != SeqArgType.NONE:
                                cmd = compute_prefix(MMLEX(ex_cmd))
                                cmd.args.insert(0, arg16)
                                cmd.args.insert(0, arg)
                                return cmd

                            return Cmd(wrap_if(MMLEX(ex_cmd)), [arg, arg16])
                else:
                    if _is_prefix_applicable(MML(b)) and self.use_arg_type and self.arg_type1 != SeqArgType.NONE:
                        return compute_prefix(MML(b))

                    arg = self._read_byte()
                    if _is_prefix_applicable(MML(b)) and self.arg_type2 != SeqArgType.NONE:
                        cmd = compute_prefix(MML(b))
                        cmd.args.insert(0, arg)
                        return cmd

                    return Cmd(wrap_if(MML(b)), [arg])
