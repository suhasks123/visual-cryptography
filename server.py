from account import *
import threading
import json
from typing import *
import select

class Server:

    def __init__(self, accounts):
        self.accounts = accounts
        self.current_request = None

# Threads synchronization mechanism
is_transaction = False
transaction_lock = threading.Lock()

def handle_client(conn, server):

    # Receive the initial_ids
    initial_ids = receive_data(conn)

    print("Initial IDs packet received: ", initial_ids)

    server.accounts[initial_ids['account_id']].stakeholders[initial_ids['client_id']].conn = conn

    while True:
        #request_json_bin = ""
        read_list, write_list, excep_list = select.select([conn], [], [], 0.5)
        for inp in read_list:

            # If data is received through the packet
            if inp == conn:

                # Receiving huge files is done in chunks
                request = receive_data(conn)

                print("Request packet received: ", request)
                transaction_lock.acquire(blocking=False)
                global is_transaction
                is_transaction = True
                server.current_request = request
                handle_server_request(request, server, initial_ids['account_id'], initial_ids['client_id'])
                is_transaction = False
                transaction_lock.release()
                server.current_request = None

        if is_transaction == True and server.current_request != None:
            print("Request packet received: ", server.current_request)
            handle_server_request(server.current_request, server, initial_ids['account_id'], initial_ids['client_id'])

def handle_server_request(request: Dict, server: Server, account_id, client_id):
    if request['type'] == 'credit':
        server.accounts[request['account_id']].credit(request, client_id)
    elif request['type'] == 'debit':
        server.accounts[request['account_id']].debit(request, client_id)
    elif request['type'] == 'view_request':
        server.accounts[request['account_id']].view_balance(request, client_id)
