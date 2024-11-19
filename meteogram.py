#!/usr/bin/env python3

import os
import sys
import time
import json
import argparse
import wget
from PIL import Image, ImageDraw
import imagequant

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

def get_file_size_kb(file_path):
    return os.path.getsize(file_path) / 1024

def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

def crop_image(input_file, output_file, crop_area):
    print_flush("Cropping image")
    with Image.open(input_file) as img:
        cropped_img = img.crop(crop_area)
        cropped_img = cropped_img.resize((480, 272), Image.LANCZOS)
        cropped_img.save(
            output_file,
            format="PNG",
            optimize=True,
            compress_level=9
        )
        print_flush(f"Saved cropped image to {output_file} (Size: {get_file_size_kb(output_file):.1f}KB)")

def draw_debug_rectangle(image_file, rectangle):
    print("Drawing debug rectangle")
    with Image.open(image_file) as img:
        draw = ImageDraw.Draw(img)
        x, y, width, height = rectangle
        draw.rectangle([x, y, x + width, y + height], outline="red", width=2)
        img.save(image_file)
        print(f"Drew rectangle on {image_file}")

def optimize_meteogram(input_file, quality=(50, 85), colors=16):
    try:
        initial_size = get_file_size_kb(input_file)
        print_flush(f"\nStarting optimization. Initial size: {initial_size:.1f}KB")
        
        output_dir = os.path.dirname(input_file)
        optimized_output = input_file
        
        input_image = Image.open(input_file).convert('P', palette=Image.ADAPTIVE)
        
        quantized = imagequant.quantize_pil_image(
            input_image,
            dithering_level=0.5,
            max_colors=colors,
            min_quality=quality[0],
            max_quality=quality[1]
        )
        
        quantized.save(
            optimized_output,
            format="PNG",
            optimize=True,
            compress_level=9,
            bits=8,
            include_all_chunks=False
        )
        
        after_quantize_size = get_file_size_kb(optimized_output)
        print_flush(f"Size after quantization: {after_quantize_size:.1f}KB (Reduced by {initial_size - after_quantize_size:.1f}KB)")
        
        # Additional optipng optimization
        os.system(f"optipng -o7 {optimized_output}")
        
        final_size = get_file_size_kb(optimized_output)
        print_flush(f"Final size after optipng: {final_size:.1f}KB")
        print_flush(f"Total size reduction: {initial_size - final_size:.1f}KB ({((initial_size - final_size) / initial_size * 100):.1f}%)")
        
        return True
        
    except Exception as e:
        print_flush("Error during meteogram optimization:", str(e))
        return False

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
    image_height = config.get('image_height', 1200)
    crop_area = config.get('crop_area', [10, 256, 960, 544])

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
        
        # Optimize the meteogram
        optimize_meteogram(meteogram_png)

        if debug:
            draw_debug_rectangle(meteogram_png, rectangle)
            keep_running = False
        else:
            time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
