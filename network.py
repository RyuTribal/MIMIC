"""
This file contains everything about 
communication with the open ai
api and other network related stuff
"""


import os
import requests
import json


URL = "https://api.openai.com/v1/completions"
HEADERS= {
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
    "OpenAI-Organization": os.getenv("OPENAI_API_ORG"),
    "Content-Type": "application/json"
}

def send_and_recieve_response(prompt):
    """
    This function sends the prompt to the 
    open ai api and recieves the response
    """
    data = {"model": "text-davinci-003", "temperature": 0, "max_tokens": 150, "prompt": ""}
    data["prompt"] = prompt

    response = requests.post(URL, data=json.dumps(data), headers=HEADERS, verify=False)
    return response
    
