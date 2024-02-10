from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips, ImageClip, ColorClip
from src.video_processing import crop_to_916, create_text_clip_for_body
from src.audio_processing_xi import speed_up_mp3, text_to_speech, generate_captions

# Hardcoded Reddit banner
def assemble_video(title_text, body_text, background_video_path, banner_image_path, output_path):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Extract project name from output_path
    project_name = output_path.split("/")[-1].split(".")[0]

    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the title text to speech and speed it up
    normal_title_audio_path = f"resources/audio_files/normal/{project_name}_title_audio.mp3"
    faster_title_audio_path = f"resources/audio_files/faster/{project_name}_title_audio.mp3"
    text_to_speech(title_text, normal_title_audio_path) 
    speed_up_mp3(normal_title_audio_path, faster_title_audio_path, 1.25)
    title_audio = AudioFileClip(faster_title_audio_path)

    # Load the pre-rendered title image as a clip
    title_image_clip = ImageClip(banner_image_path).set_duration(title_audio.duration).set_audio(title_audio)

    # Create a 0.5 second silent audio clip and blank video clip for the pause
    pause_duration = 0.5
    pause_audio_clip = AudioFileClip("resources/audio_files/silence.mp3").subclip(0, pause_duration)
    pause_video_clip = ColorClip(size=title_image_clip.size, color=(0,0,0,0), duration=pause_duration).set_audio(pause_audio_clip)

    # Convert the body text to speech and speed it up
    normal_body_audio_path = f"resources/audio_files/normal/{project_name}_body_audio.mp3"
    faster_body_audio_path = f"resources/audio_files/faster/{project_name}_body_audio.mp3"
    text_to_speech(body_text, normal_body_audio_path) 
    speed_up_mp3(normal_body_audio_path, faster_body_audio_path, 1.25) 
    body_audio = AudioFileClip(faster_body_audio_path)

    # Initialize list to hold all video clips
    video_clips = [title_image_clip, pause_video_clip]

    # Initialize list to hold all audio clips
    audio_clips = [title_audio, pause_audio_clip]

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions(faster_body_audio_path)
    for caption in body_captions:
        start_time = caption['start'] + title_audio.duration + pause_duration
        end_time = caption['end'] + title_audio.duration + pause_duration
        text_clip = create_text_clip_for_body(caption['text'], start_time, end_time, clip_size=background_clip.size)
        video_clips.append(text_clip)

    # Combine the title audio and body audio
    combined_audio = concatenate_audioclips(audio_clips + [body_audio])

    # Set the duration of the background clip to match the total duration
    background_clip = background_clip.set_duration(combined_audio.duration)

    # Combine all clips into the final video
    final_clip = CompositeVideoClip([background_clip] + video_clips, size=background_clip.size).set_audio(combined_audio)
    final_clip.write_videofile(output_path, fps=60)

# Example usage
if __name__ == "__main__":
    title_text = "I destroyed a public bathroom and when I was running away, from the scene, I heard someone scream “oh my god” after they saw what I did."
    body_text = "I was abroad and had gotten extremely sick. I came home with black diarrhea (I think I had a parasite) and was throwing up. I had never shit so much."
    background_video_path = "resources/background_videos/minecraft.mp4"
    banner_image_path = "resources/static_files/reddit_banner.png"
    output_path = "output/minecraft.mp4"
    assemble_video(title_text, body_text, background_video_path, banner_image_path, output_path)