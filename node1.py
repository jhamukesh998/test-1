import socket
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor

# Set up socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.126.17.236', 8000))
sock.listen(1)

# Generate data
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

# Initialize model
model = SGDRegressor(random_state=42)

# Connect to Node 2
node2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node2_sock.connect(('10.126.17.241', 8000))

# Send data to Node 2
np.save('data.npy', (X, y))
with open('data.npy', 'rb') as f:
    data = f.read()
node2_sock.sendall(data)

# Receive model parameters from Node 2 and update own model
model_params = node2_sock.recv(1024)
model.set_params(**np.load(model_params, allow_pickle=True).item())

# Train model on own data
model.partial_fit(X, y)

# Send own model parameters to Node 2
np.save('model_params.npy', model.get_params())
with open('model_params.npy', 'rb') as f:
    data = f.read()
node2_sock.sendall(data)

# Clean up
node2_sock.close()
sock.close()
