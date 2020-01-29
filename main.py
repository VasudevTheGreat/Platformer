import turtle
import math
from random import randint

height = 600
width = 800

line = [[50,0], [100,100]]

def drawBox():
  box = turtle.Turtle()
  box.speed(0)
  box.penup()
  box.goto(-400,-300)
  box.pendown()
  for i in range(2):
    box.forward(width)
    box.left(90)
    box.forward(height)
    box.left(90)

class Player(object):
  dx = None
  dy = None
  player = None
  radius = None
  gravity = None
  jumping = None
  traction = None
  
  def __init__(self):
    self.player = turtle.Turtle()
    self.player.tracer(0,0)
    self.player.speed(0)
    self.player.penup()
    self.dx = 0
    self.dy = 0
    self.player.shape("pennant")
    self.radius = 10
    self.gravity = 1
    self.jumping = False
    self.traction = 0.98
    
  def right(self):
    self.dx = 5 
  
  def up(self):
    if not self.jumping:
      self.dy = 15
      self.jumping = True
  
  def left(self):
    self.dx = -5
    
  def move(self):
    self.dy = self.dy - self.gravity
    self.dx = self.dx * self.traction
    if (self.player.xcor() + self.radius <= 0) and (self.player.xcor() + self.radius >= 200):
      self.dy = self.dy - self.gravity
    elif self.player.xcor() + self.radius >= 0 and self.player.xcor() + self.radius <= 200:
      self.gravity = 1
    x = self.player.xcor() + self.dx
    y = self.player.ycor() + self.dy
    self.player.goto(x,y)
    
  def checkboundary(self):
    x = self.player.xcor()
    y = self.player.ycor()
    
    if x + self.radius >= 400:
      x = 400 - self.radius
    if x - self.radius <= -400:
      x = -400 + self.radius
    if y + self.radius >= 300:
      y = 300 - self.radius
    if y - self.radius <= -300:
      y = -300 + self.radius
      self.jumping = False
    '''
    if x - self.radius <= 0 and x + self.radius >= 200:
      self.gravity = 0
    '''
      
    self.player.goto(x,y)
  
  def checkplatform(self):
    x = self.player.xcor()
    y = self.player.ycor()
    for p in platforms:
      if x - self.radius > p.x - p.width/2 and x + self.radius < p.x + p.width/2 and y - self.radius < p.y + p.height/2:
        if y - self.radius > p.y - p.height/2:
          self.jumping = False
          self.dy = 0
          self.player.sety(p.y + p.height/2 + self.radius)
        elif y + self.radius > p.y - p.height/2:
          self.player.sety(p.y - p.height/2 - self.radius)
          self.dy = 0
          
  def checkcoin(self):
    global count, score
    for coin in coins:
      x1 = self.player.xcor()
      x2 = coin.x
      y1 = self.player.ycor()
      y2 = coin.y
      r1 = self.radius
      r2 = coin.radius
      d = ((x1 - x2)**2) + ((y1 - y2)**2)
      if d <= (r1 + r2)**2:
        coin.coin.reset()
        coins.remove(coin)
        count += 1
        score.score.clear()
        score.drawscore()
  
  def checkMonster(self):
    for monster in monsters:
      x1 = self.player.xcor()
      x2 = monster.monster.xcor()
      y1 = self.player.ycor()
      y2 = monster.monster.ycor()
      r1 = self.radius
      r2 = monster.radius
      d = ((x1 - x2)**2) + ((y1 - y2)**2)
      if d <= (r1 + r2)**2:
        self.player.penup()
        self.player.goto(-79,-200)
        self.player.pendown()
        self.player.write("Game Over", font=("Arial", 20, "normal"))
        #self.player.reset()
        #self.player = None
        break








  def update(self):
    self.move()
    self.checkboundary()
    self.player.update()
    self.checkplatform()
    self.checkcoin()
    self.checkMonster()
    

class Coin(object):
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.drawcoin()
  def drawcoin(self):
    self.coin = turtle.Turtle()
    self.coin.speed(0)
    self.coin.penup()
    self.coin.shape("circle")
    self.radius = 10
    self.coin.goto(self.x,self.y)


class Platform(object):
  def __init__(self,x,y,width,height):
    global coins
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.drawplatform()
    x = randint(self.x-self.width/2,self.x+self.width/2)
    coins.append(Coin(x,y + self.height/2 + 10))
    x = randint(self.x-self.width/2,self.x+self.width/2)
    startx = self.x - (self.width/2)
    endx = self.x + (self.width/2)
    monsters.append(Monster(x,y + self.height/2 + 10, startx, endx))


  def drawplatform(self):
    platform = turtle.Turtle()
    platform.speed(0)
    platform.penup()
    platform.goto(self.x,self.y)
    platform.penup()
    platform.goto(self.x+self.width/2,self.y+self.height/2)
    platform.pendown()
    platform.goto(self.x+self.width/2,self.y-self.height/2)
    platform.goto(self.x-self.width/2,self.y-self.height/2)
    platform.goto(self.x-self.width/2,self.y+self.height/2)
    platform.goto(self.x+self.width/2,self.y+self.height/2)

class Score(object):
  def __init__(self):
    self.score = turtle.Turtle()
    self.score.penup()
    self.score.goto(-400,320)
    self.drawscore()
  def drawscore(self):
    global count

    self.score.write("score: " + str(count), font=("Arial", 20, "normal"))

    if count == 5:
      score.score.clear()
      self.score.write("Good Job!", font=("Arial", 20, "normal"))


class Monster(object):
  def __init__(self,x,y,startx,endx):
    self.x = x
    self.y = y
    self.dx = None
    self.dy = None
    self.monster = turtle.Turtle()
    self.monster.speed(0)
    self.monster.penup()
    self.monster.shape("square")
    self.radius = 10
    self.monster.goto(self.x,self.y)
    self.direction = 1
    self.speed = 2
    self.startx = startx
    self.endx = endx

  
  
  def monsterMove(self):
    if self.monster.xcor() < self.startx or self.monster.xcor() > self.endx:
      self.direction *= -1
    x = self.monster.xcor() + self.speed * self.direction
    self.monster.setx(x)


#class GameOver(object):
 # def __init__(self):
  #  self.gameover = turtle.Turtle()
   # self.gameover.penup()
    #self.gameover.goto(0,0)
    #self.drawGameOver()
  
  #def drawGameOver(self):
   # self.score.score.clear()
    #self.score.write("Game Over", font=("Arial", 20, "normal"))




platforms = []
coins = []
monsters = []
platforms.append(Platform(150,-200,200,50))
platforms.append(Platform(-150,-125,200,25))
platforms.append(Platform(130,-25,200,25))
platforms.append(Platform(-120,75,200,25))
platforms.append(Platform(-150,-250,300,25))



#center of rect : x=100, y= -282
#top part : y= -276, x= 0 to 200 

s = turtle.Screen()
drawBox()
player = Player()
count = 0
score = Score()

s.onkey(player.right,"D")

s.onkey(player.left,"A")

s.onkey(player.up,"W")

s.listen()

while player.player != None:

  for m in monsters:
    m.monsterMove()
  player.update()
