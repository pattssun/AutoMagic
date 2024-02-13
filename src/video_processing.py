from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
from PIL import Image

def crop_to_916(clip):
    """
    Crops a clip to a 9:16 aspect ratio and centered from its sides.
    """
    original_width, original_height = clip.size
    # Calculate the target width based on the original height to maintain a 9:16 aspect ratio
    target_width = int((9.0 / 16.0) * original_height)

    # Ensure target width is not greater than the original width
    target_width = min(target_width, original_width)

    # Calculate the amount to crop from the sides to achieve the target width
    crop_amount_per_side = (original_width - target_width) / 2

    # Crop the clip centered from its sides
    cropped_clip = clip.crop(x1=crop_amount_per_side, y1=0, x2=original_width - crop_amount_per_side, y2=original_height)
    
    # Resize the clip to 1080x1920
    cropped_clip = cropped_clip.resize((1080, 1920))

    return cropped_clip

def create_text_clip_for_title(text, start_time, end_time, clip_size, fontsize=65, font='Arial', color='black', bg_color=(255, 255, 255)):
    """
    Creates a moviepy TextClip object for a title text in a dynamic box.
    The box has a fixed width of 780 pixels and is centered within a 1080x1920 canvas
    """
    # Create a TextClip for the text
    text_clip = TextClip(text, fontsize=fontsize, font=font, color=color)

    # Calculate text size to determine box size
    text_width, text_height = text_clip.size
    box_height = text_height 
    box_width = int(clip_size[0] * 0.72)  # 72% of the background clip's width (780/1080 = 0.72)

    # Create a box ColorClip
    box_clip = ColorClip(size=(box_width, box_height), color=bg_color, duration=end_time-start_time).set_position('center')

    # Position the text clip in the center of the box clip
    text_clip = text_clip.set_position('center').set_duration(end_time-start_time)

    # Composite the text clip over the background clip
    composite_clip = CompositeVideoClip([box_clip, text_clip], size=clip_size)
    composite_clip = composite_clip.set_position('center').set_start(start_time)

    return composite_clip

def create_text_clip_for_body(text, start_time, end_time, clip_size, font='resources/fonts/komika_poster.ttf', fontsize=65, color='white', stroke_color='black', stroke_width=4.5):
    """
    Creates a moviepy TextClip object for a body text.
    """
    return TextClip(text, font=font, fontsize=fontsize, color=color, size=clip_size, stroke_color=stroke_color, stroke_width=stroke_width).set_position("center").set_start(start_time).set_end(end_time)