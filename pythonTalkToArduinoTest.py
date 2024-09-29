# Importing Libraries 
import serial 
import time 

# arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1) 

# def write_read(x): 
# 	arduino.write(bytes(x, 'utf-8')) 
# 	time.sleep(0.05) 
# 	data = arduino.readline() 
# 	return data 

# while True: 
#     num = input("Enter a number: ") # Taking input from user 
#     value = write_read(num) 
#     print(value) # printing the value

"""
Following code taken from Tabletop Robotics on YouTube: https://youtu.be/Lm_xfm1d5h0?si=q_clN18kiD-mJb9w
"""
import serial
import time

serialcomm = serial.Serial('COM5', 9600)
serialcomm.timeout = 1

while True:
    i = input("Enter Input: ").strip()
    
    if i == "Done":
        print('finished')
        break
    
    serialcomm.write(i.encode())
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

serialcomm.close()