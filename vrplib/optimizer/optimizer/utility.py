# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 22:07:05 2022

@author: XYZ
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path
import gc
import time
from optimizer.optimizer.parse_data import IOFile
import matplotlib.pyplot as plt

#PATH="E:/DeepLrningCode/ICAV TECH 2022/data/"
#FNAME="Input_Data"


def distance(data,cust1,cust2):
    #print(f"Selecting customer {cust1} and customer2 {cust2}")
    cust1 = int(cust1)
    cust2 = int(cust2)
    cust1_xcoord = data["XCOORD"].iloc[cust1]
    cust1_ycoord = data["YCOORD"].iloc[cust1]
    cust2_xcoord = data["XCOORD"].iloc[cust2]
    cust2_ycoord = data["YCOORD"].iloc[cust2]
    #print(cust1_xcoord,cust1_ycoord,cust2_xcoord,cust2_ycoord)
    dist = round(np.sqrt((cust1_xcoord-cust2_xcoord)**2 + (cust1_ycoord-cust2_ycoord)**2 ),2)
    return dist



def plot_data(data:pd.DataFrame,probname):
    #imgpath=PATH[:-5]+"img"+"/"
    fig,ax = plt.subplots(figsize=(8,6))
    ax.scatter(data["XCOORD"].iloc[0],data["YCOORD"].iloc[0],marker="s",color="red",edgecolor="k",label="Depot")
    ax.scatter(data["XCOORD"].iloc[1:],data["YCOORD"].iloc[1:],color="blue",edgecolor="black",alpha=0.5,label="Customer")
    ax.legend(loc="center left",bbox_to_anchor=(1,0.5))
    ax.set_title(f"Position of Customers and Depot in Instance {probname}")
    ax.set_xlabel("X-Coordinate")
    ax.set_ylabel("Y-Coordinate")
    

def search_cust(fres,nextcust):
    nextc=0
    #fres = PATH[:-5] + "Result" + "/" + "result.txt"
    with open(fres,"r") as fos:
        fos = open(fres)
        for line_number, content in enumerate(fos,start=1):
             if content[0]=='x':
                val = content.replace("x"," ").replace("("," ").replace(")"," ").replace("="," ").split()
                val = val[0].split(",")  
                if int(val[0]) == int(nextcust[1]):
                   nextc = val[1]
        fos.close()          
    return nextc


def total_distance(optroute:dict,data:pd.DataFrame):
    total_dist=0.0
    for key,value in optroute.items():
        rt = optroute[key]
        route_dist=0.0
        for i in range(len(rt)-1):
            route_dist += distance(data,rt[i],rt[i+1])
        total_dist += route_dist
    return total_dist

def route_distance(optroute:dict,data:pd.DataFrame,key):
    
    #for key,value in optroute.items():
    rt = optroute[key]
    route_dist=0.0
    for i in range(len(rt)-1):
            route_dist += distance(data,rt[i],rt[i+1])
    return route_dist

def display_route(optroute:dict,data:pd.DataFrame):
    
    fig,ax = plt.subplots(figsize=(8,6))
    for key,value in optroute.items():
        rt = optroute[key]
        xcoord=[]
        ycoord=[]
        for idx in rt:
            xcoord.append(data["XCOORD"].iloc[int(idx)])
            ycoord.append(data["YCOORD"].iloc[int(idx)])
        ax.scatter(data["XCOORD"].iloc[0],data["YCOORD"].iloc[0],marker="s",color="red",edgecolor="black",alpha=0.5)
        ax.scatter(xcoord,ycoord,marker="o",color="blue",edgecolor="black",alpha=0.6)
        dist = route_distance(optroute,data,key)
        ax.plot(xcoord,ycoord,label=f"Route_{key} | Dist. {round(dist,2)} KM")
    plt.legend(loc="center left",bbox_to_anchor=(1,0.5))
    plt.title("Optimum Route")
    
    
    plt.show()    
        

def postprocessing(fpath,data):
    fresult = fpath[:-5] + "Result" + "/" + "result.txt"
    vehicle_numbers=0
    routes={}
    def next_customer(fres,next_cust):
        
        rt=[]
        #next_c = 0
        next_c = search_cust(fres,next_cust)
        #print(f"Next {next_c}")
        while int(next_c) != 0:
            rt.append(next_c)
            next_cust[1] = next_c
            #print(f"Next Cutomer# {next_c}")
            next_c = search_cust(fres,next_cust)
            #print(f"N NEXT {next_c}")
        return rt
        
    
            
    with open(fresult,"r") as fo:
        fo = open(fresult)
        for line_number,content in enumerate(fo,start=1):
            route=[]
            if content[0]=='x' and content[2]=='0':
                value = content.replace("x"," ").replace("("," ").replace(")"," ").replace("="," ").split()
                vehicle_numbers+=1
                next_cust = value[0].replace(","," ").strip().split()
                route.append(next_cust[1])
                #print(f"Next Customer {int(next_cust[1])}")
                next_to_next = next_customer(fresult,next_cust)
                #next_to_next = [next_cust[1]] + next_to_next
                route.extend(next_to_next)
                #print(f"Next to Next Customer {next_to_next}")
                #next_to_next = [int(next_cust[0])] + next_to_next
                routes[vehicle_numbers] = [0] + route + [0]
                #next_to_next=[]
        
        total_dist = total_distance(routes,data)
        print(f"Total Distance {round(total_dist,2)} | Vehicles used {vehicle_numbers}\n")
        print("Optimum Route\n")
        print(routes)
        fo.close()
        display_route(routes,data)


#if __name__=="__main__":
#    route={}
#    data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
#    route[1] = [0,3,2,1,6,0]
#    rdist = route_distance(route,data,1)
#    plot_data(data,prob_instance)
#    postprocessing(PATH,data)