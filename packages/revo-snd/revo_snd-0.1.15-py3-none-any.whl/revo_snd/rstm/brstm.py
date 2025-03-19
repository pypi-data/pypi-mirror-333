"""
BRSTM implementation for PyRSAR.

A BRSTM may be anything from one channel (mono audio) to multiple
channels (stereo sound). BRSTM files may only have up to 8 tracks
or 16 channels. This is a hard limit set by the Nintendo Ware
sound engine itself and not the file format as is. The BRSTM module
supports decoding and encoding from ADPCM encoded BRSTM files.
"""

# Try 2 in creating our own BRSTM module after
# failing for 4 days straight to get openrevolution
# to work as a Python C-Extension! So lets to it
# ourselves, shall we.
#
# Decoding/Encoding are already provided as is by the
# internal revo_snd_adpcm C-extension module, so the
# only part that needs to be done is writing the encoded
# data to a usable BRSTM file.
#
# Further references about the BRSTM file:
#    https://wiki.tockdom.com/wiki/BRSTM_(File_Format)
#    https://wiibrew.org/wiki/BRSTM_file
#
# May the force be with us.

import io
import enum
import struct
import wave
from itertools import repeat, batched
from pathlib import Path

import numpy as np

from revo_snd.nw4r import *
from revo_snd.adpcm.adpcm import (
    AdpcmParamSet,
    get_bytes_for_adpcm_samples,
    align_up
)

# We get help again from following C functions
# DSP_DecodeBlock, DSP_EncodeBlock
try:
    from revo_snd.revo_snd_adpcm import DSP_EncodeBlock, DSP_DecodeBlock
    REVO_SND_ADPCM_AVAILABLE = True
except ImportError:
    import revo_snd.adpcm.adpcm as a
    import revo_snd.adpcm.encode_adpcm as encoder

    DSP_DecodeBlock = a.decode_adpcm_block

    def throw_no_encoding():
        raise NW4RInternalError('Internal revo_snd_adpcm module was not found. Encoding BRSTM files is not available!')
    DSP_EncodeBlock = throw_no_encoding
    REVO_SND_ADPCM_AVAILABLE = False


class _Version:
    VERSION_1_0 = 0x0100


SUPPORTED_VERSIONS = {_Version.VERSION_1_0}
BRSTM_MAX_CHN_COUNT = 16
BRSTM_MAX_SAMPLE_RATE = 65535


class RSTMError(Exception):
    pass


class BrstmFormat(enum.IntEnum):
    PCM8 = 0
    PCM16 = 1
    ADPCM = 2

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class _TrkType(enum.IntEnum):
    SIMPLE = 0  # Apparently only used in Super Smash Bros Brawl
    EXTENDED = 1


class _StrmTrackInfo:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self.volume, self.pan, self.n_chn = struct.unpack('>BBI', data.read(6))
        self.chn_idx_tbl = list(struct.unpack('>' + str(self.n_chn) + 'B', data.read(self.n_chn)))


class _StrmDataInfo:
    def __init__(self, data: BinaryIO, *, n_samples: int = 0, n_chn: int = 0, sample_rate: int = 0) -> None:
        if data is not None:
            self._read_from_data(data)
        else:
            self.format = BrstmFormat.ADPCM
            self.is_looped = False
            self.n_chn = n_chn
            self.smp_rate = sample_rate

            self.loop_end = n_samples
            self.block_samples = 14336
            self.block_size = 8192

            self.n_blocks = n_samples // self.block_samples
            if n_samples % self.block_samples != 0:
                self.n_blocks += 1

            self.last_block_samples = n_samples % self.block_samples
            if self.last_block_samples == 0:
                self.last_block_samples = self.block_samples

            self.last_block_size = get_bytes_for_adpcm_samples(self.last_block_samples)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()
        (self.format, self.is_looped, self.n_chn, self.smp_rate24, self.smp_rate, self.block_header_off,
         self.loop_start, self.loop_end, self.data_off, self.n_blocks, self.block_size, self.block_samples,
         self.last_block_size, self.last_block_samples, self.last_block_padded_size, self.adpcm_data_interval,
         self.adpcm_data_size) = struct.unpack('>BBBBHHIIIIIIIIIII', data.read(52))

        self.is_looped = bool(self.is_looped)


class _AdpcEntry:
    def __init__(self, data: BinaryIO, *, yn1: int = 0, yn2: int = 0) -> None:
        if data is not None:
            self.yn1, self.yn2 = struct.unpack('>hh', data.read(4))
        else:
            self.yn1 = yn1
            self.yn2 = yn2


class _TrackInfo:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        self.n_chn, = struct.unpack('>B', data.read(1))
        self.chn_idx_tbl = struct.unpack(f'>{self.n_chn}B', data.read(self.n_chn))


class _TrackInfoEx:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        self.vol, self.pan, _, _, self.n_chn = struct.unpack('>BBHIB', data.read(9))
        self.chn_idx_tbl = struct.unpack(f'>{self.n_chn}B', data.read(self.n_chn))


class _TrackTable:
    def __init__(self, data: BinaryIO, head_offset: int = 0) -> None:
        if data is not None:
            self._read_from_data(data, head_offset)

    def _read_from_data(self, data: BinaryIO, head_offset: int) -> None:
        self._base_offset = data.tell()

        self.n_trk, self.trk_type, _ = struct.unpack('>BBH', data.read(4))
        refs = [read_nw4r_ref(data) for _ in range(self.n_trk)]

        self.trk = []
        for ref in refs:
            data.seek(get_offset_from_ref(ref, head_offset))

            if self.trk_type == _TrkType.SIMPLE:
                self.trk.append(_TrackInfo(data))
            elif self.trk_type == _TrkType.EXTENDED:
                self.trk.append(_TrackInfoEx(data))
            else:
                raise RSTMError(f'Unknown track type {self.trk_type} for BRSTM')


class _ChnTable:
    def __init__(self, data: BinaryIO, head_offset: int = 0) -> None:
        if data is not None:
            self._read_from_data(data, head_offset)

    def _read_from_data(self, data: BinaryIO, head_offset: int) -> None:
        self.n_chn, = struct.unpack('>B', data.read(1))
        data.read(3)

        refs = [read_nw4r_ref(data) for _ in range(self.n_chn)]

        self.adpcm_params = []

        for ref in refs:
            data.seek(get_offset_from_ref(ref, head_offset))
            data.seek(get_offset_from_ref(read_nw4r_ref(data), head_offset))  # Reference to AdpcmParamSet

            adpcm_params = AdpcmParamSet(data)
            self.adpcm_params.append(adpcm_params)


class _Head:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'HEAD')

        strm_info_ref = read_nw4r_ref(data)
        track_tbl_ref = read_nw4r_ref(data)
        chn_tbl_ref = read_nw4r_ref(data)

        data.seek(get_offset_from_ref(strm_info_ref, self._base_offset))
        self.strm_data_info = _StrmDataInfo(data)

        data.seek(get_offset_from_ref(track_tbl_ref, self._base_offset))
        self.trk_tbl = _TrackTable(data, self._base_offset)

        data.seek(get_offset_from_ref(chn_tbl_ref, self._base_offset))
        self.chn_tbl = _ChnTable(data, self._base_offset)


class _Data:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_header = read_nw4r_block_header(data)
        block_sanity_check(block_header.magic, 'DATA')

        self.size = block_header.block_size
        self.data_off, = struct.unpack('>I', data.read(4))


class BRSTM(RevFile):
    def __init__(self, data: BinaryIO) -> None:
        self._src_path = data.name
        if data is not None:
            self._read_from_file(data)

    def _read_from_file(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()
        self._data = data

        self.file_info = read_nw4r_file_header(data)
        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version, FileTag.BRSTM, SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        (self._head_off, self._head_size, self._adpcm_off, self._adpcm_size,
         self._data_off, self._data_size) = struct.unpack('>IIIIII', data.read(24))

        self._head_off = self._head_off + self._base_offset
        self._adpcm_off = self._adpcm_off + self._base_offset
        self._data_off = self._data_off + self._base_offset

        data.seek(self._head_off)
        self._head = _Head(data)
        self._strm_data_info = self._head.strm_data_info

        # We read the ADPC block and its
        # related data on the fly, so it
        # is not needed to be read here.

        data.seek(self._data_off)
        self._data_block = _Data(data)

        # Restore state to the expected offset of the reader
        data.seek(self._base_offset + self.file_info.file_size)

    def __get_adpc_entry(self, block: int, channel: int) -> _AdpcEntry:
        self._data.seek(self._adpcm_off + 0x08 + (block * self.n_channels + channel) * 4)
        return _AdpcEntry(self._data)

    def __get_block_data(self, block: int, channel: int) -> bytes:
        block_count = self._strm_data_info.n_blocks
        block_size = self._strm_data_info.block_size
        final_block_size = self._strm_data_info.last_block_size
        final_block_padded_size = self._strm_data_info.last_block_padded_size

        if channel != 0 and block + 1 == block_count:
            offset = (block * self.n_channels * block_size + channel * final_block_padded_size)
        else:
            offset = ((block * self.n_channels + channel) * block_size)

        if block + 1 == block_count:
            data_end = offset + final_block_size
        else:
            data_end = offset + block_size

        self._data.seek(self._data_off + 0x08 + self._data_block.data_off + offset)
        return self._data.read(data_end - offset)

    def __get_trk_pcm_samples(self, trk_id: int) -> bytes:
        if trk_id >= self.n_tracks or trk_id < 0:
            raise IndexError(f'Invalid track id {trk_id} for BRSTM! Only possible tracks {list(range(self.n_tracks))}')

        # If we have a mono BRSTM, just decode the whole block
        # At this point, this is not any more different than a
        # BRWAV file.
        if self.n_channels == 1:
            self._data.seek(self._data_off + 0x20)
            sample_data = self._data.read(self._data_block.size)

            adpcm_params = self._head.chn_tbl.adpcm_params[0]

            pcm_samples = DSP_DecodeBlock(sample_data, self.n_samples, 1,
                                          adpcm_params.adpcm_param.coefs, 0, 0)
            return pcm_samples

        trk_tbl = self._head.trk_tbl

        n_chn = trk_tbl.trk[trk_id].n_chn
        chn_idx = trk_tbl.trk[trk_id].chn_idx_tbl

        pcm_left = bytearray()
        pcm_right = bytearray()

        for c in range(n_chn):
            block_count = self._strm_data_info.n_blocks
            usual_block_samples = self._strm_data_info.block_samples
            final_block_samples = self._strm_data_info.last_block_samples

            adpcm_params = self._head.chn_tbl.adpcm_params[chn_idx[c]]

            for b in range(self._strm_data_info.n_blocks):
                adpc_entry = self.__get_adpc_entry(b, c)
                yn1 = adpc_entry.yn1
                yn2 = adpc_entry.yn2

                block_samples = final_block_samples if (b + 1 == block_count) else usual_block_samples

                block_data = self.__get_block_data(b, chn_idx[c])

                # Faster version of decode_adpcm_block (in adpcm.py),
                # this version is preferred.
                # The audio tends to be slightly corrupted, when a higher
                # stride is given. More importantly, it just generates the double/triple etc.
                # amount of sample data, which would mean, the sample_rate needs to be
                # doubled/tripled etc.
                # Leave the value at one for optimal speed and audio quality
                pcm_data = DSP_DecodeBlock(block_data, block_samples, 1,
                                           adpcm_params.adpcm_param.coefs, yn1, yn2)
                if c == 0:
                    pcm_left.extend(pcm_data)
                elif c == 1:
                    pcm_right.extend(pcm_data)
                else:
                    raise IndexError('Invalid channel ID')

        # Interleave both channels to create the original audio.
        # If we interleave from ADPCM back to PCM, we need to remember
        # that in a canonical Wave file, the data is always alternating:
        #   L0, R0, L1, R1, ...
        # where L(eft)/R(right) denotes the channel and the number
        # the sample.

        import numpy as np
        left_pcm = np.frombuffer(pcm_left, dtype=np.int16)
        right_pcm = np.frombuffer(pcm_right, dtype=np.int16)

        interleaved = np.column_stack((left_pcm, right_pcm)).ravel()
        packed_data = interleaved.tobytes()

        return packed_data

    @property
    def file_size(self) -> int:
        """
        :return: The file size of this BRSTM.
        """
        return self._file_size

    @property
    def codec(self) -> BrstmFormat:
        """
        :return: The encoding format of the samples.
        """
        return BrstmFormat(self._strm_data_info.format)

    @property
    def n_tracks(self) -> int:
        """
        :return: The number of tracks this brstm has.
        """
        n_chn = self.n_channels
        return self._strm_data_info.n_chn // 2 if n_chn > 1 else n_chn

    @property
    def n_channels(self) -> int:
        """
        :return: The number of channels this BRSTM uses.
        """
        return self._strm_data_info.n_chn

    @property
    def sample_rate(self) -> int:
        """
        :return: The sample rate (in Hz) this BRSTM uses.
        """
        return (self._strm_data_info.smp_rate24 << 16) | self._strm_data_info.smp_rate

    @property
    def is_looped(self) -> bool:
        """
        :return: Whether this BRSTM is looped or not.
        """
        return self._strm_data_info.is_looped

    @property
    def loop_start(self) -> int:
        """
        :return: The starting sample of the loop, if this BRSTM
                 is looped, otherwise always 0
        """
        return self._strm_data_info.loop_start

    # n_sample and loop_end are the same value, but for better
    # naming conventions, they are "separated"
    @property
    def n_samples(self) -> int:
        """
        :return: The number of samples in this BRSTM.
        """
        return self._strm_data_info.loop_end

    @property
    def loop_end(self) -> int:
        """
        :return: The end sample of the loop, if this BRSTM
                 is looped, otherwise always 0.
        """
        return 0 if not self.is_looped else self.n_samples

    def decode(self, out_path: str, *, one_file: bool = False) -> None:
        """
        Decodes this BRSTM to WAV audio and writes it to the given destination.
        Every track will be written to its own WAV file, marked by its track
        id. If "one_file" mode is activated, it will be instead written to one
        file.

        :param out_path: The output folder path to write the file to.
                         A folder will be generated at the given path which contains
                         the decoded data.
        :param one_file: (Optional) If True, then the all tracks will be written
                                    to one single WAV file, distributed along all available channels.
        """
        os_path = Path(out_path)
        if not os.path.isdir(out_path):
            path = os.path.join(os_path.parent, os_path.stem) + os.sep
        else:
            path = out_path

        os.makedirs(path, exist_ok=True)

        is_mono = self.n_channels == 1
        if is_mono:
            one_file = True

        if one_file:
            sample_rate = self.sample_rate
            chn_per_track = 1 if is_mono else 2

            pcm_data = []
            for track_id in range(self.n_tracks):
                pcm_data.append(
                    np.frombuffer(self.__get_trk_pcm_samples(track_id), dtype=np.int16).reshape(-1, self.n_channels))

            # Merge channels and flatten output to bytes
            output_pcm = np.hstack(pcm_data).astype(np.int16).tobytes()
            with wave.open(f'{path}{os.sep}{os_path.stem}._wav', 'wb') as trk_out:
                trk_out.setnchannels(chn_per_track * self.n_tracks)
                trk_out.setsampwidth(2)
                trk_out.setframerate(sample_rate)

                trk_out.writeframes(output_pcm)
        else:
            for track_id in range(self.n_tracks):
                with wave.open(f'{path}{os.sep}{os_path.stem}_track_{track_id}._wav', 'wb') as trk_out:
                    trk_out.setnchannels(1 if is_mono else 2)  # sono or stereo
                    trk_out.setsampwidth(2)  # signed PCM-16 audio
                    trk_out.setframerate(self.sample_rate)

                    trk_out.writeframes(self.__get_trk_pcm_samples(track_id))

    def __str__(self) -> str:
        __str = (
            f'<BRSTM(codec={self.codec}, n_tracks={self.n_tracks}, n_chn={self.n_channels}, sample_rate={self.sample_rate}'
            f', is_looped={self.is_looped}')

        if self.is_looped:
            __str += f', loop_start_sample={self.loop_start}, loop_end_sample={self.loop_end}'
        else:
            __str += f', n_samples={self.n_samples}'

        if self._base_offset > 0:
            __str += f') at 0x{self._base_offset:X}>'
        else:
            __str += ')>'

        return __str

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def encode(cls, in_file: str, out_path: str, *, loop_start: int = -1, loop_end: int = -1, volume: int = 100) -> None:
        """
        Encodes the given WAV file to a BRSTM according to the specified parameters.
        The BRSTM file with have n tracks for n / 2 channels (except for mono audio, which
        is always one channel and one track). This means, the WAV file needs to have
        an even number of channels, i.e. 2, 4, 8. Uneven channel numbers are not supported.
        The encoding will always be ADPCM.

        A WAV file with 8 channels will get translated to a BRSTM file with 4 tracks,
        each having one channel for the left and right side.

        The BRSTM file may be looped, if the given parameters are set. If no loop end is
        defined, the normal end of the WAV file will be chosen. The loop points are
        defined as sample numbers and not seconds. Only well-defined looped as
        (0 <= loop_start < loop_end <=num_samples) are accepted.

        The in-game volume of the BRSTM may be set in a range between [0, 100] where
        100 translates to a volume level of 100%.

        :param in_file:    The input file to convert.
        :param out_path:   The path to write the output to.
        :param loop_start: (Optional) The sample where a defined loop starts.
        :param loop_end:   (Optional) The sample where a defined loop ends.
        :param volume:     (Optional) The in-game volume level of the sound.
        """
        if str not in [type(in_file), type(out_path)]:
            raise RSTMError('Invalid path arguments for "BRSTM.encode()". Please use valid file paths')

        if not (0 <= volume <= 100):
            raise RSTMError('Invalid volume given for BRSTM!')

        with wave.open(in_file, 'rb') as wave_in:
            if wave_in.getnchannels() > BRSTM_MAX_CHN_COUNT:
                raise RSTMError('Only Wave files with at most 16 channels are eligible to be converted to BRSTM')

            if wave_in.getframerate() > BRSTM_MAX_SAMPLE_RATE:
                raise RSTMError(f'Cannot encode wave files with a sample rate higher that {BRSTM_MAX_SAMPLE_RATE}')

            n_channels = wave_in.getnchannels()
            if n_channels > 1 and n_channels % 2 != 0:
                raise RSTMError('Cannot convert a WAV with an uneven number of channels to a BRSTM')

            is_mono = n_channels == 1

            n_frames = wave_in.getnframes()
            frames = wave_in.readframes(n_frames)
            sample_rate = wave_in.getframerate()

        # Convert audio data to a NumPy array
        audio_np = np.frombuffer(frames, dtype=np.int16)

        # Split the interleaved data into separate channels
        channels = {}
        for ch in range(n_channels):
            # Extract every nth sample, starting from channel 'ch'
            ch_data = audio_np[ch::n_channels]

            # Store both raw bytearray and int16 array representation
            channels[ch] = {
                'raw': bytearray(ch_data.tobytes()),
                'int16': ch_data.copy()  # Explicit copy to ensure separate array
            }

        total_samples = n_frames * n_channels
        if wave_in.getsampwidth() == 2:
            fmt = '<' + 'h' * total_samples
        else:
            raise ValueError("This function only supports 16-bit PCM data.")

        # Generate general information
        n_tracks = n_channels // 2 if n_channels > 1 else 1
        blocks_size = 0x2000
        blocks_samples = 0x3800

        total_blocks = n_frames // blocks_samples
        if n_frames % blocks_samples != 0:
            total_blocks += 1

        final_block_samples = n_frames % blocks_samples
        if final_block_samples == 0:
            final_block_samples = blocks_samples

        final_block_size = get_bytes_for_adpcm_samples(final_block_samples)
        final_block_padded_size = align_up(final_block_size, 0x20)

        samples = struct.unpack(fmt, frames)
        channel_buffers = []
        adpcm_data = []

        for ch in range(n_channels):
            channel_data = list(samples[ch::n_channels])
            channel_buffers.append(channel_data)

            if REVO_SND_ADPCM_AVAILABLE:
                coefs, adpcm_samples = DSP_EncodeBlock(channel_buffers[ch], n_frames)
            else:
                print(len(channels[ch]['int16']), n_frames)
                coefs, adpcm_samples = encoder.dsp_encode(channel_buffers[ch], n_frames)

            # We batch the ADPCM sample data into evenly sized blocks +
            # one last remaining block which will get processed later.
            adpcm_data.append((coefs, batched(adpcm_samples, blocks_size)))

        # Write HEAD chunk
        # We need:
        #     StreamDataInfo
        #     TrackTable
        #     ChannelTable

        head_chunk = io.BytesIO()
        head_chunk_offset = 0x40  # Always 0x40

        head_chunk.write(b'HEAD\x00\x00\x00\x00')  # magic + chunk_size (will be updated later)
        ref_data_header_off = 0xC
        ref_trk_tbl_off = 0x14
        ref_chn_tbl_off = 0x1C

        head_chunk.write(struct.pack('>BBHIBBHIBBHI',
                                     1, 0, 0, 0,  # DataRef<StrmDataInfo>
                                     1, 0, 0, 0,  # DataRef<TrackTable>
                                     1, 0, 0, 0))  # DataRef<ChannelTable>
        ########################
        # Write StreamDataInfo #
        ########################
        if loop_start != -1:
            if loop_end == -1:
                loop_end = n_frames

            if loop_end != -1 and not (0 <= loop_start < loop_end <= n_frames):
                raise RSTMError('Invalid loop points set for BRSTM file!')

            is_looped = True
        else:
            is_looped = False
            loop_start = 0
            loop_end = n_frames

        strm_data_info_offset = head_chunk.tell() - 8
        codec = BrstmFormat.ADPCM
        head_chunk.write(struct.pack('>BBBBHHIIIIIIIIIII',
                                     codec, is_looped, n_channels, 0,
                                     sample_rate, 0,
                                     loop_start, loop_end,
                                     0,
                                     total_blocks, blocks_size, blocks_samples,
                                     final_block_size, final_block_samples, final_block_padded_size,
                                     blocks_samples, 4))  # Samples per entry / bytes per entry

        ####################
        # Write TrackTable #
        ####################
        trk_tbl_offset = head_chunk.tell() - 8
        head_chunk.write(struct.pack('>BBH', n_tracks, _TrkType.EXTENDED, 0))
        trk_info_offset = [0] * 8  # Max 8 tracks, so preallocate it

        # Pre-write the DataRefs for each track info
        for _ in repeat(None, n_tracks):
            head_chunk.write(struct.pack('>BBHI', 1, _TrkType.EXTENDED, 0, 0))

        volume_level = int((volume / 100) * 127)
        for i in range(n_tracks):
            trk_info_offset[i] = head_chunk.tell() - 8
            buff_old = head_chunk.tell()

            head_chunk.seek(trk_tbl_offset + 12 + 8 * i + 4)
            head_chunk.write(trk_info_offset[i].to_bytes(length=4, byteorder='big'))
            head_chunk.seek(buff_old)

            chn_per_trk = 1 if is_mono else 2
            chn_ids = [0] if is_mono else [2*i, 2*i + 1]

            head_chunk.write(struct.pack(f'>BB6sB{chn_per_trk}B',
                                         volume_level,
                                         64,
                                         b'\x00\x00\x00\x00\x00\x00',
                                         chn_per_trk,
                                         *chn_ids
                                         ))

        hs1_data = []
        hs2_data = []

        for _ in repeat(None, n_channels):
            hs1_data.append([0] * total_blocks)
            hs2_data.append([0] * total_blocks)

        for c in range(n_channels):
            for b in range(total_blocks):
                if b == 0:
                    hs1_data[c][b] = 0
                    hs2_data[c][b] = 0
                    continue

                hs1_data[c][b] = channel_buffers[c][b * blocks_samples - 1]
                hs2_data[c][b] = channel_buffers[c][b * blocks_samples - 2]

        ######################
        # Write ChannelTable #
        ######################
        chn_tbl_off = head_chunk.tell() - 8
        head_chunk.write(n_channels.to_bytes(length=1, byteorder='big') + b'\x00\x00\x00')

        chn_info_offset = [0] * 16  # Max 16 channels, so preallocate them
        for _ in repeat(None, n_channels):
            head_chunk.write(struct.pack('>BBHI', 1, 0, 0, 0))

        for i in range(n_channels):
            chn_info_offset[i] = head_chunk.tell() - 8

            buff_old = head_chunk.tell()
            head_chunk.seek(chn_tbl_off + 12 + 8 * i + 4)
            head_chunk.write(chn_info_offset[i].to_bytes(length=4, byteorder='big'))
            head_chunk.seek(buff_old)

            if is_looped:
                loop_hs1 = channel_buffers[i][loop_start - 1] if loop_start > 0 else 0
                loop_hs2 = channel_buffers[i][loop_start - 2] if loop_start > 1 else 0
            else:
                loop_hs1 = 0
                loop_hs2 = 0

            head_chunk.write(b'\x01\x00\x00\x00')
            if codec == BrstmFormat.ADPCM:
                head_chunk.write(struct.pack('>I16hhhhhhhhh',
                                             head_chunk.tell() - 4,
                                             *adpcm_data[i][0],  # history data for this channel
                                             0,  # gain, always zero
                                             0,  # predictor scale
                                             0,  # hs1, always zero
                                             0,  # hs2, always zero
                                             0,  # loop predictor scale
                                             loop_hs1,
                                             loop_hs2,
                                             0))  # padding
            else:
                head_chunk.write(b'\x00\x00\x00\x00')

        head_chunk_size = head_chunk.tell()
        # Apply padding
        head_chunk.write(b'\x00\x00\x00\x00\x00\x00')
        head_chunk.write(b'\x00' * (align_up(head_chunk_size + 6, 0x20) - (head_chunk_size + 6)))

        head_chunk_size = head_chunk.tell()

        # Write relative offsets to the subsections in the
        # HEAD chunk
        head_chunk.seek(ref_data_header_off)
        head_chunk.write(strm_data_info_offset.to_bytes(length=4, byteorder='big'))

        head_chunk.seek(ref_trk_tbl_off)
        head_chunk.write(trk_tbl_offset.to_bytes(length=4, byteorder='big'))

        head_chunk.seek(ref_chn_tbl_off)
        head_chunk.write(chn_tbl_off.to_bytes(length=4, byteorder='big'))

        head_chunk.seek(0x4)
        head_chunk.write(head_chunk_size.to_bytes(length=4, byteorder='big'))

        # Write ADPC chunk
        # Only present if this file is truly ADPCM encoded
        adpc_chunk = io.BytesIO()
        adpc_chunk_offset = head_chunk_offset + head_chunk_size

        adpc_chunk.write(b'ADPC\x00\x00\x00\x00')

        for b in range(total_blocks):
            for c in range(n_channels):
                adpc_chunk.write(struct.pack('>hh', hs1_data[c][b], hs2_data[c][b]))

        adpc_chunk_size = adpc_chunk.tell()
        adpc_chunk.write(b'\x00' * (align_up(adpc_chunk_size, 0x20) - adpc_chunk_size))
        adpc_chunk_size = adpc_chunk.tell()

        adpc_chunk.seek(0x4)
        adpc_chunk.write(adpc_chunk_size.to_bytes(length=4, byteorder='big'))

        # Write DATA chunk
        # Every sample is interlaced, so in other words the data
        # alternates every block, i.e.
        #     Channel 0 Block 0
        #     Channel 1 Block 0
        #     Channel 0 Block 1
        #     Channel 1 Block 1
        #     ...
        data_chunk = io.BytesIO()
        data_chunk_offset = adpc_chunk_offset + adpc_chunk_size

        data_chunk.write(struct.pack('>4sII', b'DATA', 0, 0x18))
        data_chunk.seek(0x20)

        for i in range(total_blocks):
            for chn in range(n_channels):
                data = bytearray(next(adpcm_data[chn][1]))
                data_chunk.write(data)

                if i == total_blocks - 1:  # final block
                    padding = abs(len(data) - align_up(len(data), 0x20))
                    data_chunk.write(b'0' * padding)

        data_chunk_size = data_chunk.tell()
        data_chunk.seek(0x4)
        data_chunk.write(data_chunk_size.to_bytes(length=4, byteorder='big'))

        ###########################
        # Write actual BRSTM file #
        ###########################
        brstm_file = io.BytesIO()
        brstm_file_size = 0x40 + data_chunk_size

        # Start by writing the base header
        brstm_file.write(struct.pack('>4sHHIHHIIIIII',
                                     b'RSTM', ByteOrder.BIG_ENDIAN, _Version.VERSION_1_0,
                                     brstm_file_size,
                                     0x40, 2,
                                     head_chunk_offset, head_chunk_size,
                                     adpc_chunk_offset, adpc_chunk_size,
                                     data_chunk_offset, data_chunk_size))
        brstm_file.seek(0x40)  # padding, start here actual writing

        brstm_file.write(head_chunk.getvalue())
        brstm_file.write(adpc_chunk.getvalue())
        brstm_file.write(data_chunk.getvalue())
        with open(out_path, 'wb') as out_file:
            out_file.write(brstm_file.getvalue())

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        if data is None:
            raise ValueError('Cannot load file from "None" data')
        return cls(open(data, 'rb')) if isinstance(data, str) else cls(data)
