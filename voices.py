from openai import OpenAI

model = OpenAI()

voice = model.audio.speech.create(
    input="Hallå hallå!?",
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

voice = model.audio.speech.create(
    input="Hej då!",
    model="tts-1-hd",
    voice="onyx",
)

voice.stream_to_file("sounds/bye.mp3")