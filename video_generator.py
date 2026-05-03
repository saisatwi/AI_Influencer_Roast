import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip

os.makedirs("video", exist_ok=True)

def create_roast_video(image_path: str, audio_path: str, roast_text: str, idx: int = 0) -> str:
    """Overlay roast text using PIL, then combine with audio in MoviePy."""
    # Open image and add text
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Choose a font (make sure arial.ttf or another font is available)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Wrap text if too long
    max_width = img.width - 100
    lines = []
    words = roast_text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y = img.height - (len(lines) * 50) - 50
    for l in lines:
        draw.text((50, y), l, font=font, fill="white")
        y += 50

    # Save temp image
    temp_img_path = f"images/product_overlay_{idx}.jpg"
    img.save(temp_img_path)

    # Combine with audio
    audio_clip = AudioFileClip(audio_path)
    img_clip = ImageClip(temp_img_path).set_duration(audio_clip.duration)
    video = img_clip.set_audio(audio_clip)

    output_path = f"video/roast_video_{idx}.mp4"
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path
