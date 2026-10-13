"""One-shot media build for Tone4DMedia facelift.
- Optimizes supplied project photos from images/ -> assets/images/ (real JPEGs, resized, EXIF-stripped)
- Extracts one poster frame per video -> assets/posters/
- Transcodes all 3 videos to web-safe H.264 720p + faststart -> assets/videos/
Run with: python build_media.py. Originals are never modified.
"""
import os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "images")
IMG_OUT = os.path.join(ROOT, "assets", "images")
POST_OUT = os.path.join(ROOT, "assets", "posters")
VID_OUT = os.path.join(ROOT, "assets", "videos")
FF = imageio_ffmpeg.get_ffmpeg_exe()

PHOTOS = [
    ("IMG_20250801_120648.jpg.jpeg", "tshirt-orlando-pirates-front.jpg"),
    ("IMG_20251017_154858_edit_9745907859040.jpg.jpeg", "tee-proud-buccaneer-back.jpg"),
    ("IMG_20251017_154912_edit_9763115020179.jpg.jpeg", "brand-wall-showroom.jpg"),
    ("IMG_20260318_162144.jpg.jpeg", "wall-banner-quantum.jpg"),
    ("IMG_20260408_124114.jpg.jpeg", "branded-gazebo-event.jpg"),
    ("IMG_20260720_151231.jpg.jpeg", "pullup-hollywood-signage.jpg"),
    ("IMG_20260723_103538.jpg.jpeg", "branded-gazebo-fnb.jpg"),
    ("IMG_20260804_124057.jpg.jpeg", "brand-wall-studio.jpg"),
    ("IMG_20260810_101435.jpg.jpeg", "xframe-fighter-banner.jpg"),
    ("IMG_20260910_100500.jpg.jpeg", "signage-wall-interior.jpg"),
    ("IMG_20260910_100521.jpg.jpeg", "signage-installation.jpg"),
    ("Branding_040120.png", "branding-mockup-flyer.jpg"),
    ("Vehicle_040039.png", "vehicle-wrap-mockup.jpg"),
    ("Tshirt printing_040152.png", "apparel-tshirt-mockup.jpg"),
]

VIDEOS = [
    ("2026-05-09-163723937.mp4", "studio-tour.mp4", "poster-studio-tour.jpg"),
    ("VID_20250901_162957.mp4", "project-install.mp4", "poster-project-install.jpg"),
    ("VID_20260424_122709.mp4", "branding-showcase.mp4", "poster-branding-showcase.jpg"),
]

def optimize_photo(src_name, out_name):
    src = os.path.join(SRC, src_name)
    dst = os.path.join(IMG_OUT, out_name)
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode in ("RGBA", "LA", "PA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dst, "JPEG", quality=72, progressive=True, optimize=True)  # no EXIF -> strips GPS/location
    s_in = os.path.getsize(src); s_out = os.path.getsize(dst)
    print(f"IMG {out_name}: {im.size} {s_in//1024}KB -> {s_out//1024}KB ({100*s_out//s_in}%)")
    return dst

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAILED:", " ".join(cmd)); print((r.stderr or "")[-2000:])
        raise SystemExit(1)

def poster_for(src_video, poster_name, ss="00:00:01"):
    src = os.path.join(SRC, src_video)
    dst = os.path.join(POST_OUT, poster_name)
    run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", ss, "-i", src,
         "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "4", dst])
    im = Image.open(dst); im.thumbnail((960, 960), Image.LANCZOS)
    im.save(dst, "JPEG", quality=70, progressive=True, optimize=True)
    print(f"POSTER {poster_name}: {im.size} {os.path.getsize(dst)//1024}KB")
    return dst

def transcode(src_video, out_name):
    src = os.path.join(SRC, src_video)
    dst = os.path.join(VID_OUT, out_name)
    run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", src,
         "-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
         "-movflags", "+faststart", "-map_metadata", "-1", dst])
    print(f"VIDEO {out_name}: {os.path.getsize(src)//1024}KB -> {os.path.getsize(dst)//1024}KB")
    return dst

if __name__ == "__main__":
    os.makedirs(IMG_OUT, exist_ok=True); os.makedirs(POST_OUT, exist_ok=True); os.makedirs(VID_OUT, exist_ok=True)
    for s, o in PHOTOS:
        optimize_photo(s, o)
    for src_v, out_v, poster in VIDEOS:
        poster_for(src_v, poster)
        transcode(src_v, out_v)
    print("DONE")
