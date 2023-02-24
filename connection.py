
import qi
import sys

class Connection():
    def __init__(self):
        self.ip = "130.240.114.12"
        self.port = 9559
        self.user = "nao"
        self.pword = "PeppKs2mpH2Al!"
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
