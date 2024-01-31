from gtts import gTTS

def text_to_speech(text, output_filename):
    """
    Converts text to an audio file using gTTS.

    :param text: The text to be converted to speech.
    :param output_filename: The filename for the output audio file.
    """
    tts = gTTS(text)
    tts.save(output_filename)

