import sys
import socket
import threading

def return404(csock):
    print("Return404: " + str(csock))
    csock.send("HTTP/1.1 404 file not found \r\n".encode())
    csock.close()

def return400(csock):
    print("Return400: " + str(csock))
    csock.send("HTTP/1.1 404 file not found \r\n".encode())
    csock.close()

def return200(requestLine, csock, body):
    lineParts = requestLine.split(" ")
    if lineParts[0] == "GET":
        requestedFile = open("." + lineParts[1], "r")
        filedata = requestedFile.read()
        httpResponse = "HTTP/1.1 200 OK \r\n\r\n"
        httpResponse += filedata
        httpResponse += "\r\n"
        print("Sending: " + httpResponse)
        csock.send(httpResponse.encode())
        csock.close()
    elif lineParts[0] == "POST":
        requestedFile = open("." + lineParts[1], "r")
        filedata = requestedFile.read()
        httpResponse = "HTTP/1.1 200 OK \r\n\r\n"
        httpResponse += filedata
        httpResponse += "\r\n"
        print("Sending: " + httpResponse)
        csock.send(httpResponse.encode())
        csock.close()
    
    print(lineParts)

#cd documents/csec-731/hw3/
#py officeHoursEx.py 127.0.0.1 9999

  

def parseData(req, csock):
    if "favicon" in req:
        return404(csock)
    lines = req.splitlines(keepends=True)
    nextLineBody=False
    body = ""
    if lines[-2] != '\r\n' and lines[-1] != '\r\n':
        return400(csock)
        exit()
    for line in range(len(lines)):
        #print(lines[line])
        currentLine = lines[line]
        #searches for \r\n to find end of headers
        if currentLine == "\r\n":
            nextLineBody=True
            #lines.remove(lines[line])
        elif nextLineBody:
            body = lines[line]
    if body != "":
        lines.remove(lines[-1])
        lines.remove(lines[-2])
    return200(req, csock, body)


def connectionHandler(csock, cinfo):
    request = csock.recv(8192)
    parseData(request.decode(), csock)
    csock.close()

def getDataFromSocket(ip,port):
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind((ip, port))
    serverSock.listen(5)
    while True:
        clientSocket, clientInfo = serverSock.accept()
        #code such that anytime someone excepts, creates new handler code for that one person's request
        cHandler = threading.Thread(target=connectionHandler, args =(clientSocket, clientInfo,))
        cHandler.start()


def generateResponse():
    pass
def main():
    ipaddr = sys.argv[1]
    port = int(sys.argv[2])
    print(ipaddr)
    print(port)

    getDataFromSocket(ipaddr, port)
    generateResponse()

main()

#cd documents/csec-731/hw3/
#py officeHoursEx.py 127.0.0.1 9999