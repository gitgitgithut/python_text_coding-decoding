# credit to https://www.youtube.com/watch?v=LJTaPaFGmM4
""" Intro
 This is a code for setting up a server to send codes and instructions to clients to run,
 as well as collecting results from clients. Clients run codes independently thus as long as the server is online
 and there is at least one client connecting to the server the program will not terminate before all instructions
 are sent out.
"""
import socket
import threading
import os
import Analysis_server
import time


code_out = 'Client-Analysis.zip'      # file you wish to send
queue_out = Analysis_server.genQue()  # generate instruction set


def RetrFile(name, sock, thread_num, ip):
    # send code
    filename = code_out
    package = sock.recv(1024).decode() # retrieve request from client
    #check if client is ready to receive code
    if (package[:6] == 'CODE  '):
        print("Sending Code...")
        sock.send(str(os.path.getsize(filename)).encode())  # send file size to client
        # transmit the code file
        with open(filename, 'rb') as f:
            bytesToSend = f.read()
            sock.send(bytesToSend)
        print("Code Delivered!")

    # create result file to store received data
    resultName = 'result' + str(thread_num) + '.txt'
    f = open(resultName, 'wb')  # wb = web binary
    # wait for client to be prepared for receiving instructions
    while (sock.recv(1024).decode()[:5] != "READY"):
        time.sleep(1)
    # main loop, send instruction one at a time and collect results from the client
    count = 0
    while len(queue_out) > 0:  # while there are still instructions remaining in the query
        instr = queue_out.pop()
        print(str(len(queue_out)) + " instruction remaining")
        sock.send(("INSTRC" + instr).encode())  # send instruction
        # wait for response
        while package[:6] != 'RESULT':
            package = sock.recv(1024).decode()
        # start receive data
        while package[:6] != 'FINISH':
            data = (package[6:] + '\n').encode()
            f.write(data)
            sock.send('READY'.encode())
            package = sock.recv(1024).decode()
        count += 1
        print(str(count) + " data collected from " + str(ip))

    # transmission finished

    f.close()
    sock.send('FINISH'.encode())
    print(str(resultName) + " collected!")
    sock.close()  # close the connection

def Run():
    host = socket.gethostbyname(socket.gethostname())  # find the host ip address
    print("Server ip: ", host)                         # display host ip address
    port = 5000
    print("The server directory is: ", os.getcwd())    # display working directory
    # with default TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))

    s.listen(5)
    print("server started:")

    count = 1
    # terminate the program if all instructions are sent out
    while(len(queue_out) != 0):
        c, addr = s.accept() # connection socekt c and address
        print("client connected ip:" + str(addr))
        t = threading.Thread(target=RetrFile, args=("retrThread"+str(count), c, count, addr)) # create new thread for
                                                                                              # each connections
        t.start() # start hosting
        count += 1
        time.sleep(5)


    s.close()
    print("All results are collected!")


if __name__ == '__main__':
    Run()
