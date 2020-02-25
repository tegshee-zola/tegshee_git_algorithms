# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 19:24:21 2019

@author: Voltron
"""

import nidaqmx
from nidaqmx import *
from nidaqmx.constants import *
from nidaqmx.errors import *

import sys
import time
import csv
import argparse
from datetime import datetime

#%% Relay-to-NIDAQ mapping
loads = {10:"Dev1/port1/line7",8:"Dev1/port1/line6",11:"Dev1/port1/line5",
         6:"Dev1/port2/line7",4:"Dev1/port2/line6",7:"Dev1/port2/line5",
         5:"Dev1/port2/line4",1:"Dev1/port2/line3",9:"Dev1/port2/line2",
         2:"Dev1/port2/line1",3:"Dev1/port2/line0",0:"Dev1/port0/line0"}

#%% Switching functions
def toggle(loadnum,activateTF):
    temptask = nidaqmx.Task('temp')
    temptask.do_channels.add_do_chan(loads[loadnum])
    if activateTF:
        temptask.write([True])
    else:
        temptask.write([False])
    temptask.close()
    
def open_all():
    for k in range(12):
        toggle(k,0)

def close_all():
    for k in range(12):
        toggle(k,1)

def mark_elapsed_time(clockstart):
    return time.time()-clockstart