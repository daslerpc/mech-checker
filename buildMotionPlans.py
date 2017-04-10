############################
##    Program Settings    ##
############################

stateSpaceFileName = "validStateSpaces.dat"
testDataFileName= "stateSpaceTestData.dat"

motionPlansFileName = "motionPlans.dat"

goalPos = 2.0
timeStep = 1.0/16.0

endTime = 3.0

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
        stateSpace.append( [] )

    inputFile = open(fileName, 'r')

    for line in inputFile:

        data = line.strip().split(',')

        v0 = float( data[0] )
        v1 = float( data[1] )

        h0 = float( data[2] )
        h1 = float( data[3] )

        time = float( data[4] )

        state = (v0,v1,h0,h1,time)

        index = int(time / timeStep)

        stateSpace[index].append( state )
    
    inputFile.close()

    print ("Load complete\n")

def generateTestData( fileName ) :
    outputFile = open(fileName, 'w')
    for step in range(0, 33):
        t = step/16.0
        state = ""
        for x in range(0, 5):
            state = state + str(t)
            if x !=4:
                state = state +","
            else:
                state = state +"\n"
                
        outputFile.write(state)
        
    outputFile.close()

def findMotionPlans( ) :
    print( "Finding Motion Plans" )
    
    planStart = [(0.0, 0.0, 0.0, 0.0, 0.0)]
    # planStart = [(2.0, 2.0, 2.0, 2.0, 2.0)]

    motionPlansFile = open( motionPlansFileName, 'w' )
    findMotionPlansRecurse( planStart, motionPlansFile )
    motionPlansFile.close()

def findMotionPlansRecurse( motionPlan, outFile ) :
    latestState = motionPlan[ len(motionPlan) - 1 ]

    if isFinalState ( latestState ):
        writeToFile( motionPlan, outFile )
        #solutionsFound = solutionsFound + 1
    else:
        nextTime = latestState[4] + timeStep

        if nextTime <= endTime :
            timeIndex = int(nextTime / timeStep)

            for state in stateSpace[timeIndex]:
                if areAdjacentStates( latestState, state ) :
                    newPlan = copyList(motionPlan)
                    newPlan.append(state)
                    findMotionPlansRecurse( newPlan, outFile )

    
def copyList( inList ):
    newList = []
    for item in inList:
        newList.append( item )
    return newList

def isFinalState ( state ):
    v0 = state[0]
    v1 = state[1]
    h0 = state[2]
    h1 = state[3]
    return v0 == goalPos and v1 == goalPos and h0 == goalPos and h1 == goalPos

def writeToFile( plan, outFile ) :
    for state in plan:
        count = 0
        for number in state:
            outFile.write( str(number) )
            if count != 4:
                outFile.write( "," )
                count = count + 1
            
        outFile.write("\n")
        
    outFile.write( "\n" )
        
def areAdjacentStates( firstState, nextState ) :
    adjacent = (firstState[4] + timeStep == nextState[4])
    
    for index in range(0, 4) :
        if not (firstState[index] == nextState[index] or firstState[index] + timeStep == nextState[index]):
            adjacent = False            

    return adjacent
        
    
####################
##      Main      ##
####################

#loadStateSpace( testDataFileName )
loadStateSpace( stateSpaceFileName )

#findMotionPlans()

startingIndex = 24

reachableCount = 0
totalCount = len(stateSpace[startingIndex + 1])

for nextState in stateSpace[startingIndex + 1]:
    reachable = False
    for firstState in stateSpace[startingIndex]:
        if areAdjacentStates( firstState, nextState ) :
            reachableCount = reachableCount + 1
            break
    

print ( str(reachableCount) + " valid links out of a total of " + str(totalCount) )
print ( str( round(float(reachableCount)/totalCount*100,2)) + "%")

print ( "Run completed." )
#print ( str(solutionsFound) + " solutions found." )



