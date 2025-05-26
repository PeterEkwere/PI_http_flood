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
ulimit -n 10485760  # File descriptors
ulimit -u 1048576  # Max user processes
ulimit -s 256  
