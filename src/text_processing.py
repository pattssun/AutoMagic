import whisper_timestamped as whisper

def read_text_file(file_path):
    """
    Reads text from a file and removes all newline characters.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')
    return text

def read_text_file_by_line(file_path):
    """
    Reads text from a file and returns a list of lines.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
    return lines

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
    # Transcribe an audio file
    audio_path = "projects/2024-03-26/3/Snaptik.app_7332859583280680238.mp3"
    output_path = "projects/2024-03-26/3/text_file.txt"
    transcribe_mp3(audio_path, output_path)