import whisper_timestamped as whisper

def read_text_file(file_path):
    """
    Reads text from a file and removes all newline characters.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')
    return text

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

def transcribe_mp3(audio_path, output_path):
    """
    Transcribes an audio file and writes the text into a text file.
    """
    # Load a whisper model and transcribe the audio
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("base")
    json_result = whisper.transcribe(model, audio, language="en")

    # Write the transcribed text to a file
    with open(output_path, 'w', encoding='utf-8') as file:
        for segment in json_result["segments"]:
            for word in segment["words"]:
                file.write(word["text"] + " ")
            file.write("\n")

    return output_path

# Example usage
if __name__ == "__main__":
    transcribe_mp3("tiktok.mp3", "tiktok_test.txt")