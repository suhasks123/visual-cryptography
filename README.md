# Shared Bank Account Management System

## About:
This application uses Visual Cryptography to implement a management system for a shared bank account.

A shared bank account can be modified only when all the concerned entities agree on the transaction. This makes use of visual cryptography to split a shared password among all the maintainers of the account and the bank server. In this way, no transactions can happen unless everyone approves it. This is a form of strong consensus to make sure the security and integrity of the data is maintained.

This is a course project for Cryptography and Applications Lab(CS352) taught by Dr. Alwyn Roshan Pais, Department of Computer Science and Engineering.

## Contributors:
- Suhas K S (181CO253).
- Sai Krishna Anand (181CO244).
- Aditya Chandrashekhar Sohoni (181CO203).

## Python dependencies: (Apart from the inbuilt libraries)
- PIL
- Imagehash
- json
- select

## Instructions to execute: 
The current implementation consists of a shared account between 2 users only. Open 3 terminals(Linux or even WSL) and run the following :

- For server : python3 main.py -m s
- For user 1 : python3 main.py -m c -c 0 -a 0
- For user 2 : python3 main.py -m c -c 1 -a 0

Note : The client ids must begin from 0, hence the commands.
