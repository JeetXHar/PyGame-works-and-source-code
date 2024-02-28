import random
from math import ceil
import pygame

pygame.init()
pygame.font.init()
color={
    "black" :  (0,0,0),
    "white" :  (255,255,255),
    "road"  :  (64,64,64),
    "sky"   :  (135,206,250),
    "brown" :  (150,75,0),
    "green" :  (0,255,0),
    "blue"  :  (0,0,225)
}

num_font=pygame.font.SysFont('comicsansms',20)
menu_font=pygame.font.SysFont("mvboli",16)
gameover_font=pygame.font.SysFont("inkfree",50)
num_color={
    1: "black",
    2: "green",
    3: "red",
    4: "orange",
    5: "yellow",
    6: "purple",
    7: "blue",
    8: "pink",


    -1: "brown",
    0: "dark green"
}

top_margin=70
cell_color=(200,200,200)
used_cell_color=(100,100,100)

# cell_color="grey"
# used_cell_color="dark grey"

class baseMinesweepergame:

    def __init__(self, board: tuple[int] = (20,20), mines: int = 40) -> None:
        
        self.__wid,self.__hgt=board
        self.__mines=mines
        self.__build()
        self.__count_used_cells=0

    def rebuild (self, board: tuple[int] = (10,10), mines: int = 8) -> None:
        self.__wid,self.__hgt=board
        self.__mines=mines
        self.__build()

    def __build(self):
        self.__realboard=[[0]*self.__wid for i in range(self.__hgt)]
        self.__displayboard=[[-1]*self.__wid for i in range(self.__hgt)]

        self.__minesloc=list(random.sample([(i,j) for i in range(self.__hgt) for j in range(self.__wid)],
                                            self.__mines))
        self.__minesloc.sort()
        for i,j in self.__minesloc:

            self.__realboard[i][j]=-1

            for di in {-1,0,1}:
                for dj in {-1,0,1}:
                    if di==dj==0: continue
                    if 0<=i+di<self.__hgt and 0<=j+dj<self.__wid and self.__realboard[i+di][j+dj]!=-1:
                        self.__realboard[i+di][j+dj]+=1
        
    def check(self, i : int, j : int):
        if self.__displayboard[i][j]!=-1:
            return False
        if self.__realboard[i][j]==-1:
            return True
        self.__displayboard[i][j]=self.__realboard[i][j]
        self.__count_used_cells+=1
        if self.__displayboard[i][j]==0:
            for di in {-1,0,1}:
                for dj in {-1,0,1}:
                    if 0<=i+di<self.__hgt and 0<=j+dj<self.__wid and self.__displayboard[i+di][j+dj]==-1:
                        self.check(i+di,j+dj)
        return False
    
    def placeflag(self,i : int,j : int):
        if self.__displayboard[i][j]==-1:
            self.__displayboard[i][j]=-2
        elif self.__displayboard[i][j]==-2:
            self.__displayboard[i][j]=-1

    def getdisplay(self):
        return [x.copy() for x in self.__displayboard]
    
    def getfield(self):
        return [x.copy() for x in self.__realboard]
    
    def getmineloc(self):
        return [x for x in self.__minesloc]

    def getheight(self):
        return self.__hgt

    def getwidth(self):
        return self.__wid

    def is_game_complete(self):
        return self.__wid*self.__hgt-self.__count_used_cells==self.__mines

    def exit(self):
        del self.__displayboard
        del self.__realboard

class gameUI:

    def __init__(self, width: int = 600, height: int = 600+top_margin) -> None:
        
        self.currectstate="home"
        self.__win=pygame.display.set_mode((width,height))
        pygame.display.set_caption("Minesweeper")
        self.__clock=pygame.time.Clock()
        self.mouseclicked=False
        self.mouseclickedloc=""
        self.placeflag=False
        self.__icon=pygame.image.load("resources/icon.png")
        self.__homelogo=pygame.transform.rotozoom(pygame.image.load("resources/homelogo.png"),0,0.4)
        self.__back=pygame.transform.rotozoom(pygame.image.load("resources/back.png"),0,0.35)
        self.__home=pygame.transform.rotozoom(pygame.image.load("resources/home.png"),0,0.055)
        self.__bomb=pygame.image.load("resources/bomb.png")
        self.__flag=pygame.image.load("resources/flag.png")
        self.__game=None
        pygame.display.set_icon(self.__icon)

    def display(self)->None:
        self.__win.fill(color["sky"])
        
        width,height=pygame.display.get_surface().get_size()
        mouse_pos=pygame.mouse.get_pos()
        t=True
        if self.currectstate=="home":
            t=self.displayHome(width,height,mouse_pos)
        elif self.currectstate=="select size":
            self.displaySelect(width,height,mouse_pos)
        elif self.currectstate=="game":
            self.displayGame(width,height,mouse_pos)
        elif self.currectstate=="gameover":
            self.gameover(width,height,mouse_pos)
        if not t: return t
        pygame.display.update()
        self.__clock.tick(60)
        return True
    
    def displayHome(self,width,height,mouse_pos):
            self.__win.blit(self.__homelogo,(width//2-self.__homelogo.get_width()//2,
                                             50))
            
            f=True
            if self.__game:
                f=False
                cont_game=menu_font.render("CONTINUE GAME", True, "white")
                cont_game_button=pygame.Rect(width//2-cont_game.get_width()//2-10,
                                            height//2-cont_game.get_height()//2-100,
                                            cont_game.get_width()+20,
                                            cont_game.get_height()+20)
                
                if cont_game_button.x<=mouse_pos[0]<=cont_game_button.x+cont_game.get_width()+20 and cont_game_button.y<=mouse_pos[1]<=cont_game_button.y+cont_game.get_height()+20:
                    pygame.draw.rect(self.__win,"grey",cont_game_button)
                else:
                    pygame.draw.rect(self.__win,"black",cont_game_button)
                
                self.__win.blit(cont_game,(cont_game_button.x+10,cont_game_button.y+10))



            new_game=menu_font.render("NEW GAME", True, "white")
            new_game_button=pygame.Rect(width//2-new_game.get_width()//2-10,
                                        height//2-new_game.get_height()//2-100*f,
                                        new_game.get_width()+20,
                                        new_game.get_height()+20)
            
            if new_game_button.x<=mouse_pos[0]<=new_game_button.x+new_game.get_width()+20 and new_game_button.y<=mouse_pos[1]<=new_game_button.y+new_game.get_height()+20:
                pygame.draw.rect(self.__win,"grey",new_game_button)
            else:
                pygame.draw.rect(self.__win,"black",new_game_button)
            
            self.__win.blit(new_game,(new_game_button.x+10,new_game_button.y+10))

            quit=menu_font.render("QUIT", True, "white")
            quit_button=pygame.Rect(width//2-quit.get_width()//2-10,
                                        height//2-quit.get_height()//2+100-100*f,
                                        quit.get_width()+20,
                                        quit.get_height()+20)
            
            if quit_button.x<=mouse_pos[0]<=quit_button.x+quit.get_width()+20 and quit_button.y<=mouse_pos[1]<=quit_button.y+quit.get_height()+20:
                pygame.draw.rect(self.__win,"grey",quit_button)
            else:
                pygame.draw.rect(self.__win,"black",quit_button)
            
            self.__win.blit(quit,(quit_button.x+10,quit_button.y+10))
            
            if self.mouseclicked:
                self.mouseclicked=False
                if new_game_button.collidepoint(self.mouseclickedloc):
                    self.currectstate="select size"
                if quit_button.collidepoint(self.mouseclickedloc):
                    self.exit()
                    return False
                if not f and cont_game_button.collidepoint(self.mouseclickedloc):
                    self.currectstate="game"
            return True

    def displayGame(self,width,height,mouse_pos):
            self.__win.blit(self.__back,(10,10))
            back=self.__back.get_rect()
            back.x=back.y=10
            self.__win.blit(self.__home,(70,10))
            home=self.__home.get_rect()
            home.x=70
            home.y=10

            self.cellw=width//self.__game.getwidth()
            self.cellh=(height-top_margin)//self.__game.getheight()
            
            tempflag=pygame.transform.rotozoom(self.__flag,0,self.cellw/450)
            dx=self.cellw/2 - tempflag.get_width()/2
            dy=self.cellh/2 - tempflag.get_height()/2


            if self.mouseclicked:
                self.mouseclicked=False

                if back.collidepoint(self.mouseclickedloc):
                    self.currectstate="select size"
                if home.collidepoint(self.mouseclickedloc):
                    self.currectstate="home"
                i,j=self.get_cell_loc(mouse_pos=mouse_pos)
                if self.__game.getheight()>i>=0 and self.__game.getwidth() >j>=0 :
                    state = self.__game.check(i,j)
                    if state:
                        self.currectstate="gameover"
            
            if self.placeflag:
                self.placeflag=False
                i,j = self.get_cell_loc(mouse_pos)
                if 0<=i<self.__game.getheight() and 0<=j<self.__game.getwidth():
                    self.__game.placeflag(i,j)

            for i, row in enumerate(self.__game.getdisplay()):
                y=self.cellh*i+top_margin
                for j, val in enumerate(row):
                    x=self.cellw*j
                    pygame.draw.rect(
                        self.__win,
                        used_cell_color if val>=0 else cell_color,
                        (x,y,self.cellw,self.cellh)
                    )
                    pygame.draw.rect(self.__win,"black",(x,y,self.cellw,self.cellh),1)
                    
                    if 9>val>0:
                        text=num_font.render(str(val),1,num_color[val])
                        self.__win.blit(text,(x + self.cellw/2 - text.get_width()/2,
                                              y + self.cellh/2 - text.get_height()/2))
                    elif val==-2:
                        self.__win.blit(tempflag,(x + dx,y + dy))
            if self.__game.is_game_complete():
                self.currectstate="gameover"

    def displaySelect(self,width,height,mouse_pos):
        self.__win.blit(self.__homelogo,(width//2-self.__homelogo.get_width()//2,
                                             50))
        
        self.__win.blit(self.__back,(10,10))
        back=self.__back.get_rect()
        back.x=back.y=10

        size=[10,30,40]
        mines=[12,135,304]
        size_button=[0]*3

        for i,s in enumerate(["10 X 10", "30 X 30", "40 X 40"]):

            size_=menu_font.render(s, True, "white")
            size_button[i]=pygame.Rect(width//2-size_.get_width()//2-10,
                                            height//2-size_.get_height()//2-100+50*i,
                                            size_.get_width()+20,
                                            size_.get_height()+20)
            
            if size_button[i].x<=mouse_pos[0]<=size_button[i].x+size_.get_width()+20 and size_button[i].y<=mouse_pos[1]<=size_button[i].y+size_.get_height()+20:
                pygame.draw.rect(self.__win,"grey",size_button[i])
            else:
                pygame.draw.rect(self.__win,"black",size_button[i])
            
            self.__win.blit(size_,(size_button[i].x+10,size_button[i].y+10))

        if self.mouseclicked:
                self.mouseclicked=False
                for i,x in enumerate(size_button):
                    if x.collidepoint(self.mouseclickedloc):
                        if self.__game:
                            self.__game.exit()

                        self.__game=baseMinesweepergame((size[i],size[i]),mines[i])
                        self.currectstate="game"
                        return
                if back.collidepoint(self.mouseclickedloc):
                    self.currectstate="home"
    
    def gameover(self,width,height,mouse_pos):
            self.__win.blit(self.__back,(10,10))
            back=self.__back.get_rect()
            back.x=back.y=10
            self.__win.blit(self.__home,(70,10))
            home=self.__home.get_rect()
            home.x=70
            home.y=10
            self.cellw=width//self.__game.getwidth()
            self.cellh=(height-top_margin)//self.__game.getheight()

            if self.mouseclicked:
                self.mouseclicked=False
                if back.collidepoint(self.mouseclickedloc):
                    self.currectstate="select size"
                    self.__game.exit()
                    self.__game=None
                    return
                if home.collidepoint(self.mouseclickedloc):
                    self.currectstate="home"
                    self.__game.exit()
                    self.__game=None
                    return
            
            tempflag=pygame.transform.rotozoom(self.__flag,0,self.cellw/450)
            dx=self.cellw/2 - tempflag.get_width()/2
            dy=self.cellh/2 - tempflag.get_height()/2

            for i, row in enumerate(self.__game.getdisplay()):
                y=self.cellh*i+top_margin
                for j, val in enumerate(row):
                    x=self.cellw*j
                    pygame.draw.rect(
                        self.__win,
                        used_cell_color if val>=0 else cell_color,
                        (x,y,self.cellw,self.cellh)
                    )
                    pygame.draw.rect(self.__win,"black",(x,y,self.cellw,self.cellh),1)
                    
                    if 9>val>0:
                        text=num_font.render(str(val),1,num_color[val])
                        self.__win.blit(text,(x + self.cellw/2 - text.get_width()/2,
                                              y + self.cellh/2 - text.get_height()/2))
                    elif val==-2:
                        self.__win.blit(tempflag,(x + dx,
                                                    y + dy))
            
            tempbomb=pygame.transform.rotozoom(self.__bomb,0,self.cellh/330)

            for i,j in self.__game.getmineloc():
                x=self.cellw*j
                y=self.cellh*i+top_margin
                self.__win.blit(tempbomb,(x,y))
            
            if self.__game.is_game_complete():
                text=gameover_font.render("YOU WON",1,"blue")
                self.__win.blit(text,(width/2-text.get_width()/2,(height-top_margin)/2-text.get_height()/2+top_margin))
            else:
                text=gameover_font.render("GAND MARA LI?",1,"blue")
                self.__win.blit(text,(width/2-text.get_width()/2,(height-top_margin)/2-text.get_height()/2+top_margin))

    def get_cell_loc(self,mouse_pos):
        i=int((mouse_pos[1]-top_margin)/self.cellw)
        j=int((mouse_pos[0])/self.cellh)
        return (i,j)

    def exit(self):
        if self.__game:
            self.__game.exit()
            self.__game=None
        pygame.quit()