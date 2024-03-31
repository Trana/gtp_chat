import audioop
import whisper
import pyaudio
import wave
import os
from datetime import datetime, timedelta

whisper_model = whisper.load_model("small")
ambient_detected = False
speech_volume = 100

def live_speech(wait_time=10, timeout=15):
    global ambient_detected
    global speech_volume

    wait_time=10

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    CHUNK = 2048

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    recording = False
    frames_recorded = 0
    last_interaction_time = datetime.now()
    
    try:
        while True:
            frames_recorded += 1
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 2)

            if not ambient_detected:
                if frames_recorded < 40:
                    if frames_recorded == 1:
                        print("Detecting ambient noise...")
                    if frames_recorded > 5:
                        if speech_volume < rms:
                            speech_volume = rms
                    continue
                elif frames_recorded == 40:
                    print("Listening...")
                    speech_volume = speech_volume * 3
                    ambient_detected = True

            if rms > speech_volume:
                recording = True
                frames_recorded = 0
            elif recording and frames_recorded > wait_time:
                recording = False

                wf = wave.open("audio.wav", 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()

                result = whisper_model.transcribe(
                    "audio.wav",
                    language="sv", 
                    fp16=False, 
                    verbose=True
                )

                os.remove("audio.wav")

                yield result["text"].strip()
                last_interaction_time = datetime.now()
                frames = []
            if recording:
                frames.append(data)

            if not recording:
                if datetime.now() >= last_interaction_time + timedelta(seconds=timeout):
                    print("Timeout reached")
                    yield "_exit_"
                    last_interaction_time = None
                    

    finally:
        if not stream:
            stream.stop_stream()
        if stream.is_active():
            stream.close()
        audio.terminate()