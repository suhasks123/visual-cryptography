from PIL import Image
import imagehash
# hash = imagehash.average_hash(Image.open('test.png'))
# print(hash)
from typing import *

class User:

    # The TCP connection associated with the user
    conn = None

    def __init__(self, uid, name, email, img_hash, ip, port):
        self.uid = uid
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
        print("credit")

    def debit(self, request: Dict):
        # self.authenticate(Dict.uid)
        #
        # print("debit")
    
    def view_balance(self, request: Dict):
        print("view_balance")

    def get_partial_image(self, user: User):
        #Use socket to get partial image
        #return it

    def get_approval(self, user):


    def check_hash(self, img_hash, user):
        return img_hash == user.img_hash

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

        approved = self.get_approval(user)

        return True







