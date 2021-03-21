from account import *
import threading
import json
from typing import *
import select

class Server:

    def __init__(self, accounts):
        self.accounts = accounts # List of all accounts
        self.current_request = None # Variable to check if a request has been made by some client

# Threads synchronization mechanism
is_transaction = False
transaction_lock = threading.Lock()

def handle_client(conn, server):

    # Receive the initial_ids
    initial_ids = receive_data(conn)

    print("Initial IDs packet received: ", initial_ids)

    # Initialize connection between the client and server
    server.accounts[initial_ids['account_id']].stakeholders[initial_ids['client_id']].conn = conn

    while True:
        #request_json_bin = ""
        # Wait for input from socket with a timeout of 0.5 seconds
        read_list, write_list, excep_list = select.select([conn], [], [], 0.5)
        for inp in read_list:

            # If data is received through the packet
            if inp == conn:

                # Receiving huge files is done in chunks
                request = receive_data(conn)

                print("Request packet received: ", request)
                transaction_lock.acquire(blocking=False) # Acquire lock, 1 request at a time only
                global is_transaction
                is_transaction = True
                server.current_request = request # Update server's currently executing request
                handle_server_request(request, server, initial_ids['account_id'], initial_ids['client_id'])
                is_transaction = False  
                transaction_lock.release() # Release lock
                server.current_request = None

        if is_transaction == True and server.current_request != None: # If no data through socket for 0.5 seconds, check if another client has made request.
            print("Request packet received: ", server.current_request)
            handle_server_request(server.current_request, server, initial_ids['account_id'], initial_ids['client_id'])

def handle_server_request(request: Dict, server: Server, account_id, client_id):
    # Handler function depending on client transaction type 
    if request['type'] == 'credit':
        server.accounts[request['account_id']].credit(request, client_id)
    elif request['type'] == 'debit':
        server.debit_done = False
        server.accounts[request['account_id']].debit(request, client_id)
    elif request['type'] == 'view_request':
        server.accounts[request['account_id']].view_balance(request, client_id)
