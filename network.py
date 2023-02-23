"""
This file contains everything about 
communication with the open ai
api and other network related stuff
"""


import os
import json
import openai

OPENAI_PARAMS = {
    "engine": "davinci",
    "temperature": 0.9,
    "max_tokens": 150,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0.6,
    "stop": ["\n", " Human:", " AI:"]
}


def send_and_recieve_response(prompt):
    """
    This function sends the prompt to the 
    open ai api and recieves the response
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine=OPENAI_PARAMS["engine"],
        prompt=prompt,
        temperature=OPENAI_PARAMS["temperature"],
        max_tokens=OPENAI_PARAMS["max_tokens"],
        top_p=OPENAI_PARAMS["top_p"],
        frequency_penalty=OPENAI_PARAMS["frequency_penalty"],
        presence_penalty=OPENAI_PARAMS["presence_penalty"],
        stop=OPENAI_PARAMS["stop"]
    )
    return response
