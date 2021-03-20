import json

from PIL import Image
import threading
import imagehash
from typing import *

class User:

    def __init__(self, uid, account_id, name, email, img_hash):
        self.uid = uid
        self.account_id = account_id
        self.name = name
        self.email = email
        self.img_hash = img_hash
        self.conn = None

class SharedAccount:

    def __init__(self, account_id: int, balance: float, stakeholders: List[User]):
        self.id = account_id
        self.balance = balance
        self.stakeholders = stakeholders
        self.barrier_obj = threading.Barrier(len(stakeholders))


    def credit(self, request: Dict):
        self.balance = self.balance + int(request['amt'])
        print("Credit successful, balance: ", self.balance)

    def debit(self, request: Dict):
        if self.authenticate(request['client_id']) == True:
            if self.balance - request['amt'] > 0:
                self.balance = self.balance - int(request['amt'])
            else:
                print("Debit not successful")
                return
            print("Debit successful")
            packet = {
                'type': 'response',
                'msg': 'Debit',
                'status': 'Successful'
            }
            packet_json = json.dumps(packet)

            to_send = packet_json.encode('utf-8')

            self.stakeholders[request['client_id']].conn.send(to_send)

        else:
            print("Debit not successful")
    
    def view_balance(self, request: Dict):
        if self.authenticate(request['client_id']) == True:
            packet = {
                'type': 'response',
                'msg': 'Balance',
                'balance': self.balance
            }

            packet_json = json.dumps(packet)

            to_send = packet_json.encode('utf-8')

            self.stakeholders[request['client_id']].conn.send(to_send)
        else:
            print('Authentication failed')


    def get_partial_image(self, user: User):
        packet = {
            'type' : "partial_image"
        }
        packet_json = json.dumps(packet)
        to_send = packet_json.encode('utf-8')
        user.conn.send(to_send) 

        response_json_bin = user.conn.recv(524288)
        response_json = response_json_bin.decode('utf-8')
        # f = open("debug.txt", "w")
        # f.write(response_json)
        response = json.loads(response_json)

        img_bytes = response["img"].encode("latin1")
        img_object = Image.frombuffer(mode="1", data=img_bytes, size=(response['w'], response['h']))
        
        return img_object

    def get_approval(self, user):
        packet = {
            'type' : "approval"
        }
        packet_json = json.dumps(packet)
        to_send = packet_json.encode('utf-8')
        user.conn.send(to_send)
        response_json_bin = user.conn.recv(524288)
        response_json = response_json_bin.decode('utf-8')
        response = json.loads(response_json)

        return response["approval"]

    def check_hash(self, img_hash, user):
        return img_hash == user.img_hash
    
    def combine(self):

        # Two input images
        input_images = []
        for i in range (self.stakeholders.size):
            filename = "img" + self.stakeholders[i].uid
            img = Image.open(filename)
            input_images.append(img)

        outfile = Image.new('1', input_images[0].size)

        # Combine images
        for x in range(input_images[0].size[0]):
            for y in range(input_images[0].size[1]):
                outfile.putpixel((x, y), min(input_images[0].getpixel((x, y)), input_images[1].getpixel((x, y))))

        return outfile

    def authenticate(self, uid):
        """
        Requests for the partial images from each user and receives them
        After receiveing the images, it checks the hash for all the images
        :return:
        """

        user = self.stakeholders[uid]

        img = self.get_partial_image(user)
        img_hash = imagehash.average_hash(img)

        if self.check_hash(img_hash, user) == 0:
            raise Exception("The Hash From user dosent match")

        filename = "img" + str(uid)
        img.save(filename)
        
        # Check for all threads
        # If all are done then combine()
        # Wait till all the partial images are obtained
        self.barrier_obj.wait()

        # Combine the images
        combined_img = self.combine()

        w, h = combined_img.size

        img_str = combined_img.tobytes().decode("latin1")

        packet = {
            "img": img_str,
            "width": w,
            "height": h
        }

        packet_json = json.dumps(packet)
        to_send = packet_json.encode('utf-8')
        user.conn.send(to_send)

        approved = self.get_approval(user)
        
        if approved == "YES":
            return True
        elif approved == "NO":
            return False






