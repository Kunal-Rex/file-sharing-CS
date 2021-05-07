# File Sharing (Client-Server)

• Handshake Phase – The server awaits for a new connection. 
– The client connects to the server. 
– The server expects one of the following commands from the client: 

  * LIST_FILES

  * DOWNLOAD 

  * UPLOAD 
  
  * DISCONNECT 


• Command Phase 

– **LIST FILES** 

- The client sends the “LIST FILE” command in ASCII and awaits from the server a reply with a list of files that are available for download. The server’s reply format is “file1 id;file1 name;file1 size (newline) file2 id;file2 name;file2 size (newline) ...” or a custom message in case there are no files (for example: “No files available at the moment”).

– **DOWNLOAD**  

- The client sends the “DOWNLOAD” command in ASCII. The server will reply, asking for a “file id” of the file that should be downloaded to the client. Then, the client sends the “file id” and awaits for the file as byte-stream. 


– **UPLOAD**

- The client sends the “UPLOAD” command in ASCII. The server will reply, asking for the “File Name” and “File Size”. The client sends the file details in the following format “file name;file size” in ASCII. Once the server receives the file details, it will reply that it’s ready to receive the file as byte-stream. Only after this reply the client will start sending the file as byte-stream.


– **Verification Phase** 

- To check whether an uploaded or downloaded file was transferred intact, a verification is required. To achieve this, both the server and client each generate an MD5 hash of the file. When uploading, the server will send its generated hash to the client for comparison. When downloading, you can utilize the “file id” as the MD5 hash.


Usage
----

Start the Server and subsequently the Client :

    python3 ./Server/server.py
    
    python3 ./Client/client.py

Follow along the list of commands available for interaction:

    This is an interactive client, following commands are avilable:

        1. LIST_FILES - List files on server.
        2. UPLOAD - Upload files with given format.
        3. DOWNLOAD - Download files from server by providing FILE ID
        4. DISCONNECT - Disconnect from server



Note:
----

- The client is interactive and requires above *commands* as user input. In **Upload** phase user has to provide specified format and approval for upload.
- However, in **Download** phase client automatically downloads and verifies the sample file













