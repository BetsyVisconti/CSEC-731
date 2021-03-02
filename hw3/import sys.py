import sys
import socket

def getDataFromSocket(ip,port):
    serverSock = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
    serverSock.bind((ip, port))
    serverSock.listen(5)
    while True:
        clientSocket, clientInfo = serverSock.accept()
        #code such that anytime someone excepts, creates new handler code for that one person's request
        print(clientInfo)
        print(clientSocket)
def parseData():
    pass
def generateResponse():
    pass
def main():
    ipaddr = sys.argv[1]
    port = int(sys.argv[2])
    print(ipaddr)
    print(port)

    getDataFromSocket(ipaddr, port)
    parseData()
    generateResponse()

main()
