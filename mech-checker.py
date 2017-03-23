
#####################
##    Variables    ##
#####################

# All valid vehicle positions and times.
# A state is invalid if there is a vehicle collision, delay
# violation, or speed violation.
stateSpace = set()

# length of sides of square shaped space
spaceSize = 2

# speedlimit for vehicles in unit distance/unit time
topSpeed = 1.0

# total time a vehicle is allowed to delay
allowedDelay = 1.0

# maximum time needed for all vehicles to reach goal given allowable delay
maxTime = spaceSize/topSpeed + allowedDelay


# size of step into which time and space are divided
resolution = 0.1

# length of small, delayless vehicles
epsVehicleLength = resolution

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
    
    
####################
##      Main      ##
####################

currentTime = 0.0

numGridSteps = spaceSize / resolution
numTimeSteps = (spaceSize + allowedDelay) / resolution

# Loop through all possible states, i.e., all vehicle positions at all times

# if this state is valid, add it to the state space
# stateSpace.add( (vrtPos, horPos, currentTime) )

