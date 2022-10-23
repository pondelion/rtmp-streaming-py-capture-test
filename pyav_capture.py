import av
import cv2
import numpy as np
import soundfile as sf

container = av.open('rtmp://[RTMP Server IP]:[PORT]/live/testkey')

stream_audio = container.streams.audio[0]

cnt = 500
audio_all = None

for frame in container.decode(video=0, audio=0):
    cnt += 1
    if type(frame) is av.video.frame.VideoFrame:
        img = frame.to_ndarray(format='bgr24')
        # cv2.imwrite('./rtmp_pyav_cap.jpg', img)
        # print(f'img.shape : {img.shape}')
    elif  type(frame) is av.audio.frame.AudioFrame:
        audio = frame.to_ndarray(format='s16')
        audio_all = audio if audio_all is None else np.hstack([audio_all, audio])  # (CHANNEL, N_SAMPLE)  e.g. (2, N) for stereo
        # print(f'audio_all.shape : {audio_all.shape}')
    if cnt > 1000:
        break

sf.write("./rtmp_pyav_cap.wav", audio_all.transpose(), stream_audio.sample_rate, subtype="PCM_16")
