import socket
import struct
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send TC (SET_LOAD command)
tc = struct.pack(">BBBB", 0x10, 0x01, 2, 0x80)
client.sendall(tc)

# Receive TM
tm = client.recv(1024)

apid, tm_id, load_id, byte3, current, voltage = struct.unpack(">BBBBHH", tm)

state = (byte3 >> 7) & 1
ocp = (byte3 >> 6) & 1

current_a = current / 1000
voltage_v = voltage / 1000

print("Voltage:", voltage_v, "V")
print("Current:", current_a, "A")
print("OCP:", ocp)

# Decision logic
if voltage_v >= 26.5 and 1.8 <= current_a <= 2.2 and ocp == 0:
    decision = "KEEP_ON"
    reason = "all nominal"
    ocp_error_flag = 0
else:
    decision = "SHUTDOWN"
    reason = "limit violated"
    ocp_error_flag = 1

print("Decision:", decision)
print("Reason:", reason)
print("OCP:", ocp_error_flag)

# Logging
from datetime import datetime, timezone

timestamp = datetime.now(timezone.utc).isoformat()

log_line = (
    f"timestamp={timestamp}\n"
    f"voltage_v={voltage_v}\n"
    f"current_a={current_a}\n"
    f"ocp={ocp}\n"
    f"decision={decision}\n"
    f"reason={reason}\n"
    f"ocp_error_flag={ocp_error_flag}"
)

with open("log.txt", "a") as f:
    f.write(log_line + "\n")

client.close()