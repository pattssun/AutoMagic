from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips
from gtts import gTTS
import whisper_timestamped as whisper
import re

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

def crop_to_916(clip):
    """
    Crops a clip to a 9:16 aspect ratio.
    """
    original_width, original_height = clip.size
    target_aspect_ratio = 9.0 / 16.0
    # Calculate the target width to maintain a 9:16 aspect ratio based on the clip's height
    target_width = int(original_height * target_aspect_ratio)
    
    # Calculate the amount to crop from the sides to achieve the target width
    crop_amount_per_side = (original_width - target_width) / 2
    
    # Crop the clip
    cropped_clip = clip.crop(x1=crop_amount_per_side, y1=0, x2=original_width - crop_amount_per_side, y2=original_height)
    return cropped_clip

def text_to_speech(text, output_filename):
    """
    Converts text to an audio file using gTTS.
    """
    tts = gTTS(text)
    tts.save(output_filename)

def create_text_clip(text, start_time, end_time, fontsize=24, font='resources/fonts/Product Sans Regular.ttf', color='white'):
    """
    Creates a moviepy TextClip object for a given piece of text.
    """
    return TextClip(text, fontsize=fontsize, font=font, color=color, size=(800, 200)).set_position("center").set_start(start_time).set_end(end_time)

# DELETE ?????
def generate_captions(text, words_per_caption=1):
    """
    Splits a given text into chunks of a specified number of words.
    """
    words = re.split(r"[ ,.!+']+", text)
    captions = []
    
    # Iterate through words and chunk them into groups of `words_per_caption`
    for i in range(0, len(words), words_per_caption):
        caption = " ".join(words[i:i+words_per_caption])
        captions.append(caption)

    return captions

def assemble_video(title_text, body_text, background_video_path, output_filename):
    """
    Assembles the video from various components.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Create a clip for the title
    text_to_speech(title_text, "resources/audio_files/title_audio.mp3")
    title_audio = AudioFileClip("resources/audio_files/title_audio.mp3")
    title_clip = create_text_clip(title_text, 0, title_audio.duration).set_audio(title_audio)

    # Create continuous audio for the body
    text_to_speech(body_text, "resources/audio_files/body_audio.mp3")
    body_audio = AudioFileClip("resources/audio_files/body_audio.mp3")

    # DELETE ?????
    # Generate captions for the body text
    body_captions = generate_captions(body_text, words_per_caption=1)

    # Initialize list to hold all clips
    clips = [title_clip]

    # Calculate start and end times for each body caption chunk
    word_timings = extract_word_timings(result) 
    for caption in word_timings:
        start_time = caption['start'] + title_audio.duration
        end_time = caption['end'] + title_audio.duration
        text_clip = create_text_clip(caption['text'], start_time, end_time, fontsize=34)
        clips.append(text_clip)

    # Combine the title audio and body audio
    combined_audio = concatenate_audioclips([title_audio, body_audio])

    # Set the duration of the background clip to match the total duration
    background_clip = background_clip.set_duration(combined_audio.duration)

    # Combine all clips
    final_clip = CompositeVideoClip([background_clip] + clips, size=background_clip.size).set_audio(combined_audio)
    final_clip.write_videofile(output_filename, fps=24)

# Example usage
if __name__ == "__main__":
    title_text = "Finally, I got my first full-time offer"
    body_text = "After applying for almost 1000 SDE positions, I finally got an offer from Bambu Lab!!! This is a unicorn company that makes 3D printers, and I think it has great potential. Do you guys have any knowledge about their products? Some advice plz."
    assemble_video(title_text, body_text, "resources/background_videos/minecraft.mp4", "output/final_video.mp4")
    # print(generate_captions(body_text, words_per_caption=1))
