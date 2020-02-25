import time
import socket

#OGE Libs 
import helper as helper
import util as util


user_input = '' # Todo:improve user-interface
# set-up interface, with COM3
interface = helper.quick_init('COM3')
# power on
interface.serial.send_cmd("prov-set 3")
print('waiting for 60 seconds for prov-set 3')
time.sleep(60)
# condition for test run until user enters stop

#### Gridsim setup ####
# Create Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(10)
s.connect(("192.168.128.101",5025))

# Lock out the touch screen
s.send(str.encode("SYST:RWL\n"))

# Set voltage slew rate to 1 V/s
s.send(str.encode("SOURCE:VOLT:SLEW 1000\n"))

def grid_ctrl():
    interface.serial.send_cmd("eac-grid-ctrl 1")    
    print('waiting for syncing with grid')
    time.sleep(60)
    print('waited for 60 seconds')

def set_VF(sckt,voltage,frequency,safe_check = True):
    if (not safe_check) or (frequency<70 and frequency>40):
        sckt.send(str.encode("INST:SEL AC1 \n"))
        sckt.send(str.encode("SOURCE:VOLT "+ str(voltage) +"\n"))
        sckt.send(str.encode("SOURCE:FREQ "+ str(frequency) +"\n"))
    else:
        print("Safety check: You're trying to set frequency to a value outside of the set [40,70]. You have to change a flag in the code in order to do that.")

def grid_data():
    lines = interface.serial.send_cmd("eac-grid-data")
    #Check whether connection is closed
    data = util.parse_formatted_lines(lines)
    if(data.get('Grid contactor status') == 'Closed'):
        # print('it is closed')
        return [data, True]
    elif(data.get('Grid contactor status') == 'Opened'):
        # print('it is open')
        return [data, False]
    else:
        # print('syncronizing')
        return [data, 'synchronizing'] #TODO need to handle this case in main()

# print(grid_data())
# print(grid_data()[1])
# print(type(grid_data()[1]))

def main():
    i = 0
    while(i < 50):
        # 1. setting into eac-grid-ctrl 1
        grid_ctrl()

        # 1.1. Checking whether it is closed
        if (not grid_data()[1]):
            # print(data)
            print('not Closed when voltage is 230V')
            print(grid_data()[0])
            print("Exited at {}th loop".format(i))
            break
        
        # 2. Set voltage lower than 180V
        set_VF(s,20,50) 
        print('waiting for the grid change')
        time.sleep(10)
        
        # 3. Checking whether it is opened
        if (grid_data()[1]):
            # print(data)
            print('not Open when voltage is under 20V')
            print(grid_data()[0])
            print("Exited at {}th loop".format(i))
            break
        
        # 4. Set voltage back to 230V
        set_VF(s,230, 50) 
        time.sleep(1)
        print('changed grid back to 230V')
        i += 1
   
if __name__ == '__main__':
    main()

s.send(str.encode("SYST:LOC\n"))
s.close()