import random
import math

############################
##    Program Settings    ##
############################

# Turns on/off debugging text output
debugging = False

# File in which the valid state space is saved
# This is just the prefix.  The final file name will specify which parameters
# were used to create it.
stateSpaceFilePrefix = "validStateSpaces"

# File for testing, same as above, but with many fewer states
testDataFilePrefix = "stateSpaceTestData"

# File extension for saved data
fileExtension = ".dat"

#############################
##    Program Variables    ##
#############################

# All valid vehicle positions and times.
# A state is invalid if there is a vehicle collision, delay
# violation, or speed violation.
# Also, unreachable states will be pruned
stateSpace = []

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
# plus 1 added to account for position 0.0
numGridSpaces = math.ceil(spaceSize / resolution) + 1

# given the max time to reach the goal and the resolution, how many time steps
# are needed to complete the run
# plus 1 added to account for time 0.0
numTimeSteps = math.ceil(maxTime / resolution) + 1

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
# This is just a debugging tool
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

# Construct the state space of valid configurations
# To save them to a file, call writeStateSpace()
def buildStateSpace():
    print("Building state space")
    # Initialize state space
    for time in range(0, numTimeSteps) :
        stateSpace.append( [] )
    
    # Loop through all possible states, i.e., all vehicle positions at all times
    for v0 in range(0, numGridSpaces):
        print ( str(round(100*float(v0)/numGridSpaces,2)) + "% complete" )
        for v1 in range(0, numGridSpaces):
            vPos = (v0*resolution, v1*resolution)
            for h0 in range(0, numGridSpaces):
                for h1 in range(0, numGridSpaces):
                    hPos = (h0*resolution, h1*resolution)
                    for t in range(0, numTimeSteps):
                        time = t*resolution
                        if stateIsValid( vPos, hPos, time ) :
                            # Add state (v0, v1, h0, h1, t)
                            stateSpace[t].append( (vPos[0], vPos[1], hPos[0], hPos[1], time) )
    print("100% complete\nBuild complete\n")


# Creates a filename containing run parameters
def generateFileName( name ) :
    # Goal Position
    name = name + "_G" + str(spaceSize)

    # Resolution
    name = name + "_R" + str(resolution)

    # End Time
    name = name + "_E" + str(maxTime)

    # Top Speed
    name = name + "_S" + str(topSpeed)

    # Add extension
    name = name + fileExtension
    
    return name

# Generate a smaller state space for testing purposes
# This method writes to a file on its own and does not
# require the writeStateSpace() method to be called
def generateTestData( ) :
    fileName = generateFileName( testDataFilePrefix )
    outputFile = open(fileName, 'w')
    for step in range(0, 33):
        t = step*resolution
        state = ""
        for x in range(0, 5):
            state = state + str(t)
            if x !=4:
                state = state +","
            else:
                state = state +"\n"
                
        outputFile.write(state)
        
    outputFile.close()

def writeStateSpace() :
    stateSpaceFileName = generateFileName( stateSpaceFilePrefix )
    print("Writing state space to file " + stateSpaceFileName)
    stateSpaceFile = open(stateSpaceFileName, 'w')

    for statesAtTime in stateSpace:
        for state in statesAtTime:
            stateSpaceFile.write(str(state[0]) + "," + str(state[1]) + "," + str(state[2]) + "," + str(state[3]) + "," + str(state[4]) + "\n")
    
    stateSpaceFile.close()
    print("Writing complete\n")

# Remove unreachable states
def pruneStateSpace() :
    print("Pruning state space")
    
    global stateSpace
    startingSize = 0
    endingSize = 0

    tempStateSpace = []

    # How big is our starting state space?
    for timeIndex in range(0, len(stateSpace)):
        startingSize = startingSize + len( stateSpace[timeIndex] )

    # Initialize temporary state space
    for timeIndex in range(0, numTimeSteps) :
        tempStateSpace.append( [] )

    tempStateSpace[0] = stateSpace[0]

    # Remove unreachable states
    spaceSize = len(stateSpace)
    for timeIndex in range(1, spaceSize):
        print( str(round(100*float(timeIndex)/spaceSize,2)) + "% complete." )
        
        for state in stateSpace[timeIndex]:
            for prevState in tempStateSpace[timeIndex - 1]:
                if areAdjacentStates(prevState, state):
                    tempStateSpace[timeIndex].append( state )
                    break
    
    # Transfer results
    stateSpace = tempStateSpace

    # How big is our ending state space?
    for timeIndex in range(0, len(stateSpace)):
        endingSize = endingSize + len( stateSpace[timeIndex] )

    pruned = startingSize - endingSize

    print("Pruning complete")
    print("\tBegan with " + str(startingSize) + " states.")
    print("\tEnded with " + str(endingSize) + " states.")
    print("\tPruned " + str(pruned) + " states.")
    print("\tA reduction of " + str(round(100*float(pruned)/startingSize ,2)) + "%.")


# Are the two states adjacent in time (i.e., only one time step apart) and
# are the vehicle positoins in the second state reachable from the positions
# in the first in only one time step?

def areAdjacentStates( firstState, nextState ) :
    adjacent = (firstState[4] + resolution == nextState[4])
    
    for index in range(0, 4) :
        if not (firstState[index] == nextState[index] or firstState[index] + (resolution*topSpeed) == nextState[index]):
            adjacent = False            

    return adjacent

####################
##      Main      ##
####################

# Build the state space of valid states and save it to stateSpaceFileName
buildStateSpace()
pruneStateSpace()
writeStateSpace()






