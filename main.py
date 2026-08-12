# Place your creative task here!
from cmu_graphics import *
import copy
import random
import math
'''
Author: Sudeep Rawal
Creation Date: 4/3/2025
Last Modified: 4/28/2025
Project Description:
    This game is a competitive two player golf-like game where players take
    turns trying to manuever their ball into a rectangular goal. The game starts
    very easy with zero obstacles; however, as each round ends, players have the
    option to add one obstacle, or delete obstacles in a small radius. The aim
    of the game is to score as many points as possible while sabotaging your
    opponent by placing tricky obstacles. This game implements dictionaries for
    player placed obstacles, their left, right, top, and bottom coordinates,
    the strokes of each player, and maps. Though the "maps" feature is currently
    only used to change the location of the goal at the moment. The dictionary
    that stores player placed obstacles tracks the location of each obstalcle
    strictly for drawing. The dictionaries that store the left, right, top, and
    bottom of each obstacle are used to track the location of each obstacle for
    player interaction: by storing these values, it is easy to locate where each
    player is relative to the obstacles. Additionally, by using a dictionary for
    the players' strokes it is possible to store their stroke history per round.
    
Instructions:
    Click and drag your mouse to control the balls: when held down, a line with
    a circle and a larger outer circle will appear. The inner circle represents
    the current ball that is being putted. The strength behind how far the ball
    is putted depends on the length of the line; it is important to note that
    the created line reaches a maximum length when its touching the outer circle
    it's confined in and that players take moving their own ball. Players should 
    manuever towards the goal (the yellow rectangle) while competing against 
    each other. Once the players reach the goal, either player can pick and 
    choose between four options. The first three options are mystery blocks, 
    which each hide one possible obstacle that could either help or hinder the 
    players. The possible mystery obstacles are currently "platform," a wide 
    black line that players can phase through from the bottom and stand on at 
    the top; "bounce," a pink box that players bounce off from at all angles; 
    "stick," a green box that causes players to stick to it when they collide 
    with it; and "death," a red box that causes players to be exempt from the 
    round on contact. The last option is visually a skull; when pressed, it 
    allows players to delete blocks by pressing the mouse with the skull. 
    Additionally, players can see their scores by pressing either p or tab. 
    Once they press either button, a page will be shown detailing the amount of 
    times each player has successfully reached the goal, and the number of 
    strokes both players took each round. Pressing p or tab once again will 
    return the player to the page they were previously on. Pressing either 1 or
    0 will change the location of the goal, reset obstacles, and any player 
    properties: location, points, amount of strokes, etc. Whenever players
    add obstacles to the game, they add a set of values indicating the left,
    right, top, and bottom values of the obstacle. These values will also be
    removed when a player places the delete skull on top of the obstacles.
    Additionally, when a player places an obstacle, they are stored in another
    dictionary that details the top, left, width, and height values of each
    player placed obstacle.
Credits:Brian Son
Updates: Encouraged me to add visual elements for the delete skull. Also
encouraged me to add a circle indicating the maximum power, and advised me to
allow the player to move their stroke line outside of the circle for comfort.
Rubric Items:
    Dictionary Keys Values: 833
    Dictionary Input: 861
    Input Processing: 818
    Dictionary Output: 678
    Dictionary Modification: 645
    User Input System: 238 (whenever they click with this out, they add to the 
    dictionary due to storeAndPlaceBlock (818)
    .get Used: 834
'''
# start app (app.properties)
#Initializes all the app variables
def onAppStart(app):
    app.paused = False
    app.gravity = 9.8
    app.mu = 0.5
    app.mass = .9
    app.maps = dict()
    app.mysteryWidth = 120
    app.mysteryHeight = 140
    app.mysteryTop = 30
    app.mysteryLeft = 140
    app.mysteryGap = 30
    restartApp(app)

# draw graphics (redrawAll)
def redrawAll(app):
    #draws everything by calling on functions
    drawStats(app)
    drawPlayers(app)
    drawShootingLine(app)
    drawGoal(app)
    drawPlayerObstacles(app)
    drawSelectedObj(app)
    drawChoices(app)
    drawInstructions(app, app.currPage)

def drawInstructions(app, num):
    #draws the instructions to the game in segments, each page shows a different
    #set of instructions or descriptions.
    if app.showingHelp:
        drawRect(0, 0, 700, 400, fill = 'white')
        drawRect(600, 350, 126, 50, align = 'center', fill = 'yellow', 
                border = 'black', borderWidth = 5)
        drawRect(100, 350, 126, 50, align = 'center', fill = 'yellow', 
                 border = 'black', borderWidth = 5)
        drawLabel(f'Next', 600, 350, size = 24, bold = True)
        drawLabel(f'Previous', 100, 350, size = 24, bold = True)
        drawLabel(f'{num}/3', 350, 380, size= 24)
        if num == 1: 
            drawLabel("Instructions", 350, 20, size = 24, bold = True,
                               font = 'arial')
            drawLabel('Objective:', 10,60,align ='left',size = 24, bold = True)
            drawLabel(
                   'Get your ball in the yellow goal using the fewest strokes!',
                    170, 60, align = 'left',size = 16)
            drawLabel("Controls:", 10,120,align = 'left',size = 24, bold = True)
            drawLabel("Click & Drag -> Aim putt", 170, 120, 
                      align = 'left',size = 16)
            drawLabel("Release -> Shoot ball", 170, 140, 
                      align = 'left',size = 16)
            drawLabel("P/Tab -> Toggles stats", 170, 165, 
                      align = 'left',size = 16)
            drawLabel("H/I -> Toggle help", 170, 190,align = 'left',size = 16)
            drawLabel("1 or 0 -> Changes goal location and resets players", 
                      170, 215, align = 'left',size = 16)
            drawLabel("Click with object -> Place or delete", 170, 240, 
                      align = 'left', size = 16)
            drawLabel("Click mystery -> Select random object", 170, 265,
                      align = 'left', size = 16)
            drawLabel("Click skull -> Select delete", 170, 290
                      , align = 'left', size = 16)
            
        if num == 2:
            symbol = 'cmu://887649/38878731/Question+Mark.png'
            drawRect(500,20,app.mysteryWidth,app.mysteryHeight,fill = 'brown')
            drawImage(symbol, 500, 20, width = app.mysteryWidth,
                      height = app.mysteryHeight)
            drawLabel('Mystery Boxes:', 10, 30, align = 'left',
                       size = 24, bold = True)
            drawLabel('Three boxes appear each time both players have finished,'
                      ,10, 60, align = 'left', size = 16)
            drawLabel('when both players have died, or when one player has', 10,
                       80, align = 'left', size = 16)
            drawLabel('finished and the other has died. When the user clicks',
                      10, 100, align = 'left', size = 16)
            drawLabel('on one of these objects, they will have the chance to',
                      10, 120, align = 'left', size = 16)
            drawLabel('place a random obstacle.', 10, 140, align = 'left',
                      size = 16)
            
            symbol = 'cmu://887649/38878812/Delete+icon.png'
            drawImage(symbol, 560, 220,width = 50, height = 55, align ='center')
            drawLabel('Skulls:', 10, 180, align = 'left',
                       size = 24, bold = True)
            drawLabel('These skulls appear at the bottom of the screen when the'
                      , 10, 200, align = 'left', size = 16)
            drawLabel('mystery boxes do. Essentially, by clicking the skull,',
                       10, 220, align = 'left', size = 16)
            drawLabel("it's possible to move that skull on unwanted obstacles."
                      , 10, 240, align = 'left', size = 16)
            drawLabel("Once the player is satisfied with the placement, the",
                      10, 260, align = 'left', size = 16)
            drawLabel("player can click with their mouse and the obstacles will"
                      , 10, 280, align = 'left', size = 16)
            drawLabel("be deleted and thus removed from their dictionaries.", 
                       10, 300, align = 'left', size = 16)
        
        if num == 3:
            drawRect(420, 20, 75, 90, fill = 'red')
            drawRect(520, 20, 75, 90, fill = 'pink')
            drawRect(420, 120, 75, 90, fill = 'green')
            drawRect(520, 120, 150, 15, fill = 'black')
            drawLabel('Obstacles:', 10, 30, align = 'left',
                       size = 24, bold = True)
            drawLabel('The rectangles on the right are obstacles. Each obstacle' 
                      ,10, 50, align = 'left', size = 16)
            drawLabel('has a different function. The red obstacle causes the',
                       10, 70, align = 'left', size = 16)
            drawLabel("player who touches it to 'die' and be exempt from the",
                      10, 90, align = 'left', size = 16)
            drawLabel('current round (they do spawn back in the next round).',
                      10, 110, align = 'left', size = 16)
            drawLabel('The pink obstacle causes the player who touches it to',
                      10, 130, align = 'left', size = 16)
            drawLabel('bounce off with a multiplier added to their velocity.',
                      10, 150, align = 'left', size = 16)
            drawLabel('The green obstacle causes players who touch it to stick',
                      10, 170, align = 'left', size = 16)
            drawLabel('to it like glue, though it is very possible to escape.',
                      10, 190, align = 'left', size = 16)
            drawLabel('The black obstacle functions like a platform for the',
                      10, 210, align = 'left', size = 16)
            drawLabel('players. They are able to phase through the bottom;',
                      10, 230, align = 'left', size = 16)
            drawLabel('however, the top will be solid ground that functions',
                      10, 250, align = 'left', size = 16)
            drawLabel('similar to the floor by adding friction and lowering',
                      10, 270, align = 'left', size = 16)
            drawLabel('bounce strength. Placing these obstacles their values to'
                      ,10, 290, align = 'left', size = 16)
            drawLabel('dictionaries that details their locations.', 
                      10, 310, align = 'left', size = 16)

def drawStats(app):
    #Draws the players' scores, which is the amount of time they reach the goal;
    #the number of strokes each player made; and the rounds that have passed.
    if app.showingStats:
        drawLabel('Red:', 70, 150,)
        drawLabel('Blue:', 70, 250)
        drawLabel('Round:', 70, 110)
        drawLabel('Score', 110, 60)
        drawLabel('|', 110, 80)
        drawLabel('V', 110, 90)
        drawLabel(f'{app.aScore}', 110, 150)
        drawLabel(f'{app.bScore}', 110, 250)
        
        drawRect(350, 200, 500, 200, 
                 align = 'center', fill = None, border = 'black')
        drawLine(100, 120, 600,120)
        drawLine(100, 200, 600, 200)
        drawLine(120, 100, 120, 300)
        #print(app.aStrokes)
        prevLineX = 100
        if app.round != 0: 
            lineSpread = 500/(app.round)
        for i in range(1, app.round + 1):
            currKey = i-1
            lineX = 100 + i * lineSpread
            drawLine(lineX, 100, lineX, 300)
            centerBox = (lineX + prevLineX)/2
            drawLabel(f'{i}', centerBox, 110)
            drawLabel(f'{app.aStrokes[currKey]}', centerBox, 150)
            drawLabel(f'{app.bStrokes[currKey]}', centerBox, 250)
            prevLineX = lineX

def drawSelectedObj(app):
    #Draws and reveals whichever object the player selected from the mystery 
    #choices.
    if app.selectedObj != None and not app.paused:
        effect = app.selectedObj[0]
        symbol = ''
        if effect == 'death': color = 'red'
        if effect == 'bounce': color = 'pink'
        if effect == 'stick': color = 'green'
        if effect == 'platform': color = 'black'
        if effect == 'delete':
            symbol = 'cmu://887649/38878812/Delete+icon.png'
        if effect != 'delete': drawRect(*app.selectedObj[1::], fill = color)
        if symbol != '':
            imageLeft = app.selectedObj[1]
            imageTop = app.selectedObj[2]
            imageWidth = app.selectedObj[3]
            imageHeight = app.selectedObj[4]
            drawImage(symbol, imageLeft, imageTop, align = 'center',
                    width = imageWidth, height = imageHeight)

def drawPlayerObstacles(app):
    #This runs through every object placed by the players and shows it on the
    #screen.
    if len(app.playerObstacles) > 0 and not app.paused:
        for effect in app.playerObstacles:
            for key in reversed(app.playerObstacles[effect]):
                symbol = ''
                color = None
                if effect == 'death': color = 'red'
                if effect == 'bounce': color = 'pink'
                if effect == 'stick': color = 'green'
                if effect == 'platform': color = 'black'
                drawRect(*app.playerObstacles[effect][key], fill = color)
    
def drawChoices(app):
    #Draws the three mystery objects and the delete object.
    if app.betweenRound and not app.showingStats:
        symbol = 'cmu://887649/38878731/Question+Mark.png'
        ObjectTop = app.mysteryTop
        ObjectBot = app.mysteryTop + app.mysteryHeight
        Object1Left = app.mysteryLeft
        Object2Left = Object1Left + app.mysteryWidth + app.mysteryGap
        Object3Left = Object2Left +  app.mysteryWidth + app.mysteryGap
        drawRect(Object1Left, ObjectTop,app.mysteryWidth, app.mysteryHeight, 
                                                                fill = 'brown')
        drawRect(Object2Left, ObjectTop,app.mysteryWidth, app.mysteryHeight, 
                                                                fill = 'brown')
        drawRect(Object3Left, ObjectTop,app.mysteryWidth, app.mysteryHeight,
                                                                fill = 'brown')
        drawImage(symbol, Object1Left, ObjectTop, width = app.mysteryWidth,
                  height = app.mysteryHeight)
        drawImage(symbol, Object2Left, ObjectTop, width = app.mysteryWidth,
                  height = app.mysteryHeight)
        drawImage(symbol, Object3Left, ObjectTop, width = app.mysteryWidth,
                  height = app.mysteryHeight)
        #deleteObj
        symbol = 'cmu://887649/38878812/Delete+icon.png'
        imageLeft = app.deleteObj[1]
        imageTop = app.deleteObj[2]
        imageWidth = app.deleteObj[3]
        imageHeight = app.deleteObj[4]
        drawImage(symbol, imageLeft, imageTop, align = 'center',
                    width = imageWidth, height = imageHeight)
def drawGoal(app):
    #Draws the goal. Not much else to say.
    if not app.paused:
        drawRect(*app.goalRect, fill = 'yellow', border = 'black')

def drawShootingLine(app):
    #When a player is trying to shoot, this draws a line indicating the strength
    #and angle of their shot, a interior circle indicating which player is 
    #shooting, and an exterior circle indicating the furthest the line travels.
    if not app.paused:
        if app.shootingLine[0] != None and app.shootingLine[2] != None:
            drawLine(*app.shootingLine)
            drawCircle(app.shootingLine[0], app.shootingLine[1], 5,
                      fill = app.playerColors[app.currTurn], border = 'black')
            drawCircle(app.shootingLine[0], app.shootingLine[1], 
                       100, fill = None, border = 'gray')

def drawPlayers(app):
    #draws the two golf balls that are the players
    if not app.paused:
        if not app.aFinished and not app.aDead:
            drawCircle(app.aCX, app.aCY, app.aRadius, fill = 'red')
        if not app.bFinished and not app.bDead:
            drawCircle(app.bCX, app.bCY, app.bRadius, fill = 'blue')

# helper functions
def checkDelete(app, setX, setY, mouseX, mouseY):
    #Checks if the deleting skull is not touching the object, if it passes all
    #the scenarios where it can't be touching the object, this returns True.
    deleteWidth = app.deleteObj[3]
    deleteHeight = app.deleteObj[4]
    print(setX, setY, mouseX, mouseY)
    if mouseX + deleteWidth/2 < min(setX):
        print('a')
        return False
    if mouseX - deleteWidth/2 > max(setX):
        print('b')
        return False
    if mouseY + deleteHeight/2 < min(setY):
        print('c')
        return False
    if mouseY - deleteHeight/2 > max(setY):
        print('d')
        return False
    print('f')
    return True

def distance(x1, y1, x2, y2):
    #Returns the distance between two different points
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def getAngleAndPower(L):
    #Calculates the angle and power that the ball is hit at.
    A = L[0] - L[2]
    B = L[3]-L[1]
    C = distance(L[0], L[1], L[2], L[3])
    theta = math.degrees(math.atan2(B, A)) %360
    return theta, C *1.5

def pickSize(obj):
    #This chooses the size of individual objects.
    size = [50, 60]
    if obj[0] == 'platform':
        size = [100, 10]
    if obj[0] == 'delete':
        size = [50, 55]
    return size
# functions
def restartApp(app):
    #initalizes all app properties that could be modified, when called it has an
    #effect of reseting them.
    app.currPage = 1
    app.showingHelp = True
    app.deleting = False
    app.selectedObj = None
    app.betweenRound = False
    app.currLoser = None
    app.objectList = ['death', 'bounce', 'stick', 'platform']
    app.playerColors = ['red', 'blue']
    app.aScore, app.bScore = 0, 0
    app.shootingLine = [None, None, None, None]
    app.steps = 0
    app.stepsPerSecond = 30
    app.currTurn = 0
    app.InPlay = False
    app.IsMoving = False
    app.playerObstacles = dict()
    app.placedObstaclesX = dict()
    app.placedObstaclesY = dict()
    app.showingStats = False
    app.round = 0
    selectMap(app, 0)

def selectMap(app, mapNum):
    #Resets the player properties and changes the location of the goal
    if type(mapNum) == str and not mapNum.isdigit():
        return
    mapNum = int(mapNum)
    app.paused = False
    app.betweenRound = False
    app.playerObstacles = dict()
    app.placedObstacles = dict()
    if mapNum == 0:
        app.ballPropertiesA = [15, 395, 5]
        app.ballPropertiesB = [5, 395, 5]
        app.goalRect = [690, 300, 10, 100]
        app.placedObstaclesX = dict()
    if mapNum == 1:
        app.ballPropertiesA = [15, 395, 5]
        app.ballPropertiesB = [5, 395, 5]
        app.goalRect = [690, 30, 10, 100]
        
    playerProperties(app, app.ballPropertiesA, app.ballPropertiesB)
    goalProperties(app)
        
def resetPos(app):
    #Essentially resets everything with the player except their scores and putts
    A = app.ballPropertiesA
    B = app.ballPropertiesB
    app.dxA, app.dyA, app.dxB, app.dyB = 0, 0, 0, 0
    app.aCX = A[0]
    app.aCY = A[1]
    app.aRadius = A[2]
    app.bCX = B[0]
    app.bCY = B[1]
    app.bRadius = B[2]
    app.aFinished = False
    app.bFinished = False
    app.aDead = False
    app.bDead = False
    app.aStuck = False
    app.bStuck = False
    app.aStickList = []
    app.bStickList = []

def createObject(app):
    #selects three random objects and creates their dimensions, and creates the
    #delete object. Only called when between rounds.
    if (not app.paused and (app.aFinished and app.bFinished) or (app.aFinished
        and app.bDead) or (app.aDead and app.bFinished) or 
        (app.aDead and app.bDead)):
        random.shuffle(app.objectList)
        app.object1 = [app.objectList[0], 200, 30]
        app.object2 = [app.objectList[1], 300, 30]
        app.object3 = [app.objectList[2], 400, 30]
        app.deleteObj = ['delete', 350, 350]
        app.object1 += (pickSize(app.object1))
        app.object2 += (pickSize(app.object2))
        app.object3 += (pickSize(app.object3))
        app.deleteObj += (pickSize(app.deleteObj))
        print(app.object1)
        print(app.object2)
        print(app.object3)

def goalProperties(app):
    #sets all the properties of the goal
    app.goalWidth = app.goalRect[2]
    app.goalHeight = app.goalRect[3]
    app.goalLeft = app.goalRect[0]
    app.goalTop = app.goalRect[1]
    app.goalRight = app.goalLeft + app.goalWidth
    app.goalBot = app.goalTop + app.goalHeight

def checkGoal(app):
    #checks if either player has touched the goal
    if app.aFinished == False:
        if (app.aCX + app.aRadius >= app.goalLeft and 
            app.aCX - app.aRadius <= app.goalRight):
            if app.aCY >= app.goalTop and app.aCY <= app.goalBot:
                app.aScore += 1
                app.aFinished = True
                app.currTurn = 1
    if app.bFinished == False:
        if (app.bCX + app.bRadius >= app.goalLeft and
            app.bCX - app.bRadius <= app.goalRight):
            if app.bCY >= app.goalTop and app.bCY <= app.goalBot:
                app.bScore +=1
                app.bFinished = True
                app.currTurn = 0

def playerProperties(app,A, B):
    #initializes the players' dimensions, statuses, and scores.
    app.dxA, app.dyA, app.dxB, app.dyB = 0, 0, 0, 0
    app.aCX = A[0]
    app.aCY = A[1]
    app.aRadius = A[2]
    app.bCX = B[0]
    app.bCY = B[1]
    app.bRadius = B[2]
    app.aStrokes = {}
    app.bStrokes = {}
    app.aFinished = False
    app.bFinished = False
    app.aDead = False
    app.bDead = False
    app.aStuck = False
    app.bStuck = False
    app.aStickList = []
    app.bStickList = []

def putt(app):
    #changes the initial dX and dy of the ball depending on angle and distance
    theta, power = getAngleAndPower(app.shootingLine)
    theta = (theta/180) * math.pi
    if app.currTurn == 0:
        app.dxA = math.cos(theta) * power/5
        app.dyA = math.sin(theta) * power/5
    if app.currTurn == 1:
        app.dxB = math.cos(theta) * power/5
        app.dyB = math.sin(theta) * power/5
        #print(theta, app.dxA, app.dyA)

def movePlayer(app):
    #moves the player after being putt or hit, also calls on naturalForces,
    #checkGoal, and collision.
    if not app.paused and app.IsMoving:
        app.aCX += app.dxA
        app.aCY -= app.dyA
        
        app.bCX += app.dxB
        app.bCY -= app.dyB
        
        if (app.dxA == 0 and app.dyA == 0) and (app.dxB == 0 and app.dyB == 0):
            app.IsMoving = False
        if (distance(app.aCX, app.aCY, app.bCX, app.bCY) <= 10 and 
            not (app.aFinished or app.bFinished)):
            if not (app.aDead or app.bDead):
                collision(app)
        naturalForces(app)
        checkGoal(app)
    
def startBetweenRound(app):
    #Starts the object picking process whenever it's applicable. When the player
    #selects an object, this also ends the process, updates the round, and
    #calls resetPos
     if (app.aFinished and app.bFinished or (app.aFinished and app.bDead) or
        (app.bFinished and app.aDead) or (app.aDead and app.bDead)):
        app.paused = True
        app.betweenRound = True
        if not app.selectedObj == None:
            app.round += 1
            app.paused = False
            app.betweenRound = False
            resetPos(app)

def collision(app):
    #Whenever the players collide, this switches their velocities with eachother
    Vx1 = app.dxA
    Vy1 = app.dyA
    Vx2 = app.dxB
    Vy2 = app.dyB
    
    app.dxA = Vx2
    app.dxB = Vx1
    app.dyA = Vy2
    app.dyB = Vy1

def naturalForces(app):
    #Adds gravitational forces and frictional forces to the game.
    if not app.aStuck:
        app.dyA -= app.gravity/15
        if app.aCY + app.aRadius >= 400:
            if app.steps %12 == 0:
                app.dxA *= (app.mu * app.mass)
                if abs(app.dxA) < 0.01:
                    app.dxA = 0
    
        if app.aCY + app.aRadius >= 400:
            app.dyA = -app.dyA * 0.4
            if app.dyA > -1 and app.dyA < 1:
                app.dyA = 0
    if not app.bStuck:
        app.dyB -= app.gravity/15
        if app.bCY + app.aRadius >= 400:
            if app.steps %12 == 0:
                app.dxB *= (app.mu * app.mass)
                if abs(app.dxB) < 0.01:
                    app.dxB = 0
        
        if app.bCY + app.bRadius >= 400:
            app.dyB = -app.dyB * 0.4
            if app.dyB > -1 and app.dyB < 1:
                app.dyB = 0

def border(app):
    #Stops both players from exiting the visible screen.
    if not app.paused and app.IsMoving:
        if app.aCX + app.aRadius >= 700:
            app.aCX = 695
            app.dxA = -app.dxA
        if app.aCX - app.aRadius <= 0:
            app.aCX = 5
            app.dxA = -app.dxA
        if app.aCY + app.aRadius >= 400:
            app.aCY = 395
        if app.aCY + app.aRadius <= 0:
            app.aCY = 5
            app.dyA = -app.dyA
            
        if app.bCX + app.bRadius >= 700:
            app.bCX = 695
            app.dxB = -app.dxB
        if app.bCX - app.bRadius <= 0:
            app.bCX = 5
            app.dxB = -app.dxB
        if app.bCY + app.bRadius >= 400:
            app.bCY = 395
        if app.bCY + app.bRadius <= 0:
            app.bCY = 5
            app.dyB = -app.dyB

def interactWithObject(app):
    #Runs through every placed obstacle and checks if the player has touched
    #that obstacle.
    if 'platform' in app.placedObstaclesX:
        platformDictX = app.placedObstaclesX['platform']
        platformDictY = app.placedObstaclesY['platform']
        for key in platformDictX:
            platform(app, platformDictX[key], platformDictY[key])
    
    if 'bounce' in app.placedObstaclesX:
        bounceDictX = app.placedObstaclesX['bounce']
        bounceDictY = app.placedObstaclesY['bounce']
        for key in bounceDictX:
            bounce(app, bounceDictX[key], bounceDictY[key])
    
    if 'stick' in app.placedObstaclesX:
        stickDictX = app.placedObstaclesX['stick']
        stickDictY = app.placedObstaclesY['stick']
        app.aStickList = []
        app.bStickList = []
        for key in stickDictX:
            stick(app, stickDictX[key], stickDictY[key])
            if len(app.aStickList) <1:
                app.aStuck = False
            if len(app.bStickList) <1:
                app.bStuck = False
    
    if 'death' in app.placedObstaclesX:
        deathDictX = app.placedObstaclesX['death']
        deathDictY = app.placedObstaclesY['death']
        for key in deathDictX:
            death(app, deathDictX[key], deathDictY[key])
            startBetweenRound(app)
    
def deletePlayerObstacles(app, x, y):
    #Called when the player wants to delete an obstacle. Runs through every
    #obstacle and checks if the delete obstacle is touching it. Then calls
    #delete.
    obj = 0
    for effect in app.placedObstaclesX:
        while obj < len(app.placedObstaclesX[effect]):
            setX = app.placedObstaclesX[effect][obj]
            setY = app.placedObstaclesY[effect][obj]
            if checkDelete(app, setX, setY, x, y):
                delete(app, app.placedObstaclesX[effect], 
                       app.placedObstaclesY[effect], obj,
                       app.playerObstacles[effect])
                obj -=1
            obj +=1
        obj = 0
    app.deleting = False

def delete(app, effectDictX, effectDictY, obj, shownDict):
    #Deletes the obstacle touching the delete object and resets the players'
    #stuck status.
    app.aStuck = False
    app.bStuck = False
    
    effectDictX[obj] = copy.copy(effectDictX[len(effectDictX)-1])
    effectDictX.pop(len(effectDictX)-1)
    effectDictY[obj] = copy.copy(effectDictY[len(effectDictY)-1])
    effectDictY.pop(len(effectDictY)-1)
    shownDict[obj] = copy.copy(shownDict[len(shownDict)-1])
    shownDict.pop(len(shownDict)-1)
    
    
    
def platform(app, setX, setY):
    #Whenever a player is touching the black, they will experience a platform:
    #in other words, they will phase through the bottom of the platform, and at
    #the top of the platform, they will be on solid ground.
    if (app.aCX + app.aRadius >= min(setX) and 
        app.aCX -app.aRadius <= max(setX)):
        if (app.aCY + app.aRadius >= min(setY) and
            app.aCY - app.aRadius <= max(setY)):
            if app.aCX <= min(setX) + app.dxA - app.aRadius:
                app.aCX = min(setX) - app.aRadius
                app.dxA = -app.dxA
            if app.aCX >= max(setX) + app.dxA + app.aRadius:
                app.aCX = max(setX) + app.aRadius
                app.dxA = -app.dxA
            if app.aCY <= min(setY) - app.dyA + app.aRadius:
                app.aCY = min(setY) - app.aRadius
                app.dyA = -app.dyA * 0.4
                if app.steps %4 == 0:
                    app.dxA *= (app.mu * app.mass)
                if abs(app.dxA) < 0.1:
                    app.dxA = 0
                if app.dyA > -1 and app.dyA < 1:
                    app.dyA = 0
    
    if (app.bCX + app.bRadius >= min(setX) and 
        app.bCX - app.bRadius <= max(setX)):
        if (app.bCY + app.bRadius >= min(setY) and
            app.bCY - app.bRadius <= max(setY)):
            if app.bCX <= min(setX) + app.dxB - app.bRadius:
                app.bCX = min(setX) - app.bRadius
                app.dxB = -app.dxB
            if app.bCX >= max(setX) + app.dxB + app.bRadius:
                app.bCX = max(setX) + app.bRadius
                app.dxB = -app.dxB
            if app.bCY <= min(setY) - app.dyB + app.bRadius:
                app.bCY = min(setY) - app.bRadius
                app.dyB = -app.dyB * 0.4
                if app.steps %4 == 0:
                    app.dxB *= (app.mu * app.mass)
                if abs(app.dxB) < 0.1:
                    #print(app.dxB)
                    app.dxB = 0
                if app.dyB > -1 and app.dyB < 1:
                    app.dyB = 0

def stick(app, setX, setY):
    #Whenever a player is touching the green block, they will be stuck onto it.
    if (app.aCX +app.aRadius >= min(setX) and
        app.aCX - app.aRadius <= max(setX)):
        if (app.aCY + app.aRadius >= min(setY) and
            app.aCY - app.aRadius <= max(setY)):
            app.aStuck = True
            app.aStickList.append([0])
            if app.aCX <= min(setX) + app.dxA - app.aRadius:
                app.aCX = min(setX) - app.aRadius
            if app.aCX >= max(setX) + app.dxA + app.aRadius:
                app.aCX = max(setX) + app.aRadius
            if app.aCY <= min(setY) - app.dyA + app.aRadius:
                app.aCY = min(setY) - app.aRadius
            if app.aCY >= max(setY) - app.dyA - app.aRadius:
                app.aCY = max(setY) + app.aRadius
            app.dyA = 0
            app.dxA = 0
    
    if (app.bCX +app.bRadius >= min(setX) and
        app.bCX - app.bRadius <= max(setX)):
        if (app.bCY + app.bRadius >= min(setY) and
            app.bCY - app.bRadius <= max(setY)):
            app.bStickList.append([0])
            app.bStuck = True
            if app.bCX <= min(setX) + app.dxB - app.bRadius:
                app.bCX = min(setX) - app.bRadius
                
            if app.bCX >= max(setX) + app.dxB + app.bRadius:
                app.bCX = max(setX) + app.bRadius
                
            if app.bCY <= min(setY) - app.dyB + app.bRadius:
                app.bCY = min(setY) - app.bRadius
                
            if app.bCY >= max(setY) - app.dyB - app.bRadius:
                app.bCY = max(setY) + app.bRadius
            app.dyB = 0
            app.dxB = 0

def death(app, setX, setY):
    #Checks if one of the players' balls is touching the red block. If the ball
    #is in range, the player is considered dead, and is exempt from the round.
    if not app.deleting:
        if (app.aCX + app.aRadius >= min(setX) and
            app.aCX - app.aRadius <= max(setX)):
            if (app.aCY + app.aRadius >= min(setY) and 
                app.aCY - app.aRadius <= max(setY)):
                app.aDead = True
                app.currTurn = 1
        
        if (app.bCX + app.bRadius >= min(setX) and
            app.bCX - app.bRadius <= max(setX)):
            if (app.bCY + app.bRadius >= min(setY) and
                app.bCY - app.bRadius <= max(setY)):
                app.bDead = True
                app.currTurn = 0

def bounce(app, setX, setY):
    #Whenever a player collides with the pink block, their velocity is placed in
    #the opposite direction and multiplied.
    if (app.aCX + app.aRadius >= min(setX) and
        app.aCX - app.aRadius <= max(setX)):
        if (app.aCY + app.aRadius >= min(setY) and
            app.aCY - app.aRadius <= max(setY)):
            if app.aCX <= min(setX) + app.dxA - app.aRadius:
                app.aCX = min(setX) - app.aRadius
                app.dxA = -app.dxA * 1.2
            if app.aCX >= max(setX) + app.dxA + app.aRadius:
                app.aCX = max(setX) + app.aRadius
                app.dxA = -app.dxA * 1.2
            if app.aCY <= min(setY) - app.dyA + app.aRadius:
                app.aCY = min(setY) - app.aRadius
                app.dyA = -app.dyA * 1.2
            if app.aCY >= max(setY) - app.dyA - app.aRadius:
                app.aCY = max(setY) + app.aRadius
                app.dyA = -app.dyA * 1.2
    
    if (app.bCX + app.bRadius >= min(setX) and
        app.bCX - app.bRadius <= max(setX)):
        if (app.bCY + app.bRadius >= min(setY) and
            app.bCY - app.bRadius <= max(setY)):
            if app.bCX <= min(setX) + app.dxB - app.bRadius:
                #print('x')
                app.bCX = min(setX) - app.bRadius
                app.dxB = -app.dxB * 1.2
            if app.bCX >= max(setX) + app.dxB + app.bRadius:
                app.bCX = max(setX) + app.bRadius
                app.dxB = -app.dxB * 1.2
            if app.bCY <= min(setY) - app.dyB + app.bRadius:
                app.bCY = min(setY) - app.bRadius
                app.dyB = -app.dyB * 1.2
            if app.bCY >= max(setY) - app.dyB - app.bRadius:
                app.bCY = max(setY) + app.bRadius
                app.dyB = -app.dyB * 1.2

def storeAndPlaceBlock(app, mouseX, mouseY):
    #After the player selects their mystery block, they are allowed to place it
    #down using this function. When the player clicks, they cement the block's
    #left, right, top, and bottom values into app.placedObstaclesX and
    #app.placedObstaclesRight, and the block will be visible there until
    #deletion or a different screen is toggled.
    if app.selectedObj!= None:
        app.selectedObj[1], app.selectedObj[2] = mouseX, mouseY
        effect = app.selectedObj[0]
        if effect != 'delete':
            left = app.selectedObj[1]
            top = app.selectedObj[2]
            right = left + app.selectedObj[3]
            bot = top + app.selectedObj[4]
            
            app.playerObstacles[effect] =app.playerObstacles.get(effect, dict())
            Length = len(app.playerObstacles[effect])
            app.playerObstacles[effect][Length] =copy.copy(app.selectedObj[1::])
            
            app.placedObstaclesX[effect]=app.placedObstaclesX.get(effect,dict())
            app.placedObstaclesY[effect]=app.placedObstaclesY.get(effect,dict())
            
            lengthX = len(app.placedObstaclesX[effect])
            lengthY = len(app.placedObstaclesY[effect])
            
            
            app.placedObstaclesX[effect][lengthX] = set([left, right])
            app.placedObstaclesY[effect][lengthY] = set([top, bot])
        else:
            app.deleting = True
            #print(app.selectedObj, app.deleting)
            deletePlayerObstacles(app, mouseX, mouseY)
            #print(app.placedObstaclesX)
            app.selectedObj = None
    app.selectedObj = None

def startShootingLine(app, mouseX, mouseY):
    #When the player wants to shoot, this signals their beginning and stores
    #where they began their click.
    if app.selectedObj == None and not app.InPlay:
        app.InPlay = True
        app.shootingLine = [mouseX, mouseY, None, None]

def selectObj(app, mouseX, mouseY):
    #This locates which object the player clicked on, and updates the value
    #app.selectedObj to that object.
    if app.betweenRound:
        #print('c')
        ObjectTop = app.mysteryTop
        ObjectBot = app.mysteryTop + app.mysteryHeight
        ObjectWidth = app.mysteryWidth
        Object1Left = app.mysteryLeft
        Object2Left = Object1Left + app.mysteryWidth + app.mysteryGap
        Object3Left = Object2Left +  app.mysteryWidth + app.mysteryGap
        #mystery objects
        if mouseY <= ObjectBot and mouseY >= ObjectTop:
            if mouseX >= Object1Left and mouseX <= (Object1Left + ObjectWidth):
                app.selectedObj = copy.copy(app.object1)
            if mouseX >= Object2Left and mouseX <= (Object2Left + ObjectWidth):
                app.selectedObj = copy.copy(app.object2)
            if mouseX >= Object3Left and mouseX <= (Object3Left + ObjectWidth):
                app.selectedObj = copy.copy(app.object3)
        #delete playerObject
        Left = app.deleteObj[1] - 25
        Top = app.deleteObj[2] - 25
        Right = app.deleteObj[1] + app.deleteObj[3]/2
        Bot = app.deleteObj[2] + app.deleteObj[4]/2
        #print(Left, Top, Right, Bot)
        if mouseY <= Bot and mouseY >= Top:
            if mouseX >= Left and mouseX <= Right:
                app.selectedObj = copy.copy(app.deleteObj)

def dragShootingLine(app,mouseX, mouseY):
    #Updates the other endpoint of the shooting line.
    if not app.paused:
        if (app.InPlay):
            if (distance(app.shootingLine[0], app.shootingLine[1], 
                                                        mouseX, mouseY) <= 100):
                app.shootingLine[2], app.shootingLine[3] = mouseX, mouseY
            else:
                theta, power = getAngleAndPower([app.shootingLine[0], 
                                app.shootingLine[1], mouseX, mouseY])
                theta = -(theta/180) * math.pi
                xEndpoint = app.shootingLine[0] - math.cos(theta) * 100
                yEndpoint = app.shootingLine[1] - math.sin(theta) * 100
                app.shootingLine[2], app.shootingLine[3] = xEndpoint, yEndpoint

def strike(app, mouseX, mouseY):
    #This releases the shot which putts the ball, updates the turn and strokes
    #of the players, signals the start of movement, and signals the end to the
    #shooting line.
    if app.shootingLine[3] != None and not app.paused:
        putt(app)
        app.shootingLine = [None, None, None, None]
        app.IsMoving = True
        if app.currTurn == 0: 
            app.aStrokes[app.round] = app.aStrokes.get(app.round, 0) + 1
            if not app.bFinished and not app.bDead: app.currTurn = 1
        else:
            app.bStrokes[app.round] = app.bStrokes.get(app.round, 0) + 1
            if not app.aFinished and not app.aDead: app.currTurn = 0
    app.InPlay = False
def takeStep(app):
    #Each time its called in onStep, takeStep calls createObject,
    #startBetweenRound, movePlayer, border, and interact with object.
    createObject(app)
    startBetweenRound(app)
    if not app.paused:
        app.steps += 1
        if app.IsMoving:
            movePlayer(app)
            border(app)
        interactWithObject(app)
def showScreen(app, key):
    #Whenever the player presses the keys 'tab' or 'p', this function pauses the
    #game and enables a screen which shows the stats of each player. These stats
    #show the amount of times each player has scored and the amount of strokes
    #each player has made. Alternatively, when the player presses 'H' or 'I',
    #this function also pauses the game; however, it shows an instruction screen
    #instead.
    if key == 'tab' or key == 'p':
        app.currPage = 1
        app.showingHelp = False
        app.showingStats = not app.showingStats
        app.paused = app.showingStats or app.betweenRound
    
    if key == 'i' or key == 'h':
        app.currPage = 1
        app.showingStats = False
        app.showingHelp = not app.showingHelp
        app.paused = app.showingStats or app.betweenRound
    
def moveSelectedObj(app, mouseX, mouseY):
    #Changes the left and top of the selected object to match the location of
    #the player's mouse.
    if app.selectedObj != None:
        app.selectedObj[1], app.selectedObj[2] = mouseX, mouseY

def changePage(app, mouseX, mouseY):
    #Changes the shown instruction page depending on if the player clicks on
    #the next button or the previous button.
    if app.showingHelp and app.currPage <= 3:
        print(3)
        if (mouseX <= 663 and mouseX >= 537):
            if(mouseY >= 325 and mouseY <= 375):
                app.currPage += 1
            if app.currPage > 3:
                showScreen(app, 'h')
        
    if app.showingHelp and app.currPage > 1:
        print(3)
        if (mouseX <= 163 and mouseX >= 37):
            if(mouseY >= 325 and mouseY <= 375):
                app.currPage -= 1
# main function
def main():
    runApp(700, 400)

# events
def onMousePress(app, mouseX, mouseY):
    #Whenever the mouse is pressed, this calls startShootngLine,
    #storeAndPlaceBlock, and selectObj.
    storeAndPlaceBlock(app, mouseX, mouseY)
    startShootingLine(app, mouseX, mouseY)
    selectObj(app, mouseX, mouseY)
    changePage(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    #Whenever the mouse is held down and moved, this calls dragShootingLine
    dragShootingLine(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    #Whenver the mouse is released, this calls strike
    strike(app, mouseX, mouseY)

def onKeyPress(app, key):
    #Depending on which key is pressed, this event has different effects: if the
    #key pressed is a digit, the event will change the location of the goal, but
    #if the key pressed is tab or p, the event will show the stats of the two
    #players.
    selectMap(app, key)
    key = key.lower()
    showScreen(app, key)
    
def onStep(app):
    #Continuously calls takeStep throughout the entire game
    takeStep(app)
    
def onMouseMove(app, mouseX, mouseY):
    #Whenever the mouse moves, this calls moveSelectedObj
    moveSelectedObj(app, mouseX, mouseY)
main()
