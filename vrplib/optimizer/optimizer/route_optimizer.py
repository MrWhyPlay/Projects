# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 22:19:24 2022

@author: XYZ
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path
import gc
import time
from optimizer.optimizer.parse_data import IOFile
from optimizer.optimizer.utility import distance
from mip import *
import matplotlib.pyplot as plt

#PATH="E:/DeepLrningCode/ICAV TECH 2022/data/"
#FNAME="Input_Data"


class VRPSOLVER():
    def __init__(self,data,vcapacity,vnumber,path,fname):
        self.data = data
        self.model = Model()
        self.bigM = 99999
        self.customers = [i for i in range(1,len(data))]
        self.vertex = [0] + self.customers
        self.arc = [(i,j) for i in self.vertex for j in self.vertex if i!=j]
        self.status=None
        self.start=time.time()
        self.end = None
        self.vehicle_cap = vcapacity
        self.vehicle_number = vnumber
        self.path = path
        self.fname = fname
       
    def create_var(self):
        self.x_bin = [[self.model.add_var(var_type=BINARY,name =f"x({i},{j})") for j in self.vertex] for i in self.vertex]
        self.model.objective= minimize(xsum(distance(self.data,i,j)*self.x_bin[i][j] for i in self.vertex for j in self.vertex if i!=j) +\
                                       xsum(self.x_bin[0][j] for j in self.customers))
        "Constraint 1"
        for i in self.customers:
            self.model += xsum(self.x_bin[i][j] for j in self.vertex if i!=j)==1
        for j in self.customers:
            self.model += xsum(self.x_bin[i][j] for i in self.vertex if i!=j)==1
        "Indicator Constraint Equivalent:"
        "If bin_x[i,j]==1 then u[i] + demand[j] <= u[j]"
        "Where q[i] <= u[i] <= Capcity"
        self.u = [self.model.add_var(name=f"u({i})",lb=self.data["DEMAND"].iloc[i],ub=self.vehicle_cap) for i in self.vertex]     
        for i,j in self.arc:
            if i!=j and j!=0:
                self.model += self.u[i] + self.data["DEMAND"].iloc[j] + self.bigM * self.x_bin[i][j] <= self.u[j] + self.bigM
        "Indicator Constraint Equivalent:"
        "If bin_x[i,j]==1 then t[i] + service[j] <= t[j]"
        "Where q[i] <= u[i] <= Capcity"  
        "Arrival time at t[i]"
        self.t = [self.model.add_var(name = f"t({i})", lb = self.data["READY_TIME"].iloc[i], ub = self.data["DUE_DATE"].iloc[i]) for i in self.vertex]
        self.t[0] = self.data["READY_TIME"].iloc[0]
        self.bigM=99999
        for i,j in self.arc:
            if i!=j and j!=0:
               self.model += self.t[i] + self.data["SERVICE_TIME"].iloc[i] + 1 * distance(self.data,i,j) + self.bigM*self.x_bin[i][j] <= self.t[j] + self.bigM 
        "Sub-tour Elimination MTZ:"
        self.U = [self.model.add_var(name = f"U({i})",lb=0,ub=np.inf) for i in range(1,len(self.customers)+2)]
        for i in self.vertex:
            for j in self.vertex:
                if i !=j and i!=0 and j!=0:
                
                    self.model += self.U[i]-self.U[j] + (len(self.vertex)-1)*self.x_bin[i][j] <= (len(self.vertex)-2)
        self.model.max_gap = 0.16
        print("\nStarting the Open Source Solver.Please wait..\n")
        print("Searching for optimum route...\n")
        self.status = self.model.optimize(max_seconds=300)
        print(f"Status : {self.status}")
        if self.status == OptimizationStatus.OPTIMAL:
           print(f"Optimal solution  {self.model.objective_value}\n")
        elif self.status == OptimizationStatus.FEASIBLE:
             print(f"Optimal solution {self.model.objective_value} and best possible {self.model.objective_bound}\n")
        elif self.status == OptimizationStatus.NO_SOLUTION_FOUND:
             print(f" No feasible solution found, lower bound {self.model.objective_value}\n")
        else:
             print(f"Infeasible Problem\n ")
        fresult = self.path[:-5] + "Result" + "/" + "result.txt"
        if self.status == OptimizationStatus.OPTIMAL or self.status == OptimizationStatus.FEASIBLE:
           print('solution:')
           with open(fresult,"w") as fres:
                for v in self.model.vars:
           
                     if abs(v.x) > 1e-6: # only printing non-zeros
                         print('{} = {}'.format(v.name, v.x))
                         fres.write(f"{v.name} = {v.x}")
                         fres.write("\n")
           fres.close()
                   
                       
        fpath = self.path[:-5] + "LP" + "/" + self.fname +"_VRPTW_MIP.lp"
        self.model.write(fpath)
        self.end = time.time()
        print(f"Computational Time: {round(self.end - self.start,2)} Secs")


#if __name__ == "__main__":
#    data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
#    vrpsolver = VRPSOLVER(data,vehicle_cap,vehicle_number)
#    vrpsolver.create_var()