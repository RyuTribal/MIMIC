# -*- coding: future_fstrings -*-
import os
import subprocess
import threading
from naoqi import ALBroker

def load_env():
    dot_env = open(".env", "r")
    for line in dot_env.readlines():
        key_and_value = line.split('=')
        os.environ[key_and_value[0]] = key_and_value[1].replace("\n", "")

if __name__ == "__main__":
    load_env()

    import connection
    import listener

    con = connection.Connection()
      
    Listener = listener.Listener("Pepper_Listener_Module", con)

    Listener.start_recognition()

    Listener.stop_recognition()
    # spoken_word = Listener.listen()
    # print(spoken_word)



