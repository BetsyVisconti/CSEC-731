#python2.7
#https://markusholtermann.eu/2016/09/ssl-all-the-things-in-python/for sll
import socket 
import threading

bind_ip = "0.0.0.0"
bind_port = 80

#socket uses IPv7, and SOCK_STREAM is TCP, UDP is SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print"[*] Listening on %s:%d" % (bind_ip,bind_port)

#this is our client-handling thread
#in general, a client will always try to start a connection

#best version would give appropriate HTTP response

def parse_request(client_socket):
    responseLine = "\r\n"
    responseHeaders = "\r\n"
    responseBody = "\r\n"

    lines = request_str.split("\r\n")
    requestLine = lines[0]
    requestLine_parts = requestLine.split(" ")
    responseBody = getMessageBody(requestLine_parts[1]) + responseBody
    if responseBody=="":
        responseLine = "HTTP/1.1 404 Not Found" + responseLine
    else:
        responseLine = "HTTP/1.1 200 OK" + responseLine
    response = responseLine + responseHeaders + responseBody
    print "[*]********\r\n[*] Responding with: \r\n" + response + "[*]********\r\n"
    return response
#real version should call to different files 
def getMessageBody(resource):
    print resource
    if resource == "/greet.html":
        return "<html><body><b>Hello</b>World</body></html>\r\n"
    elif resource == "/goodbye.html":
        return "<html><script>alert('Goodbye')</script></html>\r\n"
    else:
        return "\r\n"


def handle_client(client_socket):
    request = client_socket.recv(1024)
    response = parse_request(request,client_socket)
    client_socket.send(response)
    client_socket.close()

while True:
    client,addr = server.accept()
    print"[*] Accepted connection from: %s:%d:" % (addr[0], addr[1])

    #spin up our client thread to handle incoming data
    #threads are used to handle more than one connection at a time
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()