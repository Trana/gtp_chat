from openai import OpenAI
from pathlib import Path
import playsound
import os
import re
from datetime import datetime, timedelta 

from recorder import live_speech

chatgpt = OpenAI()
messages = [
    {
        "role": "system",
        "content": "You are a grumpy old home made robot with humor that gets asked questions. Answer in 20 words or less. the questions will be in swedish and the answers should be ins wedish"
    },
]
wakeup_word = "volt"
last_interaction_time = None

def detect_wakeup(command: str, wakeup_word: str):
    command = re.sub(r"[,\.!?]", "", command.lower())
    print(command)
    if wakeup_word in command:
        print("Detected wakeup word!")
        return True

    return False

def play_sound(sound:str):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sound_path = os.path.join(current_dir, 'sounds', sound)
    playsound.playsound(sound_path)

while True:
    for message in live_speech(10):
        if detect_wakeup(message, wakeup_word):
            print(f"Detected: {message}")
            play_sound("detected.mp3")
            start_time = datetime.now()
            break
    for message in live_speech(50, 15):
        if message=="_exit_":
            play_sound("bye.mp3")
            last_interaction_time = None
            break
        if message == "":
            continue

        last_interaction_time = datetime.now()
        play_sound("processing.mp3")
        messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        response = chatgpt.chat.completions.create(
            model="gpt-4",  
            messages=messages
        )

        response_text = response.choices[0].message.content
        print(f"ChatGPT: {response_text}")

        messages.append(
            {
                "role": "assistant",
                "content": response_text
            }
        )

        voice = chatgpt.audio.speech.create(
            input=response_text,
            model="tts-1-hd",
            voice="onyx",
        )

        voice.stream_to_file("audio.mp3")
        playsound.playsound("audio.mp3")
        os.remove("audio.mp3")
        