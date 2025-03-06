import requests
import json


context=""" i am giving you a complent that is "there was a bus driver driving rushly" give priority for the department to perform execution on it  like is it an emergency, moderate or less priority"""
def chat(context):
    url = "http://127.0.0.1:5070/predict"  # Your local server endpoint
    headers = {"Content-Type": "application/json"} 
    data = {"prompt": context}  # JSON payload

    # Sending POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Printing the response
    code="Status Code:", response.status_code
    return response.json()["output"]
print(chat(context))
