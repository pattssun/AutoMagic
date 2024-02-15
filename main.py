from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, concatenate_audioclips
from video_processing import crop_to_916, create_text_clip_for_body, create_text_clip_for_title
from audio_processing import speed_up_mp3, text_to_speech
from text_processing import read_text_file, generate_captions
import random
from datetime import datetime
import os

# Hardcoded Reddit banner
def assemble_video(project_name, voice, background_video_path, title_text, body_text):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the title text to speech and speed it up
    normal_title_audio_path = f"resources/audio_files/normal/{project_name} (title_audio.mp3)"
    faster_title_audio_path = f"resources/audio_files/faster/{project_name} (title_audio.mp3)"
    if project_name != "TEST":
        text_to_speech(title_text, voice, normal_title_audio_path) 
        speed_up_mp3(normal_title_audio_path, faster_title_audio_path, 1.15)
    title_audio = AudioFileClip(faster_title_audio_path)

    # Create a text clip for the title
    title_clip = create_text_clip_for_title(title_text, 0, title_audio.duration, clip_size=background_clip.size)
    
    # Create a 0.5 second silent audio clip and blank video clip for the pause
    pause_duration = 0.5
    pause_audio_clip = AudioFileClip("resources/audio_files/silence.mp3").subclip(0, pause_duration)
    pause_video_clip = ColorClip(size=title_clip.size, color=(0,0,0,0), duration=pause_duration).set_audio(pause_audio_clip)

    # Convert the body text to speech and speed it up
    normal_body_audio_path = f"resources/audio_files/normal/{project_name} (body_audio.mp3)"
    faster_body_audio_path = f"resources/audio_files/faster/{project_name} (body_audio.mp3)"
    if project_name != "TEST":
        text_to_speech(body_text, voice, normal_body_audio_path) 
        speed_up_mp3(normal_body_audio_path, faster_body_audio_path, 1.15) 
    body_audio = AudioFileClip(faster_body_audio_path)

    # Initialize list to hold all video clips
    video_clips = [title_clip, pause_video_clip]

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

    # Remove audio files
    if project_name != "TEST":
        os.remove(normal_title_audio_path)
        os.remove(faster_title_audio_path)
        os.remove(normal_body_audio_path)
        os.remove(faster_body_audio_path)

# Production
if __name__ == "__main__":
    voice = "Liam" 
    background_video_path = "resources/background_videos/minecraft2.mp4" 
    today_date = datetime.today().strftime('%Y-%m-%d') # Get today's date
    # Assemble the video for each post in today's text_files directory
    for i in [1,2,3]:
        project_name = f"{today_date}-post{i}" 
        title_text = read_text_file(f"resources/text_files/{today_date}/post{i}/title_text.txt")
        body_text = read_text_file(f"resources/text_files/{today_date}/post{i}/body_text.txt")
        assemble_video(project_name, voice, background_video_path, title_text, body_text)

# # Testing
# if __name__ == "__main__":
#     voice = "Liam" 
#     background_video_path = "resources/background_videos/trackmania.mp4"
#     project_name = f"TEST" 
#     title_text = read_text_file(f"resources/text_files/{project_name}/title_text.txt")
#     body_text = read_text_file(f"resources/text_files/{project_name}/body_text.txt")
#     assemble_video(project_name, voice, background_video_path, title_text, body_text)

"""
Current workflow:
1. Import 3 Reddit posts in text_files
2. Download ouput videos
3. Select TikTok song
4. Input TikTok description
5. Upload to TikTok
"""          