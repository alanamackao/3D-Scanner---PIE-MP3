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
graphDimensions = 10             # number of points on each axis graph will have
degreeChange = int(servoRange/graphDimensions)
    # graphDimensions = 180/degreeChange # maybe necessary???
lastZpos = 85 - degreeChange     # initial tiltServo position -- full scan starts at 0
lastXpos = 85 - degreeChange     # initial panServo position -- full scan starts at 0

phiArray = np.empty(graphDimensions**2)       # will store the angles the tilt servo is at
thetaArray = np.empty(graphDimensions**2)     # will store the angles the pan servo is at
rhoArray = np.empty(graphDimensions**2)       # will store the distance from the IR sensor in cm
phi = 0
theta = 0
rho = 0

# change_rowFixer = 0     # variable to fix the strange looping error we ran into

# open serial communication
serialcomm = serial.Serial('COM5', 115200, timeout = 1)


# def convert_to_cartesian function


# def scan_row function
    # will call convert_to_cartesian

def scan_row(zPos):
    """
    description
    Args: 
        zPos: current angle that the tiltServo is at
    Returns:
    """
    global lastXpos

    for column in range(graphDimensions+1):        
        xPos = lastXpos + degreeChange
        lastXpos = xPos
        print(f"zPos: {zPos}, xPos: {xPos}") # can be taken out later
        serialcomm.write((f"{zPos},{xPos}").encode())

        # time.sleep(0.002) 
            # waits 2 milliseconds to let arduino populate computer's serial buffer
        
        dataFromArduino = serialcomm.readline().strip().decode()
            # returns as a string!!
        dataList = dataFromArduino.split(",")
            # splits the data received from the arduino on the comma between each number
        
        print(f"datalist: {dataList}")

        zPos = dataList[0]
        xPos = dataList[1]
        IRvoltage = float(dataList[2])

        rho = 13850*(IRvoltage**(-1.03))
        print(f"rho: {rho}")


        # phi = ((int(dataList[0])*np.pi)/180)
        # theta = ((int(dataList[1])*np.pi)/180)

        # np.append(phiArray, phi)
        # np.append(thetaArray, theta)

        np.append(rhoArray, rho)

        print("arduino: " + dataFromArduino) 
    None

def scan_column(xPos):
    """
    description
    Args: 
        zPos: current angle that the tiltServo is at
    Returns:
    """
    global lastZpos

    for column in range(graphDimensions+1):        
        zPos = lastZpos + degreeChange
        lastZpos = zPos
        print(f"zPos: {zPos}, xPos: {xPos}") # can be taken out later
        serialcomm.write((f"{zPos},{xPos}").encode())

        # time.sleep(0.002) 
            # waits 2 milliseconds to let arduino populate computer's serial buffer
        
        dataFromArduino = serialcomm.readline().strip().decode()
            # returns as a string!!
        dataList = dataFromArduino.split(",")
            # splits the data received from the arduino on the comma between each number
        
        print(f"datalist: {dataList}")

        while dataList[0] == '':
            time.sleep(0.002)
                # waits 2 milliseconds to let arduino populate computer's serial buffer
            dataFromArduino = serialcomm.readline().strip().decode()
                # checks serial buffer again
            dataList = dataFromArduino.split(",")
        
        # if len(dataList) > 0:
            # still occasionally fails, redundancy for above
        zPos = dataList[0]
        xPos = dataList[1]
        IRvoltage = float(dataList[2])

        rho = 13850*(IRvoltage**(-1.03))
        print(f"rho: {rho}")


        # phi = ((int(dataList[0])*np.pi)/180)
        # theta = ((int(dataList[1])*np.pi)/180)
        # rho = 13850*(int(dataList[2])**-1.03)

        # np.append(phiArray, phi)
        # np.append(thetaArray, theta)
        np.append(rhoArray, rho)

        print("arduino: " + dataFromArduino) 

        print("--------------------------")
    None

def graph_test():
    fig = plt.figure(figsize = (graphDimensions, graphDimensions))
    ax = plt.axes(projection='3d')
    ax.grid()
    
    ax.plot3D(thetaArray, rhoArray, 0)
    ax.set_title('Test :D')

    # Set axes label
    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('Z', labelpad=20)

    plt.show()
    

def scan():
    # zPos = lastZpos + degreeChange
    # xPos = lastXpos + degreeChange
    # print(f"{zPos},{xPos}")
    # serialcomm.write((f"{zPos},{xPos}").encode())
    global lastZpos
    global lastXpos

    for row in range(graphDimensions+1):
        zPos = lastZpos + degreeChange
        lastZpos = zPos
        
        for column in range(graphDimensions+1):
            xPos = lastXpos + degreeChange
            lastXpos = xPos
            print(f"{zPos},{xPos}")
            serialcomm.write((f"{zPos},{xPos}").encode())

            time.sleep(0.002) 
                # waits 2 milliseconds to let arduino populate computer's serial buffer
            
            dataFromArduino = serialcomm.readline().strip().decode()
                # returns as a string!!
            dataList = dataFromArduino.split(",")
            phi = ((int(dataList[0])*np.pi)/180)
            theta = ((int(dataList[1])*np.pi)/180)
            rho = 13850*(int(dataList[2])**-1.03)

            np.append(phiArray, phi)
            np.append(thetaArray, theta)
            np.append(rhoArray, rho)
            print("arduino: " + dataFromArduino) 
        
        lastXpos = lastXpos - ((graphDimensions+1)*degreeChange)

    print("phi array")
    print(phiArray)
    print("theta array")
    print(thetaArray)
    print("rho array")
    print(rhoArray)

    # time.sleep(0.1)
    # dataFromArduino = serialcomm.readline().strip().decode()
    # print(dataFromArduino)
    # print(type(dataFromArduino))
    None

def get_arrays_for_graph() -> None:
    global xArray
    xArray = np.empty(graphDimensions**2)
    global yArray
    yArray = np.empty(graphDimensions**2)
    global zArray
    zArray = np.empty(graphDimensions**2)
    
    for i in range(graphDimensions**2):
        x = rho*np.sin(phi)*np.cos(theta)
        np.append(xArray, x)
        y = rho*np.sin(phi)*np.sin(theta)
        np.append(yArray, y)
        z = rho*np.sin(phi)
        np.append(zArray, z)
    None

# def change_row function
def change_row() -> None: #diff variable input
    # can make an input for x or y and have this be change_servo instead
    """
    # rotates yServo up by one iteration of degreeChange degrees

    Arguments:
        None 
    Returns:
        None
    """
    # while True:
    #     i = input("test? ")

    #     if i == "y":

    # global change_rowFixer
    global lastZpos

    # if (change_rowFixer/2) == 0:
    #     change_rowFixer += 1
        
    # check to see if something is available in serial buffer -- can do it afterwards (check if thing is there)
    
    print(lastZpos)
    zPos = "y" + str(lastZpos + degreeChange) + "\n" # iterates position by degree change
                                                # converts to string for arduino to read
    # zPos += "\n"    # adds a newline character to end of string so arduino
                    # knows to stop reading it at this point
    print(zPos)
    serialcomm.write(zPos.encode('ascii'))  # encodes zPos string as bytes and sends it
    # lastZpos = (int(((serialcomm.readline())).rstrip()))  
        # should be the same as zPos, gets string from arduino, 
        # strips trailing carriage return and newline and makes it an int
    lastZpos = lastZpos + degreeChange
    print(lastZpos)
    print((serialcomm.readline().strip()))
    print("\n------")

    time.sleep(0.5)       # waits 0.5 sec

    # else:
    #     change_rowFixer += 1
    #     change_row()

        # if i == "n":
        #     break



    # while True:
    #     i = input("Enter Input: ").strip()
        
    #     if i == "Done":
    #         print('finished')
    #         break
        
    #     serialcomm.write(i.encode())
    #     time.sleep(0.5)
    #     print(serialcomm.readline().decode('ascii'))

    # serialcomm.close()


# def filter_arrays function

# def produce_graph function
def produce_graph():
    fig = plt.figure(figsize = (graphDimensions, graphDimensions))
    ax = plt.axes(projection='3d')
    ax.grid()

    global xArray
    global yArray
    global zArray
    
    ax.plot3D(xArray, yArray, zArray)
    ax.set_title('Test :D')

    # Set axes label
    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('Z', labelpad=20)

    plt.show()
    None


def main():
    # call functions here
    print("hello world")

    # scan_row(0)
    scan_column(0)
    graph_test()

    # scan()
    # get_arrays_for_graph()
    # produce_graph()


    serialcomm.close()  # closes serial port

if __name__ == '__main__':
    """
    explanation of how this works/why we use it
    """
    main()