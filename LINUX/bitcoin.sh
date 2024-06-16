#!/bin/bash
sleep_time=30
if [ "$#" -ne 0 ]; then
  sleep_time=$1
fi
while true;
  do printf "$(python3 script/bitcoin.py) $(date "+%Y-%m-%d %H:%M:%S")\n";
  sleep $sleep_time;
done
