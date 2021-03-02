import socket
import ssl
import threading

def handler(conn):
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    #default ssl is cert_optional, but this one is cert_none
    #cert_none means that the person using a web browser cannot provide a cert
    context.verify_mode=ssl.CERT_NONE
    context.load_cert_chain(certfile="./demo.crt",keyfile="./demo.key",password=None)
    s_conn = context.wrap_socket(conn,server_side=True)
    resp = "HTTP/1.1 200 OK/r/n"
    resp += "Content-Type: text/html\r\n"
    body = "<b> Hello! </b>"
    resp += "Content-Length: " + str(len(body)) + "\r\n\r\n"
    resp += body + "\r\n"

    s_conn.send(resp.encode())
    s_conn.close()


def main():
    
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("localhost", 443))
    srv.listen(5)

    while True:
        connection, addr = srv.accept()
        t = threading.Thread(target=handler, args=(connection,))
        t.start()

main()