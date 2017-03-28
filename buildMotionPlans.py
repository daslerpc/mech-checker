############################
##    Program Settings    ##
############################

stateSpaceFileName = "validStateSpaces.dat"
testDataFileName= "stateSpaceTestData.dat"

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
    
    
####################
##      Main      ##
####################

loadStateSpace( stateSpace, testDataFileName )

state = (2.0,2.0,2.0,2.0,2.0)

print ( state in stateSpace )




