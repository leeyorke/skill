# XMind JSON Format Documentation

This document describes the standard JSON format expected by the XMind Generator skill.

## Basic Structure

```json
{
  "rootTopic": {
    "title": "Central Topic",
    "structure": "org.xmind.ui.logic.right",
    "children": {
      "attached": [
        // Array of subtopics
      ]
    }
  }
}
```

## Topic Properties

### Required Properties
- `title`: The text content of the topic

### Optional Properties
- `structure`: Layout structure (e.g., "org.xmind.ui.logic.right", "org.xmind.ui.fishbone.right")
- `children`: Child topics
- `notes": Topic notes
- `labels": Array of labels
- `markers": Array of markers
- `style": Styling properties

## Example: Simple Mind Map

```json
{
  "rootTopic": {
    "title": "Project Plan",
    "structure": "org.xmind.ui.logic.right",
    "children": {
      "attached": [
        {
          "title": "Research",
          "children": {
            "attached": [
              {
                "title": "Market Analysis"
              },
              {
                "title": "Competitor Research"
              }
            ]
          }
        },
        {
          "title": "Development",
          "children": {
            "attached": [
              {
                "title": "Backend"
              },
              {
                "title": "Frontend"
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Styling

Topics can have style properties:

```json
{
  "title": "Important Topic",
  "style": {
    "svgFill": "#FF0000",
    "fo:font-weight": "bold",
    "fo:font-size": "18pt"
  }
}
```

## Relationships

Define connections between topics:

```json
{
  "relationships": [
    {
      "id": "rel1",
      "end1": {
        "topicId": "topic1"
      },
      "end2": {
        "topicId": "topic2"
      },
      "title": "depends on"
    }
  ]
}
```

## Notes

Add notes to topics:

```json
{
  "title": "Topic with Note",
  "notes": {
    "plain": "This is a detailed note about the topic."
  }
}
```

## Markers

Use markers for visual indicators:

```json
{
  "title": "High Priority",
  "markers": ["priority-1"]
}
```
