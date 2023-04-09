import socket
import numpy as np
from sklearn.linear_model import SGDRegressor

# Set up socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind(('10.126.17.241', 8000))
sock.bind(('192.168.0.104', 8000))
sock.listen(1)

# Connect to Node 1
node1_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node1_sock.connect(('10.126.17.236', 8000))

# Receive data from Node 1 and train model on it
data = node1_sock.recv(4096)
with open('data.npy', 'wb') as f:
    f.write(data)
X, y = np.load('data.npy', allow_pickle=True)
model = SGDRegressor(random_state=42)
model.partial_fit(X, y)

# Send own model parameters to Node 1
np.save('model_params.npy', model.get_params())
with open('model_params.npy', 'rb') as f:
    data = f.read()
node1_sock.sendall(data)

# Receive model parameters from Node 1 and update own model
model_params = node1_sock.recv(1024)
model.set_params(**np.load(model_params, allow_pickle=True).item())

# Clean up
node1_sock.close()
sock.close()
