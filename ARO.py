############## ARO
# starter from https://pd43.github.io/notes/notes4-2.html
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random
import time
import math
# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################


####################################
# Classes
####################################
class character(object):
    @staticmethod
    def eat(data):
        data.player.isCollected(data)
        for badGuy in data.enemies:
            badGuy.isCollected(data)
    def __init__(self,data):
        #properties
        self.speed=5
        
        self.color=rgbString(255, 0, 0)
        self.eyeColor=rgbString(255,255,255)
        
        self.properties()
        self.position(data)
        self.eyes()
        self.wanderMap(data)
        self.state()
    def position(self,data):
        self.r=30
        self.cx=random.randrange(self.r,data.map.width-self.r)
        self.cy=random.randrange(self.r,data.map.height-self.r)
        while not self.isLegalMove(data):
            self.cx=random.randrange(self.r,data.map.width-self.r)
            self.cy=random.randrange(self.r,data.map.height-self.r)
            
    def properties(self):     
        self.level=1
        self.maxLevel=5
        
        self.hp=100
        self.maxHP=100
        self.hpPlus=20
        
        self.xp=0
        self.maxXP=10
        self.xpPlus=5
        
        
    def eyes(self):
        #eyes
        self.maxEyer=self.r//4
        self.eyer1=self.r//5
        self.eyer2=self.r//5
        self.eyeDistance=4*self.r//6 #from center to eye center
        self.eyeAngle=math.pi//2
    def wanderMap(self,data):
        self.scrollMarginX=data.width//2
        self.scrollMarginY=data.height//2
        self.scrollX=0
        self.scrollY=0
    def state(self):
        self.fire=False
        self.keyCold=False
        self.cold=2
        self.coldstart=2
        self.coldend=4
        self.isAlive=True
        self.weapon=None
        self.blood=[]
        
    
    def isCollected(self,data):
        for collectable in data.collectables:
            if collectable.isCollected: continue
            if (self.cx-self.r<=collectable.cx<=self.cx+self.r and
                self.cy-self.r<=collectable.cy<=self.cy+self.r):
                if type(collectable)==XP:
                    if self==data.player: data.score+=1
                    self.levelUp(1)
                if type(collectable)==HP:
                    self.getHP(collectable.hpValue)    

                collectable.isCollected=True
    def getHP(self,hp):
        if self.hp<self.maxHP:
            self.hp+=hp        
    def levelUp(self,xp):
        if self.level<self.maxLevel:
            self.xp+=xp
            if self.xp>=self.maxXP:
                self.xp-=self.maxXP
                self.maxXP+=self.xpPlus
                                        
                self.maxHP+=self.hpPlus
                self.hp+=self.hpPlus
                
                self.level+=1

        elif self.level==self.maxLevel:
            self.xp=self.maxXP
                   
    def hitByWeapons(self,harm,angle,hop,data,player):
        self.hp-=harm
        dir=(hop*math.cos(angle)/self.speed,-hop*math.sin(angle)/self.speed)
        while not self.isLegalMove(data, dir,True):
            dir=(hop*math.cos(angle)/self.speed,-hop*math.sin(angle)/self.speed)
            hop-=1
        
        self.createBlood(data)
        if self!=data.player:
            
            self.cx+=hop*math.cos(angle)
            self.cy-=hop*math.sin(angle)
        
        if self.hp<=0:
            if self==data.player: data.gameOver=True
            self.isAlive=False
            if player==data.player:
                player.levelUp(self.maxXP)
                data.score+=self.xp
                data.enemiesKilled+=1
    
    def hit(self,position,width):
        (cx,cy,r)=position
        distance=((cx-self.cx)**2+(cy-self.cy)**2)**0.5
        
        if distance<=width+self.r:
            return True    
        return False
    
    def isLegalMove(self,data,dir=(0,0),special=False):
        (hori,vert)=dir
        cx,cy,r=self.cx,self.cy,self.r
        cx+=hori*self.speed
        cy+=vert*self.speed
        
        #bound
        horiValid = (0<cx-r and cx+r<data.map.width)
        vertValid = (0<cy-r and cy+r<data.map.height)
        if (horiValid + vertValid) < 2:
            return False

        #wall
        for wall in data.walls:
            player=(cx,cy,r)
            if wall.hit(player):
                return False
        #guys


        for badGuy in data.enemies:
            if badGuy==self or not badGuy.isAlive: continue
            position=(cx,cy,r)
            if badGuy.hit(position,r):
                return False
            if special and data.player.hit(position,r):
                return False
        return True
        
        
    def moveEyes(self,x1,y1):
        x1,y1=x1+self.scrollX,y1+self.scrollY
        x0,y0=self.cx,self.cy
        if x1-x0==0:
            if y1-y0>0:
                angle=3*math.pi/2
            else:
                angle=math.pi/2
        elif x1-x0>0:
            angle=-math.atan((y1-y0)/(x1-x0))
        else:
            angle=-math.atan((y1-y0)/(x1-x0))-math.pi
        self.eyeAngle=angle       
    
    def createBlood(self,data):
        cx,cy,r=self.cx,self.cy,self.r
        for i in range(10):
            if len(data.blood)>100:data.blood=data.blood[10:100]
            x=random.randrange(int(cx-r),int(cx+r))
            y=random.randrange(int(cy-r),int(cy+r))
            size=random.randrange(0,r//2)
            red=random.randrange(180,255)
            color=rgbString(red,0,0)
            data.blood.append((x,y,size,color))
            
        
        
        
                
    
   
    def draw(self,canvas,data):
        sx=data.player.scrollX
        sy=data.player.scrollY
        cx,cy,r=self.cx,self.cy,self.r
        canvas.create_oval(cx-r-sx,cy-r-sy,cx+r-sx,cy+r-sy
            ,fill=self.color,width=0)
        
    def drawEyes(self,canvas,data):
        sx=data.player.scrollX
        sy=data.player.scrollY
        margin=math.pi/8 #difference between center angle and eye angle
        for angle in [margin,-margin]:
            eyeAngle=self.eyeAngle+angle
            x=self.cx+self.eyeDistance*math.cos(eyeAngle)
            y=self.cy-self.eyeDistance*math.sin(eyeAngle)
            if angle==margin: r=self.eyer1
            else: r=self.eyer2
            canvas.create_oval(x-r-sx,y-r-sy,x+r-sx,y+r-sy,
                fill=self.eyeColor,width=0)    
            
class player(character):
    def __init__(self,data,weaponChose,colorChose="gray"):
        super().__init__(data)
        colorDict={"white":(240,240,240),"black":(30,30,30),
            "gray":(110,110,110)}
        (r,g,b)=colorDict[colorChose]
        self.color=rgbString(r,g,b)
        
        self.cx=random.randrange(self.r,data.width-self.r)
        self.cy=random.randrange(self.r,data.height-self.r)
        while not self.isLegalMove(data):
            self.cx=random.randrange(self.r,data.width-self.r)
            self.cy=random.randrange(self.r,data.height-self.r)
        self.weaponChose=weaponChose
        #wander map
        self.scrollMarginX=data.width//2
        self.scrollMarginY=data.height//2
        self.scrollX=0
        self.scrollY=0


    def move(self,dir,data):
        (hori,vert)=dir
        
        
        
        self.cx+=hori*self.speed
        self.cy+=vert*self.speed
        if self.cx<self.scrollX+self.scrollMarginX:
            self.scrollX=self.cx-self.scrollMarginX
            
            
        if self.cx>self.scrollX-self.scrollMarginX+data.width:
            self.scrollX=self.cx+self.scrollMarginX-data.width
            
        if self.cy<self.scrollY+self.scrollMarginY:
            self.scrollY=self.cy-self.scrollMarginY
            
            
        if self.cy>self.scrollY-self.scrollMarginY+data.height:
            self.scrollY=self.cy+self.scrollMarginY-data.height
    
    
    def isLegalMove(self,data,dir=(0,0),special=False):
        return super().isLegalMove(data,dir,special)   
    
    
    def control(self,data):
        dir=[0,0]
        if "w" in data.pressedLetters:
            dir[1]=-1
        elif "s" in data.pressedLetters:
            dir[1]=1        
        if not self.isLegalMove(data,dir):
            dir[1]=0
            
        if "a" in data.pressedLetters:
            dir[0]=-1 
        elif "d" in data.pressedLetters:
            dir[0]=1
        if not self.isLegalMove(data,dir):
            dir[0]=0    
        data.player.move(tuple(dir),data)
        
    def draw(self,canvas):
        sx=self.scrollX
        sy=self.scrollY
        cx,cy,r=self.cx,self.cy,self.r
        canvas.create_oval(cx-r-sx,cy-r-sy,cx+r-sx,cy+r-sy
            ,fill=self.color,width=0)
    def drawBars(self,canvas,data):
        margin=20
        #hp bar
        HPleft=data.width*3/5
        HPup=margin
        pHP=self.hp/self.maxHP
        canvas.create_text(HPleft-5,HPup,text="HP.%d/%d"%(self.hp,self.maxHP),
            anchor="ne",font="Times 15")
        canvas.create_rectangle(HPleft,HPup,data.width-margin,HPup+margin,
            fill="")
        canvas.create_rectangle(HPleft,HPup,
            HPleft+(data.width-margin-HPleft)*pHP,HPup+margin,fill="red")
        #xp bar
        XPleft=data.width*3/5
        XPup=margin*2.5
        XPheight=margin*1/2
        pXP=self.xp/self.maxXP
        
        level=self.level
        if self.level==self.maxLevel:
            level="Max"
        canvas.create_text(XPleft-5,XPup,text="Lv.%s"%str(self.level),
            anchor="ne",font="Times 14")
        canvas.create_rectangle(XPleft,XPup,data.width-margin,XPup+XPheight,
            fill="")
        canvas.create_rectangle(XPleft,XPup,
            XPleft+(data.width-margin-XPleft)*pXP,XPup+XPheight,fill="blue")
        
        
    def moveEyes(self,x1,y1):
        x1,y1=x1+self.scrollX,y1+self.scrollY
        x0,y0=self.cx,self.cy
        if x1-x0==0:
            if y1-y0>0:
                angle=3*math.pi/2
            else:
                angle=math.pi/2
        elif x1-x0>0:
            angle=-math.atan((y1-y0)/(x1-x0))
        else:
            angle=-math.atan((y1-y0)/(x1-x0))-math.pi
        self.eyeAngle=angle
  
        
    def drawEyes(self,canvas):
        sx=self.scrollX
        sy=self.scrollY
        margin=math.pi/8 #difference between center angle and eye angle
        for angle in [margin,-margin]:
            eyeAngle=self.eyeAngle+angle
            x=self.cx+self.eyeDistance*math.cos(eyeAngle)
            y=self.cy-self.eyeDistance*math.sin(eyeAngle)
            if angle==margin: r=self.eyer1
            else: r=self.eyer2
            canvas.create_oval(x-r-sx,y-r-sy,x+r-sx,y+r-sy,
                fill=self.eyeColor,width=0)


class Enemies(character):
    @staticmethod
    def timerFired(data):
        for i in range(len(data.enemies)):
            badGuy=data.enemies[i]
            if badGuy.isAlive==False:
                badGuy.color=""
                badGuy.eyeColor=""
            badGuy.stalk(data)
    @staticmethod
    def enemiesMove(data):
        for i in range(len(data.enemies)):
            badGuy=data.enemies[i]
            if not badGuy.isAlive: continue 
            badGuy.stalk(data)
        
    @staticmethod
    def killEnemies(data):
        for i in range(len(data.enemies)):
            badGuy=data.enemies[i]
            if badGuy.isAlive==False:
                badGuy.color=""
                badGuy.eyeColor=""
    
    def rePosition(self,data,inGame):
        self.r=30
        self.cx=random.randrange(self.r,data.map.width-self.r)
        self.cy=random.randrange(self.r,data.map.height-self.r)
        while not self.isLegalMove(data,(0,0),inGame):
            self.cx=random.randrange(self.r,data.map.width-self.r)
            self.cy=random.randrange(self.r,data.map.height-self.r)            
    def __init__(self,data,inGame=False):
        super().__init__(data)
        self.rePosition(data,inGame)
        
        self.speed=0.1
        self.movements=set()
        self.moveCount=0
        self.maxMoves=40
        self.gotCha=None
        self.target=None
        self.randomAngle=0
 
        
        
    
    
    
        
    def findSomeone(self,data):
        

        x1,y1=data.player.cx,data.player.cy        
        if distance(self.cx,self.cy,x1,y1)<data.width//2:
            self.gotCha=(x1,y1)
            return True
        
        for i in range(len(data.enemies)):
            badGuy=data.enemies[i]
            x1,y1=badGuy.cx,badGuy.cy
            if badGuy==self:continue

            if distance(self.cx,self.cy,x1,y1)<data.width//3:
                self.gotCha=(x1,y1)
                return True
        
        
        self.gotCha=None
        return False
    def stalk(self,data):
        if not self.isAlive: return 
        if self.hp<self.maxHP//3 and self.moveCount%(self.maxMoves//2)==0:
            self.getFood(data,HP)
            if (data.count%self.maxMoves==0)and self.gotCha!=None:
                (x1,y1)=self.gotCha
                self.moveEyes(x1,y1)
                self.autoShoot(data)
        elif self.gotCha!=None:
            (x1,y1)=self.gotCha
            
            self.targetAngle(x1, y1)
            
            if (distance(self.cx,self.cy,x1,y1)>data.width//4 
                and self.moveCount%(self.maxMoves//2)==0):
                self.move2Target(self.target,data)
            
            self.randomMovement(data)
            
            self.moveEyes(x1,y1)
            self.autoShoot(data)
        elif self.moveCount%(self.maxMoves//3)==0:
            self.getFood(data,XP)
        else:
            self.randomMovement(data)
        
    
    def getFood(self,data,genre):
        (x1,y1)=self.findFood(data,genre)
        self.targetAngle(x1, y1)
        self.move2Target(self.target,data)
    
    
    def findFood(self,data,genre): 
        min = data.map.width
        foodLocation=(random.randrange(0,data.width),random.randrange(0,data.height))
        for collectable in data.collectables:
            if type(collectable)==genre:
                way = distance(self.cx,self.cy,collectable.cx,collectable.cy)
                if way<min: 
                    min=way
                    foodLocation=(collectable.cx,collectable.cy)
        return foodLocation
    

    
                    
            
    def autoShoot(self,data):
        trigger(self)
            
    def targetAngle(self,x1,y1):
        x1,y1=x1+self.scrollX,y1+self.scrollY
        x0,y0=self.cx,self.cy
        if x1-x0==0:
            if y1-y0>0:
                angle=3*math.pi/2
            else:
                angle=math.pi/2
        elif x1-x0>0:
            angle=-math.atan((y1-y0)/(x1-x0))
        else:
            angle=-math.atan((y1-y0)/(x1-x0))-math.pi
        self.target=angle
        
    def move2Target(self,angle,data):
        
        if not self.isAlive: return
        dir=(self.r*math.cos(angle),-self.r*math.sin(angle))
        while not self.isLegalMove(data,dir,True):
            
            angle+=random.choice([math.pi/2,-math.pi/2])
            dir=(self.r*math.cos(angle),-self.r*math.sin(angle))
        self.eyeAngle=angle
        self.cx+=self.r*math.cos(angle)*self.speed
        self.cy-=self.r*math.sin(angle)*self.speed
        
        


    
    def randomMovement(self,data):
        
        self.moveCount+=1
        if self.moveCount%self.maxMoves==0:
            self.randomAngle=random.randrange(0,int(2*math.pi))
        
        self.move2Target(self.randomAngle,data)
        
            
    def hit(self,position,width):
        (cx,cy,r)=position
        distance=((cx-self.cx)**2+(cy-self.cy)**2)**0.5
        
        if distance<=width+self.r:
            
            return True    
        return False
    def draw(self,canvas,data):
        super().draw(canvas,data)
        super().drawEyes(canvas, data)
            
        
    



class Map(object):
    
    def __init__(self,left=0,up=0,size=0):
        self.width=1600
        self.height=1200
        
    def hit(self,player):
        
        (cx,cy,r)=player
        horiValid = (self.left+self.size<cx-r or cx+r<self.left)
        vertValid = (self.up+self.size<cy-r or cy+r<self.up)
        if (horiValid + vertValid)==0:
            
            return True    
        return False
class Wall(Map):
    @staticmethod
    def isLegal(wall,data):

        for ano in data.walls[:]:
            
            horiValid = (ano.left+ano.size<wall.left or 
                wall.left+wall.size<ano.left)
            vertValid = (ano.up+ano.size<wall.up or wall.up+wall.size<ano.up)
         
            if (horiValid + vertValid)==0:
                return False
        
        return True    
    
    
    def __init__(self,data):
        super().__init__()
        self.size=100
        self.left=random.randrange(0+self.size,self.width-self.size)
        self.up=random.randrange(0+self.size,self.height-self.size)
        
        
 
        while not Wall.isLegal(self,data):
            self.left=random.randrange(0+self.size,self.width-self.size)
            self.up=random.randrange(0+self.size,self.height-self.size)
        
    
    
    def draw(self,canvas,sx,sy):
        color1=rgbString(255, 255, 255)
        pShade=2/3
        pNull=1/9
        canvas.create_rectangle(self.left-sx,self.up-self.size*pNull-sy,
                self.left+self.size-sx,self.up+self.size-sy,fill=color1,width=1)
        canvas.create_rectangle(self.left+1-sx,self.up+self.size*pShade-sy,
            self.left+self.size-sx,self.up+self.size-sy,fill="gray",width=0)



class Weapon(character):
    def __init__(self,character):
        self.cx=character.cx
        self.cy=character.cy
        self.size=character.r
        self.angle=character.eyeAngle
        
        self.color=rgbString(0, 0, 0)
        self.used=False
    def disappear(self,data):
        self.color=""
        self.used=True

    def fire(self):
        self.cx+=self.speed*math.cos(self.angle)
        self.cy-=self.speed*math.sin(self.angle)
        
    def hitEnemies(self,data,player):
        position=(self.cx,self.cy,self.size)
        if self.used: return
        for i in range(len(data.enemies)):
            
            badGuy=data.enemies[i]
            if not badGuy.isAlive or player==badGuy: continue
            if badGuy.hit(position,0):
                angle=player.weapon.angle
                badGuy.hitByWeapons(self.harm,angle,self.hop,data,player)
                
                return True
        if player!=data.player and data.player.hit(position,0):
            angle=player.weapon.angle
            data.player.hitByWeapons(self.harm,angle,self.hop,data,player)
            return True
        return False
    def hitWalls(self,data):
        for i in range(len(data.walls)):
            wall=data.walls[i]
            position=(self.cx,self.cy,self.size)
            if wall.hit(position) and self.used==False:
                return True
        return False
    def hitBonds(self,data):
        horiValid = (0<self.cx-self.size and self.cx+self.size<data.map.width)
        vertValid = (0<self.cy-self.size and self.cy+self.size<data.map.height)
        if (horiValid + vertValid) < 2:
            return True   
        return False


        
class Arrow(Weapon):
    def __init__(self,character):
        super().__init__(character)
        self.harm=20
        self.hop=30
        self.speed=30
    def draw(self,canvas,sx,sy):
        x1=self.cx+self.size*math.cos(self.angle)
        y1=self.cy-self.size*math.sin(self.angle)
        blade=1/5*self.size
        bladeAngleR=math.pi/4+self.angle
        bladeAngleL=-math.pi/4+self.angle
        xLeft=x1-blade*math.cos(bladeAngleL)
        yLeft=y1+blade*math.sin(bladeAngleL)
        
        xRight=x1-blade*math.cos(bladeAngleR)
        yRight=y1+blade*math.sin(bladeAngleR)
        
        
        canvas.create_line(self.cx-sx,self.cy-sy,x1-sx,y1-sy,fill=self.color,
            width=2)
        canvas.create_line(xLeft-sx,yLeft-sy,x1-sx,y1-sy,fill=self.color,
            width=2)
        canvas.create_line(xRight-sx,yRight-sy,x1-sx,y1-sy,fill=self.color,
            width=2)
    

class FireBall(Weapon):
    def __init__(self,character):
        super().__init__(character)
        self.harm=30
        self.hop=50
        self.speed=20
        self.size=5
    def draw(self,canvas,sx,sy):
        if self.used: return
        cx,cy,r=self.cx,self.cy,self.size
        r+=random.randrange(-2,2)
        green=random.randrange(60,200)
        color=rgbString(250,green,65)
        canvas.create_oval(cx-r-sx,cy-r-sy,cx+r-sx,cy+r-sy,fill=color,width=2)
    def fire(self):
        self.cx+=self.speed*math.cos(self.angle)
        self.cy-=self.speed*math.sin(self.angle)
    
class Saber(Weapon):
    def __init__(self,character):
        super().__init__(character)
        self.harm=65
        self.hop=100
        self.speed=50

        self.cx=character.cx
        self.cy=character.cy
        self.size=character.r*2
        self.angle=character.eyeAngle
        self.arcAngle=self.angle*180/math.pi
        
        self.count=0
        self.maxCount=3
    def fire(self):
        self.count+=1
        if self.count<self.maxCount:
            self.cx+=self.speed*math.cos(self.angle)
            self.cy-=self.speed*math.sin(self.angle)
        else:
            self.used=True
    def hitEnemies(self,data,player):
        position=(self.cx,self.cy,self.size)
        if self.used: return
        for i in range(len(data.enemies)):
            
            badGuy=data.enemies[i]
            if not badGuy.isAlive or player==badGuy: continue
            if badGuy.hit(position,self.size):
                angle=player.weapon.angle
                badGuy.hitByWeapons(self.harm,angle,self.hop,data,player)
                
                return True
        if player!=data.player and data.player.hit(position,0):
            angle=player.weapon.angle
            data.player.hitByWeapons(self.harm,angle,self.hop,data,player)
            return True
        return False
    def draw(self,canvas,sx,sy):
        if self.used: return
        for i in range(2):
            cx,cy,r=self.cx,self.cy,self.size
            cx+=random.randrange(-4,4)
            cy+=random.randrange(-4,4)
            color=random.choice(["white","black"])
            width=random.randrange(3,5)
            canvas.create_arc(cx-r-sx,cy-r-sy,cx+r-sx,cy+r-sy,
                start=self.arcAngle-45,style="arc",width=width,outline=color)
        
    
    


class splashArrow(Arrow):
    def __init__(self,data):
        self.cx=random.randrange(-data.width,data.width)
        self.cy=random.randrange(-data.height,data.height)
        self.color=rgbString(0, 0, 0)
        self.size=random.randrange(10,40)
        self.angle=math.pi/4
        self.speed=random.randrange(5,30)
class Collectable(object):
    @staticmethod
    def collected(data):
        for i in range(len(data.collectables)):
            collectable=data.collectables[i]
            if collectable.isCollected:
                collectable.color=""
                
                data.collectables[i]=type(collectable)(data)
                
            
    def __init__(self,data):
        self.size=5
        self.cx=random.randrange(0+self.size,data.map.width-self.size)
        self.cy=random.randrange(0+self.size,data.map.height-self.size)
        self.isCollected=False
        self.color=rgbString(0,0,255)
        while not data.player.isLegalMove(data):
            self.cx=random.randrange(0+self.size,data.map.width-self.size)
            self.cy=random.randrange(0+self.size,data.map.height-self.size)
    def draw(self,canvas,sx,sy):
        cx,cy,size=self.cx,self.cy,self.size
        canvas.create_polygon(cx-size-sx,cy-sy,cx-sx,cy+size-sy,
            cx+size-sx,cy-sy,cx-sx,cy-size-sy,fill=self.color)



        
class XP(Collectable):
    pass    
class HP(Collectable):
    def __init__(self,data):
        super().__init__(data)
        self.color=rgbString(255,105,180)
        self.hpValue=20
        self.size=7
    def draw(self,canvas,sx,sy):
        cx,cy,size=self.cx,self.cy,self.size 
    
        canvas.create_oval(cx-size-sx,cy-size-sy,cx+size-sx,cy+size-sy,
            fill=self.color)  
    
#############  
#Event      
#############
def rgbString(r,g,b):
    return "#%02x%02x%02x" %(r,g,b)
def distance(x0,y0,x1,y1):
    result=((x0-x1)**2+(y0-y1)**2)**0.5
    return result

def trigger(player,weaponChose=Arrow):
    if player.coldend-player.coldstart>=player.cold:
        if weaponChose=="Arrow":
            weaponChose=Arrow
        elif weaponChose=="FireBall":
            weaponChose=FireBall
        elif weaponChose=="Saber":
            weaponChose=Saber
            
        player.weapon=weaponChose(player)
        player.fire=True
        player.coldstart=time.time()
         
def firing(data,player):
       
    weapon=player.weapon
    
    if weapon.used: return
    if weapon.hitEnemies(data,player):
        player.weapon.disappear(data)
        
    if weapon.hitWalls(data):
        player.weapon.disappear(data)
        
    if weapon.hitBonds(data):
        player.weapon.disappear(data)
        
    weapon.fire()

def init(data):
    data.helpClick=False
    data.gameOver=False
    data.win=False
    data.mode="splash"
    data.pressedLetters = set()
    if data.mode=="splash":
        splashInit(data)

        



def keyPressed(event, data):
    
    if data.win:
        winKeyPressed(event,data)
    
    elif data.gameOver:
        gameOverKeyPressed(event,data)
    
    elif data.mode=="splash":
        splashKeyPressed(event,data)
    elif data.mode=="option":
        optionKeyPressed(event,data)
    elif data.mode=="help":
        helpKeyPressed(event,data)
    
    elif data.mode in ["evolve","infinity","time"]:
        inGameKeyPressed(event,data)
    
        
            
def keyReleased(event, data):
    if data.win:
        winKeyReleased(event,data)
    elif data.gameOver:
        gameOverKeyReleased(event,data)
    elif data.win:
        winKeyReleased(event, data)
    elif data.mode=="splash":
        splashKeyReleased(event,data)
        
    elif data.mode in ["evolve","infinity","time"]:
        inGameKeyReleased(event,data)
    
            
            
def mousePressed(event, data):
    if data.mode=="help":
        helpMousePressed(event,data)
def mouseMotion(event, data):
    if data.win:
        winMouseMotion(event,data)
    elif data.gameOver:
        gameOverMouseMotion(event,data)
    elif data.win:
        winMouseMotion(event,data)
    elif data.mode in ["evolve","infinity","time"]:
        inGameMouseMotion(event,data)
    


def timerFired(data):
    if data.win:
        winTimerFired(data)
    elif data.gameOver:
        gameOverTimerFired(data)
    elif data.mode=="splash":
        splashTimerFired(data)
    elif data.mode=="option":
        optionTimerFired(data)
    elif data.mode=="evolve":
        evolveTimerFired(data)
    elif data.mode=="infinity":
        infinityTimerFired(data)
    elif data.mode=="time":
        timeTimerFired(data)
    elif data.mode=="help":
        helpTimerFired(data)
            
    
            

# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.

def drawGameBoard(canvas,data):
    sx=data.player.scrollX
    sy=data.player.scrollY
    color=rgbString(189, 193, 201)
    canvas.create_rectangle(0-sx,0-sy,data.map.width-sx,data.map.height-sy,
        fill=color,width=0)
    
    
def drawWalls(canvas,data,sx,sy):
    for wall in data.walls:
        wall.draw(canvas,sx,sy)



def drawWeapons(canvas,data,sx,sy):
    data.player.weapon.draw(canvas,sx,sy)
    

def drawEnemies(canvas,data,sx,sy):

    for badGuy in data.enemies:
        if badGuy.fire:
            badGuy.weapon.draw(canvas,sx,sy)
        badGuy.draw(canvas,data)

def drawCollectables(canvas,data,sx,sy):
    for thing in data.collectables:
        thing.draw(canvas,sx,sy)
        
           
def drawBlood(canvas,data,sx,sy):
    for blood in data.blood:
        (x,y,r,color)=blood
        canvas.create_oval(x-r-sx,y-r-sy,x+r-sx,y+r-sy,fill=color,width=0) 
        
def redrawAll(canvas, data):
    if data.gameOver:
        gameOverRedrawAll(canvas,data)
    elif data.win:
        
        winRedrawAll(canvas, data)
    elif data.mode=="splash":
        splashRedrawAll(canvas,data)
    elif data.mode=="option":
        optionRedrawAll(canvas,data)
        
    elif data.mode=="evolve":
        evolveRedrawAll(canvas,data)
    elif data.mode=="infinity":
        infinityRedrawAll(canvas,data)
    elif data.mode=="time":
        timeRedrawAll(canvas,data)
  
    elif data.mode=="help":
        helpRedrawAll(canvas,data)
    
    



################
#splash mode
################

        
        
def splashInit(data):
    data.weapons=[]
    for i in range(70):
        
        data.weapons.append(splashArrow(data))
def splashKeyPressed(event,data):
    
    data.mode="option"
    data.option=Option()
def splashKeyReleased(event,data):
    pass

def splashMousePressed(event,data):
    pass
def splashMouseMotion(event,data):
    pass
def splashTimerFired(data):
    for i in range(len(data.weapons)):
        weapon=data.weapons[i]
        if weapon.cx>data.width or weapon.cy>data.height:
            data.weapons[i]=splashArrow(data)
        weapon.fire()
def splashRedrawAll(canvas,data):
    
    text="ARO"
    text2="Press any key to START"
    
    textMargin=30
    margin=10
    
    #canvas.create_rectangle(0+margin,0+margin,
    #    data.width-margin,data.height-margin,fill="white",width=0)
    canvas.create_text(data.width//2,data.height//2,text=text,
        font="Times 100")
    canvas.create_text(data.width//2,data.height//2+textMargin*2,text=text2,
        font="Helvetica 12")
    for weapon in data.weapons:
        weapon.draw(canvas,0,0)


####################################
# OPTION
####################################
class Option(object):
    
    def __init__(self):
        self.row=1
        self.col=1
        self.options=[["Evolve","Infinity","Limit-Time"],
                        ["Arrow","FireBall", "Saber"],
                        ["Gray","White","Black"]]
        self.chosen=[1,1,1]

def optionKeyPressed(event,data):
    row,col=data.option.row,data.option.col
    if event.keysym=="Left":
        if 0<=col-1<len(data.option.options[row]):
            data.option.col-=1
            data.option.chosen[row]-=1
    elif event.keysym=="Right":
        if 0<=col+1<len(data.option.options[row]):
            data.option.col+=1
            data.option.chosen[row]+=1
    elif event.keysym=="Up":
        if 0<=row-1<len(data.option.options):
            data.option.chosen[data.option.row]=data.option.col
            data.option.col=data.option.chosen[data.option.row-1]
            data.option.row-=1
    elif event.keysym=="Down":
        if 0<=data.option.row+1<len(data.option.options):
            data.option.chosen[data.option.row]=data.option.col
            data.option.col=data.option.chosen[data.option.row+1]
            data.option.row+=1
    
    elif event.keysym=="space":
        data.mode="help"
    
    elif event.keysym=="Return":
        options=data.option.options
        mode=options[0][data.option.chosen[0]]
        weaponChose=options[1][data.option.chosen[1]]
        colorChose=options[2][data.option.chosen[2]].lower()
        if mode=="Evolve":
            inGameInit(data,weaponChose,colorChose)
            data.mode="evolve"
            
        elif mode=="Limit-Time":
            inGameInit(data,weaponChose,colorChose)
            data.mode="time"
            
        elif mode=="Infinity":
            inGameInit(data,weaponChose,colorChose)
            data.mode="infinity"
            
def optionKeyReleased(event,data):
    pass

def optionMousePressed(event,data):
    pass
def optionMouseMotion(event,data):
    pass
def optionTimerFired(data):
    pass
def optionRedrawAll(canvas,data):
    margin=10
    downMargin=30
    row=data.option.row
    col=data.option.col
    colors=["white","white","white"]
    colors[row]="gray"
    textColors=["black","black","black"]
    textColors[row]="white"
    helpText="[space] help [return] start"
    
    options=data.option.options
    gameMode=options[0][data.option.chosen[0]]
    weapon=options[1][data.option.chosen[1]]
    color=options[2][data.option.chosen[2]]
    
    canvas.create_rectangle(data.width//3,data.height//7,data.width*2//3,
        data.height*2//7,fill=colors[0])
    canvas.create_rectangle(data.width//3,data.height*3//7,data.width*2//3,
        data.height*4//7,fill=colors[1])
    canvas.create_rectangle(data.width//3,data.height*5//7,data.width*2//3,
        data.height*6//7,fill=colors[2])
        
    canvas.create_text(data.width//2,data.height*1//14,text="OPTION",
    font="Helvetica 25")
    canvas.create_text(data.width//2,data.height*3//14,text=gameMode,
    font="Helvetica 20",fill=textColors[0])
    canvas.create_text(data.width//2,data.height*7//14,text=weapon,
    font="Helvetica 20",fill=textColors[1])
    canvas.create_text(data.width//2,data.height*11//14,text=color,
    font="Helvetica 20",fill=textColors[2])
    
    canvas.create_text(data.width-downMargin, data.height-downMargin,
        anchor="e",text=helpText, font="Times 13")    
####################################
# help mode
####################################

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    if event.keysym=="space":
        data.helpClick=not data.helpClick
    elif event.keysym=="Escape":
        data.mode = "option"
    
def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    downMargin=30
    gameMode=data.option.options[0][data.option.chosen[0]]
    text="1. [w][a][s][d] to move\n\n2. [Space] to shoot\n\n3. Mouse to aim"
    if data.helpClick:
        canvas.create_text(data.width/2, data.height/2-100,
                            text="Contol:", font="Times 20 bold")
        canvas.create_text(data.width/2, data.height/2,
                        text=text, font="Times 15")
    else:
        if gameMode=="Evolve":
            canvas.create_text(data.width/2, data.height/2+30,
                            text="Get to level 5!", font="Times 20")
        elif gameMode=="Infinity":
            canvas.create_text(data.width/2, data.height/2+30,
                            text="Don't die and score points!",font="Times 20")
        elif gameMode=="Limit-Time":
            canvas.create_text(data.width/2, data.height/2+30,
                            text="Kill as many as you can!", font="Times 20")
                        
        canvas.create_text(data.width/2, data.height/2-40,
                            text="#%s#" %gameMode, font="Times 20 bold")
        canvas.create_text(data.width/2, data.height/2-10,
                            text="Instructions:",font="Times 26 bold") 
                                                
    canvas.create_text(data.width/2, data.height/2+100,
            text="(Press [space] to continue)", font="Times 15")
    canvas.create_text(data.width-downMargin, data.height-downMargin,
        anchor="e",text="[Esc] back to menu", font="Times 13")




################
#Win 
################
def winKeyPressed(event,data):
    if event.keysym=="r":
        init(data)
def winKeyReleased(event,data):
    pass

def winMousePressed(event,data):
    pass
def winMouseMotion(event,data):
    pass
def winTimerFired(data):
    pass
def winRedrawAll(canvas,data):
    text="You Win"
    text2="Press [R] to RESTART"
    if data.mode=="evolve":
        text3="You successfully get to Level%d!" %data.player.maxLevel
    elif data.mode=="time":
        text3="Enemies killed: %d" %data.enemiesKilled

    textMargin=30
    margin=10
    canvas.create_text(data.width//2,data.height//2-textMargin,text=text,
        font="Times 100")

    canvas.create_text(data.width//2,data.height//2+textMargin*2,text=text2,
        font="Helvetica 14")
    
    
    canvas.create_text(data.width//2,data.height//2+textMargin*3,text=text3,
        font="Helvetica 12")


################
#gameOver 
################
def gameOverKeyPressed(event,data):
    if event.keysym=="r":
        init(data)
        
def gameOverKeyReleased(event,data):
    pass

def gameOverMousePressed(event,data):
    pass
def gameOverMouseMotion(event,data):
    pass
def gameOverTimerFired(data):
    pass
def gameOverRedrawAll(canvas,data):
    if data.mode=="time" and data.player.isAlive:
        text="Time's up!"
    else:
        text="You Die"
    if data.mode=="infinity":
        text3="Your score: %d" %data.score
    elif data.mode=="time":
        text3="Enemies killed: %d" %data.enemiesKilled
    elif data.mode=="evolve":
        text3="Your current level is: %d" %data.player.level
    text2="Press [R] to RESTART"
    textMargin=30
    margin=10
    canvas.create_text(data.width//2,data.height//2-textMargin,text=text,
        font="Times 100")
    canvas.create_text(data.width//2,data.height//2+textMargin*2,text=text2,
        font="Helvetica 14")
    canvas.create_text(data.width//2,data.height//2+textMargin*3,text=text3,
        font="Helvetica 12")

################
#Infinity mode
################


 
def infinityTimerFired(data):
    if data.cheat: data.player.hp=data.player.maxHP
    
    elif not data.player.isAlive:
        data.gameOver=True
    data.count+=1
    data.player.control(data)
    Enemies.timerFired(data)
    character.eat(data)
    Collectable.collected(data)

    data.player.coldend=time.time()
    if data.player.fire:
        firing(data, data.player)
        
    for i in range(len(data.enemies)):
        badGuy=data.enemies[i]
        if not badGuy.isAlive: 
            data.enemies[i]=Enemies(data,True)
            continue
        badGuy.findSomeone(data)
        badGuy.coldend=time.time()
        if badGuy.fire:
            firing(data, badGuy)
            
def infinityRedrawAll(canvas,data):
    sx=data.player.scrollX
    sy=data.player.scrollY
    
    drawGameBoard(canvas,data)
    drawBlood(canvas,data,sx,sy)
    if data.player.fire:
        drawWeapons(canvas,data,sx,sy)
    drawCollectables(canvas,data,sx,sy) 
    
    
    
    drawEnemies(canvas, data,sx,sy)   
    data.player.draw(canvas)
    data.player.drawEyes(canvas)
    
    drawWalls(canvas,data,sx,sy)
    

    data.player.drawBars(canvas,data)
    drawScore(canvas,data)
def drawScore(canvas,data):
    margin=20
    text="Score: %d" %data.score
    canvas.create_text(data.width//2,data.height-margin,text=text,
        font="Times 20")

################
#evolve mode
################

def evolveTimerFired(data):
    if data.player.level==data.player.maxLevel:
        data.win=True
    if data.cheat: data.player.hp=data.player.maxHP
    
    elif not data.player.isAlive:
        data.gameOver=True
    data.count+=1
    data.player.control(data)
    Enemies.timerFired(data)
    character.eat(data)
    Collectable.collected(data)

    data.player.coldend=time.time()
    if data.player.fire:
        firing(data, data.player)
        
    for i in range(len(data.enemies)):
        badGuy=data.enemies[i]
        if not badGuy.isAlive: 
            data.enemies[i]=Enemies(data,True)
            continue
        badGuy.findSomeone(data)
        badGuy.coldend=time.time()
        if badGuy.fire:
            firing(data, badGuy)
            
def evolveRedrawAll(canvas,data):
    sx=data.player.scrollX
    sy=data.player.scrollY
    
    drawGameBoard(canvas,data)
    drawBlood(canvas,data,sx,sy)
    if data.player.fire:
        drawWeapons(canvas,data,sx,sy)
    drawCollectables(canvas,data,sx,sy) 
    
    
    
    drawEnemies(canvas, data,sx,sy)   
    data.player.draw(canvas)
    data.player.drawEyes(canvas)
    
    drawWalls(canvas,data,sx,sy)
    

    data.player.drawBars(canvas,data)
    


################
#limit-time mode
################

  
def timeTimerFired(data):
    
    if time.time()-data.initTime>=data.limitTime:
        data.gameOver=True
        
    elif not data.player.isAlive:
        data.gameOver=True
    
    if data.cheat: data.player.hp=data.player.maxHP
    
    
    data.count+=1
    data.player.control(data)
    Enemies.timerFired(data)
    character.eat(data)
    Collectable.collected(data)

    data.player.coldend=time.time()
    if data.player.fire:
        firing(data, data.player)
        
    for i in range(len(data.enemies)):
        badGuy=data.enemies[i]
        if not badGuy.isAlive: 
            data.enemies[i]=Enemies(data,True)
            continue
        badGuy.findSomeone(data)
        badGuy.coldend=time.time()
        if badGuy.fire:
            firing(data, badGuy)

def drawTime(canvas,data):
    
    timeText=round(data.limitTime-(time.time()-data.initTime),2)
    
    margin=80
    canvas.create_text(margin,margin//2,text=timeText,
        font="Times 20")

def drawEnemiesKilled(canvas,data):
    margin=20
    text="Enemies Killed: %d" %data.enemiesKilled
    canvas.create_text(data.width//2,data.height-margin,text=text,
        font="Times 20")

def timeRedrawAll(canvas,data):
    sx=data.player.scrollX
    sy=data.player.scrollY
    
    drawGameBoard(canvas,data)
    drawBlood(canvas,data,sx,sy)
    if data.player.fire:
        drawWeapons(canvas,data,sx,sy)
    drawCollectables(canvas,data,sx,sy) 
    
    
    
    drawEnemies(canvas, data,sx,sy)   
    data.player.draw(canvas)
    data.player.drawEyes(canvas)
    
    drawWalls(canvas,data,sx,sy)
    

    data.player.drawBars(canvas,data)
    drawTime(canvas,data)
    drawEnemiesKilled(canvas,data)
###########
#In Game
###########
def inGameInit(data,weaponChose,colorChose):
    data.map=Map()
    data.cheat=False
    data.initTime=time.time()
    data.limitTime=100
    data.count=0
    data.score=0
    data.enemiesKilled=0
    
    data.blood=[]
    data.enemies=[]
    data.walls=[]
    data.collectables=[]
    for i in range(10):
        data.walls.append(Wall(data))
        
    for i in range(5):
        data.enemies.append(Enemies(data))
    data.player=player(data,weaponChose,colorChose)
    for i in range(20):
        if i%2==0:
            data.collectables.append(HP(data))
        data.collectables.append(XP(data))
def inGameKeyPressed(event,data):
    if (event.keysym not in data.pressedLetters):
        data.pressedLetters.add(event.keysym)
    
    if event.keysym=="space" and not data.player.keyCold:
        data.player.keyCold=True
        trigger(data.player,data.player.weaponChose)
    if "c" in data.pressedLetters:
        data.cheat=not data.cheat    
        
    if "r" in data.pressedLetters:
        init(data)

def inGameKeyReleased(event,data):
    if (event.keysym in data.pressedLetters):
        data.pressedLetters.remove(event.keysym)
    #initialize player speed

    if "space" not in data.pressedLetters:
        data.player.keyCold=False
def inGameMousePressed(event,data):
    pass
    
def inGameMouseMotion(event, data):
    data.player.moveEyes(event.x,event.y)    





####################################
####################################
# use the run function as-is
####################################
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, data)
        #redrawAllWrapper(canvas, data)


    def keyWrapper(keyFn, event, canvas, data):
        keyFn(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct() 
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    canvas.bind("<Motion>", lambda event:
                            mouseWrapper(mouseMotion, event, canvas, data))
    root.bind("<KeyPress>", lambda event:
                            keyWrapper(keyPressed, event, canvas, data))
    root.bind("<KeyRelease>", lambda event:
                                keyWrapper(keyReleased, event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 550)
