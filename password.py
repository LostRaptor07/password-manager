import csv

import hashlib

import getpass

import os
if not os.path.exists('passwords.csv'):
    with open('passwords.csv', 'w', newline='') as f:
        pass


import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
   

def info_collector():
    service_1= encrypter(input("What is the name of the service: ").strip()).decode()
    username_1= encrypter(input("What is the username you are using: ").strip()).decode()
    password_1= encrypter(input("What password are you setting: ").strip()).decode()

    passwords_d = {
        "service":service_1,
        "username":username_1,
        "password":password_1
    }
    return passwords_d


def info_writer():
    with open('passwords.csv','a',newline='') as csvfile:
        fieldnames = ['service','username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writerow(info_collector())

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def info_reader():
    with open('passwords.csv','r') as csvfile:
        fieldnames = ['service','username', 'password']
        data_list = list(csv.DictReader(csvfile,fieldnames= fieldnames))


        while True:
            mode_1 = input("What would you like to search for(service/username/exit): ").lower().strip()
            
            if mode_1 == "service":
                service_2 = input("What service: ").lower().strip()
                found = False
                
                for row in data_list:
                    if decrypter(row['service']) == service_2:
                        found = True
                        if found:
                            print(f"Service: {decrypter(row['service'])}, User: {decrypter(row['username'])}, Password: {decrypter(row['password'])}")
                            input("\nPress Enter to hide this sensitive info...")
                            clear_screen()
                
                if not found:
                    print(decrypter(row['service']).lower())
                    print("No such service found try agian or try listing")
            
            
            elif mode_1 == "username":
                username_2 = input("What username: ").strip()
                found = False


                for row in data_list:
                    if decrypter(row['username'])== username_2:
                        found = True
                        if found:
                            print(f"Service: {decrypter(row['service'])}, User: {decrypter(row['username'])}, Password: {decrypter(row['password'])}")
                            input("\nPress Enter to hide this sensitive info...")
                            clear_screen()
                
                if not found:
                    print("No such username found try agian or try listing")
            
            elif mode_1 == "exit":
                return False
            else:
                print("Wrong Input try again")



def info_lister():
    with open('passwords.csv','r') as csvfile:
        fieldnames = ['service','username', 'password']
        reader = csv.DictReader(csvfile,fieldnames= fieldnames)
        
        
        for row in reader:
            print(f"{decrypter(row['service'])}, {decrypter(row['username'])} , {decrypter(row['password'])}")
   


def main():
    while True:
        mode = input("what do you want to do? (read/write/list/exit): ").lower()
        
        
        if mode == "write":
            info_writer()
        elif mode == "read":
            info_reader()
        elif mode =="list":
            info_lister()
        elif mode =="exit":
            print("Thnak You")
            exit()
        else:
            print("wrong input , try again")
    


def login():
    if master_password: 
        main()
        exit()



def hasher(strng):
    strng_bytes= strng.encode()
    hashed = hashlib.sha256(strng_bytes)

    return hashed.hexdigest()




def set_master_password(anything):
    with open('master_password.txt','a') as f:
        f.write(hasher(anything))
        print("Master password set successfully!")



def get_salt():
    salt = os.urandom(16)
    with open('salt.bin', 'wb') as f:
        f.write(salt)

def fernet_key():
    if not os.path.exists('salt.bin'):
        get_salt()

    with open('salt.bin','rb' ) as salt_bin:
        salt = salt_bin.read()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,        
        iterations=480000,
    )

    raw_key = kdf.derive(master_password.encode())

    final_key = base64.urlsafe_b64encode(raw_key)

    return final_key
    


def encrypter(new_data):
    engine = Fernet(key)
    new_data_encrypted = new_data.encode()
    token = engine.encrypt(new_data_encrypted)
    return token
    

def decrypter(previous_data):
    engine = Fernet(key)
    original = engine.decrypt(previous_data.encode()).decode()
    return original


def get_master_password():
    if not os.path.exists("master_password.txt"):
        print("Welcome set a master_password: ")
        initial_master_password = getpass.getpass("Enter the master password")
        confirm_second = getpass.getpass("Enter again to confirm: ")
        if initial_master_password == confirm_second:
            set_master_password(confirm_second)
            master_password_1 = confirm_second
            return master_password_1
        else:
            print("your password didn't match, restarting ... ")
            return get_master_password()
    else :
        master_password_1 = getpass.getpass("Enter Master Password: ")
        hashed_password_1 = hasher(master_password_1)
        with open('master_password.txt','r') as f:
            stored_hash = f.read().strip()
            if stored_hash == hashed_password_1:
                return master_password_1
            else:
                print("Try Again")
                return get_master_password()


master_password = get_master_password()

key = fernet_key()

login()
