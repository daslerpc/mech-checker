def loadStateSpace(fileName):
    print ( "Loading state space from " + fileName )

    stateSpace = []

    endTime = float(fileName.split('_')[3][1:])
    timeStep = float(fileName.split('_')[2][1:])
    
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

    return stateSpace

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

def isFinalState ( state, goalPos ):
    v0 = state[0]
    v1 = state[1]
    h0 = state[2]
    h1 = state[3]
    return v0 == goalPos and v1 == goalPos and h0 == goalPos and h1 == goalPos

def areAdjacentStates( firstState, nextState, timeStep, topSpeed ) :
    adjacent = (firstState[4] + timeStep == nextState[4])
    
    for index in range(0, 4) :
        if not (firstState[index] == nextState[index] or firstState[index] + (timeStep*topSpeed) == nextState[index]):
            adjacent = False            

    return adjacent

# Creates a filename containing run parameters
def generateFileName( name, goalPos, timeStep, endTime, topSpeed, fileExtension ) :
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

# Write the states in the state space to a file
def writeStateSpaceToFile( stateSpace, stateSpaceFileName) :
    print("Writing state space to file " + stateSpaceFileName)
    stateSpaceFile = open(stateSpaceFileName, 'w')

    for statesAtTime in stateSpace:
        for stateString in statesAtTime:
            state = stringToState( stateString )
            stateSpaceFile.write(str(state[0]) + "," + str(state[1]) + "," + str(state[2]) + "," + str(state[3]) + "," + str(state[4]) + "\n")
    
    stateSpaceFile.close()
    print("Writing complete\n")

