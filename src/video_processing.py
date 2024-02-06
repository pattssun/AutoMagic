from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, ImageClip

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

def create_text_clip_for_body(text, start_time, end_time, fontsize=24, font='Arial', color='white'):
    """
    Creates a moviepy TextClip object for a given piece of text.
    """
    return TextClip(text, fontsize=fontsize, font=font, color=color, size=(800, 200)).set_position("center").set_start(start_time).set_end(end_time)

# def create_text_clip_for_title(text, start_time, end_time, fontsize=24, font='Arial', color='black', bg_color=(255, 255, 255)):
#     """
#     Creates a moviepy TextClip object for a given piece of text with a dynamic background.
#     """
#     # Create a TextClip for the text
#     text_clip = TextClip(text, fontsize=fontsize, font=font, color=color)

#     # Calculate text size to determine background size
#     text_width, text_height = text_clip.size
#     bg_height = text_height
#     bg_width = 780  # Fixed width

#     # Create a background ColorClip
#     background_clip = ColorClip(size=(bg_width, bg_height), color=bg_color, duration=end_time-start_time)

#     # Position the text clip in the center of the background clip
#     text_clip = text_clip.set_position('center').set_duration(end_time-start_time)

#     # Composite the text clip over the background clip
#     composite_clip = CompositeVideoClip([background_clip, text_clip], size=(bg_width, bg_height))
#     composite_clip = composite_clip.set_position('center').set_start(start_time)

#     return composite_clip

def create_text_clip_for_title(text, start_time, end_time, fontsize=24, font='Arial', color='black', bg_color=(255, 255, 255)):
    """
    Creates a moviepy TextClip object for a given piece of text with a dynamic background.
    The background box width is fixed at 780, and its height adjusts based on the text input size.
    The text is left-justified inside the box, which is centered in the 1080x1920 canvas.
    """
    # Fixed width for the background
    bg_width = 780

    # Create a TextClip for the text, ensuring it doesn't exceed the background width
    text_clip = TextClip(text, fontsize=fontsize, font=font, color=color, align='West', size=(bg_width, None))

    # Calculate text size to adjust background height accordingly
    text_width, text_height = text_clip.size
    bg_height = text_height + 20  # Adding a small padding

    # Create a background ColorClip with the calculated size
    background_clip = ColorClip(size=(bg_width, bg_height), color=bg_color, duration=end_time-start_time)

    # Composite the text clip over the background clip
    # The text is left-justified within the background
    text_clip = text_clip.set_pos('center').set_duration(end_time-start_time)
    composite_clip = CompositeVideoClip([background_clip, text_clip.set_position(('center', 'center'))], size=(bg_width, bg_height))

    # Calculate the position to center the composite clip in the full canvas
    full_canvas_size = (1080, 1920)
    x_center = (full_canvas_size[0] - bg_width) / 2
    y_center = (full_canvas_size[1] - bg_height) / 2

    # Create an outer canvas with transparent background
    outer_canvas = ColorClip(size=full_canvas_size, color=(0, 0, 0, 0), duration=end_time-start_time)

    # Center the composite clip on the outer canvas
    centered_composite_clip = CompositeVideoClip([outer_canvas, composite_clip.set_position((x_center, y_center))], size=full_canvas_size)
    centered_composite_clip = centered_composite_clip.set_start(start_time)

    return centered_composite_clip

