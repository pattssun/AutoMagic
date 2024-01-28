from banner_creation import create_banner
from caption_generation import generate_captions
from audio_narration import create_audio_narration
from video_processing import process_video

def get_user_input():
    title_text = input("Enter the title text: ")
    body_text = input("Enter the body text: ")
    return title_text, body_text

def main():
    # Step 1: Get user input (title and body text)
    title_text, body_text = get_user_input()

    # Step 2: Create banner
    banner_image = create_banner(title_text)

    # Step 3: Generate captions
    captions = generate_captions(body_text)

    # Step 4: Create audio narration
    audio_file = create_audio_narration(title_text, body_text)

    # Step 5: Process and export video
    process_video(banner_image, captions, audio_file)

if __name__ == "__main__":
    main()
