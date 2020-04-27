#!/bin/bash

#argus installation
sudo apt-get install argus-client

#pandas
pip install pandas
#tkinter
sudo apt-get install python-tk
#numpy
sudo apt-get install python-numpy

sudo apt-get update

for variable in `find *.pcap`
do
	argus -r $variable -w $variable.argus
	ra -r $variable.argus -u -s rank,stime,ltime,dur,saddr,daddr,proto,pkts,spkts,dpkts,bytes,sbytes,dbytes,rate,srate,drate,sport,dport > $variable.csv
done
find -name '*.argus' -not -path /tmp -exec rm -vr {} \;
python preprocess.py
python main.py
