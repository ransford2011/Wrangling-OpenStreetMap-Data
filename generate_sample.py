# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET  # Use cElementTree or lxml if too slow

#OSM_FILE = "C:\\Users\\ransf\\Documents\\atlanta_georgia.osm"  # Replace this with your osm file
OSM_FILE = "C:\\Users\\ransf\\OneDrive\\Documents\\GitHub\\Data-Wrangling-With-MongoDB\\Project 3\\sample.osm"
SAMPLE_FILE = "C:\\Users\\ransf\\OneDrive\\Documents\\GitHub\\Data-Wrangling-With-MongoDB\\Project 3\\sample2.osm"

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every 10th top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % 30 == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')