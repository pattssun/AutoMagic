import whisper_timestamped as whisper

audio = whisper.load_audio('resources/audio_files/body_audio.mp3')
model = whisper.load_model("base")
result = whisper.transcribe(model, audio, language="en")

def extract_word_timings(json_data):
    word_timings = []

    # Iterate through each segment in the JSON data
    for segment in json_data["segments"]:
        # Iterate through each word in the segment
        for word_info in segment["words"]:
            word_timings.append({
                "text": word_info["text"],
                "start": word_info["start"],
                "end": word_info["end"]
            })

    return word_timings

word_timings = extract_word_timings(result)
print(word_timings)