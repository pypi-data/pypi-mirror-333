from enum import IntEnum, auto

NOTE_MASK = 0x80


class Note(IntEnum):
    # -1
    CNM1 = 0
    CSM1 = auto()
    DNM1 = auto()
    DSM1 = auto()
    ENM1 = auto()
    FNM1 = auto()
    FSM1 = auto()
    GNM1 = auto()
    GSM1 = auto()
    ANM1 = auto()
    ASM1 = auto()
    BNM1 = auto()

    # 0
    CN0 = auto()
    CS0 = auto()
    DN0 = auto()
    DS0 = auto()
    EN0 = auto()
    FN0 = auto()
    FS0 = auto()
    GN0 = auto()
    GS0 = auto()
    AN0 = auto()
    AS0 = auto()
    BN0 = auto()

    # 1
    CN1 = auto()
    CS1 = auto()
    DN1 = auto()
    DS1 = auto()
    EN1 = auto()
    FN1 = auto()
    FS1 = auto()
    GN1 = auto()
    GS1 = auto()
    AN1 = auto()
    AS1 = auto()
    BN1 = auto()

    # 2
    CN2 = auto()
    CS2 = auto()
    DN2 = auto()
    DS2 = auto()
    EN2 = auto()
    FN2 = auto()
    FS2 = auto()
    GN2 = auto()
    GS2 = auto()
    AN2 = auto()
    AS2 = auto()
    BN2 = auto()

    # 3
    CN3 = auto()
    CS3 = auto()
    DN3 = auto()
    DS3 = auto()
    EN3 = auto()
    FN3 = auto()
    FS3 = auto()
    GN3 = auto()
    GS3 = auto()
    AN3 = auto()
    AS3 = auto()
    BN3 = auto()

    # 4
    CN4 = auto()
    CS4 = auto()
    DN4 = auto()
    DS4 = auto()
    EN4 = auto()
    FN4 = auto()
    FS4 = auto()
    GN4 = auto()
    GS4 = auto()
    AN4 = auto()
    AS4 = auto()
    BN4 = auto()

    # 5
    CN5 = auto()
    CS5 = auto()
    DN5 = auto()
    DS5 = auto()
    EN5 = auto()
    FN5 = auto()
    FS5 = auto()
    GN5 = auto()
    GS5 = auto()
    AN5 = auto()
    AS5 = auto()
    BN5 = auto()

    # 6
    CN6 = auto()
    CS6 = auto()
    DN6 = auto()
    DS6 = auto()
    EN6 = auto()
    FN6 = auto()
    FS6 = auto()
    GN6 = auto()
    GS6 = auto()
    AN6 = auto()
    AS6 = auto()
    BN6 = auto()

    # 7
    CN7 = auto()
    CS7 = auto()
    DN7 = auto()
    DS7 = auto()
    EN7 = auto()
    FN7 = auto()
    FS7 = auto()
    GN7 = auto()
    GS7 = auto()
    AN7 = auto()
    AS7 = auto()
    BN7 = auto()

    # 8
    CN8 = auto()
    CS8 = auto()
    DN8 = auto()
    DS8 = auto()
    EN8 = auto()
    FN8 = auto()
    FS8 = auto()
    GN8 = auto()
    GS8 = auto()
    AN8 = auto()
    AS8 = auto()
    BN8 = auto()

    # 9
    CN9 = auto()
    CS9 = auto()
    DN9 = auto()
    DS9 = auto()
    EN9 = auto()
    FN9 = auto()
    FS9 = auto()
    GN9 = auto()

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return self.__str__()
