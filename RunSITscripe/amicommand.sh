sleep 2
AmiClient_demo
sleep 5
echo "======================="
echo "Start AMI test"
echo "======================="
#echo "===========IO log Setting enable============"
#AmiClient_demo -log 1
#sleep 5
echo "===========Enter FTM mode============"
AmiClient_demo -ftm 1
sleep 5
AmiClient_demo -qp
sleep 5
echo ""
echo "===========LTE TX============"
AmiClient_demo -a 1 -ltp 230 -ltd -1
sleep 5
AmiClient_demo -a 1 -ltp 230 -ltd 0
sleep 5
AmiClient_demo -a 5 -ltp 230 -ltd -1
sleep 5
AmiClient_demo -a 5 -ltp 230 -ltd 0
sleep 5
echo ""
echo "===========LTE RX============"
AmiClient_demo -lra 1
sleep 5
AmiClient_demo -lra 2
sleep 5
AmiClient_demo -lra 3
sleep 5
AmiClient_demo -lra 4
sleep 5
AmiClient_demo -lra 5
sleep 5
AmiClient_demo -lra 6
sleep 5
echo ""
echo "===========CV2X TX============"
AmiClient_demo -a 7 -vtp1 230 -vtp2 100 -vtd -1
sleep 5
AmiClient_demo -a 7 -vtp1 230 -vtp2 100 -vtd 0
sleep 5
AmiClient_demo -a 8 -vtp1 230 -vtp2 100 -vtd -1
sleep 5
AmiClient_demo -a 8 -vtp1 230 -vtp2 100 -vtd 0
sleep 10
echo ""
echo "===========CV2X RX============"
AmiClient_demo -vra 7
sleep 5 
AmiClient_demo -vra 8
sleep 5
echo ""
echo ""
#echo "===========IO log Setting disable============"
#AmiClient_demo -log 0
#sleep 5
echo "===========Exit FTM mode============"
AmiClient_demo -ftm 0
sleep 5
echo ""
echo "======================="
echo "finish Ami test "

#echo " Please Restart DUT after Test 5GNR "
#echo "===========NR5G TX============"
#echo " AmiClient_demo -ntp 100 -ntd -1 "
#echo ""
#echo "===========NR5G RX============"
#echo " AmiClient_demo -nra "



