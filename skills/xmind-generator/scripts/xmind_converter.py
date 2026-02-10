#!/usr/bin/env python3
"""
XMind JSON to .xmind file converter

This script converts standard XMind JSON format to .xmind file format.
XMind files are ZIP archives containing XML files that define the mind map structure.
"""

import json
import zipfile
import os
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET

def create_content_xml(json_data):
    """Create the content.xml file for XMind"""
    
    # Create the root element
    root = ET.Element('xmap-content', {
        'xmlns': 'urn:xmind:xmap:xmlns:content:2.0',
        'xmlns:fo': 'http://www.w3.org/1999/XSL/Format',
        'xmlns:svg': 'http://www.w3.org/2000/svg',
        'version': '2.0'
    })
    
    # Create sheet
    sheet = ET.SubElement(root, 'sheet', {
        'id': str(uuid.uuid4())
    })
    
    # Process root topic
    if 'rootTopic' in json_data:
        root_topic = json_data['rootTopic']
        topic_elem = create_topic_element(root_topic, is_root=True)
        sheet.append(topic_elem)
    
    # Process relationships
    if 'relationships' in json_data:
        for rel in json_data['relationships']:
            rel_elem = create_relationship_element(rel)
            sheet.append(rel_elem)
    
    return ET.tostring(root, encoding='unicode', method='xml')

def create_topic_element(topic_data, is_root=False):
    """Create XML element for a topic"""
    
    topic_id = topic_data.get('id', str(uuid.uuid4()))
    
    if is_root:
        elem = ET.Element('root-topic', {
            'id': topic_id,
            'structure-class': topic_data.get('structure', 'org.xmind.ui.logic.right')
        })
    else:
        elem = ET.Element('topic', {
            'id': topic_id
        })
    
    # Add title
    title_elem = ET.SubElement(elem, 'title')
    title_elem.text = topic_data.get('title', 'Untitled')
    
    # Add children
    if 'children' in topic_data:
        children = topic_data['children']
        if 'attached' in children and children['attached']:
            children_elem = ET.SubElement(elem, 'children')
            topics_elem = ET.SubElement(children_elem, 'topics', {'type': 'attached'})
            for child in children['attached']:
                child_elem = create_topic_element(child)
                topics_elem.append(child_elem)
    
    # Add notes
    if 'notes' in topic_data:
        notes_elem = ET.SubElement(elem, 'notes')
        plain_elem = ET.SubElement(notes_elem, 'plain')
        plain_elem.text = topic_data['notes'].get('plain', '')
    
    # Add labels
    if 'labels' in topic_data and topic_data['labels']:
        labels_elem = ET.SubElement(elem, 'labels')
        for label in topic_data['labels']:
            label_elem = ET.SubElement(labels_elem, 'label')
            label_elem.text = label
    
    # Add markers
    if 'markers' in topic_data and topic_data['markers']:
        markers_elem = ET.SubElement(elem, 'markers')
        for marker in topic_data['markers']:
            marker_elem = ET.SubElement(markers_elem, 'marker', {'marker-id': marker})
    
    # Add style
    if 'style' in topic_data:
        style_elem = ET.SubElement(elem, 'style')
        for key, value in topic_data['style'].items():
            if key == 'svgFill':
                ET.SubElement(style_elem, 'svg:fill')
                style_elem.find('svg:fill').text = value
            elif key.startswith('fo:'):
                prop_name = key.replace('fo:', '')
                ET.SubElement(style_elem, f'fo:{prop_name}')
                style_elem.find(f'fo:{prop_name}').text = value
    
    return elem

def create_relationship_element(rel_data):
    """Create XML element for a relationship"""
    
    rel_elem = ET.Element('relationship', {
        'id': rel_data.get('id', str(uuid.uuid4()))
    })
    
    # Add end points
    end1 = rel_data.get('end1', {})
    end2 = rel_data.get('end2', {})
    
    end1_elem = ET.SubElement(rel_elem, 'end1')
    end1_topic_elem = ET.SubElement(end1_elem, 'topic')
    end1_topic_elem.set('id', end1.get('topicId', ''))
    
    end2_elem = ET.SubElement(rel_elem, 'end2')
    end2_topic_elem = ET.SubElement(end2_elem, 'topic')
    end2_topic_elem.set('id', end2.get('topicId', ''))
    
    # Add title
    if 'title' in rel_data:
        title_elem = ET.SubElement(rel_elem, 'title')
        title_elem.text = rel_data['title']
    
    return rel_elem

def create_manifest_xml():
    """Create the manifest.xml file for XMind"""
    
    root = ET.Element('manifest', {
        'xmlns': 'urn:xmind:xmap:xmlns:manifest:1.0'
    })
    
    # Add file entries
    file_entry = ET.SubElement(root, 'file-entry', {
        'full-path': 'content.xml',
        'media-type': 'text/xml'
    })
    
    file_entry = ET.SubElement(root, 'file-entry', {
        'full-path': 'meta.xml',
        'media-type': 'text/xml'
    })
    
    return ET.tostring(root, encoding='unicode', method='xml')

def create_meta_xml():
    """Create the meta.xml file for XMind"""
    
    root = ET.Element('meta', {
        'xmlns': 'urn:xmind:xmap:xmlns:meta:2.0'
    })
    
    author = ET.SubElement(root, 'Author')
    author.text = 'XMind Generator'
    
    created = ET.SubElement(root, 'Created')
    created.text = datetime.now().isoformat()
    
    return ET.tostring(root, encoding='unicode', method='xml')

def convert_json_to_xmind(json_file_path, output_file_path):
    """Convert JSON file to XMind file"""
    
    # Read JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Create XMind ZIP file
    with zipfile.ZipFile(output_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add content.xml
        content_xml = create_content_xml(json_data)
        zipf.writestr('content.xml', content_xml)
        
        # Add manifest.xml
        manifest_xml = create_manifest_xml()
        zipf.writestr('META-INF/manifest.xml', manifest_xml)
        
        # Add meta.xml
        meta_xml = create_meta_xml()
        zipf.writestr('meta.xml', meta_xml)
    
    print(f"Successfully created XMind file: {output_file_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python xmind_converter.py <input.json> <output.xmind>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    try:
        convert_json_to_xmind(input_file, output_file)
    except Exception as e:
        print(f"Error converting file: {e}")
        sys.exit(1)
