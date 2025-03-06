import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.2",  # Change to the model you want
    "prompt": ''' ['Police Department','Cyber Crime Department','Women Helpline','Fire Department','Consumer Protection Department','Child Welfare Department','Traffic Police Department','Social Welfare Department','Disaster Management','Anti-Corruption Bureau','Human Right Department','Muncipal Coporation Department']''',
    "stream": False  # Set to False to get full JSON response
}

response = requests.post(url, json=payload)

try:
    # Parse JSON response correctly
    result = response.json()
    print(result.get("response", "No response found"))
except requests.exceptions.JSONDecodeError as e:
    print("JSON Decode Error:", e)
    print("Raw Response:", response.text)
