from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, concatenate_audioclips
from src.video_processing import crop_to_916, create_text_clip_for_body, create_image_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech
from src.text_processing import read_text_file, read_text_file_by_line, generate_captions
from src.image_processing import generate_all_image_queries, retrieve_pixabay_images
import random
from datetime import datetime
import os
import re

def assemble_video(project_name, background_video_path, body_text_path):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    body_text = read_text_file(body_text_path)
    body_text_chunks = read_text_file_by_line(body_text_path)

    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the body text to speech and speed it up
    normal_path = f"{project_name}_normal.mp3"
    faster_path = f"{project_name}_faster.mp3"
    text_to_speech(body_text, f"test/{normal_path}") 
    speed_up_mp3(f"test/{normal_path}", f"test/{faster_path}", 1.15) 
    body_audio = AudioFileClip(f"test/{faster_path}")

    # Initialize list to hold all video clips
    video_clips = []

    # Initialize list to hold all audio clips
    audio_clips = []

    # Generate image queries for the body text
    queries = generate_all_image_queries(body_text_chunks)

    # Retrieve images for the image queries
    images = retrieve_pixabay_images(queries)

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions(f"test/{faster_path}")

    # Generate text clips for the body captions
    caption_images = []
    for caption in body_captions:
        caption_text = caption['text']
        start_time = caption['start'] 
        end_time = caption['end']
        text_clip = create_text_clip_for_body(caption_text, start_time, end_time, clip_size=background_clip.size)
        video_clips.append(text_clip)
        # Pre-process captions to map them directly to images
        for image in images:
            # If the keyword is in the caption text and the image has a path, add it to the list
            if image['keyword'] in caption_text and 'image_path' in image and image['image_path']:
                caption_images.append({
                    'start': start_time,
                    'end': end_time,
                    'text': caption_text,
                    'image_path': image['image_path']
                })
                break  # Stop after finding the first matching image

    # Generate image clips 
    last_image_end = 0
    for i, caption_image in enumerate(caption_images):
        # Set the start time to 0 if it's the first item; otherwise, use the last image end
        start_time = body_captions[0]['start'] if i == 0 else last_image_end
        # If this isn't the last item, set the end time to the start of the next item; otherwise, use the caption end
        end_time = caption_images[i + 1]['start'] if i + 1 < len(caption_images) else caption_image['end']
        last_image_end = max(last_image_end, end_time)  # Update the last image end time
        # Create the image clip
        image_clip = create_image_clip_for_body(start_time, last_image_end, clip_size=background_clip.size, image_path=caption_image['image_path'])
        video_clips.append(image_clip)

    # Ensure clips are sorted by start time as adding them out of order can cause issues
    video_clips.sort(key=lambda clip: clip.start)

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
    final_clip = CompositeVideoClip([background_clip] + video_clips, size=background_clip.size).set_audio(combined_audio).set_duration(combined_audio.duration)
    final_clip.write_videofile(f"test/{project_name}_final.mp4", fps=60, audio_codec='aac')

    # Remove all files in test/pixabay
    for file in os.listdir("test/pixabay"):
        os.remove(f"test/pixabay/{file}")

# Testing
if __name__ == "__main__":
    project_name = "tiktok"
    background_video_path = "resources/background_videos/minecraft.mp4"
    body_text_path = f"test/{project_name}.txt"
    assemble_video(project_name, background_video_path, body_text_path)
