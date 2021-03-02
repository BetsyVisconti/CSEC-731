import sys


def checkURL(uri):
    uri.lower() #converts to lowercase because url is not case sensitive
    if (uri[:8] == " http://" or uri[:9] == " https://" ): #valid urls must start with http:// or https://
        uri = uri[8:]
                            
    else:
        print("HTTP/1.1 400 BAD REQUEST.")
        quit()
    

def reqURI(uri):
    uri.lower()
    if (uri[:1]=="/"):
        for i in uri:
            if (i.isalnum() or i == "-" or i =="/" or i == "~" or i == ":" or i == "/" or i == "?"
            or i == "#" or i == "#" or i == "[" or i == "]" or i == "@" or i == "!" or i == "$" or i == "="
            or i == "&" or i == "'" or i == "(" or i == ")" or i == "*" or i == "+" or i == "," or i == ";"):
                pass
            else:
                print("HTTP/1.1 400 BAD REQUEST.")
                quit()
        
          
    else:
        print("HTTP/1.1 400 BAD REQUEST.")
        quit()
#checks HTTP version
#if it is not HTTP/1.1 or HTTP/1.2, return 400 Bad Request
def reqHTTPVer(http):
    if (http=='HTTP/1.1' or http=='HTTP/1.2'):
        pass
    else:
        print("HTTP/1.1 400 BAD REQUEST.")

#Request Lines are validated by ensuring that the methods are valid (ex. 'GET')
#If they're valid, test the uri with reqURI() and the HTTPVersion with reqHTTPVer()
def ValReqLine(HTTPReqLine):
    HTTPReqStr = ""
    HTTPReqStr = HTTPReqStr.join(HTTPReqLine)
    try:
        HTTPReqStr=HTTPReqStr.split( )
    except:
        print("200 Internal Server Error")
    HTTPReq=HTTPReqLine.split( )      
    if (HTTPReq[0] == "GET" or HTTPReq[0] == "HEAD" or HTTPReq[0] == "POST" or HTTPReq[0] == "PUT" or HTTPReq[0] == "DELETE"):
        reqURI(HTTPReq[1])
        reqHTTPVer(HTTPReq[2])
    elif (HTTPReq[0] == "CONNECT"):
        reqHTTPVer(HTTPReq[2])
    else:
        print("HTTP/1.1 400 BAD REQUEST")
        exit()
def ValHeaderTypes(HeaderName, HeaderContent, HTTPReq):
    HTTPReqLine = HTTPReq.split( ) 
    #initialize necessary headers
    hostIncluded = 0
    for i in range(len(HeaderName)):

        #validates Host 
        if (HeaderName[i] == "Host"):
            hostIncluded += 1
            if hostIncluded > 1: #a 400 BAD REQUEST when more than one host is found
                print("HTTP/1.1 400 BAD REQUEST.")
                exit()
            else:
                if HeaderContent[i][0] != " ":
                    print("HTTP/1.1 400 BAD REQUEST.")
                    exit()

                for char in HeaderContent[i]:
                    if (char.isalnum() or char == "-" or char =="/" or char == "~" or char == ":" or char == "/" or char == "?"
                    or char == "#" or char == "#" or char == "[" or char == "]" or char == "@" or char == "!" or char == "$" or char == "="
                    or char == "&" or char == "'" or char == "(" or char == ")" or char == "*" or char == "+" or char == "," or char == ";" or char == " "):
                        pass
                    else:
                        print("HTTP/1.1 400 BAD REQUEST.")
                        quit()
        if (HeaderName[i] == "User-Agent"):
            UserAgentCount = 0
            HeaderContPart = HeaderContent[i].split( )
            for part in HeaderContPart:
                if '/' in part:
                    UserAgent = part.split('/')
                    UserAgentCount += 1
                    for char in UserAgent[1]:
                        
                        if (char.isdigit() or '.'):
                            pass
                        else:
                            print("HTTP/1.1 400 BAD REQUEST.")
                            quit()
            if (UserAgentCount == 0): #there should be at least one valid user agent 
                print("HTTP/1.1 400 BAD REQUEST.")
                quit()
                
                
        if (HeaderName[i] == "Connection"):
            if (HeaderContent[i] == " keep-alive" or HeaderContent[i] == "close"):
                pass
            else:
                print("HTTP/1.1 400 BAD REQUEST.")
                exit() 

        if (HeaderName[i] == "From"):
            at = 0
            period = 0
            for char in HeaderContent[i]:
                if char =='@':
                    at += 1  
                if char =='.':
                    period += 1
                    
            if (at != 1 or period == 0):
                print("HTTP/1.1 400 BAD REQUEST.")
                exit()                     
        if (HeaderName[i] == "Referer"):
            #the referer header must not include the fragrment adn userinfo components
            #of the URI reference
            if (HeaderContent[i] == HTTPReqLine):
                print("HTTP/1.1 400 BAD REQUEST.")
                exit()

            checkURL(HeaderContent[i])
    if hostIncluded == 0:
        print("HTTP/1.1 400 BAD REQUEST.")
        exit()  

#seporates HeaderList into the two arrays: HeaderName and HeaderContent by ':'
#calls ValHeaderTypes with new arrays as parameters
def ValHeaderList (HTTPReq):
        HTTPReqLine = HTTPReq[0]
        HTTPReq.pop(0) #remove HTTP Request Line
        HTTPHeader = []
        for i in range (len(HTTPReq)):          
            if (HTTPReq[i]=='\n'): #stop appending i to array after finding '\n' (after this, body would be found)
                break
            HTTPHeader.append(HTTPReq[i])
        if (len(HTTPHeader) == 0): 
            print("HTTP/1.1 400 BAD REQUEST")
            exit()
        HeaderName = []
        HeaderContent = []
        colon = [] #index of where first colon is located
        for i in range (len(HTTPHeader)):

            HTTPReqStr = ""
            HTTPReqStr = HTTPReqStr.join(HTTPHeader[i])
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
                    print ("HTTP/1.1 400 BAD REQUEST")
                    exit()
        ValHeaderTypes(HeaderName, HeaderContent, HTTPReqLine)
       
 
def main():
    file = open(sys.argv[1], "r")
    input = file.read() 
    requestMess = input.splitlines(keepends=True)
    ValReqLine(requestMess[0])
    ValHeaderList(requestMess)
    print("HTTP/1.1 200 OK")


main()