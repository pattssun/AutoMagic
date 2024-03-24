from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
from src.video_processing import crop_to_916, create_text_clip_for_body, create_image_clip_for_body
from src.audio_processing import speed_up_mp3, text_to_speech
from src.text_processing import read_text_file, read_text_file_by_line, generate_captions
from src.image_processing import generate_all_image_queries, retrieve_pixabay_images
import random
from datetime import datetime
import os
import re

def assemble_video(today_date, accounts, background_video_path, text_path):
    """
    Assembles the video from various components.
    """
    # Time total execution of the function
    start_time = datetime.now()

    # Get the current text file directory
    current_text_file_dir = text_path.split('/')[2]
    # Verify that current_text_file_dir is a number between 1-3
    if not re.match(r'^[1-3]$', current_text_file_dir):
        raise ValueError("The current_text_file_dir is not a number between 1-3")

    # Load the text and split it into chunks
    text = read_text_file(text_path)
    text_chunks = read_text_file_by_line(text_path)
    print(f"text_chunks for {current_text_file_dir}: Completed.\n")

    # Generate image queries for the text
    queries = generate_all_image_queries(text_chunks)
    print(f"queries for {current_text_file_dir}: Completed.\n")

    # Retrieve images for the image queries
    images = retrieve_pixabay_images(queries, dir_path=f"projects/{today_date}/{current_text_file_dir}/image_files")
    print(f"images for {current_text_file_dir}: Completed.\n")

    # Generate audio chunks for the text chunks and combine them into a single audio file
    character_voice_ids = []
    character_image_paths = []
    for i, account in enumerate(accounts):
        characters = accounts[account]
        for i, character in enumerate(characters):
            character_voice_ids.append(accounts[account][character]["voice_id"])
            character_image_paths.append(accounts[account][character]["image_path"])

        audio_path = f"projects/{today_date}/{current_text_file_dir}/{account}/audio.mp3"
        audio_chunks = text_to_speech(text_chunks, character_voice_ids, output_path=audio_path)
        audio_full = AudioFileClip(audio_path)
        print(f"audio_chunks and audio_full for {current_text_file_dir} - {account}: Completed.\n")

        # Calculate start and end times for each caption chunk
        captions = generate_captions(audio_path)
        print(f"captions for {current_text_file_dir} - {account}: Completed.\n")

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
            image_path = character_image_paths[0] if audio_chunk["voice_id"] == character_voice_ids[0] else character_image_paths[1]
            image_clip = ImageClip(image_path).set_duration(end_time - start_time).set_start(start_time).set_position(('center', 'bottom'))
            video_clips.append(image_clip)
        print(f"video_clips for {current_text_file_dir} - {account}: Completed.\n")

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
        final_clip.write_videofile(f"projects/{today_date}/{current_text_file_dir}/output/{account}.mp4", fps=60, audio_codec='aac')

        # # Remove all files in image_files
        # for file in os.listdir(f"projects/{today_date}/{current_text_file_dir}/image_files"):
        #     os.remove(f"projects/{today_date}/{current_text_file_dir}/image_files/{file}")

        # # Remove all files in audio_files
        # for file in os.listdir(f"projects/{today_date}/{current_text_file_dir}/{account}"):
        #     os.remove(f"projects/{today_date}/{current_text_file_dir}/{account}/{file}")

        # Time total execution of the function
        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"Execution time for {current_text_file_dir} - {account}: {execution_time}")

# Testing
if __name__ == "__main__":
    today_date = datetime.today().strftime('%Y-%m-%d')
    accounts = {
        "account1": {
            "ricky": {
                "voice_id": "F7GmQe0BY7nlHiDzHStR",
                "image_path": "resources/character_images/rick.png"
            },
            "morty": {
                "voice_id": "8ywemhKnE8RrczyytVz1",
                "image_path": "resources/character_images/morty.png"
            }
        },
        "account2": {
            "spongebob": {
                "voice_id": "k2kyIOkVvjmBBY9jw4PR",
                "image_path": "resources/character_images/spongebob.png"
            },
            "patrick": {
                "voice_id": "MIrTQN3cNhi4BPBOIEMH",
                "image_path": "resources/character_images/patrick.png"
            }
        },
        "account3": {
            "peter": {
                "voice_id": "ZxjQmbC520BZfHkeKd1l",
                "image_path": "resources/character_images/peter.png"
            },
            "stewie": {
                "voice_id": "jYLjZign3GxODGd9N9AQ",
                "image_path": "resources/character_images/stewie.png"
            }
        }
    }
    background_video_path = "resources/background_videos/minecraft.mp4"
    for dir in os.listdir(f"projects/{today_date}"):
        for file in os.listdir(f"projects/{today_date}/{dir}"):
            if file.endswith(".txt"):
                text_path = f"projects/{today_date}/{dir}/{file}"
                print(f"Video assembly for {today_date}/{dir}: Started.")
                assemble_video(today_date, accounts, background_video_path, text_path)
                print(f"Video assembly for {today_date}/{dir}: Completed.\n")

