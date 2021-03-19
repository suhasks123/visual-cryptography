import argparse, sys, socket
import json
#import _thread
from server import *
from client import *
import threading
import select

def run_server():
    # Create a server object
    server = Server()

    # Create the socket
    print("Starting Server....")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    s.connect('', 4000)

    client = Client(s)

    # Send the ID of the user and their account
    packet = {
        "account_id": accountid,
        "client_id": clientid
    }
    s.send(json.dumps(packet))

    # Create two events, one for the start of a transaction and one for end
    # transaction_start = threading.Event()
    # transaction_end = threading.Event()

    # input_thread = threading.Thread(target=take_input, args=(s,))
    # input_thread.start()

    while True:
        print("Enter a choice:\n")
        print("1. Credit Amount\n")
        print("2. Debit Amount\n")
        print("3. View Balance\n")
        print("4. Exit\n")

        # The select statement is used to select between the data being read from the socket and stdin
        read_list, write_list, excep_list = select.select([s, sys.stdin], [], [])

        request_json = ""

        # Check the data that has been read
        for inp in read_list:
            if inp == s:
                request_json = s.recv(1024)
                print("Request received from server")
                break
            elif inp == sys.stdin:
                user_input = sys.stdin.readline()

        # Requests from the server are prioritized over user requests
        if len(request_json) != 0:
            client.handle_client_request(request_json)
            continue

        # If there are no requests from the server, the user requests are executed
        if user_input == "1":
            client.initiate_request("credit")
        if user_input == "2":
            client.initiate_request("debit")
        if user_input == "3":
            client.initiate_request("view_request")
        if user_input == "4":
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
        if args.clientid > 0 and args.accountid > 0:
            run_client(args.clientid, args.accountid)
        else:
            print("Client ID or Account ID not specified or invalid")

if __name__=="__main__": 
    main()