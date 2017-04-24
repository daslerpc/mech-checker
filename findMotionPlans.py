from helperMethods import *

############################
##   Program Parameters   ##
############################

fileExtension = ".dat"

prunedSpaceFilePrefix = "prunedStateSpaces"
testDataFilePrefix= "stateSpaceTestData"
motionPlansFilePrefix = "motionPlans"

goalPos = 2.0
timeStep = 1.0/16.0
endTime = 3.0
topSpeed = 1.0

#############################
##    Program Variables    ##
#############################

stateSpace = []
solutionsFound = 0

#####################
##     Methods     ##
#####################


def writePlanToFile( plan, outFile ) :
    for state in plan:
        outFile.write( stateToString( state ) + "\n" )
        
    outFile.write( "\n" )
        
## The methods below search the tree of vehicle decisions (i.e., does a vehicle move or stay put) at each time step
def findMotionPlansInActionSpace( ) :
    print( "Finding motion plans in action space" )
    planStart = [(0.0, 0.0, 0.0, 0.0, 0.0)]

    motionPlansFile = open( generateFileName(motionPlansFilePrefix), 'w' )
    findMotionPlansInActionSpaceRecurse( planStart, motionPlansFile )
    motionPlansFile.close()

def findMotionPlansInActionSpaceRecurse( plan, outFile ):
    planSize = len(plan)
    lastState = plan[ planSize-1 ]
    index = int(lastState[4]/timeStep)

    if stateToString(lastState) in stateSpace[index]:
        if isFinalState ( lastState, goalPos ):
            writePlanToFile( plan, outFile )
            print ("Solution Found!")
        else:
            state = plan[ len(plan) - 1 ]
            time = state[4] + timeStep

            for moveV0 in range(0, 2):
                v0 = state[0] + moveV0 * timeStep * topSpeed
                for moveV1 in range(0, 2):
                    v1 = state[1] + moveV1 * timeStep * topSpeed
                    for moveH0 in range(0, 2):
                        h0 = state[2] + moveH0 * timeStep * topSpeed
                        for moveH1 in range(0, 2):
                            h1 = state[3] + moveH1 * timeStep * topSpeed
                            newState = (v0, v1, h0, h1, time)
                            newPlan = plan.copy()
                            newPlan.append(newState)
                            findMotionPlansInActionSpaceRecurse( newPlan, outFile )


###################################
##      Alternative Methods      ##
###################################

def findMotionPlansInStateSpace( ) :
    print( "Finding motion plans in state space" )
    
    planStart = [(0.0, 0.0, 0.0, 0.0, 0.0)]

    fileName = generateFileName( motionPlansFilePrefix, goalPos, timeStep, endTime, topSpeed, fileExtension)
    motionPlansFile = open( fileName, 'w' )
    findMotionPlansInStateSpaceRecurse( planStart, motionPlansFile )
    motionPlansFile.close()

def findMotionPlansInStateSpaceRecurse( motionPlan, outFile ) :
    latestState = motionPlan[ len(motionPlan) - 1 ]

    if isFinalState ( latestState, goalPos ):
        print("Solution Found!")
        writePlanToFile( motionPlan, outFile )
    else:
        nextTime = latestState[4] + timeStep

        if nextTime <= endTime :
            timeIndex = int(nextTime / timeStep)

            for stateString in stateSpace[timeIndex]:
                state = stringToState(stateString)
                if areAdjacentStates( latestState, state, timeStep, topSpeed ) :
                    # Deep copy list and add newest state
                    newPlan = list(motionPlan)
                    newPlan.append(state)
                    findMotionPlansInStateSpaceRecurse( newPlan, outFile )
    
    
####################
##      Main      ##
####################

fileName = generateFileName( prunedSpaceFilePrefix, goalPos, timeStep, endTime, topSpeed, fileExtension)

stateSpace = loadStateSpace( fileName )
#stateSpace = loadStateSpace( generateFileName(stateSpaceFilePrefix) )

#findMotionPlansInActionSpace()
findMotionPlansInStateSpace()

print ( "\nRun completed." )



