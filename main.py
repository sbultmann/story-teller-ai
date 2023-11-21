from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()



def generate_story(gpt_prompt):
    messages=[
        {"role": "system", "content":   "Du bist ein Autor von Geschichten und Erzählungen, die als Hörbuch vertont werden. \
                                        Erzeuge eine interessante Geschichte anhand der User angaben. Die Geschichte darf \
                                        nicht mehr als 4096 characters haben."},
        {"role": "user", "content": gpt_prompt}
        ]
    client = OpenAI()
    print("Creating story ...")
    response = client.chat.completions.create(
        temperature = 1.3,
        model="gpt-4-1106-preview",
        messages=messages,
    )
    return response.choices[0].message.content

def text_to_speech(text, voice="onyx", file_name="speech.mp3"):
    """possible voices: ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']"""
    client = OpenAI()
    print('TTS running ...')
    #speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=text
    )
    response.stream_to_file(f"{file_name}")

def save_story(prompt, file_name):
    with open(f'{file_name}', "w") as f:
        f.write(prompt)


if __name__ == "__main__":
    gpt_prompt = input("Was soll in der Geschichte passieren: ")
    story = generate_story(gpt_prompt)
    text_to_speech(story, "onyx", f'Story.{time.time()}.mp3')
    save_story(story, f'Story.{time.time()}.txt')
    print('done!')
