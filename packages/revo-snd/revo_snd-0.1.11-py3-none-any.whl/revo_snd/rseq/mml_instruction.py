from enum import IntEnum


class MML(IntEnum):
    # SPECIAL CONSTANTS
    NOTE_WAIT_OFF = -1
    NOTE_WAIT_ON = -2
    MONOPHONIC_OFF = -3
    MONOPHONIC_ON = -4
    DAMPER_OFF = -5
    DAMPER_ON = -6
    PORTA_OFF = -7
    PORTA_ON = -8
    TIE_OFF = -9
    TIE_ON = -10

    # INSTRUCTIONS
    WAIT = 0x80
    PRG = 0x81

    OPEN_TRACK = 0x88
    JUMP = 0x89
    CALL = 0x8a

    RANDOM = 0xa0
    VARIABLE = 0xa1
    IF = 0xa2
    TIME = 0xa3
    TIME_RANDOM = 0xa4
    TIME_VARIABLE = 0xa5

    # u8 parameter instructions
    TIMEBASE = 0xb0
    ENV_HOLD = 0xb1
    MONOPHONIC = 0xb2
    VELOCITY_RANGE = 0xb3
    BIQUAD_TYPE = 0xb4
    BIQUAD_VALUE = 0xb5
    PAN = 0xc0
    VOLUME = 0xc1
    MAIN_VOLUME = 0xc2
    TRANSPOSE = 0xc3
    PITCH_BEND = 0xc4
    BEND_RANGE = 0xc5
    PRIO = 0xc6
    NOTE_WAIT = 0xc7
    TIE = 0xc8
    PORTA = 0xc9
    MOD_DEPTH = 0xca
    MOD_SPEED = 0xcb
    MOD_TYPE = 0xcc
    MOD_RANGE = 0xcd
    PORTA_SW = 0xce
    PORTA_TIME = 0xcf
    ATTACK = 0xd0
    DECAY = 0xd1
    SUSTAIN = 0xd2
    RELEASE = 0xd3
    LOOP_START = 0xd4
    VOLUME2 = 0xd5
    PRINTVAR = 0xd6
    SURROUND_PAN = 0xd7
    LPF_CUTOFF = 0xd8
    FXSEND_A = 0xd9
    FXSEND_B = 0xda
    MAINSEND = 0xdb
    INIT_PAN = 0xdc
    MUTE = 0xdd
    FXSEND_C = 0xde
    DAMPER = 0xdf

    # S16 parameter instructions
    MOD_DELAY = 0xe0
    TEMPO = 0xe1
    SWEEP_PITCH = 0xe3

    # Extended instructions.
    EX_COMMAND = 0xf0

    # Other
    ENV_RESET = 0xfb
    LOOP_END = 0xfc
    RET = 0xfd
    ALLOC_TRACK = 0xfe
    FIN = 0xff

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self):
        return self.__str__()


class MMLEX(IntEnum):
    SETVAR = 0x80
    ADDVAR = 0x81
    SUBVAR = 0x82
    MULVAR = 0x83
    DIVVAR = 0x84
    SHIFTVAR = 0x85
    RANDVAR = 0x86
    ANDVAR = 0x87
    ORVAR = 0x88
    XORVAR = 0x89
    NOTVAR = 0x8a
    MODVAR = 0x8b

    CMP_EQ = 0x90
    CMP_GE = 0x91
    CMP_GT = 0x92
    CMP_LE = 0x93
    CMP_LT = 0x94
    CMP_NE = 0x95

    USERPROC = 0xe0

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self):
        return self.__str__()