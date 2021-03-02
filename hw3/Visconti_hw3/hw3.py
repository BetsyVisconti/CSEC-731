import sys
import socket
import threading
import os
import copy

def return505(csock):
    print("Return505: " + str(csock))
    csock.send("HTTP/1.1 505 HTTP version not supported \r\n".encode())
    csock.close()
    exit()
def return501(requestLine, csock, body):
    print("Return501: " + str(csock))
    csock.send("HTTP/1.1 501 method not allowed \r\n".encode())
    csock.close()
    exit()

def return500(csock):
    print("Return500: " + str(csock))
    csock.send("HTTP/1.1 500 Server cannot process request \r\n".encode())
    csock.close()
    exit() 
    
def return411(csock):
    print("Return411: " + str(csock))
    httpResponse = "HTTP/1.1 411 Content-length not set \r\n\r\n"
    print("Sending: " + httpResponse)
    csock.send(httpResponse.encode())
    csock.close()
    exit()

def return403(csock):
    print("Return403: " + str(csock))
    httpResponse = "HTTP/1.1 403 Permission Error. \r\n\r\n"
    print("Sending: " + httpResponse)
    csock.send(httpResponse.encode())
    csock.close()
    exit()

def return404(csock):
    print("Return404: " + str(csock))
    httpResponse = "HTTP/1.1 404 file not found \r\n\r\n"
    print("Sending: " + httpResponse)
    csock.send(httpResponse.encode())
    csock.close()
    exit()

def return400(csock):
    print("Return400: " + str(csock))
    csock.send("HTTP/1.1 400 HTTP request not valid \r\n".encode())
    csock.close()
    exit()
    
def return200(requestLine, csock, body,HeaderName, HeaderContent):
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
    elif lineParts[0] == "DELETE":
        requestedFile = open("." + lineParts[1], "r")
        filedata = requestedFile.read()
        httpResponse = "HTTP/1.1 200 OK \r\n\r\n"
        httpResponse += filedata
        httpResponse += "\r\n"
        print("Sending: " + httpResponse)
        csock.send(httpResponse.encode())
        csock.close()
    elif lineParts[0] == "HEAD":
        
        httpResponse = "HTTP/1.1 200 OK \r\n\r\n"
        httpResponse += "\r\n"
        print("Sending: " + httpResponse)
        for i in range(len(HeaderName)):
            if HeaderName[i] == "Content-Length":
                print("Content-Length: " + HeaderContent[i])
                pass
        csock.send(httpResponse.encode())
        csock.close()

def return201(requestLine, csock, body):
    lineParts = requestLine.split(" ")
    if lineParts[0] == "PUT":
        requestedFile = open("." + lineParts[1], "r")
        filedata = requestedFile.read()
        httpResponse = "HTTP/1.1 201 OK \r\n\r\n"
        httpResponse += filedata
        httpResponse += "\r\n"
        print("Sending: " + httpResponse)
        csock.send(httpResponse.encode())
        csock.close()

#used to test if a uri is valid
def reqURI(uri,csock):
    uri.lower()
    if (uri[:0]=="/"):
        for i in uri:
            if (i.isalnum() or i == "-" or i =="/" or i == "~" or i == ":" or i == "/" or i == "?"
            or i == "#" or i == "#" or i == "[" or i == "]" or i == "@" or i == "!" or i == "$" or i == "="
            or i == "&" or i == "'" or i == "(" or i == ")" or i == "*" or i == "+" or i == "," or i == ";"):
                pass
            else:
                return400(csock)
                exit()

#if it is not HTTP/1.1 or HTTP/1.2, return 400 Bad Request
def reqHTTPVer(http,csock):
    if (str(http)=='HTTP/1.1\r' or str(http)=='HTTP/1.2\r'or str(http)=='HTTP/1.2'or str(http)=='HTTP/1.2'):
        pass
    else:
        return505(csock)
        exit()

#returns HeaderName (an array of all headernames) HeaderContent(an array of all header content)
def ValHeaderList (req,csock,body):
    reqHeaderList = copy.deepcopy(req)
    reqHeaderList.pop(0) #remove HTTP Request Line
    if body != "":
        reqHeaderList.pop(-1)
    reqHeaderList.pop(-1)
    reqHeaderList.pop(-1)
    HeaderName = []
    HeaderContent = []
    colon = [] #index of where first colon is located
    for i in range (len(reqHeaderList)):
        HTTPReqStr = ""
        HTTPReqStr = HTTPReqStr.join(reqHeaderList[i])
        foundColon = 'false'
        for i in range(len(HTTPReqStr)):
                
                #seporate string after first ':' 
                #this is better than split() because it works with examples
                #such as Host: localhost:5432
            if (HTTPReqStr[i] == ':' and foundColon == 'false'):
                HeaderName.append(HTTPReqStr[0:i])
                colon = i
                foundColon='true'
            elif (i == len(HTTPReqStr) -1 and foundColon=='true'):
                HeaderContent.append(HTTPReqStr[colon+1:i]) 
                break
            #catches case where the string doesn't have a ':'
            elif (i == len(HTTPReqStr) -1 and foundColon=='false'):
                return404(csock)
                exit()
    return (HeaderName, HeaderContent)

#parses the different requests for errors, sends appropriate response depending on tests
def parseMethods(req,csock,body):
    HeaderName, HeaderContent = ValHeaderList(req,csock,body)  

    lineParts = req[0].split(" ")
    if lineParts[0] == "GET":
        if len(lineParts) != 3:
            return400(csock)
            exit()
        reqURI(lineParts[1],csock)
        reqHTTPVer(lineParts[2],csock)
        return200(req[0], csock, body,HeaderName, HeaderContent)
    
    elif lineParts[0] == "HEAD":
        if len(lineParts) != 3:
            return400(csock)
            exit()
        reqURI(lineParts[1],csock)
        return200(req[0], csock, body,HeaderName, HeaderContent)

    elif lineParts[0] == "PUT":
        # if len(lineParts) != 3:
        #     return400(csock)
        #     exit()
        reqURI(lineParts[1],csock)
        reqHTTPVer(lineParts[2],csock)
        for i in range(len(HeaderName)):
            if HeaderName[i] == "Location":
                fileName = HeaderContent[i]
        else:
            fileName = lineParts[1]
            
        fileName = fileName[1:]
        if body != "":
            try:
                text_file = open(fileName, "w")
            except FileNotFoundError:
                return404(csock)
            text_file = open(fileName, "w")
            text_file.write(body)
            text_file.close()
            return201(req[0], csock, body)

    #put create or replace file

    elif lineParts[0] == "POST":
        if len(lineParts) != 3:
            return400(csock)
            exit()
        ContentLength = False
        for i in range(len(HeaderName)):
            if HeaderName[i] == "Content-Length":
                ContentLength = True
        if ContentLength == False:
            return411(csock)
            exit()
        reqURI(lineParts[1],csock)
        reqHTTPVer(lineParts[2],csock)
        for i in range(len(HeaderName)):
            if HeaderName[i] == "Location":
                fileName = HeaderContent[i]
        else:
            fileName = lineParts[1]
        fileName = fileName[1:]
        if body != "":
            if os.path.exists(fileName):
                return200(req[0], csock, body,HeaderName, HeaderContent)
            else:
                try:
                    text_file = open(fileName, "w")
                except FileNotFoundError:
                    return404(csock)
                text_file = open(fileName, "w")
                text_file.write(body)
                text_file.close()
                return200(req[0], csock, body,HeaderName, HeaderContent)
       
    elif lineParts[0] == "DELETE": 
        if len(lineParts) != 3:
            return400(csock)
            exit()   
        fileName = lineParts[1]
        fileName = fileName[1:]
        try:
            os.remove(fileName)
        except FileNotFoundError:
            return404(csock)
            exit()
        except PermissionError:
            return403(csock)
            exit()
        except:
            return500(csock)
            exit()
       
        os.remove(fileName)
        return200(req[0],csock,body,HeaderName, HeaderContent)
                   
    else:
        return501(req[0], csock, body)

#seporates the different parts of the request, returns the lines and body
def parseData(req, csock):
    if "favicon" in req:
        return404(csock)
    lines = req.split("\n")
    nextLineBody=False
    body = ""
    if lines[-2] != '\r' and lines[-1] != '\r':
        return400(csock)
        exit()
    for line in range(len(lines)):
        
        currentLine = lines[line]
        #searches for \r\n to find end of headers
        if currentLine == "\r\n" or currentLine == "\r":
            nextLineBody=True
        
        elif nextLineBody:
            body = lines[line]
    if body != "":
        lines.remove(lines[-1])
        lines.remove(lines[-2])

    parseMethods(lines, csock, body)
    

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

def main():
    ipaddr = sys.argv[1]
    port = int(sys.argv[2])
    getDataFromSocket(ipaddr, port)


main()

