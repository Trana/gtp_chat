import whisper

model = whisper.load_model("base")
result = model.transcribe("output.wav", fp16=False)
print(result["text"])