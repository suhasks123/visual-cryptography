import json

from PIL import Image
import threading
import imagehash
# hash = imagehash.average_hash(Image.open('test.png'))
# print(hash)
from typing import *

class User:

    # The TCP connection associated with the user
    conn = None

    def __init__(self, uid, account_id, name, email, img_hash):
        self.uid = uid
        self.account_id = account_id
        self.name = name
        self.email = email
        self.img_hash = img_hash

class SharedAccount:

    def __init__(self, id: int, balance: float, stakeholders: List[User]):
        self.id = id
        self.balance = balance
        self.stakeholders = stakeholders
        self.barrier_obj = threading.Barrier(stakeholders.size())


    def credit(self, request: Dict):
        self.balance = self.balance + request['amt']
        print("Credit successful")

    def debit(self, request: Dict):
        if self.authenticate(request['uid']) == True:
            if self.balance - request['amt'] > 0:
                self.balance = self.balance - request['amt']
            else:
                print("Debit not successful")
                return
            print("Debit successful")
            packet = {
                'type': 'response',
                'msg': 'Debit',
                'status': 'Successful'
            }
            self.stakeholders[request['uid']].conn.send(json.dumps(packet))

        else:
            print("Debit not successful")
    
    def view_balance(self, request: Dict):
        if self.authenticate(request['uid']) == True:
            packet = {
                'type': 'response',
                'msg': 'Balance',
                'balance': self.balance
            }
            self.stakeholders[request['uid']].conn.send(json.dumps(packet))
        else:
            print('Authentication failed')


    def get_partial_image(self, user: User):
        packet = {
            'type' : "partial_image"
        }
        user.conn.send(json.dumps(packet))
        response_json = user.conn.recv(65536)
        response = json.loads(response_json)

        img_bytes = response["img"].encode("latin1")
        img_object = Image.frombuffer(mode="1", data=img_bytes, size=(response['w'], response['h']))
        
        return img_object

    def get_approval(self, user):
        packet = {
            'type' : "approval"
        }
        user.conn.send(json.dumps(packet))
        response_json = user.conn.recv(65536)
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
        user.conn.send(packet_json)

        approved = self.get_approval(user)
        
        if approved == "YES":
            return True
        elif approved == "NO":
            return False






