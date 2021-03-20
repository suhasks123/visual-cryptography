from account import *
import threading
import json
from typing import *

class Server:

    def __init__(self, accounts):
        self.accounts = accounts
        self.current_request = None

# Threads synchronization mechanism
is_transaction = False
transaction_lock = threading.Lock()

def handle_client(conn, server):

    # Receiving huge files is done in chunks
    data_length_bin = conn.recv(8)
    (data_length,) = unpack('>Q', data_length_bin)
    initial_ids_json_bin = b''
    while len(initial_ids_json_bin) < data_length:
        to_read = data_length - len(initial_ids_json_bin)
        initial_ids_json_bin += conn.recv(4096 if to_read > 4096 else to_read)

    initial_ids_json = initial_ids_json_bin.decode('utf-8')
    print("Initial IDs packet received: ", initial_ids_json)
    initial_ids = json.loads(initial_ids_json)

    server.accounts[initial_ids['account_id']].stakeholders[initial_ids['client_id']].conn = conn

    while True:
        #request_json_bin = ""
        # Receiving huge files is done in chunks
        data_length_bin = conn.recv(8)
        (data_length,) = unpack('>Q', data_length_bin)
        request_json_bin = b''
        while len(request_json_bin) < data_length:
            to_read = data_length - len(request_json_bin)
            request_json_bin += conn.recv(4096 if to_read > 4096 else to_read)

        request_json = request_json_bin.decode('utf-8')
        print("Request packet received: ", request_json)
        transaction_lock.acquire(blocking=False)
        global is_transaction
        is_transaction = True
        request = json.loads(request_json)
        handle_server_request(request, server, initial_ids['account_id'], initial_ids['client_id'])
        is_transaction = False
        transaction_lock.release()

def handle_server_request(request: Dict, server: Server, account_id, client_id):
    if request['type'] == 'credit':
        server.accounts[request['account_id']].credit(request)
    elif request['type'] == 'debit':
        server.accounts[request['account_id']].debit(request)
    elif request['type'] == 'view_request':
        server.accounts[request['account_id']].view_balance(request)
