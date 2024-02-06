from gtts import gTTS
import whisper_timestamped as whisper

def text_to_speech(text, output_filename):
    """
    Converts text to an audio file using gTTS.
    """
    tts = gTTS(text)
    tts.save(output_filename)

def generate_captions(audio_path):
    """
    Generates captions for an audio file using the whisper library and extracting timestamps.
    """
    # Load a whisper model and transcribe the audio
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("base")
    json_result = whisper.transcribe(model, audio, language="en")

    captions = []
    # Iterate through each segment in the JSON data
    for segment in json_result["segments"]:
        # Iterate through each word in the segment
        for word_info in segment["words"]:
            captions.append({
                "text": word_info["text"],
                "start": word_info["start"],
                "end": word_info["end"]
            })
    return captions