"""
PIE Mini Project 2: 3D Scanner - 9/30/2024
Written by Alana MacKay-Kao and Andrea Chhour

Sends instructions to Arduino to move 2 servos mounted so that they tilt
or pan an infrared sensor. Takes readings from that sensor from Arduino
and the angles of the servos and converts polar coordinates to cartesian
coordinates to graph the points observed by the IR sensor.
"""

# import used libraries
import serial
import time
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


# initialize variables
servoRange = 45             # number of degrees servos will rotate over -- full range: 180
graphDimensions = 30        # number of points on each axis graph will have
degreeChange = int(servoRange/graphDimensions) # number of degrees to iterate by each time servos move

lastZpos = 75 - degreeChange     # initial tiltServo position -- full range starts at 0
lastXpos = 65 - degreeChange     # initial panServo position -- full range starts at 0

phi = 0                     # the angle between the z axis and the xy-plane
theta = 0                   # the angle between the x axis and the projection of rho onto the xy-plane
rho = 0                     # the distance between the IR sensor and the point it has scanned 
                                # magnitude of the position vector if IR sensor is origin of coord system

blankArray = [] # np.empty(graphDimensions**2) 

phiArray = blankArray       # will store the angles the tilt servo is at
thetaArray = blankArray     # will store the angles the pan servo is at
rhoArray = blankArray       # will store the distance from the IR sensor in cm

xArray = blankArray         # these 3 arrays will be used to graph the scan in cartesian coordinates
yArray = blankArray             
zArray = blankArray

# open serial communication
serialcomm = serial.Serial('COM5', 115200, timeout = 1)


def scan_column(xPos):
    """
    Loops over the number of rows given by the assigned graphDimensions
    to change the angle of the tiltServo by degreeChange degrees, 
    fetch a list of (tiltServo position, panServo position, IR sensor
    voltage) and separate them. Then converts those values to phi, theta,
    and rho spherical coordinates for use in plotting cartesian 
    coordinates later.

    Args: 
        xPos: current angle that the panServo is at
    Returns: None
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
            # changes angle range from 0-180 to -90 - +90, then converts that angle to radians
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
    """
    Loops over the number of columns given by the assigned graphDimensions
    to change the angle of the panServo by degreeChange degrees, 
    then scans the column at that panServo position.

    Args: None
    Returns: None
    """
    global lastXpos, lastZpos
    
    for column in range(graphDimensions):
        xPos = lastXpos + degreeChange
        lastXpos = xPos
        scan_column(xPos)
        lastZpos = lastZpos - ((graphDimensions)*degreeChange)
    
    print(f"**** scanned row *****")
    

def convert_to_cartesian(phiArray, thetaArray, rhoArray):
    """
    Loops over the number of points that will be graphed. Takes the
    phi, theta, and rho values for each point the IR sensor scanned and
    uses them to calculate cartesian coordinates for each point. 

    Args: 
        phiArray, thetaArray, rhoArray:
            Arrays storing the phi, theta, and rho values for each point
            the IR sensor returned a value for
    Returns:
        cartesianArrayList
            A list of 3 arrays storing x, y, and z values respectively
            for each point
    """
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
        if y <= 40:
            yArray = np.append(yArray, y)
        else:
            yArray = np.append(yArray, 100)
        zArray = np.append(zArray, z)

    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")

    cartesianArrayList = [xArray, yArray, zArray]
    return cartesianArrayList

def graph_3D():
    """
    Graphs the points scanned by the IR sensor in cartesian 
    coordinates as a 3D scatterplot.

    Args: None
    Returns: None
    """
    cartesianArrayList = convert_to_cartesian(phiArray, thetaArray, rhoArray)
    xArray = cartesianArrayList[0]
    yArray = cartesianArrayList[1]
    zArray = cartesianArrayList[2]

    print("-------")
    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")    
    
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
    """
    Graphs y and z points in a 2D line plot.
    """
    cartesianArrayList = convert_to_cartesian(phiArray, thetaArray, rhoArray)
    xArray = cartesianArrayList[0]
    yArray = cartesianArrayList[1]
    zArray = cartesianArrayList[2]

    print("-------")
    print(f"xArray\n{xArray}\nyArray\n{yArray}\nzArray\n{zArray}")
    
    plt.plot(yArray,zArray)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.show()

def main():
    """
    Calls functions to complete one full scan and closes the serial port.

    Args: None
    Returns: None
    """
    # call functions here
    # print("hello world")

    # scan_row(90)
    scan_column(90)
    # scan_columns_and_rows()
    # graph_3D()
    graph_column()

    serialcomm.close()  # closes serial port

if __name__ == '__main__':
    main()