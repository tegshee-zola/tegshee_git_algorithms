'''
This is a script that takes in a load schedule and activates the relays in the lab NI DAQ accordingly.
'''

import socket

#%% Gridsim setup
# Create Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(10)
s.connect(("192.168.128.101",5025))

# Lock out the touch screen
s.send(str.encode("SYST:RWL\n"))

# Set voltage slew rate to 1 V/s
s.send(str.encode("SOURCE:VOLT:SLEW 1000\n"))

#%% Switching and gridsim functions

def setVF(sckt,voltage,frequency,safe_check = True):
    if (not safe_check) or (frequency<70 and frequency>40):
        sckt.send(str.encode("INST:SEL AC1 \n"))
        sckt.send(str.encode("SOURCE:VOLT "+ str(voltage) +"\n"))
        sckt.send(str.encode("SOURCE:FREQ "+ str(frequency) +"\n"))
    else:
        print("Safety check: You're trying to set frequency to a value outside of the set [40,70]. You have to change a flag in the code in order to do that.")

setVF(s,130,50)

#%% Close out gridsim
s.send(str.encode("SYST:LOC\n"))
s.close()
