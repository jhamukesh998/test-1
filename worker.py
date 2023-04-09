import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import socket
import time
import threading


# Define the neural network architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Initialize the model and optimizer
model = Net()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Set the IP addresses of the workers
worker_ips = ["10.126.17.236", "10.126.17.241"]

# Set the port number for the worker-to-worker communication
port = 12345
 
# Define a function to listen for incoming connections
def listen_for_connections(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(False)
        s.bind(("", port))
        s.listen(2)
        while True:
            try:
                conn, addr = s.accept()
                yield conn
            except socket.error:
                time.sleep(0.1)

# creating thread
t1 = threading.Thread(target=listen_for_connections, args=(port,))
t1.start()
                
# Define a function to exchange model parameters with the neighbors
def exchange_params(worker_id, worker_ips, port, model_state):
    # Get the IP addresses of the neighboring workers
    num_workers = len(worker_ips)
    neighbor_ips = [worker_ips[(worker_id-1)%num_workers], worker_ips[(worker_id+1)%num_workers]]
    
    # Connect to the neighboring workers and exchange model parameters
    for neighbor_ip in neighbor_ips:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(False)
            try:
                s.connect((neighbor_ip, port))
            except socket.error:
                pass
            s.sendall(model_state)

    # Accept connections from neighboring workers and receive model parameters
    connections = []
    for conn in listen_for_connections(port):
        connections.append(conn)
        if len(connections) == 2:
            break
    for conn in connections:
        received_state = conn.recv(1024)
        model.load_state_dict(torch.load(received_state))
        conn.sendall(model_state)


"""
# Define a function to exchange model parameters with the neighbors
def exchange_params(worker_id, worker_ips, port, model_state):
    # Get the IP addresses of the neighboring workers
    num_workers = len(worker_ips)
    neighbor_ips = [worker_ips[(worker_id-1)%num_workers], worker_ips[(worker_id+1)%num_workers]]
    
    # Connect to the neighboring workers and exchange model parameters
    for neighbor_ip in neighbor_ips:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((neighbor_ip, port))
            s.sendall(model_state)
            received_state = s.recv(1024)
            model.load_state_dict(torch.load(received_state))
"""

# Define the training loop
def train(worker_id, worker_ips, port, num_epochs=10):
    for epoch in range(num_epochs):
        # Load the local data
        x = torch.randn(10)
        y = torch.randn(1)

        # Compute the starting point for local training
        model_state = torch.save(model.state_dict(), f"model_{worker_id}.pt")
        exchange_params(worker_id, worker_ips, port, model_state)
        model.load_state_dict(torch.load(model_state))

        # Perform one round of local training
        for i in range(10):
            optimizer.zero_grad()
            output = model(x)
            loss = (output - y)**2
            loss.backward()
            optimizer.step()

        # Update the model parameters and exchange with neighbors
        model_state = torch.save(model.state_dict(), f"model_{worker_id}.pt")
        exchange_params(worker_id, worker_ips, port, model_state)
        model.load_state_dict(torch.load(model_state))

        print(f"Worker {worker_id}, Epoch {epoch+1}, Loss {loss.item()}")

# Start the worker process
if __name__ == "__main__":
    # Get the ID of this worker based on its IP address
    worker_id = worker_ips.index(socket.gethostbyname(socket.gethostname()))

    # Start the training loop
    train(worker_id, worker_ips, port)
