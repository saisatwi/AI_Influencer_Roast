import os, random, textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

os.makedirs("images", exist_ok=True)
os.makedirs("video",  exist_ok=True)

PALETTES = [
    [(20,8,0),   (80,20,0)  ],  # ember
    [(5,5,20),   (20,0,60)  ],  # purple
    [(0,15,10),  (0,50,30)  ],  # toxic
    [(20,0,0),   (60,0,10)  ],  # blood
    [(5,10,20),  (10,30,60) ],  # steel
]

def _font(size, bold=False):
    paths = ([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ] if bold else [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ])
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def _gradient(size, top, bot):
    W, H = size
    img  = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(top[0]+(bot[0]-top[0])*t)
        g = int(top[1]+(bot[1]-top[1])*t)
        b = int(top[2]+(bot[2]-top[2])*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    return img

def make_roast_card(title: str, roast: str, idx: int) -> str:
    W, H = 720, 1280
    pal  = PALETTES[idx % len(PALETTES)]
    img  = _gradient((W, H), pal[0], pal[1])
    draw = ImageDraw.Draw(img)

    # grain texture
    for _ in range(6000):
        v = random.randint(0, 40)
        draw.point((random.randint(0,W-1), random.randint(0,H-1)), fill=(v,v,v))

    # badge
    draw.text((40,60), "🔥 ROASTED", font=_font(44,True), fill=(255,80,20))
    # rule
    draw.rectangle([(40,128),(W-40,131)], fill=(255,80,20))

    # product title
    tf = _font(28)
    for i, line in enumerate(textwrap.wrap(title[:90], 36)[:3]):
        draw.text((42, 162+i*36+1), line, font=tf, fill=(0,0,0))
        draw.text((40, 162+i*36),   line, font=tf, fill=(180,160,140))

    # flame
    draw.text((W//2-45, H//2-110), "🔥", font=_font(90,True), fill=(255,100,0))

    # roast text
    rf    = _font(40,True)
    lines = textwrap.wrap(roast, 22)
    ry    = H//2 + 50
    for line in lines[:6]:
        bb = draw.textbbox((0,0), line, font=rf)
        x  = (W-(bb[2]-bb[0]))//2
        draw.text((x+2,ry+2), line, font=rf, fill=(0,0,0))
        draw.text((x,  ry),   line, font=rf, fill=(255,245,220))
        ry += 54

    # watermark
    draw.text((40,H-65), "AI ROASTER  •  brutally honest", font=_font(24), fill=(70,60,50))

    path = f"images/roast_card_{idx}.jpg"
    img.save(path, quality=92)
    return path


def create_roast_video(card_path: str, audio_path: str, roast: str, idx: int) -> str | None:
    out = f"video/roast_{idx}.mp4"
    try:
        audio = AudioFileClip(audio_path)
        clip  = ImageClip(card_path).with_duration(audio.duration)
        video = clip.with_audio(audio)
        video.write_videofile(out, fps=15, codec="libx264",
                              preset="ultrafast", audio_codec="aac",
                              threads=4, logger=None)
        audio.close(); clip.close()
        return out
    except Exception as e:
        print(f"[video_generator] Error: {e}")
        return None