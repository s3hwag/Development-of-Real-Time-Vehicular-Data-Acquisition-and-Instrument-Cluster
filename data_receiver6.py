import socket
import threading
import time
import struct

def receive_and_respond(UDPServerSocket):
    while not exit_event.is_set():
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            message = message.decode()
            clientMsg = "Message from client: {}".format(message)
            clientIP = "Client IP Address: {}".format(address)
            print(clientMsg)
            print(clientIP)
            
            if (message[:8] == '00000101'): #Reading the RPM header
                RPM_hex = message[-2:] # checking the LSB of RPM
                print('RPM:', int(RPM_hex,16)) #converting hex into integer
            if (message[:8] == '00000102'): #Reading the speed header
                Speed_hex = message[-2:] #Checking LSB of speed
                print('Speed', int(Speed_hex,16)) #Converting hex into integer
            if (message[:8] == '00000103'):#Reading the charge 
                Charge_hex = message[-2:]
                print('Charge', int(Charge_hex,16)) #reading the HVAC - Not completely done need to reverify again
            if (message[:8] == '00000104'):
                HVAC_hex = message[-2:] #Checking LSB of speed
                print('HVAC', int(HVAC_hex,16))
            if (message[:8] == '00000105'): # Reading the Door status
                Door_status = message[-2:]
                Door_status = int(Door_status,16)
                Door_status = bin(Door_status)[2:].zfill(8)
                print(Door_status, Door_status[0], Door_status[1])
                if (Door_status[0] == 1):
                    print('Front Right Door Open')
                else:
                    print('Front Right Door Close')
                if (Door_status[1] == 1):
                    print('Front Left Door Open')
                else:
                    print('Front Left Door Close')
                if (Door_status[2] == 1):
                    print('Rear Right Door Open')
                else:
                    print('Rear Right Door Close')
                if (Door_status[3] == 1):
                    print('Rear Left Door Open')
                else:
                    print('Rear Left Door Close')
                if (Door_status[4] == 1):
                    print('Trunk Open')
                else:
                    print('Trunk Close')
                if (Door_status[5] == 1):
                    print('Boot Open')
                else:
                    print('Boot Close')
            if (message[:8] == '00000106'): # Reading the Indicator status 
                Indicator_status = message[-2:]
                Indicator_status = int(Indicator_status,16)
                Indicator_status = bin(Indicator_status)[2:].zfill(8)
                print (Indicator_status, Indicator_status[0], Indicator_status[1], Indicator_status[7])
                if (Indicator_status[6] == '1'):
                    print('Right Indicator On')
                else:
                    print('Indicator Off') 
                if (Indicator_status[7] == '1'):
                    print('Left Indicator On')
                else:
                    print('Indicator Off')                     
            if not exit_event.is_set():
                UDPServerSocket.sendto(bytesToSend, address)
        except KeyboardInterrupt:
            print("Server terminated by user.")
        except Exception as e:
            print("Error:", e)

localIP = "0.0.0.0"
localPort = 5000
bufferSize = 1024
msgFromServer = "Hello VM Client\n"
bytesToSend = str.encode(msgFromServer)

# Create an event to signal the thread to exit
exit_event = threading.Event()

try:
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    receiver_thread = threading.Thread(target=receive_and_respond, args=(UDPServerSocket,))
    receiver_thread.start()

except KeyboardInterrupt:
    print("Server terminated by user.")
    exit_event.set()  # Signal the receiver thread to exit
    receiver_thread.join()  # Wait for the receiver thread to exit
    UDPServerSocket.close()

except Exception as e:
    print("Error:", e)