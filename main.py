import argparse, sys, socket
import json
#import _thread
from server import *
from client import *
from account import *
from shared import *
import threading
import select

def InitializeServer():

    # Dummy account details for the purpose of demo
    uid1 = 0
    uid2 = 1
    account_id = 0
    name1 = "Raj"
    name2 = "Kumar"
    email1 = "raj@gmail.com"
    email2 = "kumar@gmail.com"
    img_hash1 = "ff81a1818589bd00"
    img_hash2 = "ff8191818181bd00"

    user1 = User(uid1, account_id, name1, email1, img_hash1)
    user2 = User(uid2, account_id, name2, email2, img_hash2)

    users = []
    users.append(user1)
    users.append(user2)

    balance = 10000
    account = SharedAccount(account_id, balance, users)

    accounts = []
    accounts.append(account)

    server_obj = Server(accounts)

    return server_obj

def run_server():
    # Create a server object
    server = InitializeServer()

    # Create the socket
    print("Starting Server....")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 4000))
    s.listen(5)

    while True:
        # s.accept() is blocking
        conn, addr = s.accept()

        # Prints the IP and port of client when connected
        print('Connected to :', addr[0], ':', addr[1])

        # Start new thread for handling the client
        T = threading.Thread(target=handle_client, args=(conn,server,))
        T.start()

    # Close the socket when loop exits
    s.close()


def run_client(clientid: int, accountid: int):
    print("Starting Client....")

    # Create the socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Connect to the server
    s.connect(('', 4000))

    client = Client(s, accountid, clientid)

    # Send the ID of the user and their account
    packet = {
        "account_id": accountid,
        "client_id": clientid
    }

    send_data(packet, s)

    while True:
        print("Enter a choice:\n")
        print("1. Credit Amount\n")
        print("2. Debit Amount\n")
        print("3. View Balance\n")
        print("4. Exit\n")

        # The select statement is used to select between the data being read from the socket and stdin
        read_list, write_list, excep_list = select.select([s, sys.stdin], [], [])

        flag = False

        # Check the data that has been read
        for inp in read_list:
            if inp == s: # If input data is from the socket
                request = receive_data(s)
                flag = True
                print("Request received from server: ", request['type'])
                if request['type'] == 'balance_response':
                    if request['status'] == 'Authentication successful':
                        print("Available Balance: ", request['balance'])
                    else:
                        print("Request Denied")

                elif request['type'] == 'debit_response':
                    if request['status'] == 'Successful':
                        print("Available Balance after Debit: ", request['balance'])
                    else:
                        print("Request Denied")
                break
            elif inp == sys.stdin: # If input data is from the stdin of client
                user_input = sys.stdin.readline()
                print("user_input:", user_input)

        # Requests from the server are prioritized over user requests
        if flag == True:
            client.handle_client_request(request)
            continue

        # If there are no requests from the server, the user requests are executed
        if user_input == "1\n":
            client.initiate_request("credit")
        if user_input == "2\n":
            client.initiate_request("debit")
        if user_input == "3\n":
            client.initiate_request("view_request")
        if user_input == "4\n":
            sys.exit()



def main():
    # Let the user choose from the two procedures: server and client
    # This choice is done through the command line arguments

    help_description = "Welcome to the Shared Bank Account Management System"

    # Initialize parser
    parser = argparse.ArgumentParser(description=help_description)

    # Adding optional arguments
    parser.add_argument("-m", "--mode", help = "Select between the server and the client mode")
    parser.add_argument("-c", "--clientid", type=int, help = "Enter the client ID")
    parser.add_argument("-a", "--accountid", type=int, help = "Enter the account ID")

    # Read Arguments
    args = parser.parse_args()

    # If server process
    if args.mode == "server" or args.mode == "s" or args.mode == "Server" or args.mode == "S":
        run_server()
    elif args.mode == "client" or args.mode == "c" or args.mode == "Client" or args.mode == "C":
        if args.clientid >= 0 and args.accountid >= 0:
            run_client(args.clientid, args.accountid)
        else:
            print("Client ID or Account ID not specified or invalid")

if __name__=="__main__": 
    main()