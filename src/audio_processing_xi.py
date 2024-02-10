from dotenv import load_dotenv
import os
import requests
import whisper_timestamped as whisper
from pydub import AudioSegment
from pydub.playback import play

def speed_up_mp3(input_path, output_path, speed_factor):
    """
    Speeds up an audio file and saves the result to a new file.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_path, format="mp3")

    # Speed up the audio
    sped_up = audio.speedup(playback_speed=speed_factor)

    # Export the sped-up audio to a new file
    sped_up.export(output_path, format="mp3")

def text_to_speech(text, output_path):
    """
    Converts text to speech using the Eleven API and saves the audio to a file.
    """
    # Retrieve API key
    load_dotenv()
    xi_api_key = os.getenv('xi_api_key')

    # Select voice ID and model ID
    voice_id = "TX3LPaxmHKxFdv7VOQHJ"
    model_id = "eleven_multilingual_v1"

    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    payload = {
    "text": text,
    "voice_settings": {
        "similarity_boost": 0.75,
        "stability": 0.25
        },
        "model_id": model_id
    }
    headers = {
        "xi-api-key": xi_api_key,
        "Content-Type": "application/json"
    }

    # Make the POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # Save the received audio content to the specified output file
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def generate_captions(audio_path):
    """
    Generates 2-word captions for an audio file using the whisper library and extracting timestamps.
    """
    # Load a whisper model and transcribe the audio
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("base")
    json_result = whisper.transcribe(model, audio, language="en")

    captions = []
    # Iterate through each segment in the JSON data
    for segment in json_result["segments"]:
        # Iterate through each word in the segment
        words = segment["words"]
        num_words = len(words)
        # Combine every two words into a single caption
        for i in range(0, num_words, 2):
            if i + 1 < num_words:
                start = words[i]["start"]
                end = words[i + 1]["end"]
                text = words[i]["text"] + " " + words[i + 1]["text"]
            else:
                start = words[i]["start"]
                end = words[i]["end"]
                text = words[i]["text"]
            captions.append({
                "text": text,
                "start": start,
                "end": end
            }) 

    return captions