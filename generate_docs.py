import os
import subprocess
from openai import OpenAI
import requests
import json

# Get environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
notion_api_key = os.getenv('NOTION_API_KEY')
notion_page_id = os.getenv('NOTION_PAGE_ID')

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Get the diff
result = subprocess.run(['git', 'diff', 'HEAD~1'], stdout=subprocess.PIPE)
diff = result.stdout.decode('utf-8')
print(diff)

# Generate documentation using GPT-4
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Generate technical documentation for the following diff:\n\n{diff}\n\nDescription and Usage:"}
    ]
)

# Extract the generated documentation
documentation = completion.choices[0].message.content.strip()

# Split documentation into chunks of 2000 characters or less
def split_text(text, max_length=2000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

chunks = split_text(documentation)

# Create Notion page with the split chunks
url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

children = []
for chunk in chunks:
    children.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "text": [
                {
                    "type": "text",
                    "text": {
                        "content": chunk
                    }
                }
            ]
        }
    })

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
    "children": children
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    print("Documentation successfully exported to Notion.")
else:
    print(f"Failed to export documentation to Notion. Status code: {response.status_code}")
    print(response.text)
