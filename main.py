from pygame import *
import time
from board import *
from popup import *
from UI import *
import globals
import math

fps = 60
whiteSqColor = (235, 236, 208)
blackSqColor = (115,149,82)
grid_size = 80
piece_size = 64
rcolor=(200, 210, 250)

# while(login()!=1):
#     continue
    
mode, team, botrating = opening()
board = Board(mode,botrating,'normal')
pygame.init()
screen = pygame.display.set_mode((grid_size*8.5, grid_size*8 ))
pygame.display.set_caption("Chess!")

def draw():
    screen.fill((255,255,255))
    #BOARD
    for i in range(8):
        for j in range(8):
            if(i+j)%2 == 0:
                color = whiteSqColor
            else:
                color = blackSqColor
            pygame.draw.rect(screen, color, pygame.Rect(j*grid_size, i*grid_size, grid_size, grid_size))
            
            #PIECES
            if(board.board[i][j].code != " "):
                offset = (grid_size-piece_size)/2
                screen.blit(Pieces.getImage(board.board[i][j].code),(j*grid_size + offset, i*grid_size + offset), pygame.Rect(0,0,piece_size, piece_size))
    
    #Adding the highlight feature for the previous made move
    if (len(board.history) > 0):
        x1, y1, x2, y2 = board.history[-1][:4]
        print(x1, y1, x2, y2)
        pygame.draw.rect(screen, (255, 128, 128), pygame.Rect(x1*grid_size, y1*grid_size, grid_size, grid_size))

        pygame.draw.rect(screen, (255, 128, 128), pygame.Rect(x2*grid_size, y2*grid_size, grid_size, grid_size))
        screen.blit(Pieces.getImage(board.board[y2][x2].code),(x2*grid_size + offset, y2*grid_size + offset), pygame.Rect(0,0,piece_size, piece_size))


    
    pygame.draw.rect(screen, (64,64,64), pygame.Rect(8*grid_size, 0, grid_size, 8*(1 - (1 / (1 + math.exp(-0.004 * board.get_eval()["value"]))))*grid_size))
    pygame.display.update()
    globals.chess_board_copy = screen.copy()

    

#print('Mode =',mode,'\nColour =','White' if team=='b' else 'Black','\nBot Rating =',botrating)

draw()
running = True
x1,y1,x2,y2 = 0,0,0,0

while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            running = False

        elif(event.type == pygame.MOUSEBUTTONDOWN):
            x1, y1 = pygame.mouse.get_pos()
            x1, y1 = (x1//grid_size), (y1//grid_size)
            #print(x1,y1)

        elif(event.type == pygame.MOUSEBUTTONUP):
            x2, y2 = pygame.mouse.get_pos()
            x2, y2 = (x2//grid_size), (y2//grid_size)
            if x2 in range(8) and y2 in range(8):
                c = board.edit(x1,y1,x2,y2,"normal",mode,team)
            if c=='GO':
                print("GAME OVER")
                running = False
            draw()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board.undo(mode,team,'NC')
                draw()
            elif event.key == pygame.K_r:
                if(reset_popup()):
                    print("-"*40,"Reset","-"*40)
                    board.reset(mode,'normal',botrating)   
                    draw()
            elif event.key == pygame.K_m:
                mode='null'
                team='null'
                botrating=0
                mode,team,botrating=opening()
                print("-"*40,"Mode Changed","-"*40)
                #print('Mode =',mode,'\nColour =',team,'\nBot Rating =',botrating)
                board.reset(mode,'normal',botrating)
                pygame.display.set_mode((grid_size*8, grid_size*8))
                pygame.display.set_caption("Chess!")
                draw()
            elif event.key == pygame.K_ESCAPE:
                running = False

    time.sleep(1/fps)
    
    