#Smoke test /
#ver ALPS RSU


arg1="$1"

#result
tmp_HW="/tmp/HWresult"
tmp_SW="/tmp/SWresult"
tmp_end="/home/root/result"

#tmp
tmp_1="/tmp/tmp1.txt"
tmp_2="/tmp/tmp2.txt"
tmp_="/tmp/tmp.txt"

#pc side setting 
eth0="10.0.0.2"

#ping WWAN 
ipv4_="8.8.8.8"
ipv6_="2001:4860:4860::8888"
dns_="dns.google "


###############

function ami_Check(){
	#AMI
	echo "AMI " >> ${tmp_end}
	AmiClient_demo | grep fwver >> ${tmp_end}
}

function internet_check(){
echo "Network"
echo "Ipv4/6/DNS ICMP check"
	ping -I usb0.10 -c 1 ${ipv4_}
	if [ $? == "0" ]; then
			sim1_ipv4="1"	
	else 
		echo "usb0.10 ipv4 Ping : false" >> ${tmp_end}
			sim1_ipv4="0"
	fi
		
	ping -I usb0.10 -c 2 ${ipv6_} 
	if [ $? == "0" ]; then
			sim1_ipv6="1"
	else 
		echo "usb0.10 ipv6 Ping : false " >> ${tmp_end} 
		sim1_ipv6="0"
	fi

	ping -I usb0.10 -c 2 ${dns_}
	if [ $? == "0" ]; then
		sim1_DNS="1"
	else 
		echo "usb0.10 DNS Ping : false " >> ${tmp_end} 
		sim1_DNS="0"
	fi	
		
	sleep 1
					
		
	if [ $sim1_ipv4 = "1" ] && [ $sim1_ipv6 = "1" ] && [ $sim1_DNS = "1" ]; then
		echo "SIM1 : true" >> ${tmp_end}
	else
		echo "SIM1 : false" >> ${tmp_end}
	fi
		
	sleep 1				
	clear
}

function ethernet_check(){
	ping -c 1 ${eth0}
	if [ $? == "0" ]; then
		echo "eth0 : true " >> ${tmp_end}
	else 
		echo "eth0 : false " >> ${tmp_end}			
	fi
		
}

function gps_check(){
	echo " **GPS function test"
	chronyc sources -v
	sleep 1 
	gpspipe -r | grep RMC &
	sleep 1
	killall gpspipe -r

	#echo " =====================MQTT v2x/gnss======================================="
	#mosquitto_sub -h 127.0.0.1 -p 1883 -u admin -P admin -t "/v2x/gnss" &
	#sleep 1
	#killall mosquitto_sub
	echo " ==================================================================="
		
	sleep 1	
}

function acme_check(){

	echo " **Check CV2X status"
	kinematics-sample-client -a -n 1 | grep -E "lat|long"
	echo " ==================================================================="
	echo " ==================================================================="
	cv2x-config --get-v2x-status | grep V2X
	echo " ==================================================================="
	sleep 1
		
	echo "acme TX"
	acme &
	sleep 5
	killall acme 
		
	echo "acme RX"
	acme -R &
	sleep 5
	killall acme

	clear
}

function store_space_check(){
#dmesg | grep -i FAILED >> HWrerult
	echo " **OTG/eMMC space"
	df -h 
	echo " ===================================================================" >> result
}

function time_check(){

echo "time_check" >> ${tmp_end}
date -R >> ${tmp_end}
sleep 1

}

function result_show(){
cat ${tmp_HW} >> ${tmp_end}
cat ${tmp_SW} >> ${tmp_end}
sleep 1	
cat ${tmp_end}
}

function result_del(){
rm -r ${tmp_end}
}

function sim_information(){

echo -e "1\n15\n1\n4\n0\n0\n" | telsdk_console_app | grep -i3 iccid
sleep 1

}
###############
function Setup(){
	clear
    echo "Setup env"
}

function hw_Check(){
    clear
	rm -r ${tmp_HW}
	echo "HW check"
	CHECKSPI=`dmesg | grep -Fo "fsl-flexspi 5d120000.flexspi: mt35xu256aba (32768 Kbytes)"`
	if [ "$CHECKSPI" = "fsl-flexspi 5d120000.flexspi: mt35xu256aba (32768 Kbytes)" ]; then
		echo "Kernel SPI NOR : true " >> ${tmp_HW} 
	else 
		echo " Kernel SPI NOR : false " >> ${tmp_HW}
	fi

	EV1=`fw_printenv HW_VER`
	if [ "$EV1" = "HW_VER=EV1" ]; then
		echo "HW_Version : true " >> ${tmp_HW} 	
	else 
		echo "HW_Version : false  " >> ${tmp_HW} 
	fi

 
	echo "  {fdisk -l (get mtblock0 ~ mtdblock2 data)" >> ${tmp_HW}
	fdisk -l  > tmp.txt 
	cat tmp.txt | grep -i "/dev/mmcblk0p1" >> ${tmp_HW}
	cat tmp.txt | grep -i "/dev/mmcblk0p2" >> ${tmp_HW} 
	cat tmp.txt | grep -i "/dev/mmcblk0p3" >> ${tmp_HW}
	cat tmp.txt | grep -i "/dev/mmcblk0p4" >> ${tmp_HW}
	rm -r tmp.txt
	

	echo " DDR4/DRAM 1.7G"
	DRAM=`free -h | grep -o 1.7G`
	if [ "$DRAM" = "1.7G" ]; then
		echo "DRAM : true " >> ${tmp_HW}
	else 
		echo " DRAM : false  " >> ${tmp_HW}
	fi
	
	echo " **HSM"
	touch ${tmp_}
	touch ${tmp_2}
	/usr/bin/sxf1800/v2xse-se-info  > ${tmp_}
	cat ${tmp_} | grep -i "Utility ver" > ${tmp_2}
	cat ${tmp_2}

	HSM=`cat ${tmp_2}`
	if [ "$HSM" = "Utility version is: 2.1.2" ]; then
		echo "HSM : true " >> ${tmp_HW}
	else 
		echo "HSM : false " >> ${tmp_HW}
	fi
	rm -r ${tmp_}
	rm -r ${tmp_2}


}

function sw_Check(){

	rm -r ${tmp_SW}
	
	clear
    #####################
	echo "SW check"
	sleep 1	
	echo "SW_Version " >> ${tmp_SW}
	cat /proc/sw_version >> ${tmp_SW}
	echo "OBU build "
	cat /etc/build 
	#pt_diagnostics
	
	#pt_diagnostics >> ${tmp_1}
	
	#cat ${tmp_1} | grep -i soc_fw_ver >> ${tmp_SW}
	#cat ${tmp_1} | grep -i mcu_fw_ver >> ${tmp_SW}
	#cat ${tmp_1} | grep -i alps_sdk_ver >> ${tmp_SW}
	#cat ${tmp_1} | grep -i alps_fw_ver >> ${tmp_SW}
	
	#rm -r ${tmp_1}
	
	echo "RSU SDK Version " >> ${tmp_SW}
	cat /etc/alap_version | grep Version >> ${tmp_SW}

	#echo "MCU APP_VER " >> ${tmp_SW}
	#echo "TEST_START" > /opt/sfifo
	#tail -f /run/media/mmcblk0p4/runlog.txt | grep "MCU ver" & >> ${tmp_}
	#echo "TEST_MCU get_mcu_ver" > /opt/sfifo && sleep 3
	#cat ${tmp_} >> ${tmp_SW}
	#killall tail 
	#echo "TEST_STOP" > /opt/sfifo
	#rm -r ${tmp_}
	
	echo "================================================"
	echo "ALPS Ver = " >> ${tmp_SW}
	adb shell cat /firmware/image/Ver_Info.txt | grep -i 5AB >> ${tmp_SW}

#####################
	echo " ===================================================================" >> ${tmp_SW}
	
	clear
}

function func_check(){

    echo "Test Scripe " >> ${tmp_end}
	echo "Function check"		
	
	ami_Check

	while true : 
	do 		
		result_del							
		
		#SIM Check
		#telsdk fail TBD		
		##sim_information
		
		#sim1 sim2 
		internet_check
		
		#ETH
		ethernet_check			
						
		gps_check
		
		#acme_check
		
		time_check
				
		result_show		
		
		sleep 10
		
		if [ "$arg1" = "reboot" ]; then
			echo " received reboot arg system reboot "
			reboot
		else 
			store_space_check
		fi
	done	
}

function print_help(){

echo "basic ex: ./rsu_demo.sh basic"

echo "=================detail================="
echo "'basic' : function test "
echo "Rsu test point V2X/mqtt/ssh "

}

function rm_config(){

echo "remove config"
rm -r /run/media/mmcblk0p4/runlog*

}

###############
case "${arg1}" in
	"basic")
		Setup
		hw_Check
		sw_Check
		func_check
		;;
	*)
		print_help
		;;
esac



