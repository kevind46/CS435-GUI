import os
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

def parse_xml_for_components(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    components = []

    def traverse(element):
        if len(element) == 0:  # This is a leaf node
            bounds = element.get('bounds')
            if bounds:
                x1, y1, x2, y2 = map(int, bounds.replace('][', ',').strip('[]').split(','))
                components.append((x1, y1, x2 - x1, y2 - y1))
        else:
            for child in element:
                traverse(child)

    traverse(root)
    return components