import json
import threading

class Client:

    def __init__(self, conn, listen_thread, request_thread):
        self.conn = conn
        self.listen_thread = listen_thread
        self.request_thread = request_thread
    

def listen_for_requests(conn):
    while True:
        request_json = conn.recv(1024)

        # Send main thread to background
        main_t = threading.main_thread()

        # Convert message to dictionary
        request = json.loads(request_json)

        if request['type'] == 'partial_image':
            print("Request for partial image")
        elif request['type'] == 'approval':
            print("Request for approval")

