#!/usr/bin/env python3

import os
import sys
import time
import wget
import json
from PIL import Image, ImageDraw

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

def download_svg(url, output_dir):
    filename = os.path.join(output_dir, 'meteogram.svg')
    if os.path.exists(filename):
        os.remove(filename)
    print(f"Downloading SVG from {url}")
    wget.download(url, out=filename)
    return filename

def convert_svg_to_png(svg_file, png_file, height):
    print("Converting SVG to PNG")
    os.system(f"rsvg-convert -h {height} {svg_file} -o {png_file}")

def crop_image(input_file, output_file, crop_area):
    print("Cropping image")
    with Image.open(input_file) as img:
        cropped_img = img.crop(crop_area)
        cropped_img = cropped_img.resize((480, 272), Image.LANCZOS)
        cropped_img.save(output_file)
        print(f"Saved cropped image to {output_file}")

def draw_debug_rectangle(image_file, rectangle):
    print("Drawing debug rectangle")
    with Image.open(image_file) as img:
        draw = ImageDraw.Draw(img)
        x, y, width, height = rectangle
        draw.rectangle([x, y, x + width, y + height], outline="red", width=2)
        img.save(image_file)
        print(f"Drew rectangle on {image_file}")

def main():
    config = load_config()
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    
    svg_url = config.get('svg_url')
    image_height = config.get('image_height', 600)
    crop_area = config.get('crop_area', [5, 128, 480, 272])

    debug = False
    if len(sys.argv) == 5:
        debug = True
        rectangle = tuple(map(int, sys.argv[1:5]))

    while True:
        current_hour = time.localtime().tm_hour
        if 7 <= current_hour < 23:
            sleep_duration = 900  # 15 minutes
        else:
            sleep_duration = 3600  # 1 hour

        svg_file = download_svg(svg_url, output_dir)
        raw_png = os.path.join(output_dir, 'meteogram-raw.png')
        convert_svg_to_png(svg_file, raw_png, image_height)
        
        meteogram_png = os.path.join(output_dir, 'meteogram.png')
        x, y, width, height = crop_area
        crop_box = (x, y, x + width, y + height)
        crop_image(raw_png, meteogram_png, crop_box)

        if debug:
            draw_debug_rectangle(meteogram_png, rectangle)

        time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
