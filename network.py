"""
This file contains everything about 
communication with the open ai
api and other network related stuff
"""


import os
import json
import requests


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

    print("Sending to OpenAI with these parameters")
    print(data)
    print("And these headders")
    print(HEADERS)

    response = requests.post(URL, headers=HEADERS, json=data)
    return response
    
