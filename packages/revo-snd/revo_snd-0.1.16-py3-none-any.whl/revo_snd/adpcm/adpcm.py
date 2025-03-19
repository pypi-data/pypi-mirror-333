"""
Common functions related to ADPCM data
"""
import math
import struct
from typing import BinaryIO

import numpy as np
from numba import njit

FRAME_SIZE = 8  # Each ADPCM frame is 8 bytes.
PACKET_SAMPLES = 14  # 1 header byte + 7 data bytes => 14 samples


def align_up(val, alignment):
    return math.ceil(val / alignment) * alignment


def get_bytes_for_adpcm_samples(samples: int) -> int:
    packets = samples // PACKET_SAMPLES
    extra_samples = samples % PACKET_SAMPLES
    extra_bytes = 0

    if extra_samples != 0:
        extra_bytes = (extra_samples // 2) + (extra_samples % 2) + 1

    return FRAME_SIZE * packets + extra_bytes


class AdpcmError(Exception):
    pass


class AdpcmParam:
    def __init__(self, data: BinaryIO = None, *,
                 coefs: list[int] = None, gain: int = 0, pred_scale: int = 0, yn1: int = 0, yn2: int = 0) -> None:
        if data is not None:
            self.coefs = struct.unpack('>16h', data.read(32))
            (self.gain, self.pred_scale, self.yn1, self.yn2) = struct.unpack('>hhhh', data.read(8))
        else:
            if coefs is None:
                self.coefs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                if len(coefs) != 16:
                    raise AdpcmError('Invalid number of coefficients! There need to be exactly 16!')

                self.coefs = coefs
                self.gain = gain
                self.pred_scale = pred_scale
                self.yn1 = yn1
                self.yn2 = yn2

    def to_bytes(self) -> bytes:
        return struct.pack('>16h', *self.coefs) + struct.pack('>hhhh', self.gain, self.pred_scale,
                                                              self.yn1, self.yn2)

    def __str__(self) -> str:
        return f'<AdpcmParams(yn1={self.yn1}, yn2={self.yn2}, coefs={self.coefs})>'

    def __repr__(self) -> str:
        return self.__str__()


class AdpcmLoopParam:
    def __init__(self, data: BinaryIO = None, *,
                 pred_scale: int = 0, yn1: int = 0, yn2: int = 0) -> None:
        if data is not None:
            self.pred_scale, self.yn1, self.yn2 = struct.unpack('>hhh', data.read(6))
        else:
            self.pred_scale = pred_scale
            self.yn1 = yn1
            self.yn2 = yn2

    def to_bytes(self) -> bytes:
        return struct.pack('>hhh', self.pred_scale, self.yn1, self.yn2)

    def __str__(self) -> str:
        return f'<AdpcmLoopParams(yn1={self.yn1}, yn2={self.yn2})>'

    def __repr__(self) -> str:
        return self.__str__()


class AdpcmParamSet:
    def __init__(self, data: BinaryIO, *,
                 coefs: list[int] = None, gain: int = 0, pred_scale: int = 0, yn1: int = 0, yn2: int = 0,
                 loop_pred_scale: int = 0, loop_yn1: int = 0, loop_yn2: int = 0) -> None:
        if data is not None:
            self.adpcm_param = AdpcmParam(data=data)
            self.adpcm_loop_param = AdpcmLoopParam(data=data)
        else:
            self.adpcm_param = AdpcmParam(coefs=coefs, gain=gain, pred_scale=pred_scale, yn1=yn1, yn2=yn2)
            self.adpcm_loop_param = AdpcmLoopParam(pred_scale=loop_pred_scale, yn1=loop_yn1, yn2=loop_yn2)

    def __str__(self) -> str:
        return f'<AdpcmParamSet(adpcm_params={self.adpcm_param}, adpcm_loop_param={self.adpcm_loop_param})>'

    def __repr__(self) -> str:
        return self.__str__()


def decode_pcm8_block(sample_data: (bytes | bytearray), n_samples: int, n_chn: int) -> bytearray:
    """
        Decodes a block of PCM8 audio data (unsigned 8-bit) to 16-bit PCM.
        Each byte is converted by subtracting 128 and shifting left 8 bits.

        :return: The decoded data.
    """
    # Allocate enough space: 2 bytes per 16-bit sample
    out_bytes = bytearray(2 * n_samples * n_chn)
    for i in range(n_samples):
        sample8 = sample_data[i]
        sample = (sample8 - 128) << 8  # Convert to signed 16-bit value
        offset = (i * n_chn) * 2
        out_bytes[offset:offset+2] = struct.pack('<h', sample)
    return out_bytes


def decode_pcm16_block(sample_data: (bytes | bytearray), n_samples: int, n_chn: int) -> bytearray:
    """
        Decodes a block of PCM16 audio data.
        Each sample is assumed to be stored as a little-endian 16-bit signed integer.

        :return: The decoded data.
    """
    out_bytes = bytearray(2 * n_samples * n_chn)
    for i in range(n_samples):
        # Unpack a 16-bit little-endian sample from the input data.
        sample = struct.unpack_from('<h', sample_data, offset=i * 2)[0]
        # Calculate byte offset for the first channel in this frame
        offset = (i * n_chn) * 2
        # Pack the sample back into the output bytearray.
        out_bytes[offset:offset+2] = struct.pack('<h', sample)
    return out_bytes


@njit
def _decode_adpcm_block(sample_data, n_samples, n_chn, coefs, yn1, yn2):
    samples_per_frame = 14
    frame_size = 8

    output = np.zeros(n_samples * n_chn, dtype=np.int16)
    samples_written = 0
    offset = 0

    while samples_written < n_samples:
        header = sample_data[offset]
        predictor = header >> 4
        shift = header & 0x0F

        for i in range(samples_per_frame):
            if samples_written >= n_samples:
                break

            byte_idx = 1 + (i // 2)
            nibble_shift = 4 if (i % 2) == 0 else 0
            nibble_byte = sample_data[offset + byte_idx]
            nibble = (nibble_byte >> nibble_shift) & 0x0F

            # Sign-extend the nibble
            if nibble >= 8:
                nibble -= 16

            # Compute predicted sample
            predicted = ((coefs[predictor * 2] * yn1) + (coefs[predictor * 2 + 1] * yn2)) // 2048
            sample = (nibble << shift) + predicted

            # Clamp to int16 range
            if sample > 32767:
                sample = 32767
            elif sample < -32768:
                sample = -32768

            yn2 = yn1
            yn1 = sample

            output[samples_written * n_chn] = sample
            samples_written += 1

        offset += frame_size

    return output


def decode_adpcm_block(sample_data: (bytes | bytearray), n_samples: int, n_chn: int,
                       coefs: list[int], yn1: int, yn2: int) -> bytearray:
    """
    Decodes a block of ADPCM audio data to PCM audio data.
    This function is JITed, with only one function needed
    to decode the code. The speed may be as fast as the
    C function.

    :param sample_data: The ADPCM sample data.
    :param n_samples:   The number of samples inside the data block.
    :param n_chn:       The number of channels of the audio data.
    :param coefs:       The coefficient matrix, passed as a list of 16 values. The list has to be exactly
                        16 in size.
    :param yn1:         First history data.
    :param yn2:         Second history data.
    :return: A tuple containing the decoded data in a list and both history values.
    """
    sample_data_np = np.frombuffer(sample_data, dtype=np.uint8)
    coefs_np = np.array(coefs, dtype=np.int16)

    decoded_pcm = _decode_adpcm_block(sample_data_np, n_samples, n_chn, coefs_np, yn1, yn2)

    return bytearray(decoded_pcm.tobytes())
