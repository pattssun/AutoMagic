from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
from src.video_processing import crop_to_916, create_text_clip_for_body, create_image_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech
from src.text_processing import read_text_file, read_text_file_by_line, generate_captions
from src.image_processing import generate_all_image_queries, retrieve_pixabay_images
import random
from datetime import datetime
import os
import re

def assemble_video(project_name, text_path, background_video_path, voices):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Time total execution of the function
    start_time = datetime.now()

    # Load the text and split it into chunks
    text = read_text_file(text_path)
    text_chunks = read_text_file_by_line(text_path)
    print("(1) text_chunks: Completed.\n")

    # Generate audio chunks for the text chunks and combine them into a single audio file
    audio_filename = f"{project_name}_normal.mp3"
    # audio_chunks = text_to_speech(text_chunks, voices, output_filename=audio_filename)
    audio_chunks = [{'voice_id': 'F7GmQe0BY7nlHiDzHStR', 'audio_path': 'test/audio_files/0.mp3', 'start': 0.0, 'end': 4.859}, {'voice_id': '8ywemhKnE8RrczyytVz1', 'audio_path': 'test/audio_files/1.mp3', 'start': 4.859, 'end': 6.296}, {'voice_id': 'F7GmQe0BY7nlHiDzHStR', 'audio_path': 'test/audio_files/2.mp3', 'start': 6.296, 'end': 12.174}]
    audio_full = AudioFileClip(f"test/audio_files/{audio_filename}")
    print("(2) audio_chunks and audio_full: Completed.\n")

    # Calculate start and end times for each caption chunk
    captions = generate_captions(f"test/audio_files/{audio_filename}")
    print("(3) captions: Completed.\n")

    # Generate image queries for the text
    queries = generate_all_image_queries(text_chunks)
    print("(4) queries: Completed.\n")

    # Retrieve images for the image queries
    images = retrieve_pixabay_images(queries)
    print("(5) images: Completed.\n")

    # Initialize lists to hold all video clips
    video_clips = []

    # Generate text clips for the captions
    matched_images = []
    for caption in captions:
        caption_text = caption['text']
        start_time = caption['start'] 
        end_time = caption['end']
        text_clip = create_text_clip_for_body(caption_text, start_time, end_time, clip_size=(1080, 1920))
        video_clips.append(text_clip)
        # Add timestamps to images that match the caption
        for image in images:
            # If the keyword is in the caption text and the image has a path, add it to the list
            if image['keyword'] in caption_text and 'image_path' in image and image['image_path']:
                matched_images.append({
                    'start': start_time,
                    'end': end_time,
                    'text': caption_text,
                    'image_path': image['image_path']
                })
                break  # Stop after finding the first matching image  

    # Generate image clips 
    last_image_end = 0
    for i, caption_image in enumerate(matched_images):
        # Set the start time to 0 if it's the first item; otherwise, use the last image end
        start_time = captions[0]['start'] if i == 0 else last_image_end
        # If this isn't the last item, set the end time to the start of the next item; otherwise, use the caption end
        end_time = matched_images[i + 1]['start'] if i + 1 < len(matched_images) else caption_image['end']
        # If this is the last item, set the end time to the caption end
        end_time = captions[-1]['end'] if i + 1 == len(matched_images) else end_time
        # Update the last image end time
        last_image_end = max(last_image_end, end_time)  
        # Create the image clip
        image_clip = create_image_clip_for_body(start_time, last_image_end, clip_size=(1080, 1920), image_path=caption_image['image_path'])
        video_clips.append(image_clip)

    # Ensure clips are sorted by start time as adding them out of order can cause issues
    video_clips.sort(key=lambda clip: clip.start)

    # Add character image clips to the video
    for i, audio_chunk in enumerate(audio_chunks):
        # Alternate between Rick and Morty 
        start_time = audio_chunk['start']
        end_time = audio_chunk['end']
        image_path = "test/Rick.png" if audio_chunk["voice_id"] == voices["rick"] else "test/Morty.png"
        image_clip = ImageClip(image_path).set_duration(end_time - start_time).set_start(start_time).set_position(('center', 'bottom'))
        video_clips.append(image_clip)
    print("(6) video_clips: Completed.\n")

    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Select a random start time for the background video
    if background_clip.duration > audio_full.duration:
        max_start_time = background_clip.duration - audio_full.duration
        start_time = random.uniform(0, max_start_time)
        end_time = start_time + audio_full.duration
        background_clip = background_clip.subclip(start_time, end_time)
    else:
        # If the background clip is shorter or equal to the content duration, return error
        raise ValueError("Background video is shorter than the combined audio duration")

    # Combine all clips into the final video
    final_clip = CompositeVideoClip([background_clip] + video_clips, size=((1080, 1920))).set_audio(audio_full).set_duration(audio_full.duration)
    final_clip.write_videofile(f"test/{project_name}_final2.mp4", fps=60, audio_codec='aac')

    # Remove all files in test/image_files
    for file in os.listdir("test/image_files"):
        os.remove(f"test/image_files/{file}")

    # Time total execution of the function
    end_time = datetime.now()
    print(f"Execution time: {end_time - start_time}")

# Testing
if __name__ == "__main__":
    project_name = "tiktok_sample"
    text_path = f"test/text_files/{project_name}.txt"
    background_video_path = "resources/background_videos/minecraft.mp4"
    voices = {"rick":"F7GmQe0BY7nlHiDzHStR", "morty":"8ywemhKnE8RrczyytVz1"}
    assemble_video(project_name, text_path, background_video_path, voices)
