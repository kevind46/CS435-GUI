import os
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import re

def parse_xml_for_components(xml_path):
    # Finds each component in XML file
    try:
        with open(xml_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex to find all node elements with bounds
        pattern = r'<node[^>]*bounds="(\[[0-9,]+\]\[[0-9,]+\])"[^>]*>'
        matches = re.findall(pattern, content)
        
        components = []
        for bounds in matches:
            x1, y1, x2, y2 = map(int, bounds.replace('][', ',').strip('[]').split(','))
            components.append((x1, y1, x2 - x1, y2 - y1))
        
        return components
    except Exception as e:
        print(f"Error processing XML file {xml_path}: {e}")
        return None

def highlight_components(image_path, components, output_path):
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Highlight each component with a yellow rectangle
        for x, y, width, height in components:
            draw.rectangle([x, y, x + width, y + height], outline="yellow", width=2)
        
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return False

def process_files(data_folder, output_folder):
    # Create output folder if it doesn't exist
    # Moves through each input PNG and annotates
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(data_folder)
    png_files = [f for f in files if f.endswith('.png')]

    for png_file in png_files:
        base_name = png_file[:-4] 
        xml_file = base_name + '.xml'
        
        if xml_file in files:
            png_path = os.path.join(data_folder, png_file)
            xml_path = os.path.join(data_folder, xml_file)
            output_path = os.path.join(output_folder, f"highlighted_{png_file}")

            components = parse_xml_for_components(xml_path)
            if components is not None:
                if highlight_components(png_path, components, output_path):
                    print(f"Processed {png_file}")
                else:
                    print(f"Failed to process {png_file}")
            else:
                print(f"Skipped {png_file} due to XML parsing error")
        else:
            print(f"Warning: No matching XML file found for {png_file}")

current_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(current_dir, "Programming-Assignment-Data")
output_folder = os.path.join(current_dir, "Output-Images")

process_files(data_folder, output_folder)