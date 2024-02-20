from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, concatenate_audioclips
from src.video_processing import crop_to_916, create_text_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech
from src.text_processing import read_text_file, generate_captions
import random
from datetime import datetime
import os

def assemble_video(project_name, voice, background_video_path, body_text):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the body text to speech and speed it up
    normal_body_audio_path = f"resources/audio_files/normal/{project_name} (body_audio.mp3)"
    faster_body_audio_path = f"resources/audio_files/faster/{project_name} (body_audio.mp3)"
    if project_name != "TEST":
        text_to_speech(body_text, voice, normal_body_audio_path) 
        speed_up_mp3(normal_body_audio_path, faster_body_audio_path, 1.15) 
    body_audio = AudioFileClip(faster_body_audio_path)

    # Initialize list to hold all video clips
    video_clips = []

    # Initialize list to hold all audio clips
    audio_clips = []

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions(faster_body_audio_path)
    for caption in body_captions:
        start_time = caption['start'] 
        end_time = caption['end']
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
        os.remove(normal_body_audio_path)
        os.remove(faster_body_audio_path)

# Testing
if __name__ == "__main__":
    voice = "Liam" 
    background_video_path = "resources/background_videos/trackmania.mp4"
    project_name = f"TEST" 
    body_text = read_text_file("tiktok_test copy.txt")
    assemble_video(project_name, voice, background_video_path, body_text)
