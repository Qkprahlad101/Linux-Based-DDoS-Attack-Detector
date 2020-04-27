import pandas as pd
import numpy as np
import pickle
import time
import os
import time
import tkinter as tk
from tkinter import simpledialog

def preprocessing():
	#dialog box input
        root = tk.Tk()
        root.withdraw()
        #the dialog box
        inp = simpledialog.askstring(title="File", prompt ="Which file you wanna check? ")
        
        print('\x1b[0;30;47m' + ' Preprocessing... ' + '\x1b[0m')
        df = pd.read_csv(inp,delimiter=',')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	#df = df.drop(['Proto','Sport', 'Dport', 'SrcAddr', 'DstAddr', 'Dur' ], axis = 1)
	# y = df.iloc[:, -1].values
        if 'Label' in df.columns:
                df = df.drop(['Label'], axis = 1)
        x = (df-df.mean())/df.std()
        return x

def prediction(input):
	predicted = model.predict(input)[0]
	if(predicted == 0):
		global c1
		c1 += 1
		return 0

	else:
		global c2
		c2 += 1
		return 1

def details():
	print("\033[93m {}" .format('Summary: ')) 
	print(" Total packets captured:\t{}" .format(c1 + c2))
	print(" Total attacking packets:\t{}" .format(c2))
	print(" Total non-attacking packets:\t{}\033[00m" .format(c1))
	print("-------------------------------------------------------\n")

c1, c2, c = 0, 0, 1
model = pickle.load(open('DTddosFinal', 'rb'))
def driver():
	os.system('color')
	x = preprocessing()
	global model
	global c
	prevflag = -1
	flag = 0
	n = len(x)
	for i in range(n):
		input = np.array(x.iloc[i, :])
		input = np.expand_dims(input, axis = 0)
		flag = prediction(input)
		if(flag != prevflag):
			prevflag = flag
			os.system('cls' if os.name == 'nt' else 'clear')
			if(flag == 0):
				print('\x1b[6;30;42m' + ' Model Prediction: Safe ' + '\x1b[0m')
			else:
				print('\x1b[0;30;41m' + ' Model Prediction: DDoS Attack!!! ' + '\x1b[0m')
		if(c % 10000 == 0):
			os.system('cls' if os.name == 'nt' else 'clear')
			if(flag == 0):
				print('\x1b[6;30;42m' + ' Model Prediction: Safe ' + '\x1b[0m')
			else:
				print('\x1b[0;30;41m' + ' Model Prediction: DDoS Attack!!! ' + '\x1b[0m')
			details()
		c += 1

driver()
