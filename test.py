# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 23:07:29 2022
Open CMD
Go to the directory where you copied the test.py
python -m unittest test.py
@author: XYZ
"""

import unittest
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


class testvrpsolver(unittest.TestCase):

      def testiofile(self):
          print("Testing IOFILE...\n")
          data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
          expected_prob_instance="C104"
          expected_vehicle_cap = 70
          expected_vehicle_number = 10
          self.assertEqual(prob_instance,expected_prob_instance)
          self.assertEqual(vehicle_cap,expected_vehicle_cap)
          self.assertEqual(vehicle_number,expected_vehicle_number)
    
      def testroutedistance(self):
          print("Testing Route Distance...\n")
          route={}
          data,prob_instance,vehicle_cap,vehicle_number = IOFile(PATH,FNAME)
          expected =  47.22
          route[1] = [0,3,2,1,6,0]
          actual = route_distance(route,data,1)
          self.assertEqual(round(actual,2),expected)


