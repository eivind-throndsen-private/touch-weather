#!/usr/bin/env python3

import os
import sys
import time
import json
import argparse
import wget
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
    print("\nConverting SVG to PNG")
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

#def transform_svg_to_dark(svg_file, config_file='color_transform_config.yaml'):
#    print("Transforming SVG to dark mode")
#    os.system(f"python3 svg_color_transform.py {svg_file} {config_file} {svg_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate meteogram images.')
    parser.add_argument('--night-mode', action='store_true', help='Force night mode for testing.')
    parser.add_argument('--debug', nargs=4, metavar=('X', 'Y', 'Width', 'Height'),
                        type=int, help='Debug mode with rectangle coordinates.')
    args = parser.parse_args()

    config = load_config()
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    
    svg_url = config.get('svg_url')
    image_height = config.get('image_height', 600)
    crop_area = config.get('crop_area', [5, 128, 480, 272])

    debug = False
    if args.debug:
        debug = True
        rectangle = tuple(args.debug)

    keep_running = True
    
    while keep_running:
        if args.night_mode:
            is_dark_mode = True
        else:
            current_hour = time.localtime().tm_hour
            if 7 <= current_hour < 23:
                is_dark_mode = False
            else:
                is_dark_mode = True

        sleep_duration = 3600  # sleep for 1 hour between each invocation

        final_svg_url = svg_url  # Store the original URL in a temporary variable

        if is_dark_mode:
            final_svg_url += "?mode=dark"

        svg_file = download_svg(final_svg_url, output_dir)

        #if is_dark_mode:
        #    transform_svg_to_dark(svg_file)

        raw_png = os.path.join(output_dir, 'meteogram-raw.png')
        convert_svg_to_png(svg_file, raw_png, image_height)
        
        meteogram_png = os.path.join(output_dir, 'meteogram.png')
        x, y, width, height = crop_area
        crop_box = (x, y, x + width, y + height)
        crop_image(raw_png, meteogram_png, crop_box)

        if debug:
            draw_debug_rectangle(meteogram_png, rectangle)
            keep_running = False
        else:
            time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
