# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 22:34:24 2022

@author: XYZ
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path
import gc
import time
from optimizer.optimizer.parse_data import IOFile
from mip import *
import matplotlib.pyplot as plt
from optimizer.optimizer.route_optimizer import *
from optimizer.optimizer.utility import distance,plot_data,search_cust,total_distance,route_distance,display_route,\
       postprocessing


PATH="E:/DeepLrningCode/ICAV TECH 2022/data/"
FNAME="Input_Data"


data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
plot_data(data,prob_instance)
vrpsolver = VRPSOLVER(data,vehicle_cap,vehicle_number,PATH,prob_instance)
vrpsolver.create_var()
postprocessing(PATH,data)
