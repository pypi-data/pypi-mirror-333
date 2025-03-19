import revo_snd.engine.seq.OS_SeqPlayer as _OS_seq
import revo_snd.engine.wav.OS_WaveSound as _OS_wav

WII_PHYSICAL_CHN_NUM    = 96
WII_MIN_CHN             = 0
WII_MAX_CHN             = WII_MIN_CHN + WII_PHYSICAL_CHN_NUM

STRM_SND_HANDLE_CHN_MAX = 32
STRM_FILE_MAX_CHN       = STRM_SND_HANDLE_CHN_MAX >> 2  # => 16

SEQ_BASE_NOTE = _OS_seq.SEQ_BASE_NOTE

OS_PlaySeq  = _OS_seq.OS_SeqHandle_Play
OS_PlaySeq2 = _OS_seq.OS_SeqHandle_Play2

OS_Wave = _OS_wav.OS_WaveSoundHandle
OS_PlayWav = _OS_wav.OS_PlayWaveSound
OS_KillWav = _OS_wav.OS_KillWaveSound
