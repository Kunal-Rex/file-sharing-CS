#!/usr/bin/env python3

import socket
import os
import hashlib
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'ascii'

def generate_md5_hash(file_name):
    with open(file_name, "rb") as FILE:
        HASH = hashlib.md5()
        BUFFER ="EMPTY"
        while BUFFER:
            BUFFER = FILE.read(1024)
            HASH.update(BUFFER)
        FILE.close
    return HASH.hexdigest()

def list_files(conn,addr):
    file_ids = []
    file_names = []
    exclude = 'server.py'
    # while True:
        # to_show = {}
    list_of_files = os.listdir()
    time.sleep(2)
    conn.send(str(len(list_of_files)-1).encode(FORMAT))
    time.sleep(2)
    if list_files:
        for file_name in list_of_files:
            if file_name == exclude:
                continue
            file_id = generate_md5_hash(file_name)
            file_ids.append(file_id)
            file_names.append(file_name)
            file_size = os.path.getsize(file_name)
            print(file_name,file_id,file_size)
            conn.send(f"{file_id};{file_name};{file_size}".encode(FORMAT))
            return file_ids,file_names
        return file_ids,file_names
 



def main():
    print("[*] Starting the Server.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[*] Ready!!")
    conn, addr = server.accept()
    while True:
        
        print("[*] Client connected: " + str(addr))
        time.sleep(2)
        response = conn.recv(SIZE).decode(FORMAT)

        if response == "LIST_FILES":
            file_id_list,file_name_list = list_files(conn,addr)
        elif response == "UPLOAD":
            conn.send("[SERVER] Please provide file name and file size".encode(FORMAT))
            up_name,up_size = conn.recv(SIZE).decode(FORMAT).split(" ")
            print(f"[CLIENT] Client wants to upload: \n File Name : {up_name} \n File Size : {up_size}")
            conn.send(f"[SERVER] Ready to receive.\n".encode(FORMAT))
            print(f"[*] Ready to receive the file")
            file = open(up_name, "wb")
            data = conn.recv(SIZE)
            while data:
                file.write(data)
                data = conn.recv(SIZE)
                if data == b"SEND_DONE":
                    break
                
            file.close()

            if int(up_size) == os.path.getsize(up_name):
                print("[*] UPLOAD Successful")
                conn.send("[SERVER] File data Uploaded Successfully \n".encode(FORMAT))
                time.sleep(1)
                conn.send(f"[SERVER] MD5 Hash of {up_name}: {generate_md5_hash(up_name)}\n".encode(FORMAT))
        

        elif response == "DOWNLOAD":
            conn.send("[SERVER] Please provide file_id for dowloading the file.. \n".encode(FORMAT))
            
            file_id_download = conn.recv(SIZE).decode(FORMAT)
            if file_id_download != 1:
                for i in range(len(file_id_list)):
                    if file_id_list[i] == file_id_download:
                        #file_size = os.path.getsize(file_name_list[i])
                        file = open(file_name_list[i], "rb")
                        data = file.read(SIZE)
                        pad = b'SEND_DONE'
                        conn.send(data)
                        while(data):
                            data = file.read(SIZE)
                            if not data:
                                conn.send(pad)
                            else:
                                conn.send(data)
                        
                        file.close()
                        print("[*] Done Sending..\n")
                        time.sleep(1)
                    else:
                        print("No file available here with this id")

        elif response == "DISCONNECT":
            print(f"[DISCONNECTED] {addr} disconnected.")
            break

        else:
            print("Not a valid input or invalid escape sequence")
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected.")
            continue
    conn.close()

if __name__ == "__main__":
    main()
