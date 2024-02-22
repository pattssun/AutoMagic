from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, concatenate_audioclips
from src.video_processing import crop_to_916, create_text_clip_for_body, create_image_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech
from src.text_processing import read_text_file, generate_captions
from src.image_processing import generate_image_queries, retrieve_pixabay_images
import random
from datetime import datetime
import os

def assemble_video(background_video_path, body_text):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the body text to speech and speed it up
    # text_to_speech(body_text, "test/tiktok_normal.mp3") 
    # speed_up_mp3("test/tiktok_normal.mp3", "test/tiktok_faster.mp3", 1.15) 
    body_audio = AudioFileClip("test/tiktok_faster.mp3")

    # Initialize list to hold all video clips
    video_clips = []

    # Initialize list to hold all audio clips
    audio_clips = []

    # Generate image queries for the body text
    queries = generate_image_queries(body_text)

    # Retrieve images for the image queries
    images = retrieve_pixabay_images(queries)

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions("test/tiktok_faster.mp3")
    for caption in body_captions:
        caption_text = caption['text']
        start_time = caption['start'] 
        end_time = caption['end']
        text_clip = create_text_clip_for_body(caption['text'], start_time, end_time, clip_size=background_clip.size)
        # Match each keyword in images with the caption text
        for image in images:
            if any(word in caption_text.split() for word in image['keyword'].split()):
                image_clip = create_image_clip_for_body(start_time, end_time, clip_size=background_clip.size, image_path=image['image_path'])
                video_clips.append(image_clip)
                break  # Stop after the first match to prevent overwriting
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
    final_clip.write_videofile(f"test/tiktok_final.mp4", fps=60, audio_codec='aac')

    for caption in body_captions:
            print(caption)

    print()

    for image in images:
        print(image)

# Testing
if __name__ == "__main__":
    background_video_path = "resources/background_videos/minecraft2.mp4"
    body_text = read_text_file("test/tiktok.txt")
    assemble_video(background_video_path, body_text)
