def generate_captions(text, max_length=20):
    """
    Splits a given text into caption-sized chunks.
    
    :param text: The text to be split into captions.
    :param max_length: Maximum character length for each caption.
    :return: A list of caption strings.
    """
    words = text.split()
    captions = []
    current_caption = ""

    for word in words:
        if len(current_caption) + len(word) + 1 <= max_length:
            current_caption += " " + word
        else:
            captions.append(current_caption.strip())
            current_caption = word

    if current_caption:
        captions.append(current_caption.strip())

    return captions

# Test the function
body_captions = generate_captions("Your lengthy body text here that will be split into smaller chunks suitable for video captions.")
print("Body Captions:", body_captions)