#############################
# Term Project (8 Ball Pool)  
# By: Sebastian Andreu
# andrew id: sandreu
#############################
import math, copy, random, time
from cmu_112_graphics import *
from PIL import Image

class Ball(object):
    def __init__(self, cx, cy, speed, angle, color, player):
        self.cx = cx #center x cordinate of ball
        self.cy = cy #center y cordinate of ball
        self.speed = speed
        self.angle = angle
        self.radius = 10
        self.color = color
        self.player = player
    
    def moveBalls(self):
        margin = 50
        width = 800
        height = 500
        friction = 0.2 #rate to slow down balls linearly with friction
        #self.speed -= friction
        self.speed *= 0.985 #feels more realistic than friction
        if self.speed <= 0.2:
            self.speed = 0
        self.cx += self.speed * math.cos(math.radians(self.angle))
        self.cy += self.speed * math.sin(math.radians(self.angle))
        cx, cy = self.cx, self.cy
        r = self.radius
        if cx - r <= (margin*2):
            self.cx = margin*2 + r
            self.angle = 180 - self.angle 
        elif cx + r >= (width - (margin*2)):
            self.cx = width - (margin*2) - r
            self.angle = 180 - self.angle 
        elif cy - r <= (margin*2):
            self.cy = margin*2 + r
            self.angle = 360 - self.angle
        elif cy + r >= (height - (margin*2)):
            self.cy = height - (margin*2) - r
            self.angle = 360 - self.angle

class Pocket(object):
    def __init__(self, code, cx, cy):
        self.code = code
        self.cx = cx
        self.cy = cy
        self.radius = 20

def newBalls():
    balls = []
    cueBall = Ball(250, 250, 0, 0, 'white', 0)
    eightBall = Ball(510, 250, 0, 0, 'black', 0) #col 2
    b1 = Ball(460, 250, 0, 0, 'red', 1) #leading ball col 0
    b2 = Ball(485, 265, 0, 0, 'blue', 2) # col 1 
    b3 = Ball(485, 235, 0, 0, 'red', 1) #col 1
    b4 = Ball(510, 280, 0, 0, 'blue', 2) #col 2
    b5 = Ball(510, 220, 0, 0, 'red', 1) #col 2
    b6 = Ball(535, 265, 0, 0, 'blue', 2) #col 3
    b7 = Ball(535, 235, 0, 0, 'red', 1) #col 3
    b8 = Ball(535, 295, 0, 0, 'blue', 2) #col 3
    b9 = Ball(535, 205, 0, 0, 'red', 1) #col 3
    b10 = Ball(560, 250, 0, 0, 'blue', 2) #col 4
    balls.append(cueBall)
    balls.append(eightBall)
    balls.append(b1)
    balls.append(b2)
    balls.append(b3)
    balls.append(b4)
    balls.append(b5)
    balls.append(b6)
    balls.append(b7)
    balls.append(b8)
    balls.append(b9)
    balls.append(b10)
    return balls

def makePockets():
    pockets = []
    margin = 50
    width = 800
    height = 500
    p1 = Pocket('tl', 2*margin, 2*margin) #top left
    p2 = Pocket('tm', (width - (4*margin))/2 + 2*margin, 2*margin) #top middle
    p3 = Pocket('tr', width - (2*margin), 2*margin) #top right
    p4 = Pocket('bl', 2*margin, height - (2*margin)) #bottom left
    p5 = Pocket('tp', (width - (4*margin))/2 + 2*margin, height - (2*margin)) #bottom middle
    p6 = Pocket('tp', width - (2*margin), height - (2*margin)) #bottom right
    pockets.append(p1)
    pockets.append(p2)
    pockets.append(p3)
    pockets.append(p4)
    pockets.append(p5)
    pockets.append(p6)
    return pockets

def appStarted(app):
    app.margin = 50
    app.balls = newBalls()
    app.pockets = makePockets()
    app.time0 = time.time()
    app.time1 = time.time()
    app.ballsGone = []
    app.cueX0 = app.cueY0 = app.cueX1 = app.cueY1 = None
    app.aimAngle = app.aimX0 = app.aimY0 = app.aimX1 = app.aimY1 = None #prediction/aim bar points
    app.ballHit = None #ball the ray casting hits
    app.cueForce = None
    app.angle = None
    app.timerDelay = 1
    app.playerTurn = 1 #what player's turn it is 
    app.playerColor = 'red' #player 0 -> red and 
    app.gameOver = False
    app.winner = None
    app.predictionAngle = None
    app.predictionCX = None
    app.predictionCY = None
    app.aIDifficulty = 1 #difficuty for AI
    app.difficultyScreen = False
    app.singlePlayerMode = False
    app.multiPlayerMode = False
    app.skillChallengeMode = False
    app.score = 0 #score for skill challenge

    app.startScreen = True #first page
    app.instructions = False
    app.leaderboardScreen = False

#help test out code by manually moving the first ball
def keyPressed(app, event):
    if event.key == 'i':
        if app.instructions == False:
            app.instructions = True
        else:
            app.instructions = False
    if app.skillChallengeMode == True:
        if event.key == 'l':
            if app.leaderboardScreen == False:
                app.leaderboardScreen = True
            else:
                app.leaderboardScreen = False
    if len(app.balls) > 0:
        if event.key == 'Up':
            app.balls[0].angle += 10
        elif event.key == 'Down':
            app.balls[0].angle -= 10
        elif event.key == 'Right':
            app.balls[0].speed += 5
        elif event.key == 'Left':
            app.balls[0].speed -= 5
        elif event.key == 'r': #restart game with r
            appStarted(app)

def findBallHitCenter(app, x, y):
    for ball in app.balls:
        x0, y0 = ball.cx, ball.cy
        distance = math.sqrt((x-x0)**2 + (y-y0)**2)
        if distance <= ball.radius:
            return (x0, y0) #returns center of ball cue stick lies on
    return (None, None)

def mousePressed(app, event):
    if app.instructions == True or app.leaderboardScreen == True: return
    if app.startScreen == True:
        x, y = event.x, event.y
        h = app.height/10
        w = app.width/10
        if y >= app.height*3/4 and y <= app.height*3/4 + h:
            if x >= app.width/4 - w and x <= app.width/4 + w: 
                app.startScreen = False
                app.difficultyScreen = True
            elif x >= app.width/2 - w and x <= app.width/2 + w:
                app.multiPlayerMode = True
                app.startScreen = False
            elif x >= app.width*3/4 - w and x <= app.width*3/4 + w:
                app.skillChallengeMode = True
                app.startScreen = False
    if app.difficultyScreen == True: #difficulty screen
        x, y = event.x, event.y
        h = app.height/10
        w = app.width/10
        if y >= app.height*1/2 and y <= app.height*1/2 + h:
            if x >= app.width/4 - w and x <= app.width/4 + w: 
                app.singlePlayerMode = True
                app.aIDifficulty = 3
                app.difficultyScreen = False
            elif x >= app.width/2 - w and x <= app.width/2 + w:
                app.singlePlayerMode = True
                app.aIDifficulty = 2
                app.difficultyScreen = False
            elif x >= app.width*3/4 - w and x <= app.width*3/4 + w:
                app.singlePlayerMode = True
                app.aIDifficulty = 1
                app.difficultyScreen = False
    if app.startScreen == False and app.difficultyScreen == False:
        app.cueX0, app.cueY0 = event.x, event.y
        cx, cy = findBallHitCenter(app, app.cueX0, app.cueY0)
        app.aimX0, app.aimY0, app.aimX1, app.aimY1 = cx, cy, cx, cy #both start at same spot 
 
                                                                #and second point does ray casting
def mouseDragged(app, event):
    if app.startScreen == True or app.instructions == True or app.difficultyScreen == True or app.leaderboardScreen == True:
        return
    app.cueX1, app.cueY1 = event.x, event.y
    for ball in app.balls:
        x0, y0 = ball.cx, ball.cy
        x1, y1 = app.cueX0, app.cueY0
        distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        if distance <= ball.radius:
            rise = app.cueY1 - app.cueY0 #find slope rise/run
            run = app.cueX1 - app.cueX0
            if run == 0 and rise > 0: #can't have 0 in demominator
                angle = 270
            elif run == 0 and rise < 0:
                angle = 90
            elif run < 0: #left two quadrants (tan can only do angles in 1&4)
                angle = math.degrees(math.atan(rise/run)) + 360
            elif run != 0:
                angle = math.degrees(math.atan(rise/run)) + 180
            else: # if shot distance (run) = 0
                angle = app.angle
            app.angle = angle
            app.aimAngle = angle #aim angle
            x2, y2 = app.cueX1, app.cueY1
            power = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            app.cueForce = min((power)/9, 30) #limit the force

def mouseReleased(app, event):
    if app.startScreen == True or app.instructions == True or app.difficultyScreen == True or app.leaderboardScreen == True:
        return
    for ball in app.balls:
        x0, y0 = ball.cx, ball.cy
        x1, y1 = app.cueX0, app.cueY0
        distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        if distance <= ball.radius:
            if app.cueForce != None:
                ball.speed += app.cueForce
                ball.angle = app.angle
            if app.playerTurn == 1:
                app.playerTurn = 2
                app.playerColor = 'blue'
            else:
                app.playerTurn = 1
                app.playerColor = 'red'
    app.cueX0 = app.cueY0 = app.cueX1 = app.cueY1 = None
    app.aimAngle = app.aimX0 = app.aimY0 = app.aimX1 = app.aimY1 = None
    app.ballHit = None
    app.predictionAngle = app.predictionCX = app.predictionCY = None   

def outOfBounds(app, x, y):
    bound = app.margin * 2
    if x <= bound or x >= app.width - bound or y <= bound or y >= app.height - bound:
        return True
    return False

def playerAim(app):
    if app.aimX0 == None or app.aimX1 == None or app.aimAngle == None:
        return
    angle = int(app.aimAngle)
    radius = 10 #radius of balls
    x0, y0 = app.aimX0, app.aimY0
    shortestLength = 800 #arbitrary large distance that will be beaten
    bestBallHit = None
    bestX, bestY = None, None
    for dtheta in range(angle - 90, angle + 91, 9): #ray casting 10 rays from different positions
        startX = x0 + (radius/2 * math.cos(math.radians(dtheta))) #for more accurate aiming
        startY = y0 + (radius/2 * math.sin(math.radians(dtheta)))
        x2, y2 = startX, startY
        hit = False
        while hit == False:
            x2 += math.cos(math.radians(angle)) * 0.5
            y2 += math.sin(math.radians(angle)) * 0.5
            if outOfBounds(app, x2, y2) == True:
                #print(f'border hit')
                hit = True
                bestBallHit = None
                length = math.sqrt((x2-startX)**2 + (y2-startY)**2)
                if length <= shortestLength:
                    shortestLength = length
                    bestX = x2 - math.cos(math.radians(angle)) #backtrack to last shot
                    bestY = y2 - math.sin(math.radians(angle))
                    app.ballHit = None
            for ball in app.balls:
                cx, cy = ball.cx, ball.cy 
                distance = math.sqrt((cx-x2)**2 + (cy-y2)**2)
                if distance <= ball.radius and ball.color != 'white':
                    hit = True
                    bestBallHit = ball
                    #print('hit')
                    length = math.sqrt((x2-startX)**2 + (y2-startY)**2)
                    if length <= shortestLength:
                        shortestLength = length
                        bestX = x2 - math.cos(math.radians(angle)) #backtrack to last shot
                        bestY = y2 - math.sin(math.radians(angle))
                        app.ballHit = bestBallHit
    app.aimX1 = bestX
    app.aimY1 = bestY

#idea from Iphone messages 8 ball game where it predicts where cue ball will go
def predictionShot(app):
    if app.aimX1 == None or app.ballHit == None: #avoid crashes
        return
    x0, y0 = app.aimX1, app.aimY1
    x1, y1 = app.ballHit.cx, app.ballHit.cy
    ux, uy = (x1 - x0), (y1 - y0)
    if ux == 0 or uy == 0:
        return
    un = [(ux) / (math.sqrt(ux**2 + uy**2)), 
            (uy) / (math.sqrt(ux**2 + uy**2))] #unit normal
    ut = [-1 * un[1], un[0]] #unit tanget X and Y
    if un[0] == 0: #can not devide by 0
        angle = 90
    else:
        angle = math.degrees(math.atan2(un[1], un[0])) #find angles with atan2
    if angle < 0: #in case angle is negative
        angle += 360
    app.predictionAngle = angle
    app.predictionCX = app.ballHit.cx
    app.predictionCY = app.ballHit.cy

# https://imada.sdu.dk/~rolf/Edu/DM815/E10/2dcollisions.pdf
def ballCollide(app):
    for ball0 in app.balls:
        for ball1 in app.balls:
            if ball0 == ball1:
                continue
            x0, y0, v0, angle0 = ball0.cx, ball0.cy, ball0.speed, ball0.angle
            x1, y1, v1, angle1 = ball1.cx, ball1.cy, ball1.speed, ball1.angle
            distance = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            if distance <= ball0.radius * 2:
                ux, uy = (x1 - x0), (y1 - y0)
                un = [(ux) / (math.sqrt(ux**2 + uy**2)), 
                        (uy) / (math.sqrt(ux**2 + uy**2))] #unit normal
                ut = [-1 * un[1], un[0]] #unit tanget X and Y
                v0 = [v0*math.cos(math.radians(angle0)), v0*math.sin(math.radians(angle0))]
                v1 = [v1*math.cos(math.radians(angle1)), v1*math.sin(math.radians(angle1))]
                
                v0n = v0[0] * un[0] + v0[1] * un[1] #v0 normal velocity vector
                v1n = v1[0] * un[0] + v1[1] * un[1]
                v0t = v0[0] * ut[0] + v0[1] * ut[1] #v0 tangent velocity vector
                v1t = v1[0] * ut[0] + v1[1] * ut[1]

                fv0n = v1n #normal velocities switch
                fv1n = v0n 
                fv0t = v0t #tangent velocities stay the same
                fv1t = v1t

                fv0n = [fv0n * un[0], fv0n * un[1]] #find velocities in direction
                fv1n = [fv1n * un[0], fv1n * un[1]] #of normal and tangent
                fv0t = [fv0t * ut[0], fv0t * ut[1]]
                fv1t = [fv1t * ut[0], fv1t * ut[1]]

                fv0 = [fv0n[0] + fv0t[0], fv0n[1] + fv0t[1]] #final velocity 0 vector
                fv1 = [fv1n[0] + fv1t[0], fv1n[1] + fv1t[1]] #final velocity 1 vector
                
                angle0 = math.degrees(math.atan2(fv0[1], fv0[0])) #find angles with atan2
                angle1 = math.degrees(math.atan2(fv1[1], fv1[0]))
                if angle0 < 0: #in case angle is negative
                    angle0 += 360
                elif angle1 < 0:
                    angle1 += 360

                v0 = math.sqrt(fv0[0]**2 + fv0[1]**2) #magnitude of new speeds
                v1 = math.sqrt(fv1[0]**2 + fv1[1]**2)

                ball0.angle = angle0 #assign new angles
                ball1.angle = angle1

                ball0.speed = v0 #assign speeds
                ball1.speed = v1

                ball0.cx += (ball0.speed)*math.cos(math.radians(angle0)) #move balls
                ball0.cy += (ball0.speed)*math.sin(math.radians(angle0))
                ball1.cx += (ball1.speed)*math.cos(math.radians(angle1))
                ball1.cy += (ball1.speed)*math.sin(math.radians(angle1))

def checkBallInPocket(app):
    for ball in app.balls:
        bx, by = ball.cx, ball.cy
        for pocket in app.pockets:
            pocketRadius = pocket.radius
            px, py = pocket.cx, pocket.cy
            distance = math.sqrt((px-bx)**2 + (py-by)**2)
            if distance <= pocketRadius:
                if app.playerTurn == 1: #know who just got the eightball in
                    player = 2
                    playerColor = 'blue'
                    otherPlayer = 1
                else:   
                    player = 1
                    playerColor = 'red'
                    otherPlayer = 2
                if player == ball.player:
                    app.playerTurn = player #player turn continues since he got a ball in
                    app.playerColor = playerColor
                if ball.color == 'white': 
                    ball.cx = ball.cy = 250
                    ball.speed = ball.angle = 0
                    break
                elif ball.color == 'black' and app.skillChallengeMode == False: #check who won
                    app.gameOver = True
                    count = 0
                    for ballGone in app.ballsGone:
                        if ballGone.player == player:
                            count += 1
                    if count == 5:
                        app.winner = player
                    else:   
                        app.winner = otherPlayer
                if app.skillChallengeMode == True:
                    if ball.color != 'red':
                        app.score += 500
                app.ballsGone.append(ball)
                app.balls.remove(ball)
    if app.skillChallengeMode == True:
        r = 0
        for ballScored in app.ballsGone:
            if ballScored.color == 'red':
                r += 1
        if r == 5:
            app.gameOver = True
            leaderboard(app)       

#https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def leaderboard(app):
    contentsRead = readFile("skillChallenge-leaderboard.txt")
    leaderboard = contentsRead.split('\n')
    leaderboard += [str(app.score)]
    score1 = 10000 #arbitrary scores that will be beaten
    score2 = 10000
    score3 = 10000
    score4 = 10000
    score5 = 10000
    for score in leaderboard:
        if score == '':
            continue
        if int(score) <= int(score1):
            score5, score4, score3, score2, score1 = score4, score3, score2, score1, score #bring down scores
        elif int(score) <= int(score2):
            score5, score4, score3, score2 = score4, score3, score2, score
        elif int(score) <= int(score3):
            score5, score4, score3 = score4, score3, score
        elif int(score) <= int(score4):
            score5, score4 = score4, score
        elif int(score) <= int(score5):
            score5 = score
    contentToWrite = score1 + '\n' + score2 + '\n' + score3 + '\n' + score4 + '\n' + score5
    writeFile("skillChallenge-leaderboard.txt", contentToWrite)

def timerFired(app):
    if app.gameOver == True: return
    for ball in app.balls:
        ball.moveBalls()
    if app.playerTurn == 2 and app.singlePlayerMode == True:
        ballsMoving = False
        for ball1 in app.balls:
            if ball1.speed != 0:
                ballsMoving = True
        if ballsMoving == False:
            computerTurn(app)
            app.playerTurn = 1
    playerAim(app)
    predictionShot(app)
    ballCollide(app)
    checkBallInPocket(app)
    if app.skillChallengeMode == True:
        if (time.time() - app.time1) >= 3:
            app.score += 100
            app.time1 = time.time()

###################################
##### AI for Single-Player Mode
###################################

def computerTurn(app): #main AI function
    (bestShotAngle, bestShotDistance) = computerTurnHelper(app, 0, bestShotDelta=360, bestShotAngle=0, bestShotDistance = 100) #recursive fucntion
    if bestShotDistance <= 70:
        bestShotDistance = 100
    for ball in app.balls:
        if ball.color == 'white':
            cueForce = bestShotDistance/10
            ball.speed += cueForce
            ball.angle = bestShotAngle
            app.playerTurn = 1
            app.playerColor = 'red'


def computerTurnHelper(app, angle, bestShotDelta, bestShotAngle, bestShotDistance): #wrap recursive functio
    if angle >= 360: #base case (if it has checked every angle from 0->360)
        return (bestShotAngle, bestShotDistance) #, bestShotDelta
    else: 
        ballHit, cueBall, x, y = shotHitsBall(app, angle)
        if ballHit != None: #check if angle hits a ball
            if bestShotAngle == 0 and ballHit.color == 'blue':#make sure ball at least hits a ball
                bestShotAngle = angle
            elif bestShotAngle == 0 and ballHit.color == 'black': #no more blue balls
                bestShotAngle = angle
            if correctBall(app, ballHit) == True: #check that that ball is player 2's, which is the AI
                (delta, distance) = predictionShotHitsPocket(app, angle, ballHit, cueBall, x, y)
                if delta != None: #if prediction hits pocket
                    if delta <= bestShotDelta: #compare with best shot, depending on shot angle
                        bestShotDelta = delta
                        bestShotAngle = angle
                        bestShotDistance = distance
        (bestShotAngle, bestShotDistance) = computerTurnHelper(app, angle + app.aIDifficulty, bestShotDelta, bestShotAngle, bestShotDistance)
    return (bestShotAngle, bestShotDistance) #returns best shot angle and distance it has to travel (for cue stick Force)

def shotHitsBall(app, angle): #helper for computer turn
    radius = 10 #radius of balls
    for cueBall in app.balls: #looks for cordinates of cueBall
        if cueBall.color == 'white':
            x0, y0 = cueBall.cx, cueBall.cy
    x1, y1 = x0, y0
    shortestLength = 800 #arbitrary large distance that will be beaten
    bestBallHit = None
    bestX, bestY = None, None
    for dtheta in range(angle - 90, angle + 91, 36): #ray casting 10 rays from different positions
        startX = x0 + (radius/2 * math.cos(math.radians(dtheta))) #for more accurate aiming
        startY = y0 + (radius/2 * math.sin(math.radians(dtheta)))
        x2, y2 = startX, startY
        hit = False
        while hit == False:
            x2 += math.cos(math.radians(angle)) 
            y2 += math.sin(math.radians(angle)) 
            if outOfBounds(app, x2, y2) == True:
                hit = True
                length = math.sqrt((x2-startX)**2 + (y2-startY)**2)
                if length <= shortestLength:
                    shortestLength = length
                    bestX = x2 - math.cos(math.radians(angle)) #backtrack to last shot
                    bestY = y2 - math.sin(math.radians(angle))
                    bestBallHit = None
            for ball in app.balls:
                cx, cy = ball.cx, ball.cy 
                distance = math.sqrt((cx-x2)**2 + (cy-y2)**2)
                if distance <= ball.radius and ball.color != 'white':
                    hit = True
                    length = math.sqrt((x2-startX)**2 + (y2-startY)**2)
                    if length <= shortestLength:
                        shortestLength = length
                        bestX = x2 - math.cos(math.radians(angle)) #backtrack to last shot
                        bestY = y2 - math.sin(math.radians(angle))
                        bestBallHit = ball
    return (bestBallHit, cueBall, bestX, bestY)

def correctBall(app, ball): #helper for computer turn
    count = 0
    for ballGone in app.ballsGone: #if AI has scored all the balls
        if ballGone.color == 'blue':
            count += 1
    if count == 5:
        if ball.color == 'black':
            return True
    if ball.color == 'white' or ball.color == 'black':
        return False
    elif ball.player == 1 or ball.player == 0:
        return False
    return True #ball.player == 2 and is blue

def predictionShotHitsPocket(app, angle, ballHit, cueBall, x, y): #helper for computer turn
    x0, y0 = x, y
    x1, y1 = ballHit.cx, ballHit.cy
    ux, uy = (x1 - x0), (y1 - y0)
    un = [(ux) / (math.sqrt(ux**2 + uy**2)), 
            (uy) / (math.sqrt(ux**2 + uy**2))] #unit normal
    angle1 = math.degrees(math.atan2(un[1], un[0])) #find angles with atan2
    if angle1 < 0: #in case angle is negative
        angle1 += 360
    x2, y2 = x1, y1 #raycasting for computer
    hit = False
    while hit == False:
        x2 += math.cos(math.radians(angle1)) 
        y2 += math.sin(math.radians(angle1)) 
        if outOfBounds(app, x2, y2) == True:
            return (None, None) #if ray casting hits border, return None
        for pocket in app.pockets:
            cx, cy = pocket.cx, pocket.cy
            distance = math.sqrt((cx-x2)**2 + (cy-y2)**2)
            if distance <= pocket.radius:
                difference = math.fabs(angle - angle1)
                distance = math.sqrt((x2 - x1)**2 + (y2-y1)**2)
                return (difference, distance) #if prediction shot hits pocket, return true

def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'lightGreen')
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin,
                            app.height - app.margin, fill = 'brown')
    canvas.create_rectangle(app.margin*2, app.margin*2, 
                            app.width - (app.margin*2),
                            app.height - (app.margin*2), fill = 'green')

def drawBalls(app, canvas):
    for ball in app.balls:
        x, y = ball.cx, ball.cy
        r = ball.radius
        color = ball.color
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = color)

def drawPockets(app, canvas):
    for pocket in app.pockets:
        x, y = pocket.cx, pocket.cy
        r = pocket.radius
        color = 'black'
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = color)

def drawAddOns(app, canvas):
    time1 = int(time.time() - app.time0)
    canvas.create_text(app.width-200, app.margin/2, text=f'Time: {time1}s', 
                        font= 'Ariel 20 bold')
    canvas.create_text(200, app.margin/2, text='Balls Scored:', 
                        font= 'Ariel 20 bold', anchor= 'e')
    index = 0
    startX = 200 + 30
    for ball in app.ballsGone:
        x, y = startX + index, app.margin/2
        r = 10
        color = ball.color
        canvas.create_oval(x - r, y - r, x + r, y + r, fill = color)
        index += 30
    if app.skillChallengeMode == True:
        canvas.create_text(270, app.height - app.margin/2 , 
            text='Press "r" to restart, "i" for instructions, and "l" for the leaderboard', 
            font= 'Ariel 15 bold')
    else:
        canvas.create_text(250, app.height - app.margin/2 , 
                        text='Press "r" to restart and "i" for instructions', 
                        font= 'Ariel 20 bold')
    if app.skillChallengeMode == True:
        canvas.create_text(600, app.height - app.margin/2 , fill='grey', 
                        text=f'Score: {app.score}', 
                        font= 'Ariel 25 bold')
    else:
        canvas.create_text(600, app.height - app.margin/2 , fill=app.playerColor, 
                        text=f'Player {app.playerTurn}\'s turn', 
                        font= 'Ariel 25 bold')

def drawCue(app, canvas):
    if app.cueX0 != None and app.cueX1 != None:
        x0, y0 = app.cueX0, app.cueY0
        x1, y1 = app.cueX1, app.cueY1
        canvas.create_line(x0, y0, x1, y1, fill='black', width= 4)

def drawAim(app, canvas):
    if app.aimX0 != None and app.aimAngle != None and app.aimX1 != None:
        length = 30
        x0, y0 = app.aimX0, app.aimY0
        x1, y1 = app.aimX1, app.aimY1
        canvas.create_line(x0, y0, x1, y1, fill='red', width= 2)

def drawPrediction(app, canvas):
    if app.aimX1 != None and app.ballHit != None and app.predictionAngle != None:
        length = app.cueForce * 5 #length of bar
        x0, y0 = app.predictionCX, app.predictionCY
        x1 = x0 + math.cos(math.radians(app.predictionAngle)) * length
        y1 = y0 + math.sin(math.radians(app.predictionAngle)) * length
        canvas.create_line(x0, y0, x1, y1, fill='red', width= 2)

def drawDifficultyMenu(app, canvas):
    #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.smithsonianmag.com%2Fsmart-news%2Fonce-upon-time-exploding-billiard-balls-were-everyday-thing-180962751%2F&psig=AOvVaw3T10hwE_xWHHQ1n7jecTsH&ust=1620207097005000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCPDD6vrbr_ACFQAAAAAdAAAAABAD
    startScreen = Image.open('difficulty-screen.png')
    newScreen = startScreen.resize((app.width, app.height))
    canvas.create_image(app.width/2, app.height/2, 
                    image= ImageTk.PhotoImage(newScreen))
    #canvas.create_rectangle(0, 0, app.width, app.height, fill = 'lightGreen')
    canvas.create_text(app.width/2, app.height/5, text= 'Choose AI difficulty',
                font = 'Ariel 50 bold', fill= 'white')
    y = app.height * (1/2)
    h = app.height/10 #height of boxes
    width = app.width/10 #half the total width
    startX = app.width/4
    incX = app.width/4
    canvas.create_rectangle(startX - width, y, 
            startX + width, y + h, fill = 'white') #first box
    canvas.create_rectangle(startX - width + incX, y, 
            startX + width + incX, y + h, fill = 'white') #second box
    canvas.create_rectangle(startX - width + 2*incX, y, 
            startX + width + 2* incX, y + h, fill = 'white') #third box
    canvas.create_text(startX, y + h/2, text= 'Easy',
            font = 'Ariel 15 bold', fill= 'black')
    canvas.create_text(startX + incX, y + h/2, text= 'Medium',
            font = 'Ariel 15 bold', fill= 'black')
    canvas.create_text(startX + 2*incX, y + h/2, text= 'Hard',
            font = 'Ariel 15 bold', fill= 'black')   

#https://www.colorado.edu/umc/sites/default/files/attached-files/8-ball_rules_bca.pdf
def drawInstructions(app, canvas):
    if not app.instructions: return
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'yellow') #white background
    instructions = [
        "Eight Ball is a call shot game played with a cue ball and object balls",
        "Player 1 must pocket the 'red' balls while the other player has to pocket the 'blue' balls.", 
        "To shoot, click on the cue ball and drag the mouse back while aiming. Release to shoot!",
        "",
        "THE PLAYER POCKETING HIS GROUP FIRST AND ",
        "THEN LEGALLY POCKETING THE 8-BALL WINS THE GAME",
        "",
        "Single-Player Mode:",
        "You are player 1 who is assigned the red balls",
        "The AI is player 2 who is assigned the blue balls",
        "",
        "Multi-Player Mode:",
        "Assign a player to 'player 1' who has to pocket the red balls",
        "and the other player to 'player 2' who has to pocket the blue balls",
        "",
        "Skill Challenge Mode:",
        "Get all the red balls in the pockets in the shortest time possible",
        "Every other ball scored is a penalty which adds to your score",
        "The lower the score, the better",
        "",
        "",
        "Click 'i' to go back to game! Thanks",
        "Or 'r' to restart game"
        ]   
    inc = 0
    for line in instructions:
        inc += 18 #spaces between new lines
        canvas.create_text(app.width/2, app.height/20 + inc, text = line,
                                    font = 'Ariel 15 bold')

def drawGameOver(app, canvas):
    if app.gameOver and app.skillChallengeMode == False:
        canvas.create_text(app.width/2, app.height/2, 
            text = f'Game Over!! Player {app.winner} wins!!!',
            font = 'Ariel 30 bold', fill= 'gold')
    elif app.gameOver and app.skillChallengeMode == True:
        canvas.create_text(app.width/2, app.height/2, 
            text = f'Game Over!! Score = {app.score}!!!',
            font = 'Ariel 30 bold', fill= 'gold')
        
def startScreen(app, canvas):
    if app.startScreen == True:
        #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.tripadvisor.com%2FLocationPhotoDirectLink-g297613-d5860384-i304282249-Delta_9_Adventures-Vadodara_Vadodara_District_Gujarat.html&psig=AOvVaw1kqrQs66Lqgr5OfmGupZ23&ust=1619990586687000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMjT0LW1qfACFQAAAAAdAAAAABAD
        startScreen = Image.open('tp-start-screen.png')
        newScreen = startScreen.resize((app.width, app.height))
        canvas.create_image(app.width/2, app.height/2, 
                    image= ImageTk.PhotoImage(newScreen))
        canvas.create_text(app.width/2, app.height/5, text= '8-Ball Pool Game',
                font = 'Ariel 50 bold', fill= 'gold')
        y = app.height * (3/4)
        h = app.height/10 #height of boxes
        width = app.width/10 #half the total width
        startX = app.width/4
        incX = app.width/4
        canvas.create_rectangle(startX - width, y, 
                startX + width, y + h, fill = 'white') #first box
        canvas.create_rectangle(startX - width + incX, y, 
                startX + width + incX, y + h, fill = 'white') #second box
        canvas.create_rectangle(startX - width + 2*incX, y, 
                startX + width + 2* incX, y + h, fill = 'white') #third box
        canvas.create_text(startX, y + h/2, text= 'Single-Player Mode',
                font = 'Ariel 15 bold', fill= 'black')
        canvas.create_text(startX + incX, y + h/2, text= 'Multi-Player Mode',
                font = 'Ariel 15 bold', fill= 'black')
        canvas.create_text(startX + 2*incX, y + h/2, text= 'Skill Challenge',
                font = 'Ariel 15 bold', fill= 'black')        


def drawLeadeboard(app, canvas):
    #https://www.google.com/url?sa=i&url=https%3A%2F%2Ftribilliards.com%2Finformation%2Fofficial-8-ball-rules.html&psig=AOvVaw2_vMFho76RqsDNMhQnO9D-&ust=1620206804785000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMjupOzar_ACFQAAAAAdAAAAABAV
    startScreen = Image.open('leaderboard-screen.png')
    newScreen = startScreen.resize((app.width, app.height))
    canvas.create_image(app.width/2, app.height/2, 
                    image= ImageTk.PhotoImage(newScreen))

    contentsRead = readFile("skillChallenge-leaderboard.txt")
    leaderboard = contentsRead.split('\n')
    for score in leaderboard:
        if score == '':
            leaderboard.remove(score)
    score1 = leaderboard[0]
    score2 = leaderboard[1]
    score3 = leaderboard[2]
    score4 = leaderboard[3]
    score5 = leaderboard[4]
    canvas.create_text(app.width*1/4, app.height/5, text= 'Leaderboard:',
                font = 'Ariel 50 bold', fill= 'gold')
    startY = app.height*2/5
    x = app.width*1/4
    incY = 50
    canvas.create_text(x, startY, text= f'1st: {score1} points',
                font = 'Ariel 30 bold', fill= 'black')
    canvas.create_text(x, startY + incY, text= f'2nd: {score2} points',
                font = 'Ariel 30 bold', fill= 'black')
    canvas.create_text(x, startY + incY * 2, text= f'3rd: {score3} points',
                font = 'Ariel 30 bold', fill= 'black')
    canvas.create_text(x, startY + incY * 3, text= f'4th: {score4} points',
                font = 'Ariel 30 bold', fill= 'black')
    canvas.create_text(x, startY + incY * 4, text= f'5th: {score5} points',
                font = 'Ariel 30 bold', fill= 'black')

def redrawAll(app, canvas):
    startScreen(app, canvas)
    if app.startScreen == True:
        return
    if app.difficultyScreen == True:
        drawDifficultyMenu(app, canvas)
        return
    if app.leaderboardScreen == True:
        drawLeadeboard(app, canvas)
        return
    drawBoard(app, canvas)
    drawPockets(app, canvas)
    drawBalls(app, canvas)
    drawAddOns(app, canvas)
    drawCue(app, canvas)
    drawAim(app, canvas)
    drawPrediction(app, canvas)
    drawInstructions(app, canvas)
    drawGameOver(app, canvas)

#################################################
# main
#################################################

def main():
    runApp(width=800, height=500) #width = 800, height = 500 (These have to be the dimensions!)

if __name__ == '__main__':
    main()