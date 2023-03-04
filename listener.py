"""
This file will contain everything to do with recording 
and processing input audio to pepper. 
"""


import json
import time
import paramiko
import os
from scp import SCPClient
import speech_recognition
from naoqi import ALModule, ALProxy
import wave
import network
import threading
import actions
import random
import logging



tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_files")
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)
    print("Created temporary folder MIMIC/tmp_files/ for retrieved data")



class Listener():
    """
    This class is a listener that uses our connection api.
    It sadly has some limitations which is why it shouldnt be used unless
    we find a good solution
    """
    def __init__(self, name, conn_obj):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(os.getenv("PEPPER_IP"), username=os.getenv("PEPPER_USER"), password=os.getenv("PEPPER_PASSWORD"))
        _stdin, _stdout,_stderr = ssh.exec_command("df")
        self.scp = SCPClient(ssh.get_transport())
        self.conn = conn_obj
        self.name = name
        self.audio_module = conn_obj.get_service("ALAudioDevice")
        self.memory_service = conn_obj.get_service("ALMemory")
        self.led_service = conn_obj.get_service("ALLeds")
        self.audio_recorder = conn_obj.get_service("ALAudioRecorder")
        self.awareness_service = conn_obj.get_service("ALBasicAwareness")
        self.speech_recognition_engine = conn_obj.get_service("ALSpeechRecognition")
        self.speech_recognition_engine.pause(True)
        self.speech_recognition_engine.setLanguage("English")
        print("[Availible languages]: " + ' '.join(self.speech_recognition_engine.getAvailableLanguages()))
        self.word_spotted_answers = ["Yes?", "How can I help you?", "What's up?"]
        self.is_answering = False
        self.is_speaking = False

        # Not really necessary to put any words in here, this is just to make
        # the speech recongnition engine work. We use it only for the speech detection
        # We could force it to listen to a phrase before it starts listening
        # kind of like alexa.
        vocab = ["pepper", "hey pepper", "stop", "shut up", "cancel", "haram"]
        self.speech_recognition_engine.setVocabulary(vocab, True)
        self.framesCount=0
        self.recording_in_progress = False

        self.tts = conn_obj.get_service("ALTextToSpeech")

        self.recognizer = speech_recognition.Recognizer()
        
    
    
    def wait_and_listen(self):
        talking_ev = threading.Event()
        while True:
            if(self.memory_service.getData("ALSpeechRecognition/Status") == "SpeechDetected"):
                spotted_word_arr = self.memory_service.getData("WordRecognized")
                if(spotted_word_arr[-1] > 0.5):
                    if 'pepper' in spotted_word_arr[0] and talking_ev.is_set() == False and self.memory_service.getData("ALTextToSpeech/TextStarted") != 1:
                        print("[WAITING THREAD]: Spotted the word Pepper")
                        talking_ev.set()
                        recording_thread = threading.Thread(target=self.start_recording, args=(talking_ev,))
                        recording_thread.start()
                    elif "stop" in spotted_word_arr[0] or "shut up" in spotted_word_arr[0] or "cancel" in spotted_word_arr[0] or "haram" in spotted_word_arr[0]:
                        print("[WAITING THREAD]: Stopping all actions")
                        self.tts.stopAll()
                        self.memory_service.insertData("ALTextToSpeech/TextStarted", 0)
                        talking_ev.clear()
                

    def start_recording(self, talking_ev):
        try:
            print("[RECORDING THREAD]: Starting recording process")
            self.audio_recorder.stopMicrophonesRecording()
            self.set_awareness(False)
            print("[RECORDING THREAD]: Robot is listening to you")
            self.tts.say(random.choice(self.word_spotted_answers))
            self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
            time.sleep(1)
            while self.is_speaking:
                time.sleep(0.5)

            self.audio_recorder.stopMicrophonesRecording()
            self.set_awareness(True)
            self.download_audio("speech.wav")
            action_obj = actions.ActionProcessor(conn_obj=self.conn, audio_file_path=os.path.join(tmp_path, "speech.wav"))
            action_obj.process_action(talking_ev=talking_ev)
        except:
            talking_ev.clear()
            

        

    def download_audio(self, file_name):
        self.scp.get(file_name, local_path=tmp_path)
        print("[INFO]: File " + file_name + " downloaded")
        self.scp.close()


    def set_awareness(self, on=True):
        """
        Turn on or off the basic awareness of the robot,
        e.g. looking for humans, self movements etc.
        :param state: If True set on, if False set off
        :type state: bool
        """
        if on is True:
            self.awareness_service.resumeAwareness()
            print("[INFO]: Awareness is turned on")
        else:
            self.awareness_service.pauseAwareness()
            print("[INFO]: Awareness is paused")

    
    def speech_to_text(self, audio_file, lang="en-US"):
        """
        Translate speech to text via Google Speech API
        :param audio_file: Name of the audio (default `speech.wav`)
        :param lang: Code of the language (e.g. "en-US", "cs-CZ")
        :type audio_file: string
        :return: Text of the speech
        :rtype: string
        """
        audio_source = speech_recognition.AudioFile(os.path.join(tmp_path, audio_file))
        try:
            with audio_source as source:
                audio = self.recognizer.record(source)
                recognized = self.recognizer.recognize_google(audio, language=lang)
            return recognized
        except speech_recognition.UnknownValueError:
            return None
        

        

    
    def blink_eyes(self, rgb):
        """
        Blink eyes with defined color
        :param rgb: Color in RGB space
        :type rgb: integer
        :Example:
        >>> pepper.blink_eyes([255, 0, 0])
        """
        self.led_service.fadeRGB('AllLeds', rgb[0], rgb[1], rgb[2], 1.0)

    def start_recognition(self):
        self.speech_recognition_engine.pause(False)
        self.speech_recognition_engine.subscribe(self.name)
        self.memory_service.insertData("ALTextToSpeech/TextStarted", 0)
        try:
            self.wait_and_listen()
        except KeyboardInterrupt:
            self.stop_recognition()

        
        

    def stop_recognition(self):
        self.speech_recognition_engine.unsubscribe(self.name)


    

        
