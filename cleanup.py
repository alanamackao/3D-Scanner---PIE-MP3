"""
PIE Mini Project 2: 3D Scanner - 9/30/2024
Written by Alana MacKay-Kao and Andrea Chhour

description
"""
# importing used libraries
import serial
import time
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
# plt.style.use('seaborn-poster')

# initialize
servoRange = 60                # number of degrees servos will rotate over -- full scan: 180
graphDimensions = 20             # number of points on each axis graph will have
degreeChange = int(servoRange/graphDimensions)
    # graphDimensions = 180/degreeChange # maybe necessary???
lastZpos = 75 - degreeChange     # initial tiltServo position -- full scan starts at 0
lastXpos = 65 - degreeChange     # initial panServo position -- full scan starts at 0

blankArray = [] # np.empty(graphDimensions**2)

phiArray = blankArray       # will store the angles the tilt servo is at
thetaArray = blankArray     # will store the angles the pan servo is at
rhoArray = blankArray       # will store the distance from the IR sensor in cm

xArray = blankArray
yArray = blankArray
zArray = blankArray

phi = 0
theta = 0
rho = 0


# open serial communication
serialcomm = serial.Serial('COM5', 115200, timeout = 1)



def scan_column(xPos):
    """
    description

    Args: 
        xPos: current angle that the panServo is at
    Returns:

    """
    global lastZpos, phi, theta, rho, phiArray, thetaArray, rhoArray

    for row in range(graphDimensions):        
        zPos = lastZpos + degreeChange
        lastZpos = zPos
        print(f"zPos: {zPos}, xPos: {xPos}") # can be taken out later
        serialcomm.write((f"{zPos},{xPos}").encode())
        
        dataFromArduino = serialcomm.readline().strip().decode()
            # returns as a string!!
        dataList = dataFromArduino.split(",")
            # splits the data received from the arduino on the comma

        while dataList[0] == '':
            time.sleep(0.002)
                # waits 2 milliseconds to let arduino populate computer's serial buffer
            dataFromArduino = serialcomm.readline().strip().decode()
                # checks serial buffer again
            dataList = dataFromArduino.split(",")
                # splits the data received from the arduino on the comma
        
        
        print(f"datalist: {dataList}")

        zPos = int(dataList[0])
        xPos = int(dataList[1])
        IRvoltage = float(dataList[2])
       
        phi = (((zPos-90)*np.pi)/180)
            # changes angle range from 0-180 to -90 - 90, then converts that angle to radians
        theta = (((xPos-90)*np.pi)/180)
        rho = 13850*(IRvoltage**(-1.03)) 
            # from sensor calibration, rho is in cm
        print(f"phi: {phi}\ntheta:{theta}\nrho: {rho}")

        phiArray = np.append(phiArray, phi)
        thetaArray = np.append(thetaArray, theta)
        rhoArray = np.append(rhoArray, rho)

        print("arduino: " + dataFromArduino) 

        print("--------------------------")

def scan_columns_and_rows():
    global lastXpos, lastZpos
    
    for row in range(graphDimensions):
        xPos = lastXpos + degreeChange
        lastXpos = xPos
        scan_column(xPos)
        lastZpos = lastZpos - ((graphDimensions)*degreeChange)
    
    print(f"**** scanned row *****")
    

def convert_to_cartesian(phiArray, thetaArray, rhoArray):
    global xArray, yArray, zArray

    print(f"phiArray\n{phiArray}\nthetaArray\n{thetaArray}\nrhoArray\n{rhoArray}")
    
    for i in range(graphDimensions):
        phi = phiArray[i]
        # if phi == 0:
        #     phi = 2*np.pi
        theta = thetaArray[i]
        # if theta == 0:
        #     theta = 2*np.pi
        rho = rhoArray[i]

        print(f"phi: {phi}, theta: {theta}, rho: {rho}")
        print(f"cos theta: {np.cos(theta)}, sin theta: {np.sin(theta)}")


        y = rho*np.sin(phi)*np.cos(theta)
        # switching x and y, not sure why they're backwards?
        x = rho*np.sin(phi)*np.sin(theta)
        z = rho*np.cos(phi)

        xArray = np.append(xArray, x)
        yArray = np.append(yArray, y)
        zArray = np.append(zArray, z)

    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")

    cartesianArrayList = [xArray, yArray, zArray]
    return cartesianArrayList

def graph_test():
    cartesianArrayList = convert_to_cartesian(phiArray, thetaArray, rhoArray)
    xArray = cartesianArrayList[0]
    yArray = cartesianArrayList[1]
    zArray = cartesianArrayList[2]

    print("-------")
    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")
    
    # plt.plot(xArray,yArray)
    # plt.show()

    # fig = plt.figure(figsize = (graphDimensions, graphDimensions))
    
    
    ax = plt.axes(projection='3d')
    ax.grid()
    
    ax.scatter3D(xArray, yArray, zArray)
    ax.set_title('Test :D')

    # Set axes label
    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('z', labelpad=20)

    plt.show()

def graph_column():
    cartesianArrayList = convert_to_cartesian(phiArray, thetaArray, rhoArray)
    xArray = cartesianArrayList[0]
    yArray = cartesianArrayList[1]
    zArray = cartesianArrayList[2]

    print("-------")
    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")
    
    plt.plot(zArray,yArray)
    plt.show()


def main():
    # call functions here
    print("hello world")

    # scan_row(0)
    # scan_column(90)
    scan_columns_and_rows()
    graph_test()
    # graph_column()

    serialcomm.close()  # closes serial port

if __name__ == '__main__':
    """
    explanation of how this works/why we use it
    """
    main()