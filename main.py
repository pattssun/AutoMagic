from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips
from src.video_processing import crop_to_916, create_text_clip
from src.audio_processing import text_to_speech, generate_captions

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

    # Initialize list to hold all clips
    clips = [title_clip]

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions('resources/audio_files/body_audio.mp3') 
    for caption in body_captions:
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
    body_text = "After applying for almost 1000+ SDE positions, I finally got an offer from Bambu Lab!!! This is a unicorn company that makes 3D printers, and I think it has great potential. Do you guys have any knowledge about their products? Some advice plz."
    assemble_video(title_text, body_text, "resources/background_videos/minecraft.mp4", "output/final_video.mp4")
