import getpass
import telnetlib
import time

HOST = "192.168.0.225"

esp32 = telnetlib.Telnet()
esp32.open(HOST, timeout=2)

buf = b''
for i in range(900):
    buf += b'\a'
buf += b'\xff'    
print(buf)
    
esp32.write(buf)
print(esp32.read_all())

esp32.close()