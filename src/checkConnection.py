import socket

def is_port_open(ip, port):
    """Checks if a port is open on a given IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout after 1 second
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

network_prefix = '192.168.1.'  # Change this to your network prefix
port = 2222

for i in range(1, 255):
    ip = network_prefix + str(i)
    if is_port_open(ip, port):
        print(f"Port {port} is open on {ip}")
