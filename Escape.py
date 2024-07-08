import turtle as t                     # easier to type
from random import randint             # for spawn location
import time                            # handles game loop
import math                            # distance function

#game window
window = t.Screen()
window.title("Enemy Chase Game")
window.bgcolor("black")
window.setup(width = 720, height = 720)
window.setworldcoordinates(0,0,720,720)             # changed world coordinates because working with negative coords was cumbersome
window.tracer(0)

fontSize = 25
font1 = ('Helvetica', fontSize, 'bold')             # Discovered tuples for fonts on stack overflow
font2 = ('Helvetica', fontSize + 20, 'bold')

def endScreen(score):
    window.clearscreen()                                                     # clear EVERYTHING in the window

    window.bgcolor("black")                                                  # these 4 lines to reset window characteristics
    window.setup(width = 720, height = 720)
    window.setworldcoordinates(0,0,720,720)
    window.tracer(0)
    
    endSplash = t.Turtle()
    endSplash.speed(0)
    endSplash.color("white")
    endSplash.hideturtle()
    endSplash.goto(360,320)
    endSplash.write('GAME OVER\nSCORE: {}'.format(score),
                    align = "center",
                    font = font2,
                    )
    
    #realized because of dictionaries that you can do multiline arguments to make things easier to read. Very cool.
            
def collisionDetect(player, enemies):
    collision = False
    playerX = player.xcor()
    playerY = player.ycor()
    
    for enemy in enemies:
        enemyX  = enemy.xcor()    # Check player location (x,y), check each enemy (x,y)
        enemyY  = enemy.ycor()
        
        distance = math.sqrt(((playerX - enemyX)**2) + ((playerY - enemyY)**2))
        #Euclidian distance function to check collisions
        
        if distance < 20:
            collision = True
            return collision
    
def trackPlayer(player, enemy, acc):
    trackSpeed = 3                       # difficulty setting, how fast enemies are
    playerX = player.xcor()              # get player (x,y)
    playerY = player.ycor()
    
    for enemy in enemies:
        enemyX = enemy.xcor()            # for each enemy, get enemy (x,y)
        enemyY = enemy.ycor()
        
        if enemyX > playerX:                      # if enemy above player
            enemy.setx(enemyX - trackSpeed)       # move down
        if enemyY > playerY:                      # if enemy below player
            enemy.sety(enemyY - trackSpeed)       # move up
            
        if enemyX < playerX:                      # if enemy left of player
            enemy.setx(enemyX + trackSpeed)       # move right
        if enemyY < playerY:                      # if enemy right of player
            enemy.sety(enemyY + trackSpeed)       # move left
    
    acc += 1      #trackPlayer function runs every loop, this accumulates to handle spawning
    return acc
        
def movementLoop():                     # modifiable movement function implemented in direction functions so all can be updated more easily
    player.fd(20)                       # changing the value in .fd() changes difficulty of game

def press_up():                         # "press_" functions for when the key is initially pressed
    player.setheading(90)
    movementLoop()

def press_down():
    player.setheading(270)
    movementLoop()

def press_left():
    player.setheading(180)
    movementLoop()
    
def press_right():
    player.setheading(0)
    movementLoop()
    
def exitGame():                        # closes turtle window
    t.bye()


def spawn(shape, color, x, y):
    turtleEnemy = t.Turtle(shape, visible=False)
    turtleEnemy.speed(8)
    turtleEnemy.color(color)
    turtleEnemy.penup()
    turtleEnemy.goto(x, y)
    turtleEnemy.showturtle()
    return turtleEnemy

    
#Time Turtle: turtle used to draw and update timer
timer = t.Turtle()
timer.speed(0)
timer.color("white")
timer.hideturtle()
timer.goto(500,670)

#Box Turtle: it's the turtle...that will draw the box
box = t.Turtle()
box.speed(9999)
box.color("white")
box.hideturtle()
box.up()
box.goto(490,715)
box.down()

#Player turtle: it's the player
player = t.Turtle()                     
player.shape("circle")
player.color("white")
player.up()
player.goto(360,360)
player.speed(20)

#draw box around timer
for i in range(4):
    if i % 2 == 0:
        box.forward(220)
        box.right(90)
    else:
        box.forward(50)
        box.right(90)

window.onkeypress(press_up, 'Up')                     # onkeypress for when key is pressed
window.onkeypress(press_down, 'Down')
window.onkeypress(press_left, 'Left')
window.onkeypress(press_right, 'Right')
window.onkeyrelease(exitGame, 'Escape')               # closes turtle window with escape key
window.listen()

enemies = []                                          # initialize enemy container

rand_y = randint(0, 720)                              # these 4 lines spawn the first enemy
rand_x = randint(0, 720)
enemy = spawn("square", "red", rand_x, rand_y)
enemies.append(enemy)

startTime = time.time()                                        # record time when this line is ran
timerBool = True

acc = 0

while timerBool is True:
    timer.clear()                                              # clear previous time from timer
    secondsPast = int(time.time() - startTime)                 # time now - time then = time passed, passed as integer to get whole number
    timer.write('Score: {}'.format(secondsPast*100),           # write with timer turtle the secondsPast*100 for easy round score
                font = font1)
    window.update()                                            # update window
    acc = trackPlayer(player, enemies, acc)                    # update accumulator with return from tracking function
    collision = collisionDetect(player, enemies)               # after all enemies move, check if they collided with the player
    time.sleep(.05)                                            # delay on enemy loop to slow down tracking
    if collision == True:                                      # collisionDetect updates collision variable, if true...
        endScreen(secondsPast*100)                             # pass "score" into endScreen() for display at end
        timerBool = False                                      # stop the timer
    
    if acc % 30 == 1:                                          # acc remainder changes spawning rate
        rand_y = randint(0, 720)
        rand_x = randint(0, 720)
        enemy = spawn("square", "red", rand_x, rand_y)
        enemies.append(enemy)
    
window.mainloop()
        

        
