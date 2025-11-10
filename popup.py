import pygame
from pieces import *
import globals


pygame.init()
board_grid_size = 80


def promotion_popup(team):
    pieces = ['q','kr','n','b']
    size = 80
    offset = (size-64)/2
    chess_board = globals.chess_board_copy
    
    screen = pygame.display.set_mode((size*9, size*8))
    pygame.display.set_caption("Select the piece to promote to.")
    #DRAW
    screen.fill((255,255,255))
    screen.blit(chess_board, (0,0), pygame.Rect(0,0,size*8,size*8))
    screen.fill((200, 200, 200), special_flags=pygame.BLEND_RGB_MULT)
    for i in range(len(pieces)):
        screen.blit(Pieces.getImage(pieces[i].upper() if team == 1 else pieces[i]), (8*size + offset, i*size + offset) , pygame.Rect(0, 0, 80, 80))
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
            if(event.type == pygame.MOUSEBUTTONDOWN):
                y = pygame.mouse.get_pos()[1]
                y //= size
                if y in range(4):
                    pygame.display.set_mode((board_grid_size*8.5, board_grid_size*8))
                    pygame.display.set_caption("Chess!")
                    return pieces[y].upper() if team == 1 else pieces[y]

def reset_popup():
    pygame.init()
    screen = pygame.display.set_mode((256, 64))
    pygame.display.set_caption("Reset?")

    font = pygame.font.SysFont(None, 32)
    running = True

    while running:
        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (0, 200, 0), (32, 10, 80, 40))  # Yes button
        pygame.draw.rect(screen, (200, 0, 0), (144, 10, 80, 40))  # No button

        screen.blit(font.render("Yes", True, (255, 255, 255)), (52, 20))
        screen.blit(font.render("No", True, (255, 255, 255)), (170, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                pygame.display.set_mode((board_grid_size*8.5, board_grid_size*8))
                pygame.display.set_caption("Chess!")
                if 32 <= x <= 112 and 10 <= y <= 50:
                    return True
                elif 144 <= x <= 224 and 10 <= y <= 50:
                    return False

    