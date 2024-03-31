from openai import OpenAI

model = OpenAI()

voice = model.audio.speech.create(
    input="Ja!?",
    model="tts-1-hd",
    voice="onyx",
)

voice.stream_to_file("sounds/detected.mp3")

voice = model.audio.speech.create(
    input="Hmmm",
    model="tts-1-hd",
    voice="onyx",
)

voice.stream_to_file("sounds/processing.mp3")