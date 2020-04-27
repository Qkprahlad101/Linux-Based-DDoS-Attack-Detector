# -*- coding: utf-8 -*-
"""Deloitte_Experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ujVjAbLqMjKPfR99yzdzlcciT9CXsg5F
"""

import pandas as pd
import os
import glob

path = os.getcwd()
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)
for i in result:
        df = pd.read_csv(i,delimiter=' ',skipinitialspace=True) #skipinitialspace=True is used to remove any space before or after strings
        df = df.iloc[:,~df.columns.str.contains('Unnamed')] #removing unnamed column
        f4 = df

        #Adding extra features
        sum_sip= f4.groupby('SrcAddr')['SrcPkts'].sum()                 #Sum of all the packets sent by each source IP address
        dport_sip= f4.groupby('SrcAddr')['Dport'].count()     #Count of each destination ports contacted by each source IP address
        dadr_sip= f4.groupby('SrcAddr')['DstAddr'].count()       #Count of each destination address contacted by each source IP address
        sport_dip= f4.groupby('DstAddr')['Sport'].count()     #Count of each source ports contacted by each destination IP address
        saddr_dip= f4.groupby('DstAddr')['SrcAddr'].count()         #Count of each source address contacted by each destination IP address    
        spkt_dip= f4.groupby('DstAddr')['DstPkts'].sum()                  #Sum of all the packets sent by each destination IP address
        sbyt_sip= f4.groupby('SrcAddr')['SrcBytes'].sum()                     #Sum of all the bytes sent by each source IP address
        sbyt_dip= f4.groupby('DstAddr')['DstBytes'].sum()    #Sum of all the bytes sent by each destination IP address
        f4['Tpkt_Saddr'] = f4['SrcAddr'].map(sum_sip)
        f4['Tportcnt_Saddr'] = f4['SrcAddr'].map(dport_sip)
        f4['Tdaddrcnt_Saddr'] = f4['SrcAddr'].map(dadr_sip)
        f4['Tbytes_Saddr'] = f4['SrcAddr'].map(sbyt_sip)
        f4['Tbytes_Daddr'] = f4['DstAddr'].map(sbyt_dip)
        f4['Tpkt_Daddr'] = f4['DstAddr'].map(spkt_dip)
        f4['Tsaddrcnt_Daddr'] = f4['DstAddr'].map(saddr_dip)
        f4['Tportcnt_Daddr'] = f4['DstAddr'].map(sport_dip)   
        #zscore normalisation
        f4 = f4.drop(['SrcAddr','DstAddr','Dur','Proto','Sport','Dport'],axis=1)
        f4 = f4.replace('\*','',regex=True).astype(float)  # removing * at the end of certain numbers in the file
        f4 = (f4-f4.mean())/f4.std()
        f4.to_csv(i)

