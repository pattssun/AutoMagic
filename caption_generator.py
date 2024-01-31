# def generate_captions(text, max_length=25):
#     """
#     Splits a given text into caption-sized chunks.
    
#     :param text: The text to be split into captions.
#     :param max_length: Maximum character length for each caption.
#     :return: A list of caption strings.
#     """
#     words = text.split()
#     captions = []
#     current_caption = ""

#     for word in words:
#         if len(current_caption) + len(word) + 1 <= max_length:
#             current_caption += " " + word
#         else:
#             captions.append(current_caption.strip())
#             current_caption = word

#     if current_caption:
#         captions.append(current_caption.strip())

#     return captions

# # Test the function
# body_captions = generate_captions("Your lengthy body text here that will be split into smaller chunks suitable for video captions.")
# print("Body Captions:", body_captions)

def generate_captions(text, words_per_caption=3):
    """
    Splits a given text into chunks of a specified number of words.
    
    :param text: The text to be split into captions.
    :param words_per_caption: Number of words per caption.
    :return: A list of caption strings.
    """
    words = text.split()
    captions = []
    
    # Iterate through words and chunk them into groups of `words_per_caption`
    for i in range(0, len(words), words_per_caption):
        caption = " ".join(words[i:i+words_per_caption])
        captions.append(caption)

    return captions

def generate_audio_for_each_caption(body_captions):
    """
    Generates separate audio files for each body caption.
    
    :param body_captions: A list of strings, where each string is a caption consisting of 3 words.
    :return: A list of filenames for the generated audio files.
    """
    audio_filenames = []
    for i, caption in enumerate(body_captions):
        output_filename = f"output/body_audio_{i}.mp3"
        text_to_speech(caption, output_filename)
        audio_filenames.append(output_filename)
    return audio_filenames
