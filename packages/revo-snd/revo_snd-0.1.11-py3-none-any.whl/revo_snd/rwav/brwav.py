"""
BRWAV implementation for PyRSAR.

A BRWAV may only have one channel. The BRSTM class should be used for
multichannel audio data. Every BRWAV produced by this module is only
encoded as ADPCM audio. But the BRWAV implementation provides
compatibility to decode PCM8, PCM16 and ADPCM encoded audio data.
"""
import wave

from revo_snd.engine._wav.OS_WaveSound import OS_WaveSoundHandle
from revo_snd.nw4r import *

try:
    # We get help from following C functions:
    # DSP_EncodeBlock, DSP_DecodeBlock
    # additionally there are:
    #     DSP_CalcCoefs    (calculate the coefficient matrix for the given PCM sample data)
    #     DSP_EncodeFrame  (encode one single PCM sample to ADPCM)
    #
    # We need those functions, otherwise it would take
    # up a whole lifespan encoding/decoding data
    import revo_snd.revo_snd_adpcm as dsp
    REVO_SND_ADPCM_AVAILABLE = True
except ImportError:
    import revo_snd._adpcm.adpcm as a
    import revo_snd._adpcm.encode_adpcm as encoder

    DSP_DecodeBlock = a.decode_adpcm_block

    def throw_no_encoding():
        raise NW4RInternalError('Internal revo_snd_adpcm module was not found. Encoding BRWAV files is not available!')
    DSP_EncodeBlock = throw_no_encoding
    REVO_SND_ADPCM_AVAILABLE = False

    print_warning('BRWAV >> Could not find internal "revo_snd_adpcm" module')
    print_warning('BRWAV >> Decoding will switch to Python fallback function')
    print_warning('BRWAV >> Encoding will switch to Python fallback function')

import revo_snd._adpcm.adpcm as adpcm


class _Version:
    VERSION_1_0 = 0x0100
    VERSION_1_1 = 0x0101
    VERSION_1_2 = 0x0102


SUPPORTED_VERSIONS = {_Version.VERSION_1_2}

FORMAT_PCM_8 = 0
FORMAT_PCM_16 = 1
FORMAT_ADPCM = 2

LOC_TYPE_OFF = 0
LOC_TYPE_ADR = 1


class RWAVError(Exception):
    pass


class _INFO:
    def __init__(self, data: BinaryIO = None, *, block_size: int = 0) -> None:
        if data is not None:
            self._base_offset = data.tell()

            block_info = read_nw4r_block_header(data)
            block_sanity_check(block_info.magic, 'INFO')

            self.wave_info = _INFO._WaveInfo(data)
        else:
            self.magic = b'INFO'
            self.block_size = block_size

    def to_bytes(self) -> (bytes | bytearray):
        return struct.pack('>4sI', self.magic, self.block_size)

    class _ChannelInfo:
        def __init__(self, data: BinaryIO = None,
                     data_offset: int = 0, adpcm_data_offset: int = 0,
                     volume_fl: int = 1, volume_fr: int = 1, volume_bl: int = 1, volume_br: int = 1) -> None:
            if data is not None:
                self.data_offset, self.adpcm_data_offset = struct.unpack('>II', data.read(8))
                self.volume_fl, self.volume_fr, self.volume_bl, self.volume_br, _ = struct.unpack('IIIII', data.read(20))
            else:
                self.data_offset = data_offset
                self.volume_fl = volume_fl
                self.volume_fr = volume_fr
                self.volume_bl = volume_bl
                self.volume_br = volume_br
                self.adpcm_data_offset = adpcm_data_offset

        def to_bytes(self) -> bytes:
            return (struct.pack('>II', self.data_offset, self.adpcm_data_offset) +
                    struct.pack('IIIII', self.volume_fl, self.volume_fr, self.volume_bl, self.volume_br, 0))

    class _ADPCM:
        def __init__(self, data: BinaryIO = None) -> None:
            if data is not None:
                self.coefs = struct.unpack('>16h', data.read(32))
                (self.gain, self.pred_scale, self.yn1, self.yn2,
                 self.loop_pred_scale, self.loop_yn1, self.loop_yn2, _) = struct.unpack('>hhhhhhhh', data.read(16))
            else:
                self.coefs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # short[16]
                self.gain = self.pred_scale = self.yn1 = self.yn2 = self.loop_pred_scale = self.loop_yn1 = self.loop_yn2 = 0

        def to_bytes(self) -> bytes:
            return struct.pack('>16h', *self.coefs) + struct.pack('>hhhhhhhh', self.gain, self.pred_scale,
                                                    self.yn1, self.yn2, self.loop_pred_scale, self.loop_yn1,
                                                    self.loop_yn2, 0)

    class _WaveInfo:
        def __init__(self, data: BinaryIO = None,
                     encoding: int = 0, is_looped: bool = False, chn: int = 1, sample_rate: int = 0,
                     chn_info_tbl_offset: int = 0x1C, data_location: int = 0, loop_start: int = 0,
                     num_samples: int = 0) -> None:
            if data is not None:
                self.base_offset = data.tell()

                (self.encoding, self.is_looped, self.chn, self.sampleRate24,
                 self.sampleRate, self.data_location_type, _, self._loop_start, self._num_samples,
                 self.chn_info_tbl_offset, self.data_location, _) = struct.unpack('>BBBBHBBIIIII', data.read(28))

                data.seek(self.chn_info_tbl_offset + self.base_offset)
                self.chn_info_tbl = struct.unpack(f'>{self.chn}I', data.read(self.chn * 4))

                self.chn_info = []
                self.adpcm_info = []
                for off in self.chn_info_tbl:
                    data.seek(self.base_offset + off)

                    self.chn_info.append(_INFO._ChannelInfo(data))

                for info in self.chn_info:
                    if self.data_location_type == LOC_TYPE_OFF:
                        data.seek(self.base_offset + info.adpcm_data_offset)
                        self.adpcm_info.append(_INFO._ADPCM(data))
                    elif self.data_location_type == LOC_TYPE_ADR:
                        data.seek(info.adpcm_data_offset)
                        self.adpcm_info.append(_INFO._ADPCM(data))
                    else:
                        raise RWAVError(f'Unknown channel location type ({self.data_location}) in WavInfo!')

            else:
                (self.encoding, self.is_looped, self.chn, self.sampleRate, self.chn_info_tbl_offset,
                 self.data_location, self._loop_start, self._num_samples) = (encoding, is_looped, chn,
                                                                             sample_rate, chn_info_tbl_offset,
                                                                             data_location, loop_start, num_samples)
                self.sampleRate24 = 0
                self.data_location_type = 0
                self.chn_info = []
                self.adpcm_info = []

        def to_bytes(self) -> bytes:
            return struct.pack('>BBBBHBBIIIII', self.encoding, self.is_looped, self.chn, self.sampleRate24,
                               self.sampleRate, self.data_location_type, 0, self._loop_start, self._num_samples,
                               self.chn_info_tbl_offset, self.data_location, 0)

        @staticmethod
        def __get_adpcm_value(value) -> int:
            return int(value / 16 * 14 + (value % 16 - 2))

        @staticmethod
        def __set_adpcm_value(value) -> int:
            return int((8 * value + 16) / 7)

        @property
        def loop_start(self) -> int:
            return self.__get_adpcm_value(self._loop_start) if self.encoding == FORMAT_ADPCM else self._loop_start

        @loop_start.setter
        def loop_start(self, value: int) -> None:
            self._loop_start = self.__set_adpcm_value(value) if self.encoding == FORMAT_ADPCM else value

        @property
        def n_samples(self) -> int:
            return self.__get_adpcm_value(self._num_samples) if self.encoding == FORMAT_ADPCM else self._num_samples

        @n_samples.setter
        def n_samples(self, value: int) -> None:
            self._num_samples = self.__set_adpcm_value(value) if self.encoding == FORMAT_ADPCM else value

        def __str__(self) -> str:
            match self.encoding:
                case 0:
                    enc_str = 'PCM8'
                case 1:
                    enc_str = 'PCM16'
                case 2:
                    enc_str = 'ADPCM'
                case _:
                    enc_str = 'UNKNOWN'
            return (f'(encoding={enc_str}, looped={bool(self.is_looped)}, n_chn={self.chn}, ' 
                    f'sample_rate={self.sampleRate}, {f'loop_start={self.loop_start}, ' if self.is_looped else ''}' 
                    f'n_sample={self.n_samples})')

        def __repr__(self) -> str:
            return self.__str__()


class _DATA:
    def __init__(self, data: BinaryIO = None, *, block_size: int = 0) -> None:
        if data is not None:
            self._base_offset = data.tell()

            block_info = read_nw4r_block_header(data)
            block_sanity_check(block_info.magic, 'DATA')

            self.sample_data = data.read(block_info.block_size - 8)
        else:
            self.magic = b'DATA'
            self.block_size = block_size

    def to_bytes(self) -> (bytes | bytearray):
        return struct.pack('>4sI', self.magic, self.block_size)


class _Wave_write:
    def __init__(self, info_offset: int, info_size: int, data_offset: int, data_size: int) -> None:
        self.magic = FileTag.BRWAV.encode('ascii')
        self.byte_order = ByteOrder.BIG_ENDIAN
        self.version = 0x0102
        self.header_size = 0x20
        self.n_sections = 2
        self.file_size = 0

        self.info_offset = info_offset
        self.info_size = info_size

        self.data_offset = data_offset
        self.data_size = data_size

    def to_bytes(self) -> bytes:
        return struct.pack('>4sHHIHHIIII', self.magic, self.byte_order, self.version, self.file_size,
                           self.header_size, self.n_sections, self.info_offset, self.info_size, self.data_offset,
                           self.info_size)


class BRWAV(RevFile):
    __FRAME_SIZE = 8
    __PACKET_SAMPLES = 14
    __PACKET_NIBBLES = 16

    def __init__(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        header = read_nw4r_file_header(data)

        self.file_info = header
        file_sanity_check(header.magic, header.byte_order, header.version, FileTag.BRWAV, SUPPORTED_VERSIONS)
        self._file_size = header.file_size

        self.info_off, self.info_size, self.data_off, self.data_size\
            = struct.unpack('>IIII', data.read(16))

        data.seek(self._base_offset + self.info_off)
        self._info = _INFO(data)

        data.seek(self._base_offset + self.data_off)
        self.data_block = _DATA(data)

        data.seek(self._base_offset)
        self.raw_data = data.read(header.file_size)

        self._decoded = False
        self._raw_pcm = None

        # Restore state to the expected position of the reader
        data.seek(self._base_offset + header.file_size)

    @property
    def encoding(self) -> str:
        match self._info.wave_info.encoding:
            case 0:
                return 'PCM8'
            case 1:
                return 'PCM16'
            case 2:
                return 'ADPCM'
            case _:
                return '<UNKNOWN ENCODING>'

    @property
    def loop_start(self) -> int:
        return self._info.wave_info.loop_start

    @property
    def loop_end(self) -> int:
        return self._info.wave_info.n_samples

    @property
    def n_channels(self) -> int:
        return self._info.wave_info.chn

    @property
    def sample_rate(self) -> int:
        return self._info.wave_info.sampleRate

    def decode(self, out_path: (str | None) = None, *, return_wav: bool = False) -> (wave.Wave_read | OS_WaveSoundHandle | None):
        """
        Decodes this BRWAV file according to its encoding type and write it to a WAV.
        Supported are PCM8, PCM16 and ADPCM audio data for the BRWAV.

        :param out_path:   The path to write the output WAV file to.
        :param return_wav: (Optional) If true, the written WAV will be returned as a Wave_read
                           object, as obtained by wave.open().
        :return: The written WAV file or nothing.
        """
        if not self._decoded:
            # Although the channel parameter is passed, it is certainly a given
            # that all BRWAV files will only have one channel (mono audio).
            encoding = self._info.wave_info.encoding
            if encoding == FORMAT_PCM_8:
                samples = adpcm.decode_pcm8_block(self.data_block.sample_data,
                                                  self._info.wave_info.n_samples,
                                                  self._info.wave_info.chn)
            elif encoding == FORMAT_PCM_16:
                samples = adpcm.decode_pcm16_block(self.data_block.sample_data,
                                                   self._info.wave_info.n_samples,
                                                   self._info.wave_info.chn)
            elif encoding == FORMAT_ADPCM:
                chn_data = self._info.wave_info.adpcm_info[0]
                coeffs = chn_data.coefs
                yn1 = chn_data.yn1
                yn2 = chn_data.yn2

                if REVO_SND_ADPCM_AVAILABLE:
                    # Call C function for faster decoding
                    samples = dsp.DSP_DecodeBlock(self.data_block.sample_data,
                                                  self._info.wave_info.n_samples,
                                                  self._info.wave_info.chn,
                                                  coeffs, yn1, yn2)
                else:
                    samples = DSP_DecodeBlock(self.data_block.sample_data,
                                              self._info.wave_info.n_samples,
                                              self._info.wave_info.chn,
                                              coeffs, yn1, yn2)

            else:
                raise RWAVError(f'Unknown encoding of type {encoding}. Cannot decode data with this encoding.')

            self._decoded = True
            self._raw_pcm = samples
        else:
            samples = self._raw_pcm

        if out_path is None:
            return OS_WaveSoundHandle(n_chn=1, samp_width=2, sample_rate=self.sample_rate, pcm_data=samples)

        # Write WAV file
        wav_out = wave.open(out_path, 'w')
        wav_out.setnchannels(1)
        wav_out.setsampwidth(2)  # 16 bits = 2 bytes per sample
        wav_out.setframerate(self._info.wave_info.sampleRate)

        wav_out.writeframes(samples)
        wav_out.close()

        if return_wav:
            return wave.open(out_path, 'r')

    @staticmethod
    def __get_nibble_address(sample: int) -> int:
        packets = sample // BRWAV.__PACKET_SAMPLES
        extra_samples = sample % BRWAV.__PACKET_SAMPLES

        return BRWAV.__PACKET_NIBBLES * packets + extra_samples + 2

    @classmethod
    def encode(cls, audio_in: (str | wave.Wave_read), audio_out: str = '', *, loop_start_sample: int = -1,
               loop_end_sample: int = -1, return_brwav: bool = False) -> Self:
        """
        Converts a normal WAV audio file to a Nintendo DSP-ADPCM audio file. This function is
        intended to be used on mono-audio WAV files. For multichannel audio files, the BRSTM
        encoder should be used instead.

        :param audio_in:  Either a file path to an audio file or a Wave_read object obtained
                          by the open() function in the wave module.
        :param audio_out: (Optional) The file path to write the audio to. If this is empty,
                          the file path of the input file will be used.
        :param loop_start_sample: (Optional) The loop start sample if the audio should be looped.
        :param loop_end_sample:   (Optional) The loop end sample if the audio should be looped.
        :param return_brwav:      (Optional) Whether the generated file should be returned or not.
        :return: A BRWAV instance of the generated file or nothing.
        """
        if isinstance(audio_in, str):
            if audio_out == '':
                root, ext = os.path.splitext(audio_in)
                audio_out = root + '.brwav'
            audio_in = wave.open(audio_in, 'rb')
        else:
            if audio_out == '':
                raise RWAVError('No output path specified')

        pack = struct.pack
        unpack = struct.unpack

        sample_rate = audio_in.getframerate()
        channels = audio_in.getnchannels()
        n_samples = audio_in.getnframes()

        if channels > 1:
            raise RWAVError('Can only convert mono (1-chn) WAV audio to BRWAV! Please use BRSTM for multi-chn audio.')

        samples = audio_in.readframes(n_samples)
        samples16 = list(unpack('h' * (len(samples) // 2), samples))

        # Don't forget to always close your streams kids ;)
        audio_in.close()

        if -1 < loop_start_sample:
            loop_start_sample = BRWAV.__get_nibble_address(loop_start_sample)
            if -1 < loop_start_sample < loop_end_sample <= n_samples:
                loop_end_sample = BRWAV.__get_nibble_address(loop_end_sample)
            else:
                if loop_end_sample > -1:
                    print_warning(f'RWAV WARNING: An invalid loop end sample ({loop_end_sample}) was defined. '
                                  f'The loop end sample will be set to the last sample instead.')
                loop_end_sample = BRWAV.__get_nibble_address(n_samples)
            is_looped = True
        else:
            if loop_end_sample > -1 and loop_end_sample > -1:
                print_warning(
                    f'RWAV WARNING: An invalid loop range ({loop_start_sample}, {loop_end_sample}) was defined. '
                    f'The WAV will not be looped.')
            loop_start_sample = BRWAV.__get_nibble_address(0)
            loop_end_sample = BRWAV.__get_nibble_address(n_samples)

            is_looped = False

        block_len = int_align(n_samples, 14) // 14 * 8
        samples_per_block = block_len // 8 * 14

        blocks = (n_samples + (samples_per_block - 1)) // samples_per_block

        if (tmp := n_samples % samples_per_block) != 0:
            lb_samples = tmp
            lb_size = (lb_samples + 13) // 14 * 8
            lb_total = int_align(lb_size, 0x20)
        else:
            lb_total = lb_size = block_len

        info_size = 8
        wave_size = 0x1C
        table_size = channels * 4
        channel_size = channels * 0x1C
        adpcm_info_size = channels * 0x30

        entry_size = int_align(info_size + wave_size + table_size + channel_size + adpcm_info_size, 0x20) - 8
        data_size = ((blocks - 1) * block_len + lb_total) * channels + 8
        file_size = 32 + entry_size + 8 + data_size

        with open(audio_out, 'wb', buffering=file_size) as file:
            rwav_file = _Wave_write(info_offset=0x20, info_size=entry_size + 8,
                                    data_offset=0x20 + entry_size + 8, data_size=data_size)
            rwav_file.file_size = file_size

            file.write(rwav_file.to_bytes())

            # INFO section
            rwav_info_block = _INFO(block_size=entry_size + 8)
            file.write(rwav_info_block.to_bytes())

            wav_info_offset = file.tell()
            wav_info = _INFO._WaveInfo(encoding=FORMAT_ADPCM, is_looped=is_looped, chn=channels,
                                       sample_rate=sample_rate, data_location=rwav_file.data_offset + 8,
                                       loop_start=loop_start_sample, num_samples=loop_end_sample)

            file.write(wav_info.to_bytes())
            rwav_info_block.wave_info = wav_info

            file.seek(wav_info.chn_info_tbl_offset + wav_info_offset)
            file.write(struct.pack('>I', 0x20))

            # Create channel info and adpcm info for each channel.
            # This does not change the fact that we will only have
            # one channel.

            file.seek(wav_info_offset + 0x20)
            chn_info = _INFO._ChannelInfo(adpcm_data_offset=wave_size + table_size + channel_size + 0 * 0x30)

            if REVO_SND_ADPCM_AVAILABLE:
                coefs, adpcm_data = dsp.DSP_EncodeBlock(samples16, n_samples)
            else:
                coefs, adpcm_data = encoder.dsp_encode(samples16, n_samples)

            adpcm_info = _INFO._ADPCM()
            adpcm_info.coefs = coefs  # dsp.DSP_CalcCoefs(samples, n_samples)

            file.write(chn_info.to_bytes())
            file.seek(chn_info.adpcm_data_offset + wav_info_offset)
            file.write(adpcm_info.to_bytes())

            rwav_data_block = _DATA(block_size=data_size)
            file.seek(rwav_file.data_offset)
            file.write(rwav_data_block.to_bytes())
            file.write(adpcm_data)

        if return_brwav:
            return cls(open(audio_out, 'rb'))

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        return cls(open(data, 'rb')) if isinstance(data, str) else cls(data)

    def __bytes__(self) -> bytes:
        return self.raw_data

    def __str__(self) -> str:
        return f'<BRWAV{self._info.wave_info}>' if self._base_offset == 0 \
            else f'<BRWAV{self._info.wave_info} at 0x{self._base_offset:X}>'

    def __repr__(self) -> str:
        return self.__str__()
