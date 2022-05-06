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
        degrees = angle*2+4
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
        degrees = angle*2+5
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

        tileMap = []
        for l in range(15):
            tileRow = []
            for m in range(15):
                tileRow.append('---')
            tileMap.append(tileRow)
        currentX = 7; currentY = 7

        currentAngle = 0    #left: -ve, right: +ve
        while GLOBALS.searchingForVictims == True:
            walls = []
            for i in range(4):  #scan
                print(self.get_ultra_sensor())
                if self.get_ultra_sensor() < 15 or self.get_ultra_sensor() == 0 or self.get_ultra_sensor() == 999:   #if all 999, it will re scan
                    walls.append(1)
                else:
                    walls.append(0)
                if GLOBALS.searchingForVictims == False:
                    return
                self.turnLeft(90)
                currentAngle -= 90  
                if self.get_thermal_sensor() > 30:  # indentified victim
                    victimPosition = i+1
                    print("deploy medical package") 
                    #self.spin_medium_motor(2000)
                else:
                    victimPosition = 0
            print(walls)

            #update map
            orderedWalls = []
            if currentAngle%360 == 0:
                orderedWalls = walls
            elif currentAngle%360 == -90 or currentAngle%360 == 270:
                orderedWalls = walls[-1:] + walls[:-1]
            elif currentAngle%360 == -180 or currentAngle%360 == 180:
                orderedWalls = walls[-2:] + walls[:-2]
            else:
                orderedWalls = walls[-3:] + walls[:-3]
            print("ordered walls:  " + str(orderedWalls))    

            #GLOBALS.DATABASE.ModifyQuery("INSERT INTO mission (startTime, location, notes, endTime,userID,missionMap) VALUES (?,?,?,?,?,?)",(10,"ashgrove","dead",11,1,str(tileMap)))

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
                        currentAngle += possibleExits[0]
                    else:
                        self.turnRight(360-abs(possibleExits[0]))
                        currentAngle += 360-abs(possibleExits[0])
                else:       
                    if walls[1] == 0:
                        self.turnLeft(90)
                        currentAngle -= 90
                    elif walls[0] == 0:
                        pass
                    elif walls[3] == 0:
                        self.turnRight(90)
                        currentAngle += 90
                
                self.mapMaze(orderedWalls, currentX, currentY, victimPosition, tileMap)

                for i in range(len(tileMap)):
                    print(tileMap[i])

                if currentAngle%360 == 0:
                    currentY -= 1
                elif currentAngle%360 == -90 or currentAngle%360 == 270:
                    currentX -= 1
                elif currentAngle%360 == 90 or currentAngle%360 == -270:
                    currentX += 1
                else:
                    currentY += 1

                self.forward(10,150)


    def mapMaze(self, orderedWalls, currentX, currentY, victimPosition, tileMap):
        if orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '00'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '01'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '02'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '03'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '04'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '06'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '07'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '08'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '09'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '11'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '12'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 0 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '13'
        elif orderedWalls[0] == 0 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '14'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 1 and orderedWalls[3] == 0:
            tileMap[currentY][currentX] = '15'
        elif orderedWalls[0] == 1 and orderedWalls[1] == 1 and orderedWalls[2] == 0 and orderedWalls[3] == 1:
            tileMap[currentY][currentX] = '16'

        if victimPosition != 0:
            tileMap[currentY][currentX] += str(victimPosition)
        else:
            tileMap[currentY][currentX] += '0'
    
        return tileMap

# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    logging.basicConfig(filename='logs/robot.log', level=logging.INFO)
    ROBOT = Robot(timelimit=10)  #10 second timelimit before
    ROBOT.configure_sensors() #This takes 4 seconds
    #input("Press Enter: ")
    ROBOT.automatedSearch()
    #ROBOT.alignWithWall(30)
    ROBOT.safe_exit()

