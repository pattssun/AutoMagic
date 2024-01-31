from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips
from text_to_speech import text_to_speech
from caption_generator import generate_captions

def create_text_clip(text, start_time, end_time, fontsize=24, font='resources/fonts/Product Sans Regular.ttf', color='white'):
    """
    Creates a moviepy TextClip object for a given piece of text.
    
    :param text: The text to be displayed.
    :param start_time: Start time for the text clip.
    :param end_time: End time for the text clip.
    :param fontsize: Font size of the text.
    :param font: Font used for the text.
    :param color: Color of the text.
    :return: A TextClip object.
    """
    return TextClip(text, fontsize=fontsize, font=font, color=color, size=(800, 200)).set_position("center").set_start(start_time).set_end(end_time)

def assemble_video(title_text, body_text, background_video_path, output_filename):
    """
    Assembles the video from various components.

    :param title_text: The title text.
    :param body_text: The entire body text.
    :param body_captions: List of body text captions.
    :param background_video_path: Path to the background video.
    :param output_filename: Filename for the output video.
    """
    # Load the background video
    background_clip = VideoFileClip(background_video_path)

    # Generate audio for title and body text
    text_to_speech(title_text, "output/title_audio.mp3")
    text_to_speech(body_text, "output/body_audio.mp3")

    # Create a clip for the title
    title_audio = AudioFileClip("output/title_audio.mp3")
    title_clip = create_text_clip(title_text, 0, title_audio.duration).set_audio(title_audio)

    # Create continuous audio for the body
    body_audio = AudioFileClip("output/body_audio.mp3")

    # Chunk the body text into captions
    body_captions = generate_captions(body_text)

    # Initialize list to hold all clips
    clips = [title_clip]

    # Calculate start and end times for each caption
    start_time = title_audio.duration
    for caption in body_captions:
        caption_duration = body_audio.duration / len(body_captions)
        end_time = start_time + caption_duration
        text_clip = create_text_clip(caption, start_time, end_time)
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