import json
import threading
from PIL import Image

class Client:

    def __init__(self, conn, account_id, client_id):
        self.conn = conn
        self.account_id = account_id
        self.client_id = client_id

    def handle_client_request(self, request_json):
        request = json.loads(request_json)

        if request['type'] == 'partial_image':
            self.partial_img_request()
        elif request['type'] == 'approval':
            self.approval_request(request)

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

        self.conn.send(json.dumps(packet))

    def partial_img_request(self):
        img = Image.open('./partial.png')

        w, h = img.size

        img_str = img.tobytes().decode("latin1")

        packet = {
            "img": img_str,
            "width": w,
            "height": h,
            "account_id": self.account_id,
            "client_id": self.client_id
        }

        packet_json = json.dumps(packet)

        self.conn.send(packet_json)

    def approval_request(self, request):

        img_bytes = request["img"].encode("latin1")

        img_object = Image.frombuffer(mode="1", data=img_bytes, size=(request['w'], request['h']))

        img_object.save("combined.png")

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

        packet = {
            "approval": approval,
            "account_id": self.account_id,
            "client_id": self.client_id
        }

        self.conn.send(json.dumps(packet))
