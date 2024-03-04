from dotenv import load_dotenv
import os
from pydub import AudioSegment
from elevenlabs import set_api_key, generate, save, Voice, VoiceSettings
from gtts import gTTS

def text_to_speech(text_chunks, voices, output_filename):
    """
    Converts text to an audio file using the Eleven Labs API.
    """
    load_dotenv()
    xi_api_key = os.getenv('xi_api_key')
    set_api_key(xi_api_key)

    output = []
    combined_audio = AudioSegment.empty()
    total_duration = 0  
    for i, text_chunk in enumerate(text_chunks):
        # Alternate voices between chunks
        voice = voices["rick"] if i % 2 == 0 else voices["morty"]
        audio = generate(
            text=text_chunk, 
            voice=Voice(
                voice_id=voice,
                settings=VoiceSettings(stability=0.45, similarity_boost=0.75, style=0.05, use_speaker_boost=True)
            )
        )
        audio_path = f"test/audio_files/{i}.mp3"
        save(audio, audio_path)

        # Load the audio file as a pydub AudioSegment
        audio_segment = AudioSegment.from_file(audio_path, format="mp3")

        # Calculate the duration of the generated audio segment
        audio_duration = len(audio_segment)

        # Append the audio segment to the combined audio
        combined_audio += audio_segment

        # Assign start and end times based on the duration
        start_time = total_duration / 1000.0  # Convert milliseconds to seconds
        end_time = (total_duration + audio_duration) / 1000.0
        total_duration += audio_duration  # Update the cumulative duration
        
        # Append the voice ID, audio path, and start and end times to the output list
        output.append({"voice_id": voice, "audio_path": audio_path, "start": start_time, "end": end_time})

    # Save the combined audio to a file
    combined_audio_path = f"test/audio_files/{output_filename}"
    combined_audio.export(combined_audio_path, format="mp3")

    return output

# def text_to_speech(text, output_filename):
#     """
#     Converts text to an audio file using gTTS.
#     """
#     tts = gTTS(text)
#     tts.save(output_filename)

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

# Test 
if __name__ == "__main__":
    ricky_ID = "F7GmQe0BY7nlHiDzHStR"
    morty_ID = "8ywemhKnE8RrczyytVz1"
    text = "In case you find yourself in a fight, take a look at the UFC illegal moves."
    voice = ricky_ID
    output_path = "test/tiktok_sample.mp3"
    text_to_speech(text, voice, output_path)