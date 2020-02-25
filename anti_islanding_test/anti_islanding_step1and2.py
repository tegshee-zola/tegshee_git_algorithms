import time

#OGE Libs 
# import interface
# import util as util
import helper as helper


def main():
    user_input = ''
    interface = helper.quick_init('COM3')
    interface.serial.send_cmd("prov-set 3")
    test_running = True
    while(test_running):
        # user_input == input("type 'stop' to exit the test. ")
        if user_input == "stop":
            test_running = False
            break
        else:
            interface.serial.send_cmd("eac-grid-ctrl 1")    
            print('waiting for syncing with grid')
            time.sleep(10)
            print("grid sync finished")
            interface.serial.send_cmd("eac-grid-data")
            # print("type 'stop' to exit the test.")
            time.sleep(10)
            # user_input == input("type 'stop' to exit the test. ")
    print('exited the test')

if __name__ == '__main__':
    main()