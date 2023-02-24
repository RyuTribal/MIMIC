
import os

def load_env():
    dot_env = open(".env", "r")
    for line in dot_env.readlines():
        key_and_value = line.split('=')
        os.environ[key_and_value[0]] = key_and_value[1].replace("\n", "")


load_env()

import network

print(network.send_and_recieve_response("Hello mate!").json())
