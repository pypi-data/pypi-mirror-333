import time
import threading
import numpy as np
import sounddevice as sd
from typing import Callable, Optional


class OS_WaveSoundHandle:
    def __init__(self, n_chn: int, samp_width: int, sample_rate: int,
                 pcm_data: bytearray, debug: bool = False,
                 loop_start: int = None, loop_end: int = None,
                 timer_callback: Optional[Callable[[int, int, int, int], None]] = None,
                 final_callback: Callable = None) -> None:
        self._stop_flag = False
        self._pause_flag = False
        self._current_frame = 0  # Current frame index

        self._n_chn = n_chn
        self._samp_width = samp_width
        self._sample_rate = sample_rate

        # Load PCM data and reshape into a 2D array (n_frames, n_chn)
        self._pcm_data = np.frombuffer(pcm_data, dtype=np.int16)
        self._pcm_data = self._pcm_data.reshape(-1, n_chn)

        self._total_duration = len(self._pcm_data) / self._sample_rate
        self._total_min, self._total_sec = divmod(int(self._total_duration), 60)

        self._stream = None          # Sounddevice stream
        self._timer_thread = None   # Timer thread

        self._debug = debug

        # Loop settings: if both are provided, looping is enabled.
        self._loop_start = loop_start
        self._loop_end = loop_end
        self._loop_enabled = (loop_start is not None and loop_end is not None)

        # Lock to protect _current_frame and volume updates.
        self._lock = threading.Lock()

        # Volume control: default is 1.0 (100%)
        self._volume = 1.0

        # Optional callback for playback timer updates.
        self._timer_callback = timer_callback
        self._final_callback = final_callback

    def debug(self, flag: bool) -> 'OS_WaveSoundHandle':
        """
        Sets the debug flag of this handle. If true, debug mode is enabled
        and additional information will be printed.
        """
        self._debug = flag
        return self

    def set_timer_callback(self, callback: Callable[[int, int, int, int], None]) -> 'OS_WaveSoundHandle':
        """
        Set a callback that will be called by the playback timer.
        The callback receives four integers: (current_minute, current_second, total_minute, total_second).
        """
        self._timer_callback = callback
        return self

    def set_final_callback(self, callback: Callable) -> 'OS_WaveSoundHandle':
        """
        Sets the callback function, which should be invoked at the end
        of a playback. The callback receives no arguments.
        """
        self._final_callback = callback
        return self

    def loop_at(self, loop_start: int = -1, loop_end: int = -1) -> 'OS_WaveSoundHandle':
        if loop_start == -1 and loop_end == -1:
            self._loop_enabled = True
            return self

        if not (0 <= loop_start < loop_end <= len(self._pcm_data)):
            raise IndexError('OS_WaveSoundHandle error! Invalid loop points set!')
        self._loop_start = loop_start
        self._loop_end = loop_end
        self._loop_enabled = True
        # Do not change _current_frame so that initial playback is unaffected.
        return self

    def stop_loop(self) -> 'OS_WaveSoundHandle':
        self._loop_enabled = False
        return self

    def skip_to(self, second: float) -> 'OS_WaveSoundHandle':
        """Skip to a given time (in seconds) in the track."""
        target_frame = int(second * self._sample_rate)
        if target_frame < 0 or target_frame >= len(self._pcm_data):
            raise ValueError("Invalid skip time")
        with self._lock:
            self._current_frame = target_frame
        if self._debug:
            print(f"\n[DEBUG] Skipping to time: {second:.2f} sec (frame {target_frame})")
        return self

    def skip_to_sample(self, sample: int) -> 'OS_WaveSoundHandle':
        """Skip to a given sample index in the track."""
        if sample < 0 or sample >= len(self._pcm_data):
            raise ValueError("Invalid skip sample")
        with self._lock:
            self._current_frame = sample
        if self._debug:
            print(f"\n[DEBUG] Skipping to sample: {sample}")
        return self

    def set_volume(self, volume: float) -> 'OS_WaveSoundHandle':
        """
        Dynamically set the playback volume.
        A volume of 1.0 is 100%; 0.5 is 50%; values >1.0 amplify the signal.
        """
        if volume < 0:
            raise ValueError("Volume cannot be negative")
        with self._lock:
            self._volume = volume
        if self._debug:
            print(f"\n[DEBUG] Volume set to: {volume}")
        return self

    def get_curr_sample(self) -> int:
        """Return the current sample (frame) index."""
        with self._lock:
            return self._current_frame

    def get_curr_time(self) -> (int, int):
        """
        Return a tuple (minute, second) representing the current playback time.
        In loop mode, the time is relative to the loop start.
        """
        with self._lock:
            cur = self._current_frame
        if self._loop_enabled and cur >= self._loop_start:
            loop_elapsed = (cur - self._loop_start) % (self._loop_end - self._loop_start)
            elapsed_sec = loop_elapsed / self._sample_rate
        else:
            elapsed_sec = cur / self._sample_rate
        minute, second = divmod(int(elapsed_sec), 60)
        return minute, second

    def _audio_callback(self, outdata, frames, time_info, status):
        if status and self._debug:
            print(status)
        if self._stop_flag:
            raise sd.CallbackStop
        if self._pause_flag:
            outdata.fill(0)
            return

        # Process audio playback with or without looping.
        if self._loop_enabled:
            with self._lock:
                cur = self._current_frame
            if cur < self._loop_start:
                if cur + frames <= self._loop_end:
                    chunk = self._pcm_data[cur:cur + frames]
                    new_cur = cur + frames
                else:
                    frames_before_loop = self._loop_end - cur
                    part1 = self._pcm_data[cur:self._loop_end]
                    frames_after_loop = frames - frames_before_loop
                    loop_length = self._loop_end - self._loop_start
                    indices = (np.arange(frames_after_loop) % loop_length) + self._loop_start
                    part2 = self._pcm_data[indices]
                    chunk = np.concatenate((part1, part2), axis=0)
                    new_cur = self._loop_start + (frames_after_loop % loop_length)
            else:
                if cur + frames <= self._loop_end:
                    chunk = self._pcm_data[cur:cur + frames]
                    new_cur = cur + frames
                else:
                    frames_in_loop = self._loop_end - cur
                    part1 = self._pcm_data[cur:self._loop_end]
                    frames_wrap = frames - frames_in_loop
                    loop_length = self._loop_end - self._loop_start
                    indices = (np.arange(frames_wrap) % loop_length) + self._loop_start
                    part2 = self._pcm_data[indices]
                    chunk = np.concatenate((part1, part2), axis=0)
                    new_cur = self._loop_start + (frames_wrap % loop_length)
            with self._lock:
                self._current_frame = new_cur
        else:
            with self._lock:
                cur = self._current_frame
                new_cur = cur + frames
            chunk = self._pcm_data[cur:new_cur]
            if len(chunk) < frames:
                outdata[:len(chunk), :] = (chunk.astype(np.float32) / 32768.0) * self._volume
                outdata[len(chunk):].fill(0)
                with self._lock:
                    self._current_frame = new_cur
                raise sd.CallbackStop
            else:
                with self._lock:
                    self._current_frame = new_cur

        # Apply volume dynamically during playback.
        with self._lock:
            current_volume = self._volume
        outdata[:] = (chunk.astype(np.float32) / 32768.0) * current_volume

    def _playback_timer(self):
        """Continuously update playback progress until stopped or finished."""
        while not self._stop_flag and self._current_frame < len(self._pcm_data):
            with self._lock:
                cur = self._current_frame
            elapsed_sec = cur / self._sample_rate
            tmin, tsec = divmod(int(elapsed_sec), 60)
            total_min, total_sec = self._total_min, self._total_sec
            state = "Pause" if self._pause_flag else "Playing"

            # Call the timer callback if provided.
            if self._timer_callback:
                self._timer_callback(tmin, tsec, total_min, total_sec)

            print(f"\r{state}: {tmin:02}:{tsec:02} / {total_min:02}:{total_sec:02}", end="", flush=True)
            time.sleep(0.25)

        if self._final_callback:
            self._final_callback()
        print("\nPlayback finished!")

    def _start_timer(self):
        """Start the timer thread if not already running."""
        if self._timer_thread is None or not self._timer_thread.is_alive():
            self._timer_thread = threading.Thread(target=self._playback_timer, daemon=True)
            self._timer_thread.start()

    def _play(self):
        with self._lock:
            if hasattr(self, "_killed") and self._killed:
                raise RuntimeError("This WaveSoundHandle has been killed and cannot be used for playback.")

        self._stop_flag = False
        self._pause_flag = False
        # If playback has finished previously, reset to beginning.
        with self._lock:
            if self._current_frame >= len(self._pcm_data):
                self._current_frame = 0
        self._stream = sd.OutputStream(
            samplerate=self._sample_rate,
            channels=self._n_chn,
            callback=self._audio_callback
        )
        self._stream.start()
        self._start_timer()
        # Block until playback finishes or is stopped.
        while not self._stop_flag and self._current_frame < len(self._pcm_data):
            time.sleep(0.1)

        if self._stream:
            self._stream.stop()

    def pause(self):
        if not self._pause_flag:
            self._pause_flag = True
            if self._stream:
                self._stream.stop()
            if self._debug:
                with self._lock:
                    cur = self._current_frame
                print(f"\n[DEBUG] Playback paused at frame: {cur}")

    def resume(self):
        if self._stop_flag:
            self._play()

        if self._pause_flag:
            self._pause_flag = False
            self._stream = sd.OutputStream(
                samplerate=self._sample_rate,
                channels=self._n_chn,
                callback=self._audio_callback
            )
            self._stream.start()
            self._start_timer()
            if self._debug:
                with self._lock:
                    cur = self._current_frame
                print(f"\n[DEBUG] Resuming playback from frame: {cur}")

    def is_running(self) -> bool:
        """
        Return True if playback is currently active (i.e., not stopped or paused
        and the underlying stream is active), else False.
        """
        if self._stream is None:
            return False
        return self._stream.active and not self._pause_flag and not self._stop_flag

    def kill(self) -> None:
        """
        Stop playback and release resources. After calling kill(), this handle should not be reused.
        """
        self._stop_flag = True
        if self._stream:
            self._stream.stop()
            self._stream.close()
        with self._lock:
            self._pcm_data = None
            self._killed = True
        if self._debug:
            print("\n[DEBUG] Handle killed.")


def OS_PlayWaveSound(handle: OS_WaveSoundHandle, *, daemon: bool = True) -> None:
    """
    Spawns a new thread and starts the playback of this
    the provided sound handle.
    """
    playback_thread = threading.Thread(target=handle._play, daemon=daemon)
    playback_thread.start()
    if not daemon:
        playback_thread.join()


def OS_KillWaveSound(handle: OS_WaveSoundHandle) -> None:
    """
    Terminates the given sound handle and releases all of its
    resources. A terminated handle may not be used again.
    """
    handle.kill()
