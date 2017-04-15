############################
##    Program Settings    ##
############################

fileExtension = ".dat"

stateSpaceFilePrefix = "validStateSpaces"
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

def loadStateSpace(fileName):
    print ( "Loading state space from " + fileName )
    
    for time in range(0, int(endTime/timeStep) + 1) :
        stateSpace.append( set() )

    inputFile = open(fileName, 'r')

    for line in inputFile:
        state = stringToState(line)
        time = state[4] 

        index = int(time / timeStep)

        stateSpace[index].add( line.strip() )
    
    inputFile.close()

    print ("Load complete\n")


def isFinalState ( state ):
    v0 = state[0]
    v1 = state[1]
    h0 = state[2]
    h1 = state[3]
    return v0 == goalPos and v1 == goalPos and h0 == goalPos and h1 == goalPos

def writeToFile( plan, outFile ) :
    for state in plan:
        outFile.write( stateToString( state ) + "\n" )
        
    outFile.write( "\n" )
        
def areAdjacentStates( firstState, nextState ) :
    adjacent = (firstState[4] + timeStep == nextState[4])
    
    for index in range(0, 4) :
        if not (firstState[index] == nextState[index] or firstState[index] + (timeStep*topSpeed) == nextState[index]):
            adjacent = False            

    return adjacent

def stateToString( state ) :
    stateString = ""
    count = 0
    
    for number in state:
        stateString = stateString + str(number)
        if count != 4:
            stateString = stateString + ","
            count = count + 1

    return stateString

def stringToState( text ) :
    data = text.strip().split(',')

    v0 = float( data[0] )
    v1 = float( data[1] )

    h0 = float( data[2] )
    h1 = float( data[3] )

    time = float( data[4] )

    return (v0,v1,h0,h1,time)

# Creates a filename containing run parameters
def generateFileName( name ) :
    # Goal Position
    name = name + "_G" + str(goalPos)

    # Resolution
    name = name + "_R" + str(timeStep)

    # End Time
    name = name + "_E" + str(endTime)

    # Top Speed
    name = name + "_S" + str(topSpeed)

    # Add extension
    name = name + fileExtension
    
    return name           

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
        if isFinalState ( lastState ):
            writeToFile( plan, outFile )
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

    motionPlansFile = open( generateFileName(motionPlansFilePrefix), 'w' )
    findMotionPlansInStateSpaceRecurse( planStart, motionPlansFile )
    motionPlansFile.close()

def findMotionPlansInStateSpaceRecurse( motionPlan, outFile ) :
    latestState = motionPlan[ len(motionPlan) - 1 ]

    if isFinalState ( latestState ):
        print("Solution Found!")
        writeToFile( motionPlan, outFile )
    else:
        nextTime = latestState[4] + timeStep

        if nextTime <= endTime :
            timeIndex = int(nextTime / timeStep)

            for stateString in stateSpace[timeIndex]:
                state = stringToState(stateString)
                if areAdjacentStates( latestState, state ) :
                    # Deep copy list and add newest state
                    newPlan = list(motionPlan)
                    newPlan.append(state)
                    findMotionPlansInStateSpaceRecurse( newPlan, outFile )
    
    
####################
##      Main      ##
####################

#loadStateSpace( generateFileName(testDataFilePrefix) )
loadStateSpace( generateFileName(stateSpaceFilePrefix) )

#findMotionPlansInActionSpace()
findMotionPlansInStateSpace()

print ( "\nRun completed." )



