import numpy as np
import socket
import pickle
import threading

# define the dataset
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
Y = np.array([0, 1, 0, 1])

# define the number of nodes and the number of features
num_nodes = 2
num_features = X.shape[1]

# define the IP addresses and port numbers for each node
addresses = [("192.168.0.9", 5000), ("192.168.0.104", 5000)]

# create a socket for each node
sockets = []
for i in range(num_nodes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addresses[i])
    s.listen()
    sockets.append(s)
    
# define a function to handle incoming connections from other nodes
def handle_connection(conn, addr):
    print(f"Connected to {addr}")
    
    # receive the node index and the weights from the sender node
    node_index = pickle.loads(conn.recv(1024))
    weights = pickle.loads(conn.recv(1024))
    
    # train the local model on the received weights
    local_model = train_local_model(weights)
    
    # send the updated weights back to the sender node
    conn.send(pickle.dumps(local_model))
    
    # close the connection
    conn.close()
    
# define a function to train the local model
def train_local_model(weights):
    # initialize the local model with the received weights
    model = MyModel()
    model.set_weights(weights)
    
    # train the local model on the local data
    model.train(X, Y)
    
    # return the updated weights
    return model.get_weights()

# define a function to start listening for incoming connections from other nodes
def listen_for_connections(socket_index):
    while True:
        # accept incoming connections from other nodes
        conn, addr = sockets[socket_index].accept()
        
        # handle the incoming connection in a new thread
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

# start listening for incoming connections from other nodes
for i in range(num_nodes):
    threading.Thread(target=listen_for_connections, args=(i,)).start()

# connect to each of the other nodes and exchange weights
for i in range(num_nodes):
    for j in range(num_nodes):
        if i != j:
            # connect to the other node
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(addresses[j])
            
            # send the node index and the weights to the other node
            conn.send(pickle.dumps(i))
            conn.send(pickle.dumps(weights))
            
            # receive the updated weights from the other node
            weights = pickle.loads(conn.recv(1024))
            
            # update the local model with the received weights
            model.set_weights(weights)
            
            # close the connection
            conn.close()
