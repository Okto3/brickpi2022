#This is where your main robot code resides. It extendeds from the BrickPi Interface File
#It includes all the code inside brickpiinterface. The CurrentCommand and CurrentRoutine are important because they can keep track of robot functions and commands. Remember Flask is using Threading (e.g. more than once process which can confuse the robot)
from interfaces.brickpiinterface import *
import global_vars as GLOBALS
import logging

class Robot(BrickPiInterface):
    
    def __init__(self, timelimit=10, logger=logging.getLogger()):
        super().__init__(timelimit, logger)
        self.CurrentCommand = "stop" #use this to stop or start functions
        self.CurrentRoutine = "stop" #use this stop or start routines
        return

    
    def forward(self,distanceCm,speed=100,power=100):
        distance = distanceCm * 360 / (np.pi * 5.6)
        BP = self.BP
        try:
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
            BP.set_motor_limits(BP.PORT_A, power, speed)    # float motor D
            BP.set_motor_limits(BP.PORT_D, power, speed)          # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
            while True:
                BP.set_motor_position(BP.PORT_D, distance+10)    # set motor A's target position to the current position of motor D
                BP.set_motor_position(BP.PORT_A, distance+10)
                time.sleep(0.02) 
                if BP.get_motor_encoder(BP.PORT_D) >= distance or BP.get_motor_encoder(BP.PORT_A) >= distance:
                    break
                #print("A:  " + str(distance+10) + "   " + str(BP.get_motor_encoder(BP.PORT_A)))
                #print("D:  " + str(distance+10) + "   " + str(BP.get_motor_encoder(BP.PORT_D)))
        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all()
        return
    
    def backward(self,distanceCm,speed=100,power=100):
        distance = -1*distanceCm * 360 / (np.pi * 5.6)
        BP = self.BP
        try:
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
            BP.set_motor_limits(BP.PORT_A, power, speed)    # float motor D
            BP.set_motor_limits(BP.PORT_D, power, speed)          # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
            while True:
                BP.set_motor_position(BP.PORT_D, distance-10)    # set motor A's target position to the current position of motor D
                BP.set_motor_position(BP.PORT_A, distance-10)
                time.sleep(0.02) 
                if BP.get_motor_encoder(BP.PORT_D) <= distance or BP.get_motor_encoder(BP.PORT_A) <= distance:
                    break
                #print("A:  " + str(distance+10) + "   " + str(BP.get_motor_encoder(BP.PORT_A)))
                #print("D:  " + str(distance+10) + "   " + str(BP.get_motor_encoder(BP.PORT_D)))
        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all()
        return

    def turnLeft(self,angle,speed=100,power=100):   #power percent, degrees/second, degrees
        BP = self.BP
        degrees = angle*2-4
        try:
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
            BP.set_motor_limits(BP.PORT_A, -1*power, speed)    # float motor D
            BP.set_motor_limits(BP.PORT_D, power, speed)          # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
            while True:
                BP.set_motor_position(BP.PORT_D, degrees+5)    # set motor A's target position to the current position of motor D
                BP.set_motor_position(BP.PORT_A, -1*degrees-5)
                time.sleep(0.02) 
                if BP.get_motor_encoder(BP.PORT_D) >= degrees or BP.get_motor_encoder(BP.PORT_A) <= -1*degrees:
                    break
                #print("A:  " + str(-1*degrees+10) + "   " + str(BP.get_motor_encoder(BP.PORT_A)))
                #print("D:  " + str(degrees-10) + "   " + str(BP.get_motor_encoder(BP.PORT_D)))
        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all() 
        return

    def turnRight(self,angle,speed=100,power=100):
        BP = self.BP
        degrees = angle*2+8
        try:
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
            BP.set_motor_limits(BP.PORT_D, -1*power, speed)    # float motor D
            BP.set_motor_limits(BP.PORT_A, power, speed)          # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
            while True:
                BP.set_motor_position(BP.PORT_A, degrees+10)    # set motor A's target position to the current position of motor D
                BP.set_motor_position(BP.PORT_D, -1*degrees-10)
                time.sleep(0.02) 
                if BP.get_motor_encoder(BP.PORT_A) >= degrees or BP.get_motor_encoder(BP.PORT_D) <= -1*degrees:
                    break
                #print("D:  " + str(-1*degrees-10) + "   " + str(BP.get_motor_encoder(BP.PORT_D)))
                #print("A:  " + str(degrees+10) + "   " + str(BP.get_motor_encoder(BP.PORT_A)))
        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all() 
        return


 
    

    def automatedSearch(self):
        print(str(round(((self.get_battery()-8)*25),2))+"%")

        #GLOBALS.tileMap = []
        for l in range(15):
            tileRow = []
            for m in range(15):
                tileRow.append('---')
            GLOBALS.tileMap.append(tileRow)

        # current angle - left: -ve, right: +ve
        while GLOBALS.searchingForVictims == True:
            walls = []
            for i in range(4):  #scan
                print(self.get_ultra_sensor())
                if self.get_ultra_sensor() < 20 or self.get_ultra_sensor() == 0 or self.get_ultra_sensor() == 999:   #if all 999, it will re scan
                    walls.append(1)
                else:
                    walls.append(0)
                if GLOBALS.searchingForVictims == False:
                    return
                self.turnLeft(90)
                GLOBALS.currentAngle -= 90  
                if self.get_thermal_sensor() > 27:  # indentified victim
                    victimPosition = i+1
                    print("deploy medical package") 
                    self.spin_medium_motor(2000)
                else:
                    victimPosition = 0
            print(walls)

            #update map
            orderedWalls = []
            if GLOBALS.currentAngle%360 == 0:
                orderedWalls = walls
            elif GLOBALS.currentAngle%360 == -90 or GLOBALS.currentAngle%360 == 270:
                orderedWalls = walls[-1:] + walls[:-1]
            elif GLOBALS.currentAngle%360 == -180 or GLOBALS.currentAngle%360 == 180:
                orderedWalls = walls[-2:] + walls[:-2]
            else:
                orderedWalls = walls[-3:] + walls[:-3]
            print("ordered walls:  " + str(orderedWalls))    

            GLOBALS.DATABASE.ModifyQuery("INSERT INTO mission (startTime, location, notes, endTime,userID,missionMap) VALUES (?,?,?,?,?,?)",(10,"ashgrove","dead",11,1,str(GLOBALS.tileMap)))

            wallCount = 0
            possibleExits = []
            for i in range(len(walls)):
                if walls[i] == 1:
                    wallCount += 1
                else:
                    possibleExits.append(90*walls[i]*-1) #angle for each exit
                if wallCount == 4:
                    possibleExits.clear()
                    break

            print("possible exits: " + str(possibleExits))
            print(orderedWalls)

            if possibleExits:   #turn left algo
                if len(possibleExits) == 1:     #only 1 exit - go back the way you came
                    if abs(possibleExits[0])%360 <= 180:
                        self.turnLeft(abs(possibleExits[0]))
                        GLOBALS.currentAngle += possibleExits[0]
                    else:
                        self.turnRight(360-abs(possibleExits[0]))
                        GLOBALS.currentAngle += 360-abs(possibleExits[0])
                else:       
                    if walls[1] == 0:
                        self.turnLeft(90)
                        GLOBALS.currentAngle -= 90
                    elif walls[0] == 0:
                        pass
                    elif walls[3] == 0:
                        self.turnRight(90)
                        GLOBALS.currentAngle += 90
                
                self.mapMaze(orderedWalls, victimPosition)

                for i in range(len(GLOBALS.tileMap)):
                    print(GLOBALS.tileMap[i])

                if GLOBALS.currentAngle%360 == 0:
                    GLOBALS.currentY -= 1
                elif GLOBALS.currentAngle%360 == -90 or GLOBALS.currentAngle%360 == 270:
                    GLOBALS.currentX -= 1
                elif GLOBALS.currentAngle%360 == 90 or GLOBALS.currentAngle%360 == -270:
                    GLOBALS.currentX += 1
                else:
                    GLOBALS.currentY += 1

                self.forward(25,150)


    def mapMaze(self, orderedWalls, victimPosition):
        if orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '00'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '01'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '02'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '03'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '04'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '06'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '07'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '08'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '09'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '11'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '12'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '13'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '14'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '15'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] = '16'

        if victimPosition != 0:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] += str(victimPosition)
        else:
            GLOBALS.tileMap[GLOBALS.currentY][GLOBALS.currentX] += '0'
    
        return GLOBALS.tileMap

    def getHome(self):
        returnMap = []
        x = GLOBALS.currentX; y = GLOBALS.currentY+1
        print("x and y: " + str(x) + ", " + str(y))
        for l in range(15):
            returntileRow = []
            for m in range(15):
                returntileRow.append('-')
            returnMap.append(returntileRow)
        returnMap[y][x] = '0'
        for k in range(len(GLOBALS.tileMap)):
            print(GLOBALS.tileMap)

        count = '0'
        for z in range(10): #max number of tiles to destination - should be while loop

            for i in range(len(returnMap)):
                for j in range(len(returnMap[i])):
                    if returnMap[i][j] == count:
                        print("next possition is at: " + str(i) + ", " + str(j))
                        x=j; y=i
                        count = str(int(count)+1)

                        for k in range(len(returnMap)):
                            print(returnMap[k])
                        print(" ")
                        print(count)

                        if GLOBALS.tileMap[y][x][0:2] == '00':
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '01':
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '02':
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '03':
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '04':
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '06':
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            print("code" + str(6))
                        if GLOBALS.tileMap[y][x][0:2] == '07':
                            if returnMap[x-1][x] == '-':
                                returnMap[x-1][x] = count
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '08':
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '09':
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '11':
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '12':
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '13':
                            if returnMap[y][x-1] == '-':
                                returnMap[y][x-1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '14':
                            if returnMap[y-1][x] == '-':
                                returnMap[y-1][x] = count
                        if GLOBALS.tileMap[y][x][0:2] == '15':
                            if returnMap[y][x+1] == '-':
                                returnMap[y][x+1] = count
                        if GLOBALS.tileMap[y][x][0:2] == '16':
                            if returnMap[y+1][x] == '-':
                                returnMap[y+1][x] = count
            
        #find path back
        startX = 7; startY = 7
        pathBack = [[7,7]]
        for i in range(int(count)-1):
            largest = int(returnMap[startY][startX])
            if returnMap[startY-1][startX] == str(largest - 1):
                nextStep = [startY-1,startX]
            elif returnMap[startY][startX+1] == str(largest - 1):
                nextStep = [startY,startX+1]
            elif returnMap[startY+1][startX] == str(largest - 1):
                nextStep = [startY+1,startX]
            else:
                nextStep = [startY,startX-1]
            pathBack.append(nextStep)
            startX = nextStep[1]
            startY = nextStep[0]
        print(pathBack)

        #turn it forwards
        print("REORIENTATING!")
        if GLOBALS.currentAngle%360 == 0:
            pass
        if GLOBALS.currentAngle%360 == -90 or GLOBALS.currentAngle%360 == 270:
            self.turnRight(90)
        elif GLOBALS.currentAngle%360 == 90 or GLOBALS.currentAngle%360 == -270:
            self.turnLeft(90)
        elif GLOBALS.currentAngle%360 == 180 or GLOBALS.currentAngle%360 == -180:
            self.turnRight(180)

        steps = len(pathBack)
        for i in range(steps):
            if steps - i - 2 >= 0:
                if pathBack[steps-i-1][0] - pathBack[steps - i - 2][0] < 0: #y needs to change
                    self.turnLeft(180)
                    self.forward(25)
                    self.turnLeft(180)
                elif pathBack[steps-i-1][0] - pathBack[steps - i - 2][0] > 0:
                    self.forward(25)
                if pathBack[steps-i-1][1] - pathBack[steps - i - 2][1] > 0:
                    self.turnLeft(90)
                    self.forward(25)
                    self.turnRight(90)
                elif pathBack[steps-i-1][1] - pathBack[steps - i - 2][1] < 0:
                    self.turnRight(90)
                    self.forward(25)
                    self.turnLeft(90)





# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    logging.basicConfig(filename='logs/robot.log', level=logging.INFO)
    ROBOT = Robot(timelimit=10)  #10 second timelimit before
    ROBOT.configure_sensors() #This takes 4 seconds
    #input("Press Enter: ")
    ROBOT.automatedSearch()
    ROBOT.getHome()
    ROBOT.safe_exit()

