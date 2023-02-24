
import qi
import sys
import os

class Connection():
    def __init__(self):
        self.ip = os.getenv("PEPPER_IP")
        self.port = os.getenv("PEPPER_PORT")
        self.user = os.getenv("PEPPER_USER")
        self.pword = os.getenv("PEPPER_PASSWORD")
        self.services = {}

        self.session = qi.Session()
        self.session.connect("tcp://{}:{}".format(self.ip, self.port))

        if self.session.isConnected():
            print("Connected!")
        else:
            print("Failed to connect!")
            sys.exit(-1)

    # All services gets stored in a cache, this lets us share services between all "modules"
    # which makes configuration easier.
    # Returns None if the module is not found.
    def get_service(self, name):
        if name not in self.services:
            print("Creating new instance of service and adding to cache")

            try:
                service = self.session.service(name)
            except:
                print("Failed to retrieve service {}".format(name))
                return None

            self.services[name] = service

        else:
            print("Service is in cache")

        return self.services[name]

if __name__ == "__main__":
    con = Connection()
