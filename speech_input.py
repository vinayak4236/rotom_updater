import whisper, pyaudio, wave, tempfile, os

# load once at startup (≈ 75 MB, ~1-2 s)
_whisper_model = whisper.load_model("tiny.en")

def listen() -> str:
    CHUNK   = 1024
    RATE    = 16000
    SECONDS = 3                         # tweak if needed
    FORMAT  = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream(); stream.close(); p.terminate()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wf = wave.open(tmp.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()          # <-- close first

        text = _whisper_model.transcribe(tmp.name, language="en")["text"].strip()
        tmp.close()         # <-- close tempfile object
        os.unlink(tmp.name) # <-- now safe to delete          # cleanup
        return text