from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_audioclips
from src.video_processing import crop_to_916, create_text_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech, generate_captions
import random

def read_text_file(file_path):
    """
    Reads text from a file and removes all newline characters.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ')
    return text

# Hardcoded Reddit banner
def assemble_video(project_name, voice, background_video_path, title_text, body_text, banner_image_path):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the title text to speech and speed it up
    normal_title_audio_path = f"resources/audio_files/normal/{project_name}_title_audio.mp3"
    faster_title_audio_path = f"resources/audio_files/faster/{project_name}_title_audio.mp3"
    # text_to_speech(title_text, voice, normal_title_audio_path) 
    speed_up_mp3(normal_title_audio_path, faster_title_audio_path, 1.15)
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
    # text_to_speech(body_text, voice, normal_body_audio_path) 
    speed_up_mp3(normal_body_audio_path, faster_body_audio_path, 1.15) 
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

    # Select a random start time for the background video
    # If the background video is longer than the total content duration, select a random start time
    if background_clip.duration > combined_audio.duration:
        max_start_time = background_clip.duration - combined_audio.duration
        start_time = random.uniform(0, max_start_time)
        end_time = start_time + combined_audio.duration
        background_clip = background_clip.subclip(start_time, end_time)
    else:
        # If the background clip is shorter or equal to the content duration, return error
        raise ValueError("Background video is shorter than the combined audio duration")

    # Combine all clips into the final video
    final_clip = CompositeVideoClip([background_clip] + video_clips, size=background_clip.size).set_audio(combined_audio)
    final_clip.write_videofile(f"output/{project_name}.mp4", fps=60, audio_codec='aac')

# Example usage
if __name__ == "__main__":
    project_name = "post3" # Change this to the name of the project
    voice = "Harry" # Change this to the desired voice
    background_video_path = "resources/background_videos/minecraft2.mp4" # Change this to the path of the background video

    title_text = read_text_file(f"resources/text_files/{project_name}/title_text.txt")
    body_text = read_text_file(f"resources/text_files/{project_name}/body_text.txt")
    banner_image_path = f"resources/banners/{project_name}.png"
    assemble_video(project_name, voice, background_video_path, title_text, body_text, banner_image_path)