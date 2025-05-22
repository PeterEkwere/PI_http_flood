#!/bin/bash




for proxy in $(grep socks5 /etc/proxychains.conf | awk '{print $2":"$3}'); do
  timeout 5 curl -x "socks5h://zgxvpqbp:4dl4nb6pmf4r@$proxy" 185.113.249.191 -d "tx=test"
  echo "Proxy $proxy exit code: $?"
done
