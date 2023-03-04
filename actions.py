import network
import time
import threading

class ActionProcessor():
    def __init__(self, conn_obj, audio_file_path):
        self.conn = conn_obj
        self.tts = conn_obj.get_service("ALTextToSpeech")
        self.animation_player = conn_obj.get_service("ALAnimationPlayer")
        self.tablet_service = conn_obj.get_service("ALTabletService")
        self.tablet_service.enableWifi()
        self.audio_file_path = audio_file_path

    def process_action(self, talking_ev):
        """
        Process an action based on the detected
        audible prompt of the user
        """
        print("[ACTION]: Starting action")
        dialogflow_resp = network.send_dialogflow_audio_recieve_response(audio_path=self.audio_file_path)
        if(dialogflow_resp == None):
            animation_thread = threading.Thread(target=self.animation_player.run, args=("animations/Stand/Gestures/IDontKnow_1",))
            say_thread = threading.Thread(target=self.tts.say, args=("I didn't quite catch that",))
            animation_thread.start()
            say_thread.start()
            talking_ev.clear()
            return
        prompt = dialogflow_resp[0]
        print("[ACTION]: "+ dialogflow_resp[1])
        if(dialogflow_resp[1] == "smalltalk.greetings.hello"):
            animation_thread = threading.Thread(target=self.animation_player.run, args=("animations/Stand/Gestures/BowShort_1",))
            say_thread = threading.Thread(target=self.tts.say, args=(dialogflow_resp[2],))
            animation_thread.start()
            say_thread.start()
        elif(dialogflow_resp[1] == 'smalltalk.internet.google'):
            animation_thread = threading.Thread(target=self.animation_player.runTag, args=("affirmative",))
            say_thread = threading.Thread(target=self.tts.say, args=(dialogflow_resp[2],))
            animation_thread.start()
            say_thread.start()
            self.open_tablet_and_google(dialogflow_resp[3]['any'])
        else:
            openai_resp = network.send_openai_recieve_response(prompt=prompt)
            say_thread = threading.Thread(target=self.tts.say, args=(openai_resp,))
            say_thread.start()
        time.sleep(0.5)
        talking_ev.clear()



    def open_tablet_and_google(self, query):
        """
        This function is just for demonstration
        """
        query = query.replace(" ", "+")
        self.tablet_service.showWebview("https://www.google.com/search?q="+query)
            