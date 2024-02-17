from dotenv import load_dotenv
import os
from pydub import AudioSegment
from elevenlabs import set_api_key, generate, save

def text_to_speech(text, voice, output_path):
    """
    Converts text to speech using the Eleven API and saves the audio to a mp3 file.
    """
    # Retrieve API key
    load_dotenv()
    xi_api_key = os.getenv('xi_api_key')
    set_api_key(xi_api_key)

    # Generate speech using the Eleven API and save the audio to a mp3 file
    audio = generate(text = text, voice = voice)
    save(audio, output_path)

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

