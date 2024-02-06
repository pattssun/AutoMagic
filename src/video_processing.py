from moviepy.editor import TextClip

def crop_to_916(clip):
    """
    Crops a clip to a 9:16 aspect ratio.
    """
    original_width, original_height = clip.size
    target_aspect_ratio = 9.0 / 16.0
    # Calculate the target width to maintain a 9:16 aspect ratio based on the clip's height
    target_width = int(original_height * target_aspect_ratio)
    
    # Calculate the amount to crop from the sides to achieve the target width
    crop_amount_per_side = (original_width - target_width) / 2
    
    # Crop the clip
    cropped_clip = clip.crop(x1=crop_amount_per_side, y1=0, x2=original_width - crop_amount_per_side, y2=original_height)
    return cropped_clip

def create_text_clip(text, start_time, end_time, fontsize=24, font='resources/fonts/Product Sans Regular.ttf', color='white'):
    """
    Creates a moviepy TextClip object for a given piece of text.
    """
    return TextClip(text, fontsize=fontsize, font=font, color=color, size=(800, 200)).set_position("center").set_start(start_time).set_end(end_time)