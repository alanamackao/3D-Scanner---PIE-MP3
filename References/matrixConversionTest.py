import numpy as np
import serial

# from other script
servoRange = 180                # number of degrees servos will rotate over
graphDimensions = 18            # number of points on each axis graph will have
degreeChange = int(servoRange/graphDimensions) 
# open serial communication
serialcomm = serial.Serial('COM5', 9600, timeout = 1)


xPoints = np.zeros(2)
# will have graphDimensions instead of 2
# will also have a matrix for yPoints and zPoints
print(xPoints)
print(xPoints[0])

yServoMessage = 45
# will be lastYpos or received from arduino
xServoMessage = 60
# will be lastXpos or received info from arduino


# convert angle to radians from degrees
phi = (yServoMessage*np.pi/180)
print(phi)
theta = (xServoMessage*np.pi/180)
print(theta)


sensorVoltage = 300
# will be calling the getDistanceFromSensor function
# which will work like this:
rho = 13850*(sensorVoltage**-1.03)
    # using power series to represent distance (cm) in terms of voltage
print("\n")
print(rho)
print("\n")


# have rho array
# have xServo angles array and yServo angles array (converted to radians when added to array)
# iterate through arrays (index them w same number) as part of graphing function
# add final x, y, and z values to new arrays

x = rho*np.sin(phi)*np.cos(theta)
print(x)
y = rho*np.sin(phi)*np.sin(theta)
print(y)
z = rho*np.sin(phi)
print(z)


xServoArray = np.zeros(graphDimensions)
