import re
from gtts import gTTS
import os

def preprocess_text(body_text):
    # Split text by punctuation into lines
    sentences = re.split(r'(?<=[.!?]) +', body_text)
    
    # Split sentences into chunks of two words
    two_word_chunks = [' '.join(chunk) for sentence in sentences for chunk in zip(*[iter(sentence.split())]*2)]
    
    return two_word_chunks

def save_text_to_file(chunks, filename="processed_text.txt"):
    with open(filename, "w") as file:
        for chunk in chunks:
            file.write(chunk + "\n")

def generate_audio_from_text(filename="processed_text.txt"):
    with open(filename, "r") as file:
        for index, line in enumerate(file, start=1):
            tts = gTTS(line, lang='en')
            audio_filename = f"audio_{index}.mp3"
            tts.save(audio_filename)
            print(f"Generated {audio_filename} for: {line.strip()}")

# Example usage
if __name__ == "__main__":
    body_text = "Your body text here. This will be split by punctuation and then into groups of two words."
    chunks = preprocess_text(body_text)
    save_text_to_file(chunks)
    generate_audio_from_text()
