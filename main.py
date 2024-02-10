from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips, ImageClip, ColorClip
from src.video_processing import crop_to_916, create_text_clip_for_body, create_text_clip_for_title
from src.audio_processing_xi import speed_up_mp3, text_to_speech, generate_captions

# def assemble_video(title_text, body_text, background_video_path, output_filename):
#     """
#     Assembles the video from various components.
#     """
#     # Load the background video and crop to a 9:16 aspect ratio
#     background_clip = crop_to_916(VideoFileClip(background_video_path))

#     # Create a clip for the title
#     text_to_speech(title_text, "resources/audio_files/title_audio.mp3")
#     title_audio = AudioFileClip("resources/audio_files/title_audio.mp3")
#     title_clip = create_text_clip_for_title(title_text, start_time=0, end_time=title_audio.duration, clip_size=background_clip.size).set_audio(title_audio)

#     # Create continuous audio for the body
#     text_to_speech(body_text, "resources/audio_files/body_audio.mp3")
#     body_audio = AudioFileClip("resources/audio_files/body_audio.mp3")

#     # Initialize list to hold all clips
#     clips = [title_clip]

#     # Calculate start and end times for each body caption chunk
#     body_captions = generate_captions('resources/audio_files/body_audio.mp3') 
#     for caption in body_captions:
#         start_time = caption['start'] + title_audio.duration
#         end_time = caption['end'] + title_audio.duration
#         text_clip = create_text_clip_for_body(caption['text'], start_time, end_time, clip_size=background_clip.size)
#         clips.append(text_clip)

#     # Combine the title audio and body audio
#     combined_audio = concatenate_audioclips([title_audio, body_audio])

#     # Set the duration of the background clip to match the total duration
#     background_clip = background_clip.set_duration(combined_audio.duration)

#     # Combine all clips
#     final_clip = CompositeVideoClip([background_clip] + clips, size=background_clip.size).set_audio(combined_audio)
#     final_clip.write_videofile(output_filename, fps=24)

# # Example usage
# if __name__ == "__main__":
#     title_text = "Finally, I got my first full-time offer"
#     body_text = "After applying for almost 1000+ SDE positions, I finally got an offer from Bambu Lab!!! This is a unicorn company that makes 3D printers, and I think it has great potential. Do you guys have any knowledge about their products? Some advice plz."
#     assemble_video(title_text, body_text, "resources/background_videos/minecraft.mp4", "output/final_video.mp4")

# Hardcoded Reddit banner
def assemble_video(title_text, body_text, background_video_path, title_image_path, output_filename):
    """
    Assembles the video from various components, using a pre-rendered image for the title and narrating the title text.
    """
    # Load the background video and crop to a 9:16 aspect ratio
    background_clip = crop_to_916(VideoFileClip(background_video_path))

    # Convert the title text to speech and speed it up
    text_to_speech(title_text, "resources/audio_files/title_audio.mp3") # Un-comment when shipping!!!!!!!!
    speed_up_mp3("resources/audio_files/title_audio.mp3", "resources/audio_files/title_audio_faster.mp3", 1.25) # Un-comment when shipping!!!!!!!!
    title_audio = AudioFileClip("resources/audio_files/title_audio_faster.mp3")

    # Load the pre-rendered title image as a clip
    title_image_clip = ImageClip(title_image_path).set_duration(title_audio.duration).set_audio(title_audio)

    # Create a 0.5 second silent audio clip and blank video clip for the pause
    pause_duration = 0.5
    pause_audio_clip = AudioFileClip("resources/audio_files/silence.mp3").subclip(0, pause_duration)
    pause_video_clip = ColorClip(size=title_image_clip.size, color=(0,0,0,0), duration=pause_duration).set_audio(pause_audio_clip)

    # Convert the body text to speech and speed it up
    text_to_speech(body_text, "resources/audio_files/body_audio.mp3") # Un-comment when shipping!!!!!!!!
    speed_up_mp3("resources/audio_files/body_audio.mp3", "resources/audio_files/body_audio_faster.mp3", 1.25) # Un-comment when shipping!!!!!!!!
    body_audio = AudioFileClip("resources/audio_files/body_audio_faster.mp3")

    # Initialize list to hold all video clips
    video_clips = [title_image_clip, pause_video_clip]

    # Initialize list to hold all audio clips
    audio_clips = [title_audio, pause_audio_clip]

    # Calculate start and end times for each body caption chunk
    body_captions = generate_captions('resources/audio_files/body_audio_faster.mp3')
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
    final_clip.write_videofile(output_filename, fps=60)

# Example usage
if __name__ == "__main__":
    title_text = "I destroyed a public bathroom and when I was running away, from the scene, I heard someone scream “oh my god” after they saw what I did."
    body_text = "I was abroad and had gotten extremely sick. I came home with black diarrhea (I think I had a parasite) and was throwing up. While I was driving, I had to stop at a gas station to relieve myself. I had never shit so much. I literally covered the entire toilet with shit, it was on the floor, on the wall, and all over the seat. I was so ashamed of myself I didn’t know what to do, so I ran. When I was leaving, I heard someone scream. I think it was the gas station employee. I feel bad as the gas station employee had to clean up my mess. That is my confession. I also confess that I don’t want my boyfriend to see this as he would be disgusted with me"
    assemble_video(title_text, body_text, "resources/background_videos/gta.mp4", "resources/static_files/reddit_banner.png", "output/final_video_hardcoded_gta.mp4")