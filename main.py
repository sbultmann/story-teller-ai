from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()



def generate_story(gpt_prompt):
    messages=[
        {"role": "system", "content":   "Du bist ein Autor von Geschichten und Erzählungen. \
                                        Erzeuge eine interessante Geschichte anhand der User-Angaben."},
        {"role": "user", "content": gpt_prompt}
        ]
    client = OpenAI()
    print("Creating story ...")
    response = client.chat.completions.create(
        temperature = 1.0,
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

def split_story(story):
    """TTS cannot deal with strings longer than 4096"""
    splitted_story = story.split()
    current_chunk_length = 0
    chunk = []
    result = []
    for word in splitted_story:
        if current_chunk_length<3500:
            current_chunk_length += len(word)
            chunk.append(word)
        else:
            result.append(" ".join(chunk))
            current_chunk_length = len(word)
            chunk = []
            chunk.append(word)
    result.append(" ".join(chunk))
    return result

if __name__ == "__main__":
    gpt_prompt = input("Was soll in der Geschichte passieren: ")
    story = generate_story(gpt_prompt)
    for i,split in enumerate(split_story(story)):
        print(len(split))
        text_to_speech(split, "onyx", f'Story.{time.time()}.{str(i).zfill(3)}.mp3')
    save_story(story, f'Story.{time.time()}.txt')
    print('done!')
