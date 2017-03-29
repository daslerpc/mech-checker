############################
##    Program Settings    ##
############################

stateSpaceFileName = "validStateSpaces.dat"
testDataFileName= "stateSpaceTestData.dat"

motionPlansFileName = "motionPlans.dat"

goalPos = 2.0
timeStep = 1.0/16.0

#############################
##    Program Variables    ##
#############################

stateSpace = set()

#####################
##     Methods     ##
#####################

def loadStateSpace(fileName):
    file = open(fileName, 'r')

    for line in file:

        data = line.strip().split(',')

        v0 = float( data[0] )
        v1 = float( data[1] )

        h0 = float( data[2] )
        h1 = float( data[3] )

        time = float( data[4] )

        state = (v0,v1,h0,h1,time)

        stateSpace.add( state )
    
    file.close()

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
    findMotionPlansRecurse( planStart )


def findMotionPlansRecurse( plan ):
    planSize = len(plan)
    lastState = plan[ planSize-1 ]

    if lastState in stateSpace:
        if isFinalState ( lastState ):
            writeToFile( plan )
        else:
            advanceTime( plan )

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
        
def advanceTime( plan ) :
    state = plan[ len(plan) - 1 ]
    time = state[4] + timeStep

    for moveV0 in range(0, 2):
        v0 = state[0] + moveV0 * timeStep
        for moveV1 in range(0, 2):
            v1 = state[1] + moveV1 * timeStep
            for moveH0 in range(0, 2):
                h0 = state[2] + moveH0 * timeStep
                for moveH1 in range(0, 2):
                    h1 = state[3] + moveH1 * timeStep
                    newState = (v0, v1, h0, h1, time)
                    newPlan = plan.copy()
                    newPlan.append(newState)
                    findMotionPlansRecurse( newPlan )
    
####################
##      Main      ##
####################

motionPlansFile = open( motionPlansFileName, 'w' )

loadStateSpace( testDataFileName )
findMotionPlans()


motionPlansFile.close()



