# for fuck's sake please work

"""
Support for Binary Revolution Sound Archive files (short BRSAR).
These files serve as structures holding all sound related data
for Nintendo Wii games, such as SFX or exact location of music tracks,
loop points for tracks, MIDI data and so on.

BRSAR files have five different versions, each version differing
from each other, sometimes functionality-wise. The respective versions
being: 1.1, 1.2, 1.3, 1.4.

1.1 : Introduces the concept of having each sound reference link to some common info,
      and then have that common info link to more detailed information for each sound type
1.2 : Introduces the use of Pan Mode and Pan Curve. Before that, the default Pan Mode is Balance,
      and the Pan Curve is Square Root
1.3 : (general information currently unknown)
1.4 : Converts the stream’s allocated channel bitflag into a simple channel count, as the bitflag was
      converted to a count, as channels are sequential

See SUPPORTED_VERSIONS for the currently supported versions of this
implementation.
"""
import io
from datetime import datetime
from pathlib import Path

from revo_snd.engine.OS_Sound import OS_PlaySeq2
from revo_snd.nw4r import *
from revo_snd.rbnk.brbnk import BRBNK
from revo_snd.rsar.file import File
from revo_snd.rsar.info import (
    Info,
    _SoundType,
    GroupDataEntry,
    _GroupTableEntry,
    _FileEntry,
    _FilePositionEntry, )
from revo_snd.rsar.symbol import Symbol
from revo_snd.rseq.brseq import BRSEQ
from revo_snd.rstm.brstm import BRSTM
from revo_snd.rwar.brwar import BRWAR
from revo_snd.rwav.brwav import BRWAV
from revo_snd.rwsd.brwsd import BRWSD


class RSARError(Exception):
    pass


class _Version:
    VERSION_1_1 = 0x0101
    VERSION_1_2 = 0x0102
    VERSION_1_3 = 0x0103
    VERSION_1_4 = 0x0104


RsarGroup = GroupDataEntry
ArcInfo = namedtuple('ArcInfo', ['n_seq_snd', 'n_seq_track', 'n_strm_snd', 'n_strm_track',
                                 'n_strm_chn', 'n_wav_snd', 'n_wav_track'])

# Supported versions the implementation is able to reliable read and process
# In general, a supported version is not only fully supported implementation-wise
# but also thoroughly tested and verified to function.
SUPPORTED_VERSIONS = {_Version.VERSION_1_4}


@dataclasses.dataclass
class DetailedSoundInfo:
    brwav: (BRWAV | list[BRWAV] | None)
    brseq: (BRSEQ | None)
    brbnk: (BRBNK | None)


class BRSAR(RevFile):

    def __init__(self, data: BinaryIO, brstm_file_path: str) -> None:
        self.n_seq = 0
        self.n_wav = 0
        self.n_strm = 0

        if data is not None:
            if os.path.isdir(brstm_file_path):
                if isinstance(brstm_file_path, str):
                    self.brstm_file_path = brstm_file_path
                else:
                    raise RSARError(('Invalid path specified for the BRSTM files of the BRSAR!'
                                     'Provide an absolute path to the BRSTM data of the BRSAR.'))
            else:
                self.brstm_file_path = None

            self._load_from_data(data)

    def _load_from_data(self, data: BinaryIO) -> None:
        self._data = data
        self.base_offset = data.tell()
        self.file_info = read_nw4r_file_header(data)

        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version, FileTag.BRSAR,
                          SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        (self._symbol_off, self._symbol_size, self._info_off, self._info_size,
         self._file_off, self._file_size) = struct.unpack('>IIIIII', data.read(24))

        data.seek(self._symbol_off)
        symbol = Symbol.from_data(data)
        self._symbol = symbol

        data.seek(self._file_off)
        self._file = File(data)

        data.seek(self._info_off)
        self._info = Info.from_data(data, self._file)
        self.arc_info = ArcInfo(*self._info.snd_arc_common_info)

        # for optimization purposes
        self._bnk_map = {}  # cache for BRBNK files
        self._seq_map = {}  # cache for BRSEQ files
        self._war_map = {}  # cache for BRWAR files

        self._snd_map = {}  # cache for any kind of sound

        for snd in self._info.snd_data:
            name = self._symbol.names[snd.file_name_idx]
            self.get_detailed_sound(name)

    ##########################
    # BRSAR HELPER FUNCTIONS #
    ##########################
    def __get_file_by_id(self, file_id: int) -> tuple[str, _FileEntry] | _FilePositionEntry:
        """
        Returns the file with the given id registered in the BRSAR file
        table. If the file is an external file, a path relative to the
        BRSAR's origin is returned, together with the entry for the file.
        Otherwise, only the FilePositionEntry itself is returned.

        :param file_id: the ID of the file.
        """

        entry = self._info.file_data[file_id]
        if entry.ext_file_pth != '<None>':
            return entry.ext_file_pth, entry

        return entry.file_tbl[0]

    def __get_group_by_id(self, file_id: int) -> tuple[GroupDataEntry, _GroupTableEntry]:
        """
        Returns the entry and its parent group of an object with the given file id.
        Raises a StopIteration exception if the object could not be found.
        """
        return next(((grp, entry) for grp in self._info.grp_data for entry in grp.grp_tbl if entry.grp_idx == file_id))

    def __get_group_by_name(self, name: str) -> RsarGroup:
        str_idx = self._symbol.names.index(name)

        for grp in self._info.grp_data:
            if grp.file_name_idx == str_idx:
                return grp

        raise ValueError(f'Could not find group {name}')

    def __get_seq(self, file_id: int) -> BRSEQ:
        """
        Gets and returns the BRSEQ with the given file_id.
        """
        if file_id in self._seq_map:
            return self._seq_map[file_id]

        brseq = self.__get_file_by_id(file_id)

        parent_grp = self._info.grp_data[brseq.grp_idx]
        grp_entry = parent_grp.grp_tbl[brseq.idx]

        offset_to_brseq = parent_grp.grp_file_off + grp_entry.file_data_off
        if offset_to_brseq in self._file:
            return self._file[offset_to_brseq]

        self._data.seek(parent_grp.grp_file_off + grp_entry.file_data_off)
        brseq = BRSEQ(self._data)

        self._seq_map[file_id] = brseq
        return brseq

    def __get_bank(self, bank_idx: int) -> BRBNK:
        """
        Gets and returns the BRBNK at the given idx of the INFO bank table.
        """
        if bank_idx in self._bnk_map:
            return self._bnk_map[bank_idx]

        bnk_common_info = self._info.bnk_data[bank_idx]

        bnk_grp, bnk_entry = self.__get_group_by_id(bnk_common_info.file_idx)
        self._data.seek(bnk_grp.grp_file_off + bnk_entry.file_data_off)
        bnk = BRBNK(self._data)

        self._bnk_map[bank_idx] = bnk

        return bnk

    def __get_bnk_wavs(self, bnk_file_id: int) -> (BRWAR | None):
        if bnk_file_id in self._war_map:
            return self._war_map[bnk_file_id]

        bnk_info = self._info.bnk_data[bnk_file_id]
        bnk_grp, bnk_entry = self.__get_group_by_id(bnk_info.file_idx)

        self._data.seek(bnk_grp.grp_audio_off + bnk_entry.audio_data_off)
        brwar = BRWAR(self._data)

        self._war_map[bnk_file_id] = brwar
        return brwar

    def __get_files_of_group(self, group_name: str, file_type: FileTag) -> dict[str, int]:
        group: RsarGroup = self.__get_group_by_name(group_name)

        files = {}
        for file in set([group.file, group.audio_file] + group.files + group.audio_files):
            if self._file[file].file_type == file_type:
                files[f'B{file_type}_id_{file}'] = file

        return files

    ##########################
    # PUBLIC API             #
    ##########################

    def get_rsar_info(self) -> dict[str, (str | int)]:
        """
        :return: General information about this archive, stored as key-value
                 pairs. General information includes:

                 'version'       : version string
                 'size'          : file size
                 'n_snd'         : total number of sounds in this archive
                 'n_seq'         : number of sequence sounds
                 'n_wav'         : number of wave sounds
                 'n_strm'        : number of streamed sounds
                 'n_rseq'        : number of BRSEQ files
                 'n_rbnk'        : number of BRBNK files
                 'n_rwav'        : number of BRWAV files (those in BRWAR files included)
                 'n_wsd'         : number of BRWSD files
                 'n_rwar'        : number of BRWAR files
                 'n_player'      : number of players
                 'max_seq'       : Maximum number of sequence sounds able to be played simultaneously
                 'max_seq_trk'   : Maximum number of tracks being used by sequence sounds
                 'max_strm'      : Maximum number of streamed sounds able to be played simultaneously
                 'max_strm_chn'  : Maximum number of channels used by streamed sounds
                 'max_strm_trk'  : Maximum number of tracks used by streamed sounds
                 'max_wav'       : Maximum number of wave sounds able to be played simultaneously
        """
        return {
            'version': self.version,
            'size': self.size,
            'n_snd': self.n_seq + self.n_wav + self.n_strm,
            'n_seq': self.n_seq,
            'n_wav': self.n_wav,
            'n_strm': self.n_strm,
            'n_rseq': self._file.n_seq,
            'n_rbnk': self._file.n_bnk,
            'n_rwav': self._file.n_wav,
            'n_wsd': self._file.n_wsd,
            'n_rwar': self._file.n_rwar,
            'n_player': len(self._info.player_data),
            'max_seq': self.arc_info.n_seq_snd,
            'max_seq_trk': self.arc_info.n_seq_track,
            'max_strm': self.arc_info.n_strm_snd,
            'max_strm_chn': self.arc_info.n_strm_chn,
            'max_strm_trk': self.arc_info.n_strm_track,
            'max_wav': self.arc_info.n_wav_snd
        }

    def get_human_readable_info(self):
        return {
            'File Version': self.version,
            'File Size': self.size,
            'Total number of sounds': self.n_seq + self.n_wav + self.n_strm,
            'Total number of sequence sounds': self.n_seq,
            'Total number of wave sounds': self.n_wav,
            'Total number of stream sounds': self.n_strm,
            'Total number of BRSEQ files': self._file.n_seq,
            'Total number of BRNNK files': self._file.n_bnk,
            'Total number of BRWAV files': self._file.n_wav,
            'Total number of BRWSD files': self._file.n_wsd,
            'Total number of BRWAR files': self._file.n_rwar,
            'Total number of players': len(self._info.player_data),
            'Maximum simultaneous played sequences': self.arc_info.n_seq_snd,
            'Maximum number of tracks used per sequence': self.arc_info.n_seq_track,
            'Maximum simultaneous played streams': self.arc_info.n_strm_snd,
            'Maximum number of channels used per stream': self.arc_info.n_strm_chn,
            'Maximum number of tracks per stream': self.arc_info.n_strm_track,
            'Maximum simultaneous played waves': self.arc_info.n_wav_snd
        }

    def get_groups(self) -> dict[str, RsarGroup]:
        return {
            self._symbol.names[grp.file_name_idx] if grp.file_name_idx >= 0 else '<NULL>': grp
            for grp in self._info.grp_data
        }

    def get_brwars(self) -> dict[str, int]:
        brwar = {}
        for __id, f in self._file._file_data.items():
            if f.file_type == FileTag.BRWAR:
                brwar[f'BRWAR_id_{__id}'] = __id

        return brwar

    def get_brwar_wavs(self, file_id: int) -> dict[str, ...]:
        return {f'BRWAV_id_{idx}': wav for idx, wav in enumerate(self.get_file(file_id).wavs)}

    def get_players(self) -> dict[str, BRWAR]:
        return {
            self._symbol.names[player.file_name_idx]: player
            for player in self._info.player_data
        }

    def get_group_brwar(self, group_name: str) -> dict[str, int]:
        return self.__get_files_of_group(group_name, FileTag.BRWAR)

    def get_group_brbnk(self, group_name: str) -> dict[str, int]:
        return self.__get_files_of_group(group_name, FileTag.BRBNK)

    def get_group_brwsd(self, group_name: str) -> dict[str, int]:
        return self.__get_files_of_group(group_name, FileTag.BRWSD)

    def get_group_brseq(self, group_name: str) -> dict[str, int]:
        return self.__get_files_of_group(group_name, FileTag.BRSEQ)

    def get_group_strm_snd(self, group_name: str = None) -> dict[str, tuple] | dict:
        if group_name is None:
            sounds = {}

            for snd in self._info.snd_data:
                if snd.snd_type == _SoundType.STRM:
                    name = self._symbol.names[snd.file_name_idx]
                    sounds[name] = snd, self._snd_map[name]
            return sounds

        return {}

    def get_group_wav_snd(self, name: str) -> dict[str, dict[str, ...] | dict[str, int] | dict[str, int]]:
        sounds = {}
        brwsd = {}
        brwar = {}

        for snd in self._info.snd_data:
            if snd.snd_type == _SoundType.WAVE:
                file_info = self.__get_file_by_id(snd.file_idx)
                parent_grp = self._info.grp_data[file_info.grp_idx]
                grp_entry = parent_grp.grp_tbl[file_info.idx]

                if self._symbol.names[parent_grp.file_name_idx] == name:
                    sounds[self._symbol.names[snd.file_name_idx]] = snd

                    brwsd_file = self._file.offset_to_id(parent_grp.grp_file_off + grp_entry.file_data_off)
                    brwar_file = self._file.offset_to_id(parent_grp.grp_audio_off)

                    brwsd[f'BRWSD_id_{brwsd_file}'] = brwsd_file
                    brwar[f'BRWAR_id_{brwar_file}'] = brwar_file

        return {
            'sounds': sounds,
            'brwsd': brwsd,
            'brwar': brwar
        }

    def get_group_seq_snd(self, name: str) -> dict:
        sounds = {}
        brseq = {}
        brbnk = {}
        brwar = {}

        for snd in self._info.snd_data:
            if snd.snd_type == _SoundType.SEQ:
                file_info = self.__get_file_by_id(snd.file_idx)
                parent_grp = self._info.grp_data[file_info.grp_idx]
                grp_entry = parent_grp.grp_tbl[file_info.idx]

                if self._symbol.names[parent_grp.file_name_idx] == name:
                    sounds[self._symbol.names[snd.file_name_idx]] = snd

                    snd_info: DetailedSoundInfo = self.get_detailed_sound(self._symbol.names[snd.file_name_idx])

                    brseq_file = snd_info.brseq
                    brbnk_file = snd_info.brbnk

                    if brseq_file is not None:
                        file_id = self._file.offset_to_id(brbnk_file.base_offset)
                        brseq[f'BRSEQ_id_{file_id}'] = (file_id, snd_info.brwav)
                    else:
                        brseq['UNKNOWN_BRSEQ'] = None

                    file_id = self._file.offset_to_id(brbnk_file.base_offset)
                    brbnk[f'BRBNK_id_{file_id}'] = file_id

                    brwar_file = self._file.offset_to_id(parent_grp.grp_audio_off)
                    brwar[f'BRWAR_id_{brwar_file}'] = brwar_file

        return {
            'sounds': sounds,
            'brseq': brseq,
            'brbnk': brbnk,
            'brwar': brwar
        }

    def get_group_detailed_sounds(self, group_name: str) -> dict[str, ...]:
        sound = {}
        for snd in self._info.snd_data:
            snd_name = self._symbol.names[snd.file_name_idx]
            file_info = self.__get_file_by_id(snd.file_idx)

            if isinstance(file_info, tuple):  # external file
                continue

            parent_grp = self._info.grp_data[file_info.grp_idx]
            if self._symbol.names[parent_grp.file_name_idx] == group_name:
                sound[snd_name] = self.get_detailed_sound(snd_name)

        return sound

    def get_brbnk_inst_data(self, file_id: int) -> dict[str, ...]:
        brbnk: BRBNK = self._file[file_id]
        if brbnk.file_type != FileTag.BRBNK:
            raise RSARError('Cannot load instrument data for a non-BRBNK file')

        return {f'Instrument_id_{i}': brbnk.get_inst_param_direct(i, keep_structs=True) for i in range(len(brbnk._inst_data))}

    def get_brwsd_wsd_data(self, file_id: int) -> dict[str, ...]:
        brwsd: BRWSD = self._file[file_id]
        if brwsd.file_type != FileTag.BRWSD:
            raise RSARError('Cannot load WSD data for a non-BRWSD file')

        return {f'WSD_id_{i}': wsd for i, wsd in enumerate(brwsd._data_block.wsd)}

    def get_brseq_seq_data(self, file_id: int) -> dict[str, ...]:
        brseq: BRSEQ = self._file[file_id]
        if brseq.file_type != FileTag.BRSEQ:
            raise RSARError('Cannot load sequence data for a non-BRSEQ file')

        data = {}
        strings = []
        for label, cmd in brseq._seq_data.items():
            detailed_sound = self.get_detailed_sound(label)
            data[label] = (detailed_sound, cmd)

            # This sound exists
            if detailed_sound is not None and detailed_sound.brseq is not None:
                name, str_idx, info_idx = self._symbol._snd_trie.get_entry(label)
                if name is None and str_idx is None and info_idx is None:
                    continue

                common_info = self._info.snd_data[info_idx]
                player_id = common_info.player_idx

                strings.append('\n'.join([f';; Player id = {player_id}', cmd.pretty_string(), '']))
            else:
                strings.append('\n'.join([f';; Player id = NONE', cmd.pretty_string(), '']))

        return {'str': '\n'.join(strings), 'seq': data}

    def get_file(self, file_id: int) -> RevFile:
        return self._file[file_id]

    '''def add_file(self, file: RevFile) -> int:
        """
        Adds a new BRSAR compatible file and returns its unique id.
        If the file is not compatible, an Error is raised.

        :param file: The file to add.
        """
        return self._file.append(file)'''

    '''def create_wav_snd(self, name: str, group: RsarGroup, brwsd_id: int, player_id: int) -> None:
        if not (0 <= player_id < len(self._info.player_data)):
            raise IndexError(f'Player ID {player_id} out of bounds for BRSAR')

        str_idx = len(self._symbol.names)
        self._symbol._snd_trie.insert(name, str_idx, self._info.n_entry)

        sound_3d = Sound3DParam()
        sound_entry = SoundDataEntry(file_idx=str_idx, )'''

    def replace_wav_snd(self, name: str, brwav: BRWAV) -> None:
        """
        Replaces the WAV file associated with the given WAV sound. If the
        sound is not a WAV sound, this operation will fail.

        :param name:  The name of the sound.
        :param brwav: The new sound.
        """
        name, str_idx, info_idx = self._symbol._snd_trie.get_entry(name)
        if name is None and str_idx is None and info_idx is None:
            raise RSARError(f'Unable to find sound {name} in the BRSAR!')

        # There is a theme going on...
        # Get the common info of the sound
        common_info = self._info.snd_data[info_idx]
        snd_info = common_info.snd_info

        if common_info.snd_type != _SoundType.WAVE:
            raise TypeError('Can only replace a WAV sound with the "replace_wav_snd()" function!')

        file_info = self.__get_file_by_id(common_info.file_idx)

        parent_grp = self._info.grp_data[file_info.grp_idx]
        grp_entry = parent_grp.grp_tbl[file_info.idx]

        # We NEED the BRWAR so no point in calling
        # other API functions...
        brwsd = self._file[parent_grp.grp_file_off + grp_entry.file_data_off]
        brwar = self._file[parent_grp.grp_audio_off]

        wav = brwar[brwsd[snd_info.wave_idx][0].wave_idx]

        idx, _ = brwar.get_wav_by_offset(wav.base_offset)
        brwar.replace(idx, brwav)

        self._file._file_data[self._file.offset_to_id(brwar.base_offset)] = brwar

    def replace_seq_snd(self, name: str, brwav: BRWAV, *, wav_no: int = 0) -> None:
        """
        Replaces the WAV file used by the given sequence sound. Caution, a
        sequence file may have more than one WAV associated to it. The variant
        option sets, which WAV of the WAVs it uses should be replaced.

        :param name:    The name of the sequence sound.
        :param brwav:   The new WAV sound to insert.
        :param wav_no:  Which WAV to replace (only usable if there are multiple present).
        """
        name, str_idx, info_idx = self._symbol._snd_trie.get_entry(name)
        if name is None and str_idx is None and info_idx is None:
            raise RSARError(f'Sequence sound with the name {name} does not exist!')

        # Get the common info of the sound
        common_info = self._info.snd_data[info_idx]
        snd_info = common_info.snd_info

        brwar = self.__get_bnk_wavs(snd_info.bnk_idx)
        detailed_snd_info = self.get_detailed_sound(name)

        wavs = detailed_snd_info.brwav
        if not wavs:
            raise RSARError(f'No sample data attached to the sequence sound {name}')

        idx, _ = brwar.get_wav_by_offset(wavs[wav_no].base_offset)
        brwar.replace(idx, brwav)

        self._war_map[snd_info.bnk_idx] = brwar
        self._file._file_data[self._file.offset_to_id(brwar.base_offset)] = brwar

    def patch_brstm(self, name: str, new_brstm: BRSTM, *, new_path: str = None) -> None:
        """
        Patches the BRSAR with the given BRSTM. Automatically adjusts the number
        of channels and number of tracks needed to play the BRSTM according to
        the BRSTM itself.

        :param name:      The name of the sound to patch.
        :param new_brstm: The new BRSTM to patch in.
        :param new_path:  (Optional) Sets a new path to the BRSTM relative to the BRSAR.
                          It cannot be a parent directory of the BRSAR.
        """
        name, str_idx, info_idx = self._symbol._snd_trie.get_entry(name)
        if name is None and str_idx is None and info_idx is None:
            raise RSARError(f'Could not find BRSTM with name {name}')

        # Get the common info of the sound
        common_info = self._info.snd_data[info_idx]
        snd_info = common_info.snd_info

        if common_info.snd_type != _SoundType.STRM:
            raise RSARError(f'Tried to patch BRSTM, but a non-BRSTM sound was given')

        _, strm_file_info = self.__get_file_by_id(common_info.file_idx)

        if new_path is not None:
            strm_file_info.ext_file_pth = new_path

        strm_file_info.file_size = new_brstm.file_size
        snd_info.n_alloc_chn = new_brstm.n_channels
        snd_info.alloc_track_flag = (1 << new_brstm.n_tracks) - 1

    def get_sound(self, name) -> (BRWAV | list[BRWAV] | BRSTM | None):
        """
        Returns the sound data (either BRWAV or BRSTM) for the given
        sound, if it exists. Otherwise, returns None.

        :param name: The name of the sound to get the sound data for.
        """
        info = self.get_detailed_sound(name)
        if info is None:
            return None

        return info.brwav if isinstance(info, DetailedSoundInfo) else info

    def get_detailed_sound(self, name: str) -> (DetailedSoundInfo | BRWAV | BRSTM | None):
        """
        Gets the detailed sound info for the given sound, which differs
        according to the type of the sound:
            SEQ:
                returns the WAV/WAVs used by the sequence,
                        the BRSEQ file for the sequence,
                        the BRBNK file for the sequence
            STRM:
                returns either the BRSTM file or the relative path to it
                        if it was not found
            WAV:
                return the WAV for this sound
        If nothing was found, then None is returned.
        :param name: The name of the sound
        """
        name, str_idx, info_idx = self._symbol._snd_trie.get_entry(name)
        if name is None and str_idx is None and info_idx is None:
            return None

        if name in self._snd_map:
            return self._snd_map[name]

        # Get the common info of the sound
        common_info = self._info.snd_data[info_idx]
        snd_info = common_info.snd_info

        # Get the appropriate file according to the file
        match common_info.snd_type:
            case _SoundType.SEQ:
                brseq = self.__get_seq(common_info.file_idx)
                brbnk = self.__get_bank(snd_info.bnk_idx)

                try:
                    samples = OS_PlaySeq2(self._data, brseq, name, brbnk, self.__get_bnk_wavs(snd_info.bnk_idx))
                    seq_snd = DetailedSoundInfo(brwav=samples, brseq=brseq, brbnk=brbnk)

                    self._snd_map[name] = seq_snd

                    self.n_seq += 1
                    return seq_snd
                except IndexError:
                    # This means we could not find an appropriate BRSEQ
                    seq_snd = DetailedSoundInfo(brwav=None, brseq=None, brbnk=brbnk)
                    self._snd_map[name] = seq_snd
                    return seq_snd

            case _SoundType.STRM:
                # We only need the common info, the snd_info only contains
                # detailed data about how to play the STRM i.e. how many channels
                # are being used for this STRM.
                strm_file, _ = self.__get_file_by_id(common_info.file_idx)

                # Search in the given brstm path for the file
                os_file_name = os.path.join(self.brstm_file_path, Path(strm_file).name)
                if os.path.isfile(os_file_name):
                    brstm = BRSTM.from_file(os_file_name)
                else:
                    # Fail-safe, just to be sure:
                    # if we do not find the file, return the path
                    brstm = strm_file

                self._snd_map[name] = brstm
                self.n_strm += 1
                return brstm
            case _SoundType.WAVE:
                file_info = self.__get_file_by_id(common_info.file_idx)

                parent_grp = self._info.grp_data[file_info.grp_idx]
                grp_entry = parent_grp.grp_tbl[file_info.idx]

                brwsd = self._file[parent_grp.grp_file_off + grp_entry.file_data_off]
                brwar = self._file[parent_grp.grp_audio_off]

                self.n_wav += 1
                return brwar[brwsd[snd_info.wave_idx][0].wave_idx]
            case _:
                raise TypeError(f'Unknown sound type {snd_info.snd_type}')

    def __bytes__(self) -> bytes:
        buffer = io.BytesIO()
        buffer.write(struct.pack('>4sHHIHHIIIIII',
                                 b'RSAR', ByteOrder.BIG_ENDIAN, _Version.VERSION_1_4, 0, 0x40, 3,
                                 0, 0,  # DATA offset always at 0x40
                                 0, 0,
                                 0, 0))

        buffer.write(b'\x00' * 8)
        now = datetime.now()
        formatted_timestamp = now.strftime("%d_%m_%YT%H_%M_%S")

        buffer.write('Generated by    '.encode('ascii') + f'REVO_SND v{NW4R_LIB_VERSION} '.encode('ascii'))
        buffer.write(f'on date:        '.encode('ascii'))
        buffer.write(formatted_timestamp.split('T')[0].encode('ascii') + b'\x20' * 6)
        buffer.write(formatted_timestamp.split('T')[1].encode('ascii') + b'\x20' * 8)
        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))

        symbol_offset = buffer.tell()
        symbol = bytes(self._symbol)

        buffer.write(symbol)
        info_off, info_size, file_off, file_size = self._info.to_bytes(buffer)

        total_file_size = buffer.tell()

        buffer.seek(0x8)
        buffer.write(total_file_size.to_bytes(length=4, byteorder='big'))

        buffer.seek(0x10)
        buffer.write(struct.pack('>IIIIII', symbol_offset, len(symbol), info_off, info_size, file_off, file_size))

        return buffer.getvalue()

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        if isinstance(data, str):
            data = open(data, 'rb')

        if len(args) == 0:
            arg = ''
        else:
            arg = args[0]

        return cls(data, arg)
