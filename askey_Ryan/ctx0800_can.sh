#!/bin/bash

echo "TEST_START" > /opt/sfifo

killall tail; tail -f /run/media/mmcblk0p4/runlog.txt | grep mcu&

# echo "CAN test start, wait 10sec..... >>>"
if ps aux | grep "tail -f /run/media/mmcblk0p4/runlog.txt"
then
    echo "TEST_MCU exec_mcu_cmd=11,CAN0,1211,A1B2C3D4E5F6A7B9" > /opt/sfifo && sleep 10
else
    killall tail; tail -f /run/media/mmcblk0p4/runlog.txt | grep mcu&
    echo "TEST_MCU exec_mcu_cmd=11,CAN0,1211,A1B2C3D4E5F6A7B9" > /opt/sfifo && sleep 10
fi   
# echo "CAN test end, wait for the next test .... >>>"

echo "TEST_STOP" > /opt/sfifo
