import network
import json

class ActionProcessor():
    def __init__(self, conn_obj, prompt):
        self.conn = conn_obj
        self.tts = conn_obj.get_service("ALTextToSpeech")
        self.prompt = prompt

    def process_action(self):
        open_ai_resp = network.send_and_recieve_response(self.prompt)
        response_arr = open_ai_resp.json()["choices"][0]["text"]
        self.tts.say(response_arr)