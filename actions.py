import network
import json

class ActionProcessor():
    def __init__(self, conn_obj, prompt):
        self.conn = conn_obj
        self.tts = conn_obj.get_service("ALTextToSpeech")
        self.animation_player = conn_obj.get_service("ALAnimationPlayer")
        self.prompt = prompt

    def process_action(self):
        """
        Process an action based on the detected
        audible prompt of the user
        """

        dialogflow_resp = network.send_dialogflow_recieve_response(self.prompt)
        if(dialogflow_resp[0] == "smalltalk.greetings.hello"):
            self.animation_player.run("animations/Stand/Gestures/BowShort_1")
            self.tts.say(dialogflow_resp[1])
        else:
            openai_resp = network.send_openai_recieve_response(self.prompt)
            self.tts.say(openai_resp)
            