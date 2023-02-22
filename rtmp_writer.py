import cv2
import ffmpeg
import numpy as np


class RtmpWriter:

    def __init__(
        self,
        rtmp_url: str,
        output_width: int = 1200,
        output_height: int = 800,
    ):
        self._rtmp_url = rtmp_url
        self._opend = False
        self._output_width = output_width
        self._output_height = output_height
        self._ffmpeg_process = None

    def open(self) -> None:
        self._ffmpeg_process = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{int(self._output_width)}x{int(self._output_height)}')
            .output(self._rtmp_url, pix_fmt='yuv420p', f='flv')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        self._opend = True

    def close(self) -> None:
        if self._opend:
            try:
                self._ffmpeg_process.stdin.close()
                self._ffmpeg_process.wait()
            finally:
                self._opend = False

    def write(self, image: np.ndarray) -> None:
        if not self._opend:
            self.open()
        self._ffmpeg_process.stdin.write(
            cv2.resize(image, (self._output_width, self._output_height))
            .astype(np.uint8)
            .tobytes()
        )
