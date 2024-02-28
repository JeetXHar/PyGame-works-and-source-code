from os import closerange
import pygame
import time
import random


pygame.init()
#colours:
black=(0,0,0)
white=(255,255,255)
road=(64,64,64)
green=(0,255,0)

width=800
height=600

gamedisplay=pygame.display.set_mode((width,height))
pygame.display.set_caption('Crazy Driver')
clock=pygame.time.Clock()

icon=pygame.image.load('sources/car.png')
pygame.display.set_icon(icon)


carimg=pygame.image.load('sources/images.png')
carwidth=carimg.get_width()
carheight=carimg.get_height()

enemyimg=pygame.image.load('sources/enemy.png')
enemyw=enemyimg.get_width()
enemyh=enemyimg.get_height()


car = lambda x,y : gamedisplay.blit(carimg,(x,y))
enemy=lambda x,y : gamedisplay.blit(enemyimg,(x,y))

def score(n):
    font=pygame.font.SysFont(None,25)
    text=font.render('Score: '+str(n),True,green)
    gamedisplay.blit(text,(0,0))

def text_objects(text,font):
    textsurface=font.render(text,True,white)
    return textsurface,textsurface.get_rect()

def message(s):
    text=pygame.font.Font('freesansbold.ttf',60)
    textsurf,textrect=text_objects(s,text)
    textrect.center=((width/2,height/2))
    gamedisplay.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(2)
    game()

def game():
    x=(width * 0.5-carwidth/2)
    y=(height-carheight-5)
    x_delta=0
    play=True

    s=0

    enemyx=random.randrange(0,width-enemyw)
    enemyy=-300
    speed=3

    while play:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_delta=-5
                elif event.key == pygame.K_d:
                    x_delta=5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_delta=0

        x+=x_delta

        gamedisplay.fill(road)

        #objects(objectsx,objectsy,objectsw,objectsh,black)
        enemy(enemyx,enemyy)
        enemyy+=speed+s
        score(s)
        if enemyy>height:
            enemyy=-enemyh
            enemyx=random.randrange(0,width-enemyw)
            s+=1

        if x>width-carwidth:
            x=width-carwidth
            x_delta=0
        elif x<0:
            x=0
            x_delta=0
        car(x,y)
        if y<enemyy+enemyh-10 and (not (x+carwidth<enemyx+10 or enemyx+enemyw<x+10)):
            message('Crashed!! Score: '+str(s))
        pygame.display.update()
        clock.tick(60)
        #print(height,width)

game()
pygame.quit()
quit()
 