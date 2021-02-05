import socket
import sys
import ssl
#import urllib
data=""
conn_type = sys.argv[1].split("://")[0]
url = sys.argv[1].split("//")[1]
host = url.split("/")[0]
page = url[len(host):]
if page == "":
    page = "/"
req = "GET " + page + " HTTP/1.1 \r\n"
req += "Accept-Encoding: identity \r\n"
req += "Host: " + host + "\r\n"
req += "Connection: close \r\n\r\n"
print(req)
# set up IPv4 socket
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# if HTTP, make a connection, encode request, send over encoded request,
# recieve the response and then pring the decoded response
if conn_type == "http":
    conn.connect((host, 80))
    conn.send(req.encode())
    print(conn.recv(8192).decode())
    conn.close()
# If HTTPS, we need set up SSLContext
# wrapper for a socket declaring which version of SSL we want to use
# use context to wrap socket and check host name in encryption certificate matches host name we access
# next we connect using new s_conn object created within this elif statement and connect through port 443
elif conn_type == "https":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # wrapper for a socket
    s_conn = context.wrap_socket(conn, server_hostname=host)  # check host name
    s_conn.connect((host, 443))  # connect using new s_conn object made in previous line
    s_conn.send(req.encode())  # encode data
    data = s_conn.recv(8192).decode()  # decode request
# if there's more than 8k of data, and data is not empty, print and grab more data
# Ensures that if more than 8k data is sent, we recieve more than 8k data back
    count = 1
    data2 = ""
    while data != "":
        data = s_conn.recv(8192).decode("UTF-8")  # grab more data
        data2 = data2 + data
        count += 1
        
    conn.close()
    list = []
    resp = data2
    
    resp.replace("\n", " ")
    resp.replace("\r", " ")
    resp.replace("\t", " ")
    for part in resp.split(" "):
        if "//" in part or '.js"' in part:
            pos = 1
            while not pos == -1:
                pos = part.find(".js")
                if not pos == -1:
                    for i in range(pos + 2, 0, -1):
                        if part[i] == '"' or part[i] == "'":
                            if not (part[i + 1:pos + 3] in list):
                                list.append(part[i + 1:pos + 3])
                    part = part[pos + 3:]

    for file in list:
        print(file)
