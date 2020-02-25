"""
Created on 

@author: Tegshee

"""

import time
import csv

#OGE Libs 
import helper as helper
import util as util
import manual_relay_switcher as switcher

# set-up interface with string
interface = helper.quick_init('COM3')


#### Test Setup ####
def init():
    # power-on
    interface.serial.send_cmd("prov-set 3")
    print('waiting for 60 seconds for prov-set 3')
    time.sleep(60)
    
    # Check SOC at wake-up moment
    interface.serial.send_cmd("state-get")

    # Turn on grid
    switcher.toggle(0, 1)
    lines = interface.serial.send_cmd("eac-grid-data")
    #Check whether connection is closed
    data = util.parse_formatted_lines(lines)
    if(data.get('Grid contactor status') == 'Closed'):
        return True
    else:
        time.sleep(60)
        print('Grid not synced. Waiting for grid sync')

#### Test cycle ####
def get_cli(cli, parameter):
    lines  = interface.serial.send_cmd(cli)
    data = util.parse_formatted_lines(lines).get(parameter)
    return data


def check_inv():
    lines = interface.serial.send_cmd("eac-list")
    for i in range(3):
        if util.parse_formatted_lines(lines).get('state_%'(i)) == 'active':
            sn = util.parse_formatted_lines(lines).get('SN_%'(i))
            lines = interface.serial.send_cmd('eac-inv-data %'(sn))
            sunspec_state = util.parse_formatted_lines (lines).get('sunspec state')
            enphase_state= util.parse_formatted_lines (lines).get('enphase state')
            if sunspec_state == 5 and enphase_state == 3
                return ('on')
            elif sunspec_state == 8 and enphase_state == 7:
                return ('max_min')
            else:
                return ('on, but not (5, 3)')

        else:
            return ('Inverter not active') 


def state_check():
    while True:
        # state_check_data = []
        # get timestamp and write into csv
        ts = time.time()
                    
        # 4a - 4c
        batterySOC = get_cli('state-get', 'BatterySOC')
        curr_ac = get_cli('eac-grid-data', 'current_rms_Q10_in_A')
        curr_dc = get_cli('bq-check', 'Current mA')       

        # log data into csv
        with open('log.csv', 'a') as log:
            log.writerow([ts, soc, curr_dc, curr_ac])

        # check inverted turned off or not
        inv_status = check_inv()
        if inv_status == 'on' or 'on, but not (5, 3)':
            print(inv_status)
            return True
        else:
            break

        time.sleep(60)        

def get_soc():
    result = interface.serial.send_cmd("state-get")
    soc = util.parse_formatted_lines(result).get('BatterySOC')
    return soc 


def charging():
    state_check()
    # check if SOC is 100%, then drop off grid and turn on load back
    if get_soc() == 100:
        switcher.toggle(0, 1)
        switcher.toggle ('') # turn load back on

def discharging():    
    if get_soc() < 11:
        stitcher.toggle(0, 0)
        state_check()

def main():
    while True:
        init()
        charging()
        discharging()

if __name__ == '__main__':
    main()