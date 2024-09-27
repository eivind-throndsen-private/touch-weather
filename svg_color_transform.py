# svg_color_transform.py

import sys
import re

try:
    import yaml
except ImportError:
    print("Please install pyyaml module: pip install pyyaml")
    sys.exit(1)

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config['color_transformations']

def transform_svg(svg_file, output_file, color_transformations):
    # Read the SVG content
    with open(svg_file, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # Apply color transformations
    for original_color, new_color in color_transformations.items():
        # Create regex patterns to match colors
        pattern = re.compile(re.escape(original_color), re.IGNORECASE)
        svg_content = pattern.sub(new_color, svg_content)

    # Write the transformed SVG content to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def main():
    if len(sys.argv) != 4:
        print("Usage: python svg_color_transform.py <svg_file> <config_file> <output_file>")
        sys.exit(1)

    svg_file = sys.argv[1]
    config_file = sys.argv[2]
    output_file = sys.argv[3]

    color_transformations = load_config(config_file)
    transform_svg(svg_file, output_file, color_transformations)
    print(f"Transformed SVG saved to {output_file}")

if __name__ == '__main__':
    main()
