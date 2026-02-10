# Advanced XMind Examples

## Complex Mind Map with Styling

```json
{
  "rootTopic": {
    "title": "Business Strategy",
    "structure": "org.xmind.ui.logic.right",
    "style": {
      "svgFill": "#2E86AB",
      "fo:font-weight": "bold",
      "fo:font-size": "20pt"
    },
    "children": {
      "attached": [
        {
          "title": "Marketing",
          "style": {
            "svgFill": "#A23B72"
          },
          "children": {
            "attached": [
              {
                "title": "Digital Campaigns",
                "markers": ["priority-1"]
              },
              {
                "title": "Content Strategy",
                "notes": {
                  "plain": "Focus on SEO and social media"
                }
              }
            ]
          }
        },
        {
          "title": "Operations",
          "style": {
            "svgFill": "#F18F01"
          },
          "children": {
            "attached": [
              {
                "title": "Process Optimization"
              },
              {
                "title": "Team Management"
              }
            ]
          }
        }
      ]
    }
  },
  "relationships": [
    {
      "id": "rel1",
      "end1": {
        "topicId": "marketing"
      },
      "end2": {
        "topicId": "operations"
      },
      "title": "collaborates with"
    }
  ]
}
```

## Fishbone Diagram

```json
{
  "rootTopic": {
    "title": "Problem Analysis",
    "structure": "org.xmind.ui.fishbone.right",
    "children": {
      "attached": [
        {
          "title": "People",
          "children": {
            "attached": [
              {
                "title": "Lack of Training"
              },
              {
                "title": "Staff Turnover"
              }
            ]
          }
        },
        {
          "title": "Process",
          "children": {
            "attached": [
              {
                "title": "Inefficient Workflow"
              },
              {
                "title": "Poor Documentation"
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Timeline Structure

```json
{
  "rootTopic": {
    "title": "Project Timeline",
    "structure": "org.xmind.ui.timeline.horizontal",
    "children": {
      "attached": [
        {
          "title": "Q1 2026",
          "children": {
            "attached": [
              {
                "title": "Research Phase",
                "labels": ["Completed"]
              }
            ]
          }
        },
        {
          "title": "Q2 2026",
          "children": {
            "attached": [
              {
                "title": "Development",
                "labels": ["In Progress"]
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Task Management Mind Map

```json
{
  "rootTopic": {
    "title": "Weekly Tasks",
    "structure": "org.xmind.ui.logic.right",
    "children": {
      "attached": [
        {
          "title": "Monday",
          "markers": ["task-start"],
          "children": {
            "attached": [
              {
                "title": "Team Meeting",
                "markers": ["flag-red"]
              },
              {
                "title": "Project Review",
                "notes": {
                  "plain": "Review Q1 progress with stakeholders"
                }
              }
            ]
          }
        },
        {
          "title": "Tuesday",
          "children": {
            "attached": [
              {
                "title": "Code Development",
                "markers": ["priority-1"]
              }
            ]
          }
        }
      ]
    }
  }
}
```
