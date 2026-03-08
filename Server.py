import socket
import struct

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server listening...")

conn, addr = server.accept()
print("Connected by", addr)

tc = conn.recv(1024)

if tc:
    print("Received TC:", tc.hex())

    # TM fields
    apid = 0x20
    tm_id = 0x81
    load_id = 2
    state = 1
    ocp = 0

    byte3 = (state << 7) | (ocp << 6)

    current = 2000      # mA
    voltage = 26600     # mV

    tm = struct.pack(">BBBBHH", apid, tm_id, load_id, byte3, current, voltage)

    conn.sendall(tm)
    print("TM sent")

conn.close()
server.close()