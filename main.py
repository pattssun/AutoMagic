from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips
from gtts import gTTS
import re

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

def generate_captions(text, words_per_caption=3):
    """
    Splits a given text into chunks of a specified number of words.
    """
    words = text.split()
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

    # Generate captions for the body text, assuming 3 words per caption
    body_captions = generate_captions(body_text, words_per_caption=3)

    # Initialize list to hold all clips
    clips = [title_clip]

    # Calculate start and end times for each body caption chunk
    start_time = title_audio.duration
    for caption in body_captions:
        caption_duration = body_audio.duration / len(body_captions)
        end_time = start_time + caption_duration
        text_clip = create_text_clip(caption, start_time, end_time, fontsize=34)
        clips.append(text_clip)
        start_time = end_time

    # Combine the title audio and body audio
    combined_audio = concatenate_audioclips([title_audio, body_audio])

    # Set the duration of the background clip to match the total duration
    background_clip = background_clip.set_duration(combined_audio.duration)

    # Combine all clips
    final_clip = CompositeVideoClip([background_clip] + clips, size=background_clip.size).set_audio(combined_audio)
    final_clip.write_videofile(output_filename, fps=24)

# Example usage
if __name__ == "__main__":
    title_text = "I’ve stolen countless bottles of liquor from my parents"
    body_text = "Im 18 years old, and have always been that studious, rule following daughter my parents expected me to be. A while ago, my parents bought a new house, and we are still in the process of moving. My parents and brothers live in the new house, and I remained in the old. After a month of temporarily living alone, I had a random urge to see if they left their alcohol in the alcohol cabinet. To my surprise I ended up giving into the urge of wanting to experience what being drunk was like that same night. A week later, I did it again, and the cycle started. All my friends had moved away to university, and they were getting drunk too. I felt like I was just being a typical teenager because of that."
    assemble_video(title_text, body_text, "resources/background_videos/minecraft.mp4", "output/final_video.mp4")