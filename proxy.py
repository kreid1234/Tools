import sys
import socket
import threading
import time

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((local_host, local_port))
    except:
        print "[!] Error! - acurre in server binding process, please check permission"
        print "local host - %s:%d" %(local_host,local_port)
        sys.exit(0)
    print "[*] Listening on %s:%d" %(local_host, local_port)
    server.listen(5)
    
    while True:
        client_socket, args = server.accept()
        print "Accept from %s:%d"%(args[0], args[1])

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)

def receive_from2(connection):
    buffer = ""
    connection.settimeout(2)
 

    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

def receive_from2(connection):
    time.sleep(1)
    buf = connection.recv(4096)
    return buf

def Recvhandler(client_socket, remote_socket):
    while True:
        try:
            time.sleep(0.0001)
            data = client_socket.recv(1024)
            remote_socket.send(data)
            
        except:
            pass

        if not len(data):
            client_socket.close()
            remote_socket.close()
            break

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    RecvThread = threading.Thread(target = Recvhandler, args = (client_socket, remote_socket))
    RecvThread.start()

 
    #if receive_first:
        #remote_buffer = receive_from(remote_socket)
        #hexdump(remote_buffer)
        #remote_buffer = response_handler(remote_buffer)

        #if len(remote_buffer):
            #print " [<==] Sending %d bytes to localhost."%len(remote_buffer)
            #client_socket.send(remote_buffer)
            
    
    #loop code
    while True:
        try:
            time.sleep(0.0001)
            data = remote_socket.recv(1024)
            client_socket.send(data)
        except:
            pass

        if not len(data):
            client_socket.close()
            remote_socket.close()
            print "no more data closing connection."
            
            break




def main():
    if len(sys.argv[1:]) != 4:
        print "[!] Usage : proxy.py <local host> <local port> <remote host> <remote port> <receive first>"
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()
else:
    print "[!] Error : it is the main module"
