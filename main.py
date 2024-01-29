from src.audio_generation.text_to_speech import text_to_speech
from src.video_processing.caption_generator import generate_captions

# Example usage
title_text = "Your Title Text Here"
body_text = "Your lengthy body text here that will be split into smaller chunks suitable for video captions."

# Convert title text to speech
text_to_speech(title_text, "output/title_audio.mp3")

# Convert body text to speech (for each chunk)
body_captions = generate_captions(body_text)
for i, caption in enumerate(body_captions):
    text_to_speech(caption, f"output/body_audio_{i}.mp3")

