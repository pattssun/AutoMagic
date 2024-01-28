from PIL import Image, ImageDraw, ImageFont

def create_banner(title_text, output_filename="banner.png", banner_size=(1024, 200), background_color="black", font_color="white", font_size=40):
    # Create an image with the specified background color
    banner = Image.new('RGB', banner_size, color=background_color)
    draw = ImageDraw.Draw(banner)

    # Load a font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate text size and position
    text_size = draw.textsize(title_text, font=font)
    text_x = (banner_size[0] - text_size[0]) / 2
    text_y = (banner_size[1] - text_size[1]) / 2

    # Draw the text onto the image
    draw.text((text_x, text_y), title_text, fill=font_color, font=font)

    # Save the image
    banner.save(output_filename)

    return output_filename

# Test the function
if __name__ == "__main__":
    create_banner("Example Reddit Post Title")
