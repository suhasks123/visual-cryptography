import json
import threading

class Client:

    def __init__(self, conn, listen_thread, request_thread):
        self.conn = conn
        self.listen_thread = listen_thread
        self.request_thread = request_thread
    

def handle_client_request(request_json):
    request = json.loads(request_json)

    if request['type'] == 'partial_image':
        print("Request for partial image")
    elif request['type'] == 'approval':
        print("Request for approval")

def initiate_request(request_type):
    print(request_type)