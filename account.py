from typing import *

class SharedAccount:

    def __init__(self, id: int, balance: float, stakeholders: List[User]):
        self.id = id
        self.balance = balance
        self.stakeholders = stakeholders

    def credit(self, request: Dict):
        print("credit")

    def debit(self, request: Dict):
        print("debit")
    
    def view_balance(self, request: Dict):
        print("view_balance")

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
