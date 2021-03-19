from PIL import Image
import imagehash
# hash = imagehash.average_hash(Image.open('test.png'))
# print(hash)
from typing import *

class User:

    # The TCP connection associated with the user
    conn = None

    def __init__(self, uid, account_id, name, email, img_hash, ip, port):
        self.uid = uid
        self.account_id = account_id
        self.name = name
        self.email = email
        self.img_hash = img_hash
        self.ip = ip
        self.port = port
        
class SharedAccount:

    def __init__(self, id: int, balance: float, stakeholders: List[User]):
        self.id = id
        self.balance = balance
        self.stakeholders = stakeholders


    def credit(self, request: Dict):
        self.balance = self.balance + request['amt']
        print("Credit successful")

    def debit(self, request: Dict):
        self.authenticate(Dict.uid)
        print("Debit successful")
    
    def view_balance(self, request: Dict):
        self.authenticate(Dict.uid)
        print("The Account Balance is: ", self.balance)

    def get_partial_image(self, user: User):
        packet = {
            'type' = "partial_image"
        }
        user.conn.send(json.dumps(packet))
        response_json = user.conn.recv(65536)
        response = json.loads(response_json)

        img_bytes = response["img"].encode("latin1")
        img_object = Image.frombuffer(mode="1", data=img_bytes, size=(request['w'], request['h']))
        
        return img_object

    def get_approval(self, user):
        packet = {
            'type' = "approval"
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

        outfile = Image.new('1', infile1.size)

        # Combine images
        for x in range(img[0].size[0]):
            for y in range(img[0].size[1]):
                outfile.putpixel((x, y), min(img[0].getpixel((x, y)), img[1].getpixel((x, y))))

        # outfile.save("testImages/combined.png")
        return outfile

    def authenticate(self, uid):
        """
        Requests for the partial images from each user and receives them
        After receiveing the images, it checks the hash for all the images
        :return:
        """
        # i = 0
        # for user in self.stakeholders:
        #     i = i + 1
        user = self.stakeholders[uid]

        img = self.get_partial_image(user)
        img_hash = imagehash.average_hash(img)

        if self.check_hash(img_hash, user) == 0:
            raise Exception("The Hash From user dosent match")
            return False

        filename = "img" + str(uid)
        img.save(filename)
        #Check for all threads
        #If all are done then combine()
        
        while(allthreadsdone()==0):
        combined_img = combine()

        w, h = combined_img.size

        img_str = combined_img.tobytes().decode("latin1")

        packet = {
            "img": img_str,
            "width": w,
            "height": h
        }

        packet_json = json.dumps(packet)
        self.conn.send(packet_json)

        approved = self.get_approval(user)
        
        if approved == "YES":
            return True
        elif approved == "NO":
            return False






