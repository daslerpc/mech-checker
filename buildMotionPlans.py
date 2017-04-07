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

#####################
##     Methods     ##
#####################

def loadStateSpace(fileName):
    print ( "Loading state space from " + fileName )
    
    for time in range(0, int(endTime/timeStep) + 1) :
        stateSpace.append( [] )

    file = open(fileName, 'r')

    for line in file:

        data = line.strip().split(',')

        v0 = float( data[0] )
        v1 = float( data[1] )

        h0 = float( data[2] )
        h1 = float( data[3] )

        time = float( data[4] )

        state = (v0,v1,h0,h1,time)

        index = int(time / timeStep)

        stateSpace[index].append( state )
    
    file.close()

    print ("Load complete\n")

def generateTestData( file ) :
    file = open(fileName, 'w')
    for step in range(0, 33):
        t = step/16.0
        state = ""
        for x in range(0, 5):
            state = state + str(t)
            if x !=4:
                state = state +","
            else:
                state = state +"\n"
                
        file.write(state)
        
    file.close()


def findMotionPlans( ) :
    planStart = [(0.0, 0.0, 0.0, 0.0, 0.0)]
   # planStart = [(2.0, 2.0, 2.0, 2.0, 2.0)]

   

def findMotionPlansRecurse( motionPlan ) :
    latestState = motionPlan[ len(motionPlan) - 1 ]
    time = latestState[4]

    index = int(time / timeStep)

    

def isFinalState ( state ):
    v0 = state[0]
    v1 = state[1]
    h0 = state[2]
    h1 = state[3]
    return v0 == goalPos and v1 == goalPos and h0 == goalPos and h1 == goalPos

def writeToFile( plan ) :
    for state in plan:
        motionPlansFile.write( str(state) + "\n" )
        
    motionPlansFile.write( "\n" )
        
def areAdjacentStates( state1, state2 ) :
    adjacent = (state1[4] + timeStep == state2[4])
    
    for index in range(0, 4) :
        if not (state1[index] == state2[index] or state1[index] + timeStep == state2[index]):
            adjacent = False            

    return adjacent
        
    
####################
##      Main      ##
####################

loadStateSpace( testDataFileName )
#loadStateSpace( stateSpaceFileName )

#motionPlansFile = open( motionPlansFileName, 'w' )
#findMotionPlans()
#motionPlansFile.close()

print ( "Run completed." )



