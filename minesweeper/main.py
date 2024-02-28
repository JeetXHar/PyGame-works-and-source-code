import pygame
pygame.init()
pygame.font.init()
from game import gameUI


def main():
    _run=True
    game_instance=gameUI()
    while(_run):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                _run=False
                game_instance.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                game_instance.mouseclicked=True
                game_instance.mouseclickedloc=event.pos
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==3:
                game_instance.placeflag=True
                game_instance.mouseclickedloc=event.pos
        
        if not _run: break
        _run=game_instance.display()

    


if __name__=="__main__":
    main()