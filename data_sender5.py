import socket
import threading
import time
import struct
import sys

def listen_for_input(client_socket, lock):
    global user_input
    while not exit_event.is_set():
        try:
            print('Parameter list \n1.RPM \n2.Speed \n3.Door \n4.Indicator \n5.Charge \n6.HVAC')
            parameter = input('Please select the parameter that need to be updated :')
            # RPM
            if (parameter == 'RPM'):
                rpm = int(input("Enter RPM: "))
                if rpm > 12:
                    rpm = 12
                    rpm_bin = rpm
                elif rpm < 0:
                    rpm = 0
                    rpm_bin = rpm
                else:
                    rpm_bin = rpm
                message = (header_RPM)[2:].zfill(8)+hex(rpm_bin)[2:].zfill(8)
                print("\nFINAL 4 BYTES:", rpm)
            # Speed
            if (parameter == 'Speed'):
                speed = int(input("Enter Speed: "))
                if speed > 255:
                    speed = 255
                    speed_bin = speed
                elif speed < 0:
                    speed = 0
                    speed_bin = speed
                else:
                    speed_bin = speed
                message = (header_Speed)[2:].zfill(8)+hex(speed_bin)[2:].zfill(8)
                print("\nFINAL 4 BYTES:", message)
            # Charge
            if (parameter == 'charge'):
                charge = int(input("Enter charge percentage: "))
                if charge > 100:
                    charge = 100
                    charge_bin = charge
                elif charge < 0:
                    charge = 0
                    charge_bin = charge
                else:
                    charge_bin = charge
                message = (header_Charge)[2:].zfill(8)+hex(charge_bin)[2:].zfill(8)
                print("\nFINAL 4 BYTES:", message)
            # HVAC
            if (parameter == 'HVAC'):
                temp = int(input("Enter the temperature: "))
                if temp > 24:
                    temp = 24
                elif temp <16:
                    temp = 16
                else:
                    temp = temp
                message = (header_HVAC)[2:].zfill(8)+hex(temp)[2:].zfill(8)
                print("\nFINAL 4 BYTES:", message)
            # Door Status
            if (parameter == 'Door'):
                print("Enter door statuses 0 to close and 1 to open\n")
                FR = int(input("Front Right: "))
                FL = int(input("Front Left: "))
                RR = int(input("Rear Right: "))
                RL = int(input("Rear Left: "))
                TR = int(input("Trunk : "))
                BT = int(input("Boot : "))
                if FR == 1:
                    FR = '1'
                else:
                    FR = '0'
                if FL == 1:
                    FL = '1'
                else:
                    FL = '0'
                if RR == 1:
                    RR = '1'
                else:
                    RR = '0'
                if RL == 1:
                    RL = '1'
                else:
                    RL = '0'
                if TR == 1:
                    TR = '1'
                else:
                    TR = '0'
                if BT == 1:
                    BT = '1'
                else:
                    BT = '0'
                
                door_bin = BT+TR+RL+RR+FL+FR
                door_bin = int(door_bin,2)
                message = str(hex(door_bin))[2:]
                pad_zero_door = '0' * (8 - len(message))
                message = pad_zero_door+str(message)
                message = (header_Door)[2:].zfill(8)+(message).zfill(8)
                print("\nFINAL 4 BYTES:", message)
            # Indicators
            if (parameter == 'Indicator'):
                print("Indicator Status")
                right_indicator = int(input("Right Indicator(0/1): "))
                left_indicator = int(input("Left Indicator(0/1): "))
                if right_indicator == 0:
                    right_indicator = '0'
                else:
                    right_indicator = '1'
                    
                if left_indicator == 0:
                    left_indicator = '0'
                else:
                    left_indicator = '1'
                    
                indicators_bin = right_indicator + left_indicator
                indicators_bin = int(indicators_bin,2)
                message = str(hex(indicators_bin))[2:]
                pad_zero_door = '0' * (8 - len(message))
                message = pad_zero_door+str(message)
                message = (header_Indicator)[2:].zfill(8)+(message).zfill(8)
                print("\nFINAL 4 BYTES:", message)

            client_socket.send(message.encode())

        except KeyboardInterrupt:
            print("Client terminated by user.")
            exit_event.set()  # Signal the threads to exit

# Create an event to signal the threads to exit
exit_event = threading.Event()

# Create a lock to synchronize access to user_input
user_input_lock = threading.Lock()

user_input = ""
header_RPM = hex(int(257))
header_Speed = hex(int(258))
header_Charge = hex(int(259))
header_HVAC = hex(int(260))
header_Door = hex(int(261))
header_Indicator = hex(int(262))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 5000)  # the controller container's hostname and port

try:
    client_socket.connect(server_address)

    # Start the input listener thread
    input_thread = threading.Thread(target=listen_for_input, args=(client_socket, user_input_lock))
    input_thread.start()

    #sender_thread.join()
    input_thread.join()

except ConnectionRefusedError:
    print("Connection refused. Retrying...")

finally:
    client_socket.close()
