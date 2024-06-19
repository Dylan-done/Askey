#!/bin/bash

cd ~/askey

echo "copy data to /tmp"

cp -Rf ~/askey /tmp/
sync
cp -f /usr/bin/acme /tmp/askey/.
sync

sleep 1

echo "change path to /tmp/askey"
cd /tmp/askey

sleep 1

python3 new_ctx0800.py

