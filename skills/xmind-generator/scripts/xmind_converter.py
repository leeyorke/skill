#!/usr/bin/env python3
"""
XMind JSON to .xmind file converter (兼容 XMind 2020)

This script converts standard XMind JSON format to .xmind file format.
支持 XMind 2020 的 JSON 格式结构。
"""

import json
import zipfile
import os
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET
from PIL import Image
import io


def create_content_json(json_data):
    """Create the content.json file for XMind 2020"""

    # XMind 2020 的 content.json 结构
    content = {
        "id": str(uuid.uuid4()),
        "title": json_data.get("title", "Sheet 1"),
        "class": "sheet",
        "parent": None,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "rootTopic": None,
        "relationships": [],
    }

    # 处理根主题
    if "rootTopic" in json_data:
        root_topic = json_data["rootTopic"]
        content["rootTopic"] = create_topic_json(root_topic, is_root=True)

    # 处理关系
    if "relationships" in json_data:
        for rel in json_data["relationships"]:
            relationship = {
                "id": rel.get("id", str(uuid.uuid4())),
                "title": rel.get("title", ""),
                "end1": {"id": rel.get("end1", {}).get("topicId", "")},
                "end2": {"id": rel.get("end2", {}).get("topicId", "")},
            }
            content["relationships"].append(relationship)

    return content


def create_topic_json(topic_data, is_root=False, parent_id=None):
    """Create JSON structure for a topic"""

    topic = {
        "id": topic_data.get("id", str(uuid.uuid4())),
        "title": topic_data.get("title", "Untitled"),
        "class": "topic",
        "structureClass": topic_data.get("structure", "org.xmind.ui.logic.right")
        if is_root
        else None,
        "children": {"attached": []},
        "notes": None,
        "labels": [],
        "markers": [],
        "style": {},
        "parent": parent_id,
    }

    # 处理子主题
    if "children" in topic_data and topic_data["children"]:
        children = topic_data["children"]
        if "attached" in children and children["attached"]:
            for child in children["attached"]:
                child_topic = create_topic_json(
                    child, is_root=False, parent_id=topic["id"]
                )
                topic["children"]["attached"].append(child_topic)

    # 处理笔记
    if "notes" in topic_data and topic_data["notes"]:
        notes = topic_data["notes"]
        topic["notes"] = {"realHTML": {"content": notes.get("plain", "")}}

    # 处理标签
    if "labels" in topic_data and topic_data["labels"]:
        topic["labels"] = topic_data["labels"]

    # 处理标记
    if "markers" in topic_data and topic_data["markers"]:
        topic["markers"] = [{"markerId": marker} for marker in topic_data["markers"]]

    # 处理样式
    if "style" in topic_data:
        style = topic_data["style"]
        topic["style"] = {"properties": {}}
        for key, value in style.items():
            if key == "svgFill":
                topic["style"]["properties"]["svg:fill"] = value
            elif key.startswith("fo:"):
                prop_name = key.replace("fo:", "")
                topic["style"]["properties"][f"fo:{prop_name}"] = value

    return topic


def create_manifest_json():
    """Create the manifest.json file for XMind 2020"""

    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
            "Thumbnails/thumbnail.png": {},
        }
    }

    return manifest


def create_metadata_json():
    """Create the metadata.json file for XMind 2020"""

    metadata = {
        "creator": {"name": "XMind Generator", "version": "1.0.0"},
        "modifier": {"name": "XMind Generator", "version": "1.0.0"},
        "created": datetime.now().isoformat() + "Z",
        "modified": datetime.now().isoformat() + "Z",
        "xmind": {"version": "2020"},
    }

    return metadata


def create_thumbnail():
    """Create a simple thumbnail image"""

    # 创建一个简单的缩略图 (200x150 像素)
    img = Image.new("RGB", (200, 150), color="white")

    # 添加一些基本图形作为缩略图
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)

    # 画一个简单的心智图结构
    draw.rectangle([90, 70, 110, 80], fill="blue")  # 根节点
    draw.line([110, 75, 150, 60], fill="black", width=2)  # 连接线
    draw.line([110, 75, 150, 90], fill="black", width=2)  # 连接线
    draw.ellipse([145, 55, 165, 65], fill="green")  # 子节点1
    draw.ellipse([145, 85, 165, 95], fill="green")  # 子节点2

    # 转换为PNG字节流
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return img_byte_arr.getvalue()


def convert_json_to_xmind(json_file_path, output_file_path):
    """Convert JSON file to XMind 2020 format"""

    # 读取JSON数据
    with open(json_file_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 创建 XMind ZIP 文件
    with zipfile.ZipFile(output_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 添加 content.json
        content_json = create_content_json(json_data)
        zipf.writestr(
            "content.json", json.dumps(content_json, indent=2, ensure_ascii=False)
        )

        # 添加 manifest.json
        manifest_json = create_manifest_json()
        zipf.writestr(
            "manifest.json", json.dumps(manifest_json, indent=2, ensure_ascii=False)
        )

        # 添加 metadata.json
        metadata_json = create_metadata_json()
        zipf.writestr(
            "metadata.json", json.dumps(metadata_json, indent=2, ensure_ascii=False)
        )

        # 添加 content.xml (为了向后兼容)
        content_xml = create_content_xml(json_data)
        zipf.writestr("content.xml", content_xml)

        # 添加 Thumbnails 目录和缩略图
        thumbnail_data = create_thumbnail()
        zipf.writestr("Thumbnails/thumbnail.png", thumbnail_data)

    print(f"Successfully created XMind 2020 file: {output_file_path}")


# 保持原有的 XML 格式支持
def create_content_xml(json_data):
    """Create the content.xml file for XMind (向后兼容)"""

    # Create the root element
    root = ET.Element(
        "xmap-content",
        {
            "xmlns": "urn:xmind:xmap:xmlns:content:2.0",
            "xmlns:fo": "http://www.w3.org/1999/XSL/Format",
            "xmlns:svg": "http://www.w3.org/2000/svg",
            "version": "2.0",
        },
    )

    # Create sheet
    sheet = ET.SubElement(root, "sheet", {"id": str(uuid.uuid4())})

    # Process root topic
    if "rootTopic" in json_data:
        root_topic = json_data["rootTopic"]
        topic_elem = create_topic_element(root_topic, is_root=True)
        sheet.append(topic_elem)

    # Process relationships
    if "relationships" in json_data:
        for rel in json_data["relationships"]:
            rel_elem = create_relationship_element(rel)
            sheet.append(rel_elem)

    return ET.tostring(root, encoding="unicode", method="xml")


def create_topic_element(topic_data, is_root=False):
    """Create XML element for a topic (向后兼容)"""

    topic_id = topic_data.get("id", str(uuid.uuid4()))

    if is_root:
        elem = ET.Element(
            "root-topic",
            {
                "id": topic_id,
                "structure-class": topic_data.get(
                    "structure", "org.xmind.ui.logic.right"
                ),
            },
        )
    else:
        elem = ET.Element("topic", {"id": topic_id})

    # Add title
    title_elem = ET.SubElement(elem, "title")
    title_elem.text = topic_data.get("title", "Untitled")

    # Add children
    if "children" in topic_data:
        children = topic_data["children"]
        if "attached" in children and children["attached"]:
            children_elem = ET.SubElement(elem, "children")
            topics_elem = ET.SubElement(children_elem, "topics", {"type": "attached"})
            for child in children["attached"]:
                child_elem = create_topic_element(child)
                topics_elem.append(child_elem)

    # Add notes
    if "notes" in topic_data:
        notes_elem = ET.SubElement(elem, "notes")
        plain_elem = ET.SubElement(notes_elem, "plain")
        plain_elem.text = topic_data["notes"].get("plain", "")

    # Add labels
    if "labels" in topic_data and topic_data["labels"]:
        labels_elem = ET.SubElement(elem, "labels")
        for label in topic_data["labels"]:
            label_elem = ET.SubElement(labels_elem, "label")
            label_elem.text = label

    # Add markers
    if "markers" in topic_data and topic_data["markers"]:
        markers_elem = ET.SubElement(elem, "markers")
        for marker in topic_data["markers"]:
            marker_elem = ET.SubElement(markers_elem, "marker", {"marker-id": marker})

    # Add style
    if "style" in topic_data:
        style_elem = ET.SubElement(elem, "style")
        for key, value in topic_data["style"].items():
            if key == "svgFill":
                ET.SubElement(style_elem, "svg:fill")
                style_elem.find("svg:fill").text = value
            elif key.startswith("fo:"):
                prop_name = key.replace("fo:", "")
                ET.SubElement(style_elem, f"fo:{prop_name}")
                style_elem.find(f"fo:{prop_name}").text = value

    return elem


def create_relationship_element(rel_data):
    """Create XML element for a relationship (向后兼容)"""

    rel_elem = ET.Element("relationship", {"id": rel_data.get("id", str(uuid.uuid4()))})

    # Add end points
    end1 = rel_data.get("end1", {})
    end2 = rel_data.get("end2", {})

    end1_elem = ET.SubElement(rel_elem, "end1")
    end1_topic_elem = ET.SubElement(end1_elem, "topic")
    end1_topic_elem.set("id", end1.get("topicId", ""))

    end2_elem = ET.SubElement(rel_elem, "end2")
    end2_topic_elem = ET.SubElement(end2_elem, "topic")
    end2_topic_elem.set("id", end2.get("topicId", ""))

    # Add title
    if "title" in rel_data:
        title_elem = ET.SubElement(rel_elem, "title")
        title_elem.text = rel_data["title"]

    return rel_elem


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
    except ImportError as e:
        if "PIL" in str(e):
            print("Warning: PIL/Pillow not found, thumbnail will not be created")

            # 创建一个没有缩略图的简化版本
            def create_thumbnail():
                return b""  # 空缩略图

            convert_json_to_xmind(input_file, output_file)
        else:
            print(f"Error converting file: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Error converting file: {e}")
        sys.exit(1)
