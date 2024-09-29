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
graphDimensions = 5             # number of points on each axis graph will have
degreeChange = int(servoRange/graphDimensions)
    # graphDimensions = 180/degreeChange # maybe necessary???
lastZpos = 85 - degreeChange     # initial tiltServo position -- full scan starts at 0
lastXpos = 60 - degreeChange     # initial panServo position -- full scan starts at 0

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
        # np.append(rhoArray, rho)

        print("arduino: " + dataFromArduino) 
    None

def scan_column(xPos):
    """
    description
    Args: 
        xPos: current angle that the panServo is at
    Returns:
    """
    global lastZpos, phi, theta, rho, phiArray, thetaArray, rhoArray

    for column in range(graphDimensions):        
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
        zPos = int(dataList[0])
        xPos = int(dataList[1])
        IRvoltage = float(dataList[2])
       
        phi = ((zPos*np.pi)/180)
        theta = ((xPos*np.pi)/180)
        rho = 13850*(IRvoltage**(-1.03)) # from sensor calibration, rho is in cm
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


        x = rho*np.sin(phi)*np.cos(theta)
        # switching y and z for now
        y = rho*np.sin(phi)*np.sin(theta)
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
    #scan_column(0)
    scan_columns_and_rows()
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