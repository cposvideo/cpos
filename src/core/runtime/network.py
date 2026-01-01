import socket

def enforce_airgap():
    socket.socket = None
