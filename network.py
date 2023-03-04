"""
This file contains everything about 
communication with the open ai
api and other network related stuff
"""


import os
import requests
import json
from google.oauth2 import service_account
import google.auth
import google.oauth2
import google.auth.transport.requests
import wave
import base64
from requests.exceptions import HTTPError


OPEN_AI_URL = "https://api.openai.com/v1/completions"
OPEN_AI_HEADERS= {
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
    "OpenAI-Organization": os.getenv("OPENAI_API_ORG"),
    "Content-Type": "application/json"
}

BASE_PROMPT = """This AI is inside a Pepper and will be reffered to by the name Pepper.
It is helpful, creative, clever, and very friendly.

Person:Could you tell me the time?
Pepper:The current time is 13:32

"""

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT")

DIALOGFLOW_URL = "https://global-dialogflow.googleapis.com/v2/projects/"+PROJECT_ID+"/agent/sessions/-:detectIntent"


def send_openai_recieve_response(prompt):
    """ 
    This function sends the prompt to the 
    openai api and recieves the response.
    """


    



    data = {"model": "text-davinci-003", "temperature": 0.9, "max_tokens": 150, "prompt": ""}
    data["prompt"] = "Person:"+prompt+"\nPepper:"

    response = requests.post(OPEN_AI_URL, data=json.dumps(data), headers=OPEN_AI_HEADERS, verify=False)
    return response.json()["choices"][0]["text"]


def send_dialogflow_audio_recieve_response(audio_path):
    """
    This function take a path to an audio file instead,
    sends it to dialogflow and waits for a response
    """


    creds = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])[0]

    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    audio_file_bytes = open(audio_path, "rb").read()

    dialog_bot_query = {
        "queryInput":{
            "audioConfig":{
                "audioEncoding": "AUDIO_ENCODING_LINEAR_16",
                "sampleRateHertz": 48000,
                "languageCode": "en"
            }
        },
        "inputAudio": base64.b64encode(audio_file_bytes)
        
    }
    try:
        response = requests.post(DIALOGFLOW_URL, data=json.dumps(dialog_bot_query), headers={
            "Authorization": "Bearer "+creds.token
        })
        response = response.json()
        if "queryText" in response["queryResult"]:
            return (response["queryResult"]["queryText"], response["queryResult"]["intent"]['displayName'], response['queryResult']['fulfillmentText'])
        else:
            return None
    except HTTPError as e:
        return e.response.text

def send_dialogflow_recieve_response(prompt):
    """
    This function sends the prompt to the 
    dialogflow api and recieves the response.
    """


    creds = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])[0]

    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    audio_file_path = 'tmp_files/speech.wav'

    audio_file_bytes = open(audio_file_path, "rb").read()

    dialog_bot_query = {
        "queryInput": {
            "outputAudioConfig": {
                "sampleRateHertz": 48000
            }
        },
        "inputAudio": audio_file_bytes
    }

    dialog_bot_query = {
        "queryInput": {
            "text": {
                "languageCode": "en",
                "text": prompt
            }
        }
    }

    response = requests.post(DIALOGFLOW_URL, data=json.dumps(dialog_bot_query), headers={
        "Authorization": "Bearer "+creds.token
    })

    response = response.json()

    return (response["queryResult"]["intent"]['displayName'], response['queryResult']['fulfillmentText'])
    

if __name__ == "__main__":
    resp = send_dialogflow_audio_recieve_response("tmp_files/speech.wav")
    print(resp)
