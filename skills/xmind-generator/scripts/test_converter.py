#!/usr/bin/env python3
"""
Test script for XMind converter
"""

import json
import os
import sys

# Add parent directory to path to import the converter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_test_json():
    """Create a test JSON file"""
    
    test_data = {
        "rootTopic": {
            "title": "Project Management",
            "structure": "org.xmind.ui.logic.right",
            "style": {
                "svgFill": "#2E86AB",
                "fo:font-weight": "bold",
                "fo:font-size": "20pt"
            },
            "children": {
                "attached": [
                    {
                        "title": "Planning",
                        "children": {
                            "attached": [
                                {
                                    "title": "Requirements"
                                },
                                {
                                    "title": "Timeline"
                                }
                            ]
                        }
                    },
                    {
                        "title": "Execution",
                        "children": {
                            "attached": [
                                {
                                    "title": "Development"
                                },
                                {
                                    "title": "Testing"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
    
    return test_data

def main():
    """Test the converter"""
    
    # Create test JSON
    test_data = create_test_json()
    
    # Save test JSON
    test_json_path = "test_data.json"
    with open(test_json_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created test JSON file: {test_json_path}")
    
    # Convert to XMind
    output_xmind_path = "test_output.xmind"
    
    try:
        from xmind_converter import convert_json_to_xmind
        convert_json_to_xmind(test_json_path, output_xmind_path)
        print(f"Successfully created XMind file: {output_xmind_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False
    
    # Verify file was created
    if os.path.exists(output_xmind_path):
        file_size = os.path.getsize(output_xmind_path)
        print(f"XMind file size: {file_size} bytes")
        return True
    else:
        print("XMind file was not created")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
