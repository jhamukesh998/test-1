# import socket

# # Get the private IP address of the host machine
# HOST = socket.gethostbyname(socket.gethostname())

# PORT = 2222  # Port number you want to open

# # Create a new socket object
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     # Set the socket options to allow reuse of the address and port
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#     # Bind the socket to the host and port
#     s.bind((HOST, PORT))

#     # Listen for incoming connections
#     s.listen(1)

#     # Print a message indicating that the server is listening
#     print(f"Server listening on {HOST}:{PORT}...")

#     # Accept incoming connections and handle them
#     while True:
#         # Wait for a connection
#         conn, addr = s.accept()

#         # Print a message indicating that a connection was received
#         print(f"Connection received from {addr}")

#         # Send a response to the client
#         message = "Hello, client!"
#         conn.sendall(message.encode())

#         # Close the connection
#         conn.close()








import socket

# Get the private IP address of the host machine
HOST = socket.gethostbyname(socket.gethostname())

PORT = 8000  # Port number you want to open

# Create a new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Set the socket options to allow reuse of the address and port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    s.bind((HOST, PORT))

    # Listen for incoming connections
    s.listen(1)

    # Print a message indicating that the server is listening
    print(f"Server listening on {HOST}:{PORT}...")

    # Accept incoming connections and handle them
    while True:
        # Wait for a connection
        conn, addr = s.accept()

        # Print a message indicating that a connection was received
        print(f"Connection received from {addr}")

        # Receive incoming messages from the client and send a response
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"Received your message: {data.decode()}"
            conn.sendall(message.encode())
            print(f"Sent message: {message}")

        # Close the connection
        conn.close()
