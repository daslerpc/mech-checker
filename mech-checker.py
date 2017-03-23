import random
import math

############################
##    Program Settings    ##
############################

# Turns on/off debugging text output
debugging = False

# File in which the valid state space is saved
stateSpaceFileName = "validStateSpaces.dat"

#############################
##    Program Variables    ##
#############################

# All valid vehicle positions and times.
# A state is invalid if there is a vehicle collision, delay
# violation, or speed violation.
stateSpace = set()

# length of sides of square shaped space
spaceSize = 2.0

# speedlimit for vehicles in unit distance/unit time
topSpeed = 1.0

# total time a vehicle is allowed to delay
allowedDelay = 1.0

# maximum time needed for all vehicles to reach goal given allowable delay
maxTime = spaceSize/topSpeed + allowedDelay

# size of step into which time and space are divided
# currently using a resolution that is a power of 2 so that
# there is no internal approximation and precision is maintained
resolution = 1.0/16.0

# given the resolution and space size, how many grid cells across is the space
numGridSpaces = math.ceil(spaceSize / resolution)

# given the max time to reach the goal and the resolution, how many time steps
# are needed to complete the run
numTimeSteps = math.ceil(maxTime / resolution)

# length of small, delayless vehicles
epsVehicleLength = 2*resolution

# length of vertical and horizontal vehicles
vehicleLength = 1 - epsVehicleLength

# vehicles move in one dimension, so positions are simply distance traveled from start
#
# Vehicles start in the positions below with (0, 0) being where the two vehicles in the
# upper left meet. Movements to the right and downward are positive.
#
#      _| |
#      _

# starting positions of main vehicles
vrtVehPositions = [0.0, 0.0]
horVehPositions = [0.0, 0.0]

# starting positions of epsilon vehicles
vrtEpsPositions = [-1.5 + epsVehicleLength,     -0.5 + epsVehicleLength]
horEpsPositions = [-1.5,                        -0.5]

#####################
##     Methods     ##
#####################

# Given the position of a vehicle and which lane number we're checking (0 or 1)
# is there an intersection between that vehicle and lane?
# Lanes are numbered based on their position on the orthogonal axis
# A lane of 0.5 indicates an epsilon vehicle lane
def vehIntersectsLane ( vehiclePosition, vehLength, lane ):
    return vehiclePosition > lane and vehiclePosition < lane + vehLength

# checks the validity of a vehicle's position at a given time
# validity is false if speed limit broken or more time than the allowed delay has been taken
def vehPosValid ( vehPos, time ) :
    return (vehPos <= time * topSpeed) and (vehPos >= time * topSpeed - allowedDelay)

# get the position of epsilon vehicles at a particular time, given their starting positions
# eps vehicles travel at the speed limit and are allowed no delay
def epsPosition (startingPos, time) :
    displacement = + time * topSpeed
    eps0 = startingPos[0] + displacement
    eps1 = startingPos[1] + displacement
    return [eps0, eps1]

# Given two arrays of vehicle positions, are any of the vehicles intersecting
# There is an implicit assumption that no two vehicles from the same
# array will intersect, e.g., vertical vehicles will never collide with each other
def vehiclesIntersecting ( vrtVehs, horVehs ):

    # walk through all vertical vehicles
    for vrtVehIndex in range(0, len(vrtVehs)):
        vrtVehPos = vrtVehs[vrtVehIndex]

        # walk through all horizontal vehicles
        for horVehIndex in range(0, len(horVehs)):
            horVehPos = horVehs[horVehIndex]

            # check for collision
            if vehIntersectsLane ( horVehPos, vehicleLength, vrtVehIndex ):
                if vehIntersectsLane ( vrtVehPos, vehicleLength, horVehIndex ):
                    return True            

    return False

# Given one set of main vehicles and the corresponding set of epsilon vehicle (e.g., horizontal main vehicles
# and vertical epsilon vehicles) do they intersect at their current positions
def epsCollision( vehs, eps ) :

    # walk through all of the vehicles
    for vehIndex in range(0, len(vehs)):
        vehPos = vehs[vehIndex]

        # walk through all of the epsilon vehicles
        for epsIndex in range(0, len(eps)):
            epsPos = eps[epsIndex]

            # check for collision
            if vehIntersectsLane ( epsPos, epsVehicleLength, vehIndex ):
                if vehIntersectsLane( vehPos, vehicleLength, 0.5 ):
                    return True            

    return False
    
# Bringing it all together and checking to see if a full state is valid
def stateIsValid( vrtVehs, horVehs, time ):
    valid = True
    vrtEpsPos = epsPosition( vrtEpsPositions, time )
    horEpsPos = epsPosition( horEpsPositions, time )

    if vehiclesIntersecting(vrtVehs, horVehs):
        debugPrint("Invalid: Horizontal/Vertical Vehicle Collision!")
        valid = False
    if epsCollision( horVehs, vrtEpsPos ) :        
        debugPrint("Invalid: Horizontal/EPS Vehicle Collision!")
        valid = False
    if epsCollision( vrtVehs, horEpsPos ) :
        debugPrint("Invalid: Vertical/EPS Vehicle Collision!")
        valid = False

    # walk through all vertical vehicles
    for vrtVehIndex in range(0, len(vrtVehs)):
        if not vehPosValid( vrtVehs[vrtVehIndex], time ):
            debugPrint("Invalid: Illegal Vertical Vehicle Position: " + str(vrtVehs[vrtVehIndex]) + " at Time: " + str(time))
            valid = False

    # walk through all horizontal vehicles
    for horVehIndex in range(0, len(horVehs)):
        if not vehPosValid( horVehs[horVehIndex], time ):
            debugPrint("Invalid: Illegal Horizontal Vehicle Position: " + str(horVehs[horVehIndex]) + " at Time: " + str(time))
            valid = False

    return valid

# Function to show or hide debug text in program output
def debugPrint( text ) :
    if debugging :
        print(text)

# Validation testing method
# Creates several random states and checks their validity
def testValidators() :
    currentTime = 0.0

    for cnt in range(0, 100):
        verts = [random.randrange(0, numGridSpaces) * resolution, random.randrange(0, numGridSpaces) * resolution]
        horzs = [random.randrange(0, numGridSpaces) * resolution, random.randrange(0, numGridSpaces) * resolution]
        time = random.randrange(0, numTimeSteps) * resolution

        state = (verts, horzs, time)
        if stateIsValid( state[0], state[1], state[2] ) :
            print(str(state) + " : State is valid!\n")
        else:
            print(str(state) + " : Bad state!\n")

# Construct the state space of valid configurations and save them to a file
def buildStateSpace():
    stateSpaceFile = open(stateSpaceFileName, 'w')

    # Loop through all possible states, i.e., all vehicle positions at all times
    for v0 in range(0, numGridSpaces):
        print (v0)
        for v1 in range(0, numGridSpaces):
            vPos = (v0*resolution, v1*resolution)
            for h0 in range(0, numGridSpaces):
                for h1 in range(0, numGridSpaces):
                    hPos = (h0*resolution, h1*resolution)
                    for t in range(0, numTimeSteps):
                        time = t*resolution
                        if stateIsValid( vPos, hPos, time ) :
                            # write state (v0, v1, h0, h1, t)
                            stateSpaceFile.write(str(vPos[0]) + "," + str(vPos[1]) + "," + str(hPos[0]) + "," + str(hPos[1]) + "," + str(time) + "\n")

    stateSpaceFile.close()
    
####################
##      Main      ##
####################

buildStateSpace()




