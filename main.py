from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
import os
from src.audio_generation.text_to_speech import text_to_speech
from src.video_processing.caption_generator import generate_captions

def create_text_clip(text, duration, fontsize=24, pos='center'):
    """
    Creates a moviepy TextClip object for a given piece of text.

    :param text: The text to be displayed.
    :param duration: Duration for which the text will be displayed.
    :param fontsize: Font size of the text.
    :param pos: Position of the text in the clip.
    :return: A TextClip object.
    """
    return TextClip(text, fontsize=fontsize, color='white', size=(800, 200), method='caption').set_duration(duration)

def assemble_video(title_text, body_captions, background_video_path, output_filename):
    """
    Assembles the video from various components.

    :param title_text: The title text.
    :param body_captions: List of body text captions.
    :param background_video_path: Path to the background video.
    :param output_filename: Filename for the output video.
    """
    # Load the background video
    background_clip = VideoFileClip(background_video_path)

    # Create a clip for the title
    title_audio = AudioFileClip("output/title_audio.mp3")
    title_clip = create_text_clip(title_text, duration=title_audio.duration).set_start(0)
    title_clip = title_clip.set_audio(title_audio.set_start(0))

    # Initialize list to hold all clips
    clips = [title_clip]

    # Accumulate total duration
    total_duration = title_audio.duration

    # Create clips for each body caption
    for i, caption in enumerate(body_captions):
        audio_clip = AudioFileClip(f"output/body_audio_{i}.mp3")
        text_clip = create_text_clip(caption, duration=audio_clip.duration).set_start(total_duration)
        text_clip = text_clip.set_audio(audio_clip.set_start(total_duration))
        clips.append(text_clip)
        total_duration += audio_clip.duration

    # Set the duration of the background clip to match the total duration
    background_clip = background_clip.set_duration(total_duration)

    # Combine all clips
    final_clip = CompositeVideoClip([background_clip] + clips, size=background_clip.size)
    final_clip.write_videofile(output_filename, fps=24)

# Example usage
if __name__ == "__main__":
    title_text = "Your Title Text Here"
    body_text = "Your lengthy body text here that will be split into smaller chunks suitable for video captions."
    body_captions = generate_captions(body_text)
    assemble_video(title_text, body_captions, "resources/background_videos/minecraft.mp4", "output/final_video.mp4")