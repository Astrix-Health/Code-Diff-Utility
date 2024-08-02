import os
import subprocess
import openai
import requests
import json


# Get environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
notion_api_key = os.getenv('NOTION_API_KEY')
notion_page_id = os.getenv('NOTION_PAGE_ID')

# Get the diff
result = subprocess.run(['git', 'diff', 'origin/main...HEAD'], stdout=subprocess.PIPE)
diff = result.stdout.decode('utf-8')

# Generate documentation using GPT-4
openai.api_key = openai_api_key
response = openai.Completion.create(
  engine="gpt-4o",
  prompt=f"Generate technical documentation for the following diff:\n\n{diff}\n\nDescription and Usage:",
  max_tokens=1500,
  n=1,
  stop=None,
  temperature=0.7
)
documentation = response.choices[0].text.strip()

# Create a Notion page
url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
data = {
    "parent": { "type": "page_id", "page_id": notion_page_id },
    "properties": {
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "PR Documentation"
                }
            }
        ]
    },
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": documentation
                        }
                    }
                ]
            }
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    print("Documentation successfully exported to Notion.")
else:
    print(f"Failed to export documentation to Notion. Status code: {response.status_code}")
    print(response.text)
