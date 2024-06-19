
import os
import signal

import threading
import time
from ctypes import *

VCI_USBCAN2 = 4  # USBCAN-2A, USBCAN-2C or CANalyst-II 
STATUS_OK = 1

stop_flag = False

class VCI_INIT_CONFIG(Structure):  
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]
				
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ] 

# Channel 2 Receives Data
import ctypes
    
class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', ctypes.c_uint16), ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]
    
    def __init__(self,num_of_structs):
        self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(),ctypes.POINTER(VCI_CAN_OBJ))
        self.SIZE = num_of_structs
        self.ADDR = self.STRUCT_ARRAY[0]

CanDLLName = './ControlCAN.dll'
canDLL = windll.LoadLibrary('./ControlCAN.dll')

def thread_run01(stop_flag):
    global vci_can_obj_0
    
    # Channel 1 Send Data
    ubyte_array = c_ubyte*8
    a = ubyte_array(1, 2, 3, 4, 5, 6, 7, 8)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    
    while True:
        if stop_flag(): 
            vci_can_obj_0 = VCI_CAN_OBJ(0x1, 0, 0, 1, 0, 0,  8, a, b)
            ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj_0), 1)
            if ret == STATUS_OK:
                print('CAN1 Sent Successfully\r\n')
            if ret != STATUS_OK:
                print('CAN1 Sending Failed\r\n')
        
        if exit_flag == 1:
            break
		
        time.sleep(1000/1000)

def thread_run02(stop_flag):
    
    while True:
        rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)
        ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(rx_vci_can_obj.ADDR), 2500, 0)
        #print(ret)
        while ret <= 0:
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(rx_vci_can_obj.ADDR), 2500, 0)
            if ret > 0:
                print('CAN2 Received Successfully\r\n')
                print('ID：')
                print(vci_can_obj_0.ID)
                print('DataLen：')
                print(vci_can_obj_0.DataLen)
                print('Data：')
                print(list(vci_can_obj_0.Data))
            
            if exit_flag == 1:
                break
            
            time.sleep(1000/1000)

def thread_run03(stop_flag):
    
    while True:
        rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)
        ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR), 2500, 0)
        #print(ret)
        while ret <= 0:
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR), 2500, 0)
            if ret > 0:
                print('CAN1 Received Successfully\r\n')
                print('ID：')
                print(vci_can_obj_1.ID)
                print('DataLen：')
                print(vci_can_obj_1.DataLen)
                print('Data：')
                print(list(vci_can_obj_1.Data))
            
            if exit_flag == 1:
                break
            
            time.sleep(1000/1000)

def thread_run04(stop_flag):
    global vci_can_obj_1
    
    # Channel 1 Send Data
    ubyte_array = c_ubyte*8
    a = ubyte_array(1, 2, 3, 4, 5, 6, 7, 8)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    
    while True:
        if stop_flag():  
            vci_can_obj_1 = VCI_CAN_OBJ(0x1, 0, 0, 1, 0, 0,  8, a, b)
            ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 1, byref(vci_can_obj_1), 1)
            if ret == STATUS_OK:
                print('CAN2 Sent Successfully\r\n')
            if ret != STATUS_OK:
                print('CAN2 Sending Failed\r\n')
        
        if exit_flag == 1:
            break
		
        time.sleep(1000/1000)

def signal_handler(signum, frame):
    
    print('signal_handler: caught signal ' + str(signum))
    
    if signum == signal.SIGINT.value:
        print('SIGINT')
        sys.exit(1)

def exe_do():
    threads = []
    
    print(CanDLLName)
    
    ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        print('Open VCI Device Success\r\n')
    if ret != STATUS_OK:
        print('Open VCI Device Fail\r\n')

    vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)  # 500 Kbps, 0x00 0x1C 
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
    if ret == STATUS_OK:
        print('Initialize VCI CAN1 Success\r\n')
    if ret != STATUS_OK:
        print('Initialize VCI CAN1 Fail\r\n')
     
    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        print('Start VCI CAN1 Success\r\n')
    if ret != STATUS_OK:
        print('Start VCI CAN1 Fail\r\n')
     
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 1, byref(vci_initconfig))
    if ret == STATUS_OK:
        print('Initialize VCI CAN2 Success\r\n')
    if ret != STATUS_OK:
        print('Initialize VCI CAN2 Fail\r\n')
     
    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 1)
    if ret == STATUS_OK:
        print('Start VCI CAN2 Success\r\n')
    if ret != STATUS_OK:
        print('Start VCI CAN2 Fail\r\n')

def check_input_status(str):
    global stop_flag
    
    status = 0
    
    if str == 'd' or str == 'D' :
        print('Disable(Stop) ......\r\n')
        stop_flag = False
    elif str == 'e' or str == 'E' :
        print('Enable(Start) ......\r\n')
        stop_flag = True
    elif str == 'i' or str == 'I' :
        stop_flag = False
        status = 2
        print('Input Data ......\r\n')
    else :
        if str == 'q' or str == 'Q' :
            print('Closure VCI Device ......\r\n')
            canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)
            status = 1
    
    return status

if __name__ == '__main__':
    global exit_flag
    
    exit_flag = 0
    
    exe_do()

    # CAN1 Transmit
    #t1 = threading.Thread(target=thread_run01, args = (lambda : stop_flag, ))
    #t1.daemon = True
    #t1.start()
    
    # CAN2 Received
    #t2 = threading.Thread(target=thread_run02, args = (lambda : stop_flag, ))
    #t2.daemon = True
    #t2.start()
    
    # CAN1 Received
    t3 = threading.Thread(target=thread_run03, args = (lambda : stop_flag, ))
    t3.daemon = True
    t3.start()
    
    # CAN2 Transmit
    t4 = threading.Thread(target=thread_run04, args = (lambda : stop_flag, ))
    t4.daemon = True
    t4.start()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        input_str = input()
        print(len(input_str), input_str)
		
        fb_var = check_input_status(input_str)
        if fb_var == 1:
            exit_flag = 1
            print('Count down 3 seconds to leave ......\r\n')
            time.sleep(3000/1000)
            break
        elif fb_var == 2:
            print('Please enter eight numbers ......\r\n')
            input_a = input().split(',')
            input_a = [x for x in input_a if x != '']
            while '' in input_a:
                input_a.remove('')
            int_list = list(map(int, input_a[0:8]))
            print(int_list)
            #ubyte_array = c_ubyte*8
            #a = ubyte_array(1, 2, 3, 4, 5, 6, 7, 8)
            break
