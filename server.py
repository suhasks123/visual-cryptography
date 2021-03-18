from account import *
import threading
import json
from typing import *

class Server:

    # The list of accounts is initially empty
    accounts = []

    def add_new_account(self, new_account: SharedAccount):
        self.accounts.append(new_account)

# Threads synchronization mechanism
is_transaction = False
transaction_lock = threading.Lock()

def handle_client(conn, server):

    initial_ids_json = conn.recv(1024)
    initial_ids = json.loads(initial_ids_json)

    while True:
        request_json = conn.recv(1024)
        transaction_lock.acquire(blocking=False)
        global is_transaction
        is_transaction = True
        request = json.loads(request_json)
        handle_request(request, server)
        is_transaction = False
        transaction_lock.release()

def handle_request(request: Dict, server: Server):
    if request['type'] == 'credit':
        server.accounts[request['account_id']].credit(request)
    elif request['type'] == 'debit':
        server.accounts[request['account_id']].debit(request)
    elif request['type'] == 'view_request':
        server.accounts[request['account_id']].view_balance(request)
