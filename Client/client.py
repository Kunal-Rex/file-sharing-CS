#!/usr/bin/env python3

import socket
import time
import os
import hashlib

IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
ADDR = (IP, PORT)
FORMAT = "ascii"
SIZE = 1024


def generate_md5_hash(file_name):
    with open(file_name, "rb") as FILE:
        HASH = hashlib.md5()
        BUFFER ="EMPTY"
        while BUFFER:
            BUFFER = FILE.read(1024)
            HASH.update(BUFFER)
        FILE.close
    return HASH.hexdigest()



def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("""
    [*] Client Started.....\n
    [*] This is an interactive client, following commands are avilable:\n
        1. LIST_FILES - List files on server.
        2. UPLOAD - Upload files with given format.
        3. DOWNLOAD - Download files from server by providing FILE ID
        4. DISCONNECT - Disconnect from server
    """
    )
    
    
    while True:
        msg = input("\n[*] Enter command to perform action.....\n")
        client.send(msg.encode(FORMAT))
        # print(client.recv(SIZE).decode(FORMAT))
        if msg == "LIST_FILES":
            list_of_files_server = list()
            print("\n[*] Listing files on Server ....\n")
            number_of_files_on_server = int(client.recv(SIZE).decode(FORMAT))
            if number_of_files_on_server >= 1:
                check_download = 0
                print(f'{"Nr.":<4} {"FILE ID":<31} {"FILE NAME":<12} {"FILE SIZE":<10}\n')
                for _ in range(number_of_files_on_server):
                    f = client.recv(SIZE).decode(FORMAT)
                    list_of_files_server.append(f)
                    print(_+1," ",f) 
            else:
                print("[SERVER] No Files Available Here....\n")
                check_download = 1
                
        elif msg == "UPLOAD":
            check_download = 0
            exclude = 'client.py'
            print(client.recv(SIZE).decode(FORMAT))
            list_of_files = os.listdir()
            print("\n[*] List of files to UPLOAD:\n")
            print(f'{"File Name":<11} | {"File Size":<31}\n')
            print("++++++++++++++++++++++++++++++++++++++++\n")
            if list_of_files:
                # '''TODO: Make table with name and size'''
                for file_name in list_of_files:
                    if file_name == exclude:
                        continue
                    file_size = os.path.getsize(file_name)
                    print(file_name," ",file_size,"\n")
            else:
                print("No files here to upload.....\n")
            print("++++++++++++++++++++++++++++++++++++++++\n")
            print("[*] Enter file name and size to UPLOAD\n")   
            print("[*] FORMAT: 'file name;file size(in bytes)'\n")  
            file_name,file_size = input().split(";")
            client.send(f"{file_name} {file_size}".encode(FORMAT)) 
            time.sleep(2) 
            print(client.recv(SIZE).decode(FORMAT))
            input("Press Enter/Return to start upload ⏎ \n") #TODO:TEMP
            file = open(file_name, "rb")
            data = file.read(SIZE)
            # length = len(data.encode())
            pad = b'SEND_DONE'
            client.send(data)
            while(data):
                data = file.read(SIZE)
                if not data:
                    client.send(pad)
                else:
                    client.send(data)
            
            file.close()
            print("Done Uploading\n")
            time.sleep(1)
            print(client.recv(SIZE).decode(FORMAT))
            #TODO: Only run if file uploaded.
            md5_server = client.recv(SIZE).decode(FORMAT)
            print(md5_server)
            md5_server = str(md5_server.split(": ")[-1].strip())
            md5_client = str(generate_md5_hash(file_name))

            if md5_client == md5_server:
                print("Integrity Check: PASS\n")
            else:
                print(md5_server," != ",md5_client)
                print("Integrity Check: FAIL\n")
        
        elif msg == "DOWNLOAD":
            
            if check_download == 0:
                print("\n[*] List of files avialable on server to download")
                print(f'{"Nr.":<3} {"FILE ID":<31}')
                for i in range(len(list_of_files_server)):
                    print(i+1," ",list_of_files_server[0].split(";")[0])
                print(client.recv(SIZE).decode(FORMAT))
                
                client.send(list_of_files_server[0].split(";")[0].encode(FORMAT))
                file = open(list_of_files_server[0].split(";")[1], "wb")
                data = client.recv(SIZE)
                while data:
                    file.write(data)
                    data = client.recv(SIZE)
                    if data == b"SEND_DONE":
                        break
                    
                file.close()
                print("\n[SERVER] FILE DOWNLOAD COMPLETE \n")
                
                print("[*] Integrity check in progress...\n")
                time.sleep(3)
                md5_server_down = str(generate_md5_hash(list_of_files_server[0].split(";")[1]))
                print("File Id of Downloaded file:",md5_server_down,"\n")
                md5_client_down = str(list_of_files_server[0].split(";")[0])
                print("Hash Digest of Downloaded file:",md5_client_down,"\n")

                if md5_client_down == md5_server_down:
                    print("Integrity Check: PASS\n")
                else:
                    print(md5_server_down," != ",md5_client_down)
                    print("Integrity Check: FAIL\n")
            else:
                client.recv(SIZE).decode(FORMAT)
                print("[*] Nothing to download")
                client.send(str(check_download).encode(FORMAT))
        elif msg == "DISCONNECT":
                print(f"[DISCONNECTED] Server disconnected.")
                break

    client.close()

                      
if __name__ == "__main__":
    main()
