import os
import socket
import struct
import fcntl
import threading
import time
import subprocess

from threading import Timer

ip_list = [[], [], [], [], [], []]

thermal_value = 0
thermal_time = "2021-12-20 09:00:00 AM"

wlan0_status = wlan1_status = 'FALSE'
wlan0_time = wlan1_time = "2021-12-20 09:00:00 AM"

sim1_status = sim2_status = 'FALSE'
sim1_desc = sim2_desc = 'Description sim1/sim2 status'
sim1_time = sim2_time = "2021-12-20 09:00:00 AM"

eth0_status = eth1_status = 'FALSE'
eth0_desc = eth1_desc = 'Description eth0/eth1 status'
eth0_time = eth1_time = "2021-12-20 09:00:00 AM"

#ni0 = ['enp3s0', 'enp3s1', 'usb0.10', 'usb0.20', 'wlan0', 'wlan1']
ni0 = ['eth0', 'eth1', 'usb0.10', 'usb0.20', 'wlan0', 'wlan1']

def get_thermal_val(line):
    s1 = line.find('cpu-thermal0') + 32
    e1 = line.find(' ', s1)
    thermal_val = line[s1:e1]

    return thermal_val

def read_thermal_do():
    global thermal_time, thermal_value

    while True:
        line = os.popen('/tmp/askey/thermal | grep cpu-thermal0').readline().strip()
        thermal_value = get_thermal_val(line)
        localtime = time.localtime()
        thermal_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)

        time.sleep(1)

def thermal_do():
    t1 = threading.Thread(target=read_thermal_do)
    t1.daemon = True
    t1.start()


def get_ip_address(if_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(
            fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', if_name[:15].encode('utf-8')))[20:24])
    except IOError as err:
        if err.errno == 99:
            return 1
        elif err.errno == 19:
            return 2
        return -1


def ping_ip(num, now_ip, host_ip):  # ping the specified IP to determine whether the host is alive
    global ip_list

    p_w = 'c'

    output = os.popen('ping -%s 1 %s' % (p_w, now_ip)).readlines()
    for w in output:
        if str(w).upper().find('TTL') >= 0:
            if now_ip != host_ip:
                ip_list[num].append(now_ip)


def ping_all(num, host_ip):  # ping all IPs to get all live hosts

    # print("ping_all: ", ni0[num], ", host_ip: ", host_ip)

    if host_ip in [-1, 1, 2]:
        return -1

    if ni0[num] in ['eth0','eth1','wlan0', 'wlan1']:
        pre_ip = (host_ip.split('.')[:-1])
        for i in range(1, 255):
            now_ip = ('.'.join(pre_ip) + '.' + str(i))
            t21 = threading.Thread(target=ping_ip, args=(num, now_ip, host_ip))
            t21.daemon = True
            t21.start()
            time.sleep(0.01)
    else:
        p_w = 'c'
        now_ip = '8.8.8.8'
        output = os.popen('ping -I %s -%s 1 %s' % (ni0[num], p_w, now_ip)).readlines()
        for w in output:
            if str(w).upper().find('TTL') >= 0:
                ip_list[num].append(now_ip)

    return 0


def network_result_status(num, result):
    global sim1_time, sim2_time, wlan0_time, wlan1_time, eth0_time, eth1_time
    global sim1_status, sim2_status, wlan0_status, wlan1_status, eth0_status, eth1_status

    localtime = time.localtime()
    if ni0[num] == 'usb0.10':
        sim1_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            sim1_status = 'PASS'
        else:
            sim1_status = 'FALSE'
    elif ni0[num] == 'usb0.20':
        sim2_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            sim2_status = 'PASS'
        else:
            sim2_status = 'FALSE'
    elif ni0[num] == 'wlan0':
        wlan0_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            wlan0_status = 'PASS'
        else:
            wlan0_status = 'FALSE'
    elif ni0[num] == 'wlan1':
        wlan1_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            wlan1_status = 'PASS'
        else:
            wlan1_status = 'FALSE'
    elif ni0[num] == 'eth0':
        eth0_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            eth0_status = 'PASS'
        else:
            eth0_status = 'FALSE'
    elif ni0[num] == 'eth1':
        eth1_time = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        if result == 1:
            eth1_status = 'PASS'
        else:
            eth1_status = 'FALSE'

def network_result_desc(num, desc):
    global eth0_desc, eth1_desc

    if ni0[num] == 'eth0':
        eth0_desc = desc
    elif ni0[num] == 'eth1':
        eth1_desc = desc


def network_ping_do():
    while True:

        for i in [0, 1, 2, 3, 4, 5]:
            resp = -1
            if ping_all(i, get_ip_address(ni0[i])) == 0:
                if not ip_list[i]:
                    resp = -1
                    #print("Error: Pls check the network ", ni0[i])
                else:
                    for ip in ip_list[i]:
                        resp = 1
                        #print("IP: ", ip)
            else:
                resp = -1
                #print("Error: Pls check the network ", ni0[i])

            network_result_status(i, resp)

            ip_list[i].clear()

        time.sleep(1)


def network_only_ping_do():
    t2 = threading.Thread(target=network_ping_do)
    t2.daemon = True
    t2.start()


def get_net_io(line):
    s1 = line.find('RX bytes:') + 9
    e1 = line.find(' ', s1)
    net_i = line[s1:e1]
    s2 = line.find('TX bytes:') + 9
    e2 = line.find(' ', s2)
    net_o = line[s2:e2]

    return int(net_i), int(net_o)


def monitor_network_traffic(num):
    line = os.popen('/sbin/ifconfig %s | grep bytes' % (ni0[num])).readline().strip()
    net_io = get_net_io(line)
    net_i_start = net_io[0]
    net_o_start = net_io[1]
    time_start = time.time()

    while True:
        info = []

        time.sleep(10)
        line = os.popen('/sbin/ifconfig %s | grep bytes' % (ni0[num])).readline().strip()
        netio = get_net_io(line)
        time_curr = time.time()
        net_i_total = netio[0] - net_i_start
        net_o_total = netio[1] - net_o_start
        sec_total = time_curr - time_start
        net_i_start = netio[0]
        net_o_start = netio[1]
        time_start = time_curr
        ni_speed = (net_i_total / sec_total / 1024)
        no_speed = (net_o_total / sec_total / 1024)

        # info.append(ni0[num])
        info.append("Current network inflow speed:%.4fk/s" % ni_speed)
        info.append("outgoing speed:%.4fk/s" % no_speed)
        show = ", ".join(info)
        # print(show)
        
        network_result_desc(num, show)


def network_ftp_do(num, ftp_addr, bind_address):
    while True:
        # curl -u ftp:ftp ftp://10.0.0.10/test_001m.zip --interface eth1 --output test_001m.zip
        # wget --user=ftp --password=ftp ftp://ftp.speed.hinet.net/test_400m.zip --bind-address=10.0.0.1 --output-document=test_400m_01.zip"
        # cmd = "wget --user=ftp --password=ftp " + ftp_addr + " --bind-address=" + bind_address
		
        if bind_address == 'eth0':
            cmd = "curl -u ftp:ftp  ftp://192.168.5.10/" + ftp_addr + " --interface " + bind_address + " --output " + bind_address + "_010m.zip"
        elif bind_address == 'eth1':
            cmd = "curl -u ftp:ftp  ftp://10.0.0.10/" + ftp_addr + " --interface " + bind_address + " --output " + bind_address + "_010m.zip"
        
        timeout = 1500
        
        # print(cmd)
        
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        timer = Timer(timeout, proc.kill)

        GLO_FTP01_ERR01 = False

        try:
            timer.start()
            data = proc.communicate()
        finally:
            if proc.poll() != 0:
                GLO_FTP01_ERR01 = True
                # print("Error: Pls check the network.")
                time.sleep(5)

            timer.cancel()
            
        result = False
        if not GLO_FTP01_ERR01:
            file = bind_address + "_010m.zip"
            size = os.path.getsize(file)
            # print('%s = %d bytes' % (file, size))
            if size == 10485760:
                result = True
                # print("Match")
        
        network_result_status(num, result)
		

def network_traffic_do():
    for i in [0, 1]:
        host_ip = get_ip_address(ni0[i])
        if host_ip in [-1, 1, 2]:
            print("Error: Pls check the network ", ni0[i])
        else:
            print("Host IP: ", host_ip)
            # ftp://10.0.0.10/test_400m.zip # ftp://ftp.speed.hinet.net/test_400m.zip
            # t31 = threading.Thread(target=network_ftp_do, args=(i, "ftp://10.0.0.10/test_010m.zip", host_ip,))
            t31 = threading.Thread(target=network_ftp_do, args=(i, "test_010m.zip", ni0[i],))
            t31.daemon = True
            t31.start()
            t32 = threading.Thread(target=monitor_network_traffic, args=(i,))
            t32.daemon = True
            t32.start()


def network_can_do():
    while True:
        os.system('/tmp/askey/ctx0800_can.sh')
        time.sleep(20)


def network_acme_do():

    os.system('/tmp/askey/acme -I1000')
    
    cmd = "ps -ax | grep acme"
	
    while True:
        output = subprocess.check_output(cmd, shell=True,)
        print(output)
        if not output:
            # print("acme delay")
            time.sleep(20)
        else:
            #print("retry acme")
            os.system('/tmp/askey/acme -I1000')
        time.sleep(20)

def network_ble_do():

    os.system('nfore_ble_test')
    
    cmd = "ps -ax | grep nfore_ble_test"
    
    while True:
        output = subprocess.check_output(cmd, shell=True,)
        print(output)
        if not output:
            print("nfore_ble_test delay")
            time.sleep(20)
        else:
            print("retry nfore_ble_test")
            os.system('nfore_ble_test')
        time.sleep(20)

def display_do():
    os.system('clear')

    print("thermal: ", thermal_time, ", value: ", thermal_value)

    print("wlan0: ", wlan0_time, ", status: ", wlan0_status)
    print("wlan1: ", wlan1_time, ", status: ", wlan1_status)
    print("sim1(usb0.10): ", sim1_time, ", status: ", sim1_status)
    print("sim2(usb0.20): ", sim2_time, ", status: ", sim2_status)
    
    print("eth0: ", eth0_time, ", status: ", eth0_status)
    print("eth1: ", eth1_time, ", status: ", eth1_status)

def exe_do():
    
    os.system('echo 0 4 0 7 > /proc/sys/kernel/printk')
    
    os.system('echo 12 > /sys/class/i2c-dev/i2c-3/device/3-0060/carModel')
    os.system('echo 1 > /sys/class/i2c-dev/i2c-3/device/3-0060/init')
    os.system('echo 0 > /sys/class/i2c-dev/i2c-3/device/3-0060/vol')
    os.system('echo 0 > /sys/class/i2c-dev/i2c-3/device/3-0060/mute')
    os.system('echo 0 > /sys/class/i2c-dev/i2c-3/device/3-006c/mute')
    os.system('echo 1 > /sys/class/i2c-dev/i2c-3/device/3-006c/pwr_amp_ctl')
    os.system('echo 0x2300 0x1 > /sys/class/i2c-dev/i2c-3/device/3-0060/writeDspMem')
    
    t03 = threading.Thread(target=network_ble_do)
    t03.daemon = True
    t03.start()
    
    time.sleep(50)
    
    os.system('echo -e "4\n1\n1\n16000\n3\n2\n1\n257\n9\n" | audio_console_app > /dev/null&')
    time.sleep(10)

    t02 = threading.Thread(target=network_acme_do)
    t02.daemon = True
    t02.start()
    
    time.sleep(10)
    
    t01 = threading.Thread(target=network_can_do)
    t01.daemon = True
    t01.start()
    
    time.sleep(2)
    
    #os.system('hostapd_run')
    
    time.sleep(2)
	
    thermal_do()
    network_only_ping_do()
    # network_traffic_do()
    
    while True:
        display_do()

        time.sleep(10)


if __name__ == '__main__':
    exe_do()
