#This is where your main robot code resides. It extendeds from the BrickPi Interface File
#It includes all the code inside brickpiinterface. The CurrentCommand and CurrentRoutine are important because they can keep track of robot functions and commands. Remember Flask is using Threading (e.g. more than once process which can confuse the robot)
from interfaces.brickpiinterface import *
import global_vars as GLOBALS
import logging
import math

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
        degrees = angle*2-2
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
        #input("press enter")
        direction = 0
        updatedPossibleExits = []

        map = []    #get the map going
        tileMap = []
        for j in range(15):
            row = []
            for i in range(15):
                tile = []
                for k in range(5):
                    tile.append(0)
                row.append(tile)
            map.append(row)
        for l in range(15):
            tileRow = []
            for m in range(15):
                tileRow.append(0)
            tileMap.append(tileRow)
        x = 7; y = 7
        map[7][7][0] = True
        tileMap[7][7] = 1
        #for i in range(len(map)):
        #    print(map[i])

        currentAngle = 0    #left: -ve, right: +ve
        while True:
            walls = []
            for i in range(4):  #scan
                time.sleep(0.5)
                #print(self.get_ultra_sensor())
                if self.get_ultra_sensor() < 25 or self.get_ultra_sensor() == 0 or self.get_ultra_sensor() == 999:   #if all 999, it will re scan
                    walls.append(1)
                else:
                    walls.append(0)
                self.turnLeft(90)
                currentAngle -= 90   
                #print(currentAngle)
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
            for i in range(4):
                map[y][x][i+1] = orderedWalls[i]
            print(map)
            print(" ")

            GLOBALS.DATABASE.ModifyQuery("INSERT INTO mission (startTime, location, notes, endTime,userID,missionMap) VALUES (?,?,?,?,?,?)",(10,"ashgrove","dead",11,1,str(map)))

            for i in range(len(tileMap)):
                print(tileMap[i])

            wallCount = 0
            count1 = 0
            possibleExits = []
            for wall in walls:
                if wall == 1:
                    wallCount += 1
                else:
                    possibleExits.append(90*count1*-1) #angle for each exit
                if wallCount == 4:
                    possibleExits.clear()
                    break
                count1 += 1

            print("possible exits: " + str(possibleExits))
            print(orderedWalls)
            time.sleep(0.5)

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
                        direction = -90
                    elif walls[0] == 0:
                        direction = 0
                        pass
                    elif walls[3] == 0:
                        self.turnRight(90)
                        currentAngle += 90
                        direction = 90
                for i in range(4): #go through all of orderdwalls
                    if orderedWalls[i] == 0:	#if there isn't a wall, mark it as a place to explore
                        if i == 0 and tileMap[y-1][x] != 1: #if there ins't a wall infront and it hasn't already been explored
                            tileMap[y-1][x]=3
                        elif i == 3 and tileMap[y][x+1] != 1:
                            tileMap[y][x+1]=3
                        elif i == 2 and tileMap[y+1][x] != 1:
                            tileMap[y+1][x]=3
                        elif i == 1 and tileMap[y][x-1] != 1:
                            tileMap[y][x-1]=3

                time.sleep(0.5)
                self.forward(42,150)
                print(currentAngle)
                map[y][x][0]=0
                #map stuff
                if currentAngle%360 == 0:
                    y -= 1
                elif currentAngle%360 == 90 or currentAngle%360 == -270:
                    x+=1
                elif currentAngle%360 == 180 or currentAngle%360 == -180:
                    y+=1
                else:
                    x-=1
                map[y][x][0]=True
                tileMap[y][x] = 1

            print(x,y)
        print("finished")


# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    logging.basicConfig(filename='logs/robot.log', level=logging.INFO)
    ROBOT = Robot(timelimit=10)  #10 second timelimit before
    ROBOT.configure_sensors() #This takes 4 seconds
    #input("Press Enter: ")
    ROBOT.automatedSearch()
    #ROBOT.alignWithWall(30)
    ROBOT.safe_exit()

