#python2.7
import socket 
import threading

bind_ip = "0.0.0.0"
#port should be 80 for web server
bind_port = 9999

#socket uses IPv7, and SOCK_STREAM is TCP, UDP is SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print"[*] Listening on %s:%d" % (bind_ip,bind_port)

#this is our client-handling thread
#in general, a client will always try to start a connection

#best version would give appropriate HTTP response

def handle_client(client_socket):
    #read in what client has sent us
    #print out what hte client sends
    #1024 is maximum bites to read in
    request = client_socket.recv(1024)

    print"[*] Received: %s" % request

    #send back a packet
    client_socket.send("ACK!")

    #socket is closed, function ends and thread is closed
    client_socket.close()

while True:
    client,addr = server.accept()
    print"[*] Accepted connection from: %s:%d:" % (addr[0], addr[1])

    #spin up our client thread to handle incoming data
    #threads are used to handle more than one connection at a time
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()