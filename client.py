import json
import threading
from PIL import Image
from struct import pack
from shared import *
import numpy as np

class Client:

    def __init__(self, conn, account_id, client_id):
        self.conn = conn # Socket connection to server
        self.account_id = account_id # Account id 
        self.client_id = client_id  # Client id

    def handle_client_request(self, request):

        if request['type'] == 'partial_image':
            self.partial_img_request()
        elif request['type'] == 'approval':
            self.approval_request(request)

    # Function on client side to receive relevant details pertaining to a transaction
    def initiate_request(self, request_type):
        amt = 0
        if request_type == "credit" or request_type == "debit":
            print("Enter the amount:")
            amt = input()
        
        packet = {
            "type": request_type,
            "amt": amt,
            "account_id": self.account_id,
            "client_id": self.client_id
        }

        # Send packet from client to server 
        send_data(packet, self.conn)

    # Function to send partial image to the server on request by the server
    def partial_img_request(self):

        filename = "./testImages/part" + str(self.client_id+1) + ".jpg"
        img = Image.open(filename)

        img_str = json.dumps(np.array(img).tolist())

        packet = {
            "img": img_str,
            "account_id": self.account_id,
            "client_id": self.client_id
        }

        send_data(packet, self.conn)

    # Function to ask for verification of combined image to the client
    def approval_request(self, request):

        # Receive combined image and save it in client's directory
        img_bytes = request["img"].encode("latin1")
        img_object = Image.frombuffer(mode="1", data=img_bytes, size=(request['w'], request['h']))
        combined_filename = "./combined" + str(self.client_id) + ".jpg"

        img_object.save(combined_filename)

        # Prompt to client
        print("Combined image generated in the current directory.")
        print("Please verify whether it represents the original secret image.")

        print("Do you approve this request?\n")
        print("1. Yes")
        print("2. No")

        choice = input()

        if choice == '1':
            approval = "YES"
        elif choice == '2':
            approval = "NO"

        # Send approval packet
        packet = {
            "approval": approval,
            "account_id": self.account_id,
            "client_id": self.client_id
        }

        send_data(packet, self.conn)

        print("Please wait for all users to approve")

