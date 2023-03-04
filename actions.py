import network
import json

class ActionProcessor():
    def __init__(self, conn_obj, audio_file_path):
        self.conn = conn_obj
        self.tts = conn_obj.get_service("ALTextToSpeech")
        self.animation_player = conn_obj.get_service("ALAnimationPlayer")
        self.audio_file_path = audio_file_path

    def process_action(self):
        """
        Process an action based on the detected
        audible prompt of the user
        """

        dialogflow_resp = network.send_dialogflow_audio_recieve_response(audio_path=self.audio_file_path)
        print(dialogflow_resp)
        if(dialogflow_resp == None):
            self.animation_player.run("animations/Stand/Gestures/IDontKnow_1")
            self.tts.say("I didn't quite catch that")
            return
        prompt = dialogflow_resp[0]
        if(dialogflow_resp[1] == "smalltalk.greetings.hello"):
            self.animation_player.run("animations/Stand/Gestures/BowShort_1")
            self.tts.say(dialogflow_resp[2])
        else:
            openai_resp = network.send_openai_recieve_response(prompt=prompt)
            self.tts.say(openai_resp)
            