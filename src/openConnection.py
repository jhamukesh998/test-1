#C:\Users\jaind\Desktop\Projects\Assignments\DISML\test-1\src

import socket
import time

ips = set()

# Get the private IP address of the host machine
def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

HOST = get_private_ip()
ips.add(HOST)
PORT = 2222

# Send message to all IP addresses within the network on a particular port
for i in range(1, 255):
    if(i==104 or i==183 or i==9):
        target = f"192.168.0.{i}"
        if target != HOST:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((target, PORT))
                    s.sendall(b"Hello, network!")
                    response = s.recv(1024)
                    print(f"Response from {target}: {response.decode()}")
            except socket.error:
                pass

# Create a new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Set the socket options to allow reuse of the address and port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.settimeout(30) 

    # Bind the socket to the host and port
    s.bind((HOST, PORT))

    # Listen for incoming connections
    s.listen()

    # Print a message indicating that the server is listening
    print(f"Server listening on {HOST}:{PORT}...")

    # Accept incoming connections and handle them
    while True:
        print("accepting connection")
        
        # Wait for a connection
        conn, addr = s.accept()

        # Print a message indicating that a connection was received
        print(f"Connection received from {addr}")
        print(type(addr))
        ips.add(addr[0])
        print(addr[0])

        # # Send a response to the client
        # message = "Hello, client!"
        # conn.sendall(message.encode())

        time.sleep(3)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sf:
            print("sleeping and then will connect!")
            #sf.settimeout(0.1)
            sf.connect((addr[0], PORT))
            sf.sendall(b"Hello, network!")
            response = sf.recv(1024)
            print(f"Response from {target}: {response.decode()}")


        # Close the connection
        conn.close()

        print("List of IPs",list(ips))