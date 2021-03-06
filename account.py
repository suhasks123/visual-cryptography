import json

from PIL import Image
import threading
import imagehash
from typing import *
from struct import unpack, pack
from shared import *
import numpy as np
import threading


class User:

    # Server side information about the clients -> users
    def __init__(self, uid, account_id, name, email, img_hash):
        self.uid = uid
        self.account_id = account_id
        self.name = name
        self.email = email
        self.img_hash = img_hash # Hash of the partial image assigned to each user
        self.conn = None

class SharedAccount:

    debit_lock = threading.Lock() # Mutex lock to prevent every thread from debiting the amount
    debit_done = False

    def __init__(self, account_id: int, balance: float, stakeholders: List[User]):
        self.id = account_id
        self.balance = balance
        self.stakeholders = stakeholders
        self.barrier_obj = threading.Barrier(len(stakeholders))

    # Server credit function
    def credit(self, request: Dict, client_id):
        self.balance = self.balance + int(request['amt'])
        print("Credit successful, balance: ", self.balance)

    # Server debit function
    def debit(self, request: Dict, client_id):
        if self.authenticate(client_id) == True: # If authenticated, then debit
            acquired = self.debit_lock.acquire(blocking=False)
            if self.balance - int(request['amt']) > 0:
                if acquired == True:
                    self.balance = self.balance - int(request['amt'])
                    self.debit_done = True
                    self.debit_lock.release()
            elif self.balance - int(request['amt']) < 0 and self.debit_done == False: # If debit amt > remaining balance
                print("Debit not successful")
                packet = {
                    'type': 'debit_response',
                    'status': 'Unsuccessful',
                    'balance': self.balance
                }
                send_data(packet, self.stakeholders[client_id].conn)
                return
            print("Debit successful")
            packet = {
                'type': 'debit_response',
                'status': 'Successful',
                'balance': self.balance
            }

            send_data(packet, self.stakeholders[client_id].conn)

    def view_balance(self, request: Dict, client_id):
        if self.authenticate(client_id) == True: # If authentication passes, then display balance
            packet = {
                'type': 'balance_response',
                'status': 'Authentication successful',
                'balance': self.balance
            }

            send_data(packet, self.stakeholders[client_id].conn)

        else:
            packet = {
                'type': 'balance_response',
                'status': 'Authentication failed'
            }

            send_data(packet, self.stakeholders[client_id].conn)
            print('Authentication failed')

    # Function to request user to send partial image
    def get_partial_image(self, user: User):
        packet = {
            'type' : "partial_image"
        }

        # Send request for partial image
        send_data(packet, user.conn)

        # Receive partial image
        response = receive_data(user.conn)

        img_object = Image.fromarray(np.array(json.loads(response['img']), dtype='uint8'))
        
        return img_object

    # Function to request user to verify combined image and send approval
    def get_approval(self, user, packet):

        send_data(packet, user.conn)

        # Wait for approval response
        # Approval Response
        response = receive_data(user.conn)

        self.barrier_obj.wait()
        
        if response["approval"] == "YES":
            return True
        elif response["approval"] == "NO":
            return False

    # Checking hash between the stored hash and the hash of the partial image provided by the user
    def check_hash(self, img_hash, user):
        return str(img_hash) == user.img_hash
    
    # Combine the partial images to display output image
    def combine(self):

        # Two input images
        input_images = []
        for i in range (len(self.stakeholders)):
            filename = "img" + str(self.stakeholders[i].uid) + ".jpg"
            img = Image.open(filename)
            input_images.append(img)

        outfile = Image.new('1', input_images[0].size)

        # Combine images
        for x in range(input_images[0].size[0]):
            for y in range(input_images[0].size[1]):
                outfile.putpixel((x, y), min(input_images[0].getpixel((x, y)), input_images[1].getpixel((x, y))))

        return outfile

    # Driver function to call above helper functions in the process of authentication
    def authenticate(self, uid):
        """
        Requests for the partial images from each user and receives them
        After receiving the images, it checks the hash for all the images
        :return:
        """
        # Get user id
        user = self.stakeholders[uid]

        img = self.get_partial_image(user)
        img_hash = imagehash.average_hash(img) # Produce hash of image provided by user

        if self.check_hash(img_hash, user) == False:
            print("Current hash:", str(img_hash))
            print("User hash:", user.img_hash)
            return False

        filename = "img" + str(uid) + ".jpg"    # Store partial image for combining
        img.save(filename)
        
        # Check for all threads
        # If all are done then combine()
        # Wait till all the partial images are obtained
        self.barrier_obj.wait()

        # Reset the barrier
        self.barrier_obj.reset()

        # Combine the images
        combined_img = self.combine()

        w, h = combined_img.size
        img_str = combined_img.tobytes().decode("latin1")

        packet = {
            "img": img_str,
            "w": w,
            "h": h,
            "type": "approval"
        }
        
        # Send combined image and request verification by use
        return self.get_approval(user, packet)

