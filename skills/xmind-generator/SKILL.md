---
name: xmind-generator
description: Generate .xmind mind map files from standard XMind JSON format. Use when Claude needs to create XMind mind map files from structured JSON data that represents mind map content, topics, relationships, and styling. This skill specifically handles conversion from XMind JSON format to .xmind file format.
---

# XMind Generator Skill

This skill generates .xmind mind map files from standard XMind JSON format. The skill accepts structured JSON data that represents mind map content and converts it into a valid .xmind file.

## Overview

XMind files are ZIP archives containing XML files and resources. This skill handles the conversion from JSON to the proper XMind file structure.

## Input Format

The skill expects JSON input in the standard XMind JSON format. This typically includes:

- Root topic and structure
- Topics and subtopics hierarchy
- Relationships between topics
- Styling information
- Notes and labels

See [xmind-json-format.md](references/xmind-json-format.md) for detailed JSON schema documentation.

## Usage

### Basic Usage

Provide the XMind JSON data as input to generate a .xmind file:

```json
{
  "rootTopic": {
    "title": "Main Topic",
    "children": [
      {
        "title": "Subtopic 1",
        "children": [...]
      }
    ]
  }
}
```

### Advanced Features

- **Styling**: Include style properties for topics and relationships
- **Notes**: Add notes to topics
- **Markers**: Use markers for priority, flags, etc.
- **Relationships**: Define connections between topics

For advanced usage patterns, see [advanced-examples.md](references/advanced-examples.md).

## Output

The skill generates a .xmind file that can be opened in XMind or other mind mapping software that supports the XMind format.

## Scripts

Use the main conversion script:

```bash
scripts/xmind_converter.py <input.json> <output.xmind>
```

This script handles the complete conversion process from JSON to .xmind file format.
