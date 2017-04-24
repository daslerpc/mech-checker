from helperMethods import *

############################
##   Program Parameters   ##
############################

# File in which the valid state space is saved
# This is just the prefix.  The final file name will specify which parameters
# were used to create it.
stateSpaceFilePrefix = "validStateSpaces"

# File in which the reachable state space is saved
# This is just the prefix.  The final file name will specify which parameters
# were used to create it.
prunedSpaceFilePrefix = "prunedStateSpaces"

# File in which the unreachable state space is saved
# This is just the prefix.  The final file name will specify which parameters
# were used to create it.
rejectedStatesFilePrefix = "rejectedStates"

# File extension for saved data
fileExtension = ".dat"

goalPos = 2.0
timeStep = 1.0/16.0
endTime = 3.0
topSpeed = 1.0

#############################
##    Program Variables    ##
#############################

stateSpace = []

#####################
##     Methods     ##
#####################

# Remove unreachable states
def pruneStateSpace(stateSpace) :
    print("Pruning state space")

    # Holds two state spaces, those states which are reachable and those which are not
    reachableUnreachableStateSpaces = []
    reachableUnreachableStateSpaces.append( [] )
    reachableUnreachableStateSpaces.append( [] )

    # How big is our starting state space?
    startingSize = 0
    for timeIndex in range(0, len(stateSpace)):
        startingSize = startingSize + len( stateSpace[timeIndex] )

    # Initialize temporary state space
    for timeIndex in range(0, len(stateSpace)) :
        reachableUnreachableStateSpaces[0].append( set() )
        reachableUnreachableStateSpaces[1].append( set() )

    reachableUnreachableStateSpaces[0][0] = stateSpace[0]

    # Remove unreachable states
    spaceSize = len(stateSpace)
    for timeIndex in range(1, 20):#spaceSize):
        print( str(round(100*timeIndex/spaceSize,2)) + "% complete." )
        for stateString in stateSpace[timeIndex]:
            state = stringToState( stateString )
            reachable = False

            for prevStateString in reachableUnreachableStateSpaces[0][timeIndex - 1]:
                prevState = stringToState( prevStateString )

                if areAdjacentStates(prevState, state, timeStep, topSpeed):
                    reachableUnreachableStateSpaces[0][timeIndex].add( stateString )
                    reachable = True
                    break

            if not reachable :
                reachableUnreachableStateSpaces[1][timeIndex].add( stateString )
    
    # How big is our ending state space?
    endingSize = 0
    for timeIndex in range(0, len(reachableUnreachableStateSpaces[0])):
        endingSize = endingSize + len( reachableUnreachableStateSpaces[0][timeIndex] )

    pruned = startingSize - endingSize

    print("Pruning complete")
    print("\tBegan with " + str(startingSize) + " states.")
    print("\tEnded with " + str(endingSize) + " states.")
    print("\tPruned " + str(pruned) + " states.")
    print("\tA reduction of " + str(round(100*float(pruned)/startingSize ,2)) + "%.")

    return reachableUnreachableStateSpaces

####################
##      Main      ##
####################

fileName = generateFileName( stateSpaceFilePrefix, goalPos, timeStep, endTime, topSpeed, fileExtension )
stateSpace = loadStateSpace( fileName )

stateSpace = pruneStateSpace( stateSpace )

fileName = generateFileName( prunedSpaceFilePrefix, goalPos, timeStep, endTime, topSpeed, fileExtension )
writeStateSpaceToFile( stateSpace[0], fileName )

fileName = generateFileName( rejectedStatesFilePrefix, goalPos, timeStep, endTime, topSpeed, fileExtension )
writeStateSpaceToFile( stateSpace[1], fileName )
