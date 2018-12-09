# credit to https://www.youtube.com/watch?v=LJTaPaFGmM4
""" Intro
 This is the a code for setting up a client to download and execute the code from the server, and transmit the result
 back to the server. The ip address for the server must be entered manually.
"""
import socket
import zipfile


def Main():
    #Initialize Connection
    host = '192.168.0.175'  # need to change it to the ip of the computer hosting the server before running. Host ip is shown in server's console
                            # Don't forget to turn off the firewall on both the server and client computer
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create tcp socket
    s.connect((host,port))                                 # connect to server

    # Download Code
    s.send('CODE  '.encode())  # signal sever to send code file
    filesize = int(s.recv(1024).decode()) # receive file size
    f = open('Code.zip', 'wb')  # save file as 'Code.zip'
    data = s.recv(1024)
    totalRecv = len(data)
    f.write(data)
    print("Start Downloading Code")
    while totalRecv < filesize:
        data = s.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print("{0:2f}".format((totalRecv / float(filesize)) * 100) + "% Done")      # show downloading progress
    print("Download Complete!")
    f.close()

    # if you send a zip file use this to extract zip file
    zipfile.ZipFile("Code.zip").extractall()
    s.send("READY".encode())

    #run program and start transmition
    from Client import run                  # Here import your test function
    package = s.recv(1024).decode()
    while package[:6] != "FINISH":          # check if there is instructions remaining
        if package[:6] == "INSTRC":
            run(s, package[6:])
        package = s.recv(1024).decode()

    print("Result delivered!")
    s.close()


if __name__ == '__main__':
    Main()

