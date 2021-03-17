import argparse, sys, socket
import json
#import _thread
from .server import *
from .client import *
import threading

def run_server():
    # Create a server object
    server = Server()

    # Create the socket
    print("Starting Server....")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', '4000'))
    s.listen(5)

    while True:
        # s.accept() is blocking
        conn, addr = s.accept()

        # Prints the IP and port of client when connected
        print('Connected to :', addr[0], ':', addr[1])

        # Start new thread for handling the client
        T = threading.Thread(target=handle_client, args=(conn,))
        T.start()

    # Close the socket when loop exits
    s.close()


def run_client(clientid: int, accountid: int):
    print("Starting Client....")

    # Create the socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Connect to the server
    s.connect('', '4000')

    # Send the ID of the user and their account
    packet = {
        "accountid": accountid,
        "clientid": clientid
    }
    s.send(json.dumps(packet))

    listen_thread = threading.Thread(target=listen_for_requests, args=(s,))
    listen_thread.start()

    # Store this thread and the main thread in the Client object



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
