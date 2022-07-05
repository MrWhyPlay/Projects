# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 22:04:52 2022

@author: XYZ
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path
import gc
import time
import matplotlib.pyplot as plt


#PATH="E:/DeepLrningCode/ICAV TECH 2022/data/"
#FNAME="Input_Data"


def IOFile(path,fname):
    problem_instance=""
    vehicle_cap=0.0
    vehicle_number=0
    xcoord=[]
    ycoord=[]
    demand=[]
    readytime=[]
    duetime=[]
    servicetime=[]
    custno=[]
    fpath = Path(os.path.join(path,fname+".txt"))
    start = time.time()
    if fpath.exists():
        print(f"{fname} exists.....")
        with open(fpath,"rt",newline='') as file:
            file = open(fpath)
            for line_number,content in enumerate(file,start=1):
                if line_number==1:
                    problem_instance = content.strip()
                if line_number==5:
                    values = content.strip().split()
                    print(values)
                    vehicle_cap = float(values[1])
                    vehicle_number = int(values[0])
                if line_number>=10:
                    values = content.strip().split()
                    if len(values) >0:
                        custno.append(values[0])
                        xcoord.append(float(values[1]))
                        ycoord.append(float(values[2]))
                        demand.append(float(values[3]))
                        readytime.append(float(values[4]))
                        duetime.append(float(values[5]))
                        servicetime.append(float(values[6]))
            file.close()
    write_csv = pd.DataFrame({"CUST NO":custno,"XCOORD":xcoord,"YCOORD":ycoord,"DEMAND":demand,"READY_TIME":readytime,"DUE_DATE":duetime,"SERVICE_TIME":servicetime})
    print(write_csv.head())
    write_csv.to_csv("E:/DeepLrningCode/ICAV TECH 2022/data.csv",sep=",",index=False)
    print("\nCleaning memory...")
    del custno,xcoord,ycoord,demand,readytime,duetime,servicetime
    gc.collect()
    end=time.time()
    print(f"\nPreprocessing of data completed in {round(end-start,2)} seconds...")
    return write_csv,problem_instance,vehicle_cap,vehicle_number

#if __name__=="__main__":
#    data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
    