"""
This file will contain everything to do with recording 
and processing input audio to pepper. 
"""


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

        # Not really necessary to put any words in here, this is just to make
        # the speech recongnition engine work. We use it only for the speech detection
        # We could force it to listen to a phrase before it starts listening
        # kind of like alexa.
        vocab = ["yes", "no"]
        self.speech_recognition_engine.setVocabulary(vocab, True)
        self.framesCount=0
        self.recording_in_progress = False

        self.tts = conn_obj.get_service("ALTextToSpeech")

        self.recognizer = speech_recognition.Recognizer()
        
    

    def listen(self):
        while True:
            print(self.memory_service.getData("ALSpeechRecognition/Status"))
            if self.recording_in_progress:
                continue
            elif self.memory_service.getData("ALSpeechRecognition/Status") != "SpeechDetected":
                continue
            self.audio_recorder.stopMicrophonesRecording()
            self.set_awareness(False)
            print("[INFO]: Robot is listening to you")
            if(self.memory_service.getData("ALSpeechRecognition/Status") != "SpeechDetected"):
                self.set_awareness(True)
                continue
            self.tts.say("Yes?")
            self.recording_in_progress = True
            self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
            #self.blink_eyes([255, 255, 0])
            while True:
                time.sleep(1)
                if self.memory_service.getData("ALSpeechRecognition/Status") != "SpeechDetected":
                    time.sleep(0.5)
                    if self.memory_service.getData("ALSpeechRecognition/Status") != "SpeechDetected":
                        break

            self.audio_recorder.stopMicrophonesRecording()
            self.set_awareness(True)

            self.download_audio("speech.wav")
            prompt = self.speech_to_text(audio_file="speech.wav")
            if prompt:
                print("[INFO]: Heard " + prompt)
                action_obj = actions.ActionProcessor(conn_obj=self.conn, prompt=prompt)
                action_obj.process_action()
            self.recording_in_progress = False
            time.sleep(1)
            

        

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
        try:
            self.listen()
        except KeyboardInterrupt:
            self.stop_recognition()

        
        

    def stop_recognition(self):
        self.speech_recognition_engine.unsubscribe(self.name)


    

        
