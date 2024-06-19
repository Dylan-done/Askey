
import threading
import time
from ctypes import *

VCI_USBCAN2 = 4  # USBCAN-2A, USBCAN-2C or CANalyst-II 
STATUS_OK = 1

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

def thread_run01():
    global vci_can_obj_0
    
    # Channel 1 Send Data
    ubyte_array = c_ubyte*8
    a = ubyte_array(0, 16, 0, 0, 0, 0, 0, 0)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    
    while True:
        vci_can_obj_0 = VCI_CAN_OBJ(0x1, 0, 0, 1, 0, 0,  8, a, b)
        
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj_0), 1)
        if ret == STATUS_OK:
            print('CAN1 Sent Successfully\r\n')
        if ret != STATUS_OK:
            print('CAN1 Sending Failed\r\n')
        
        time.sleep(640/1000)

def thread_run02():
    
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
	    
        time.sleep(1000/1000)

def thread_run03():
    
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
	    
        time.sleep(1000/1000)

def thread_run04():
    global vci_can_obj_1
    
    # Channel 1 Send Data
    ubyte_array = c_ubyte*8
    a = ubyte_array(3, 65, 13, 100, 0, 0, 0, 0)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    
    while True:
        vci_can_obj_1 = VCI_CAN_OBJ(0x7E8, 0, 0, 1, 0, 0,  8, a, b)
        
        ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 1, byref(vci_can_obj_1), 1)
        if ret == STATUS_OK:
            print('CAN2 Sent Successfully\r\n')
        if ret != STATUS_OK:
            print('CAN2 Sending Failed\r\n')
        
        time.sleep(100/1000)

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
    
    # CAN1 Transmit
    #t1 = threading.Thread(target=thread_run01)
    #t1.daemon = True
    #t1.start()
    
    # CAN2 Received
    t2 = threading.Thread(target=thread_run02)
    t2.daemon = True
    t2.start()
    
    # CAN1 Received
    t3 = threading.Thread(target=thread_run03)
    t3.daemon = True
    t3.start()
    
    # CAN2 Transmit
    t4 = threading.Thread(target=thread_run04)
    t4.daemon = True
    t4.start()

if __name__ == '__main__':

    exe_do()

    while True:
        time.sleep(10)
    
    # Closure VCI Device
    canDLL.VCI_CloseDevice(VCI_USBCAN2, 0) 	