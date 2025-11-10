import pygame
import pygame_gui
from pieces import *

print('Select the database you have')
d=input("1.mySQL, 2.Postgres : ")
if(d.lower()=='mysql' or d=='1'):
    from dbmanagement_mySQL import *
elif(d.lower()=='postgres' or d=='2'):
    from dbmanagement_postgres import *
dbm=Database()

def login():
    f=0
    screen = pygame.display.set_mode((800,800))
    manager = pygame_gui.UIManager((800, 800))
    clock = pygame.time.Clock()
    done1=None
    done2=None
    done3=None
    done4=None
    
    Sign_in = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (200, 30)), text='Sign in', manager=manager)
    new_login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 300), (200, 30)), text='Create New ID', manager=manager)
    while True:
        dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == new_login:   #For New Login
                    username = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 330), (200, 30)),initial_text="" , manager=manager)
                    done1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 330), (70, 30)), text='Done', manager=manager)
                
                if event.ui_element == done1:   #Clicked done button - username
                    usn=username.get_text().strip()
                    if len(usn)>6 and ' ' not in usn:
                        done1.hide()
                        pin = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 360), (200, 30)),initial_text="" , manager=manager)
                        done3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 360), (70, 30)), text='Done', manager=manager)
                    else:
                        print('Invalid')
                
                if event.ui_element == done3:   #Clicked done button - password
                    for i in pin.get_text():
                        if(i.isalpha()):
                            print("Only no.")
                            f=1
                            break
                    if(f!=1):
                        passwrd=int(pin.get_text())
                        if len(pin.get_text())>5:
                            dbm.insert_data(usn,passwrd)
                            return 0
                    f=0
                #------------------------------------------------------------------------------------------------------------------------------------------#
                if event.ui_element == Sign_in: #For Sign in
                    username = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 230), (200, 30)),initial_text="" , manager=manager)
                    done2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 230), (70, 30)), text='Done', manager=manager)
                
                if event.ui_element == done2: #Clicked done button - username
                    usn=username.get_text().strip()
                    if len(usn)>6 and ' ' not in usn:
                        if dbm.username_check(usn):
                            done2.hide()
                            pin = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 260), (200, 30)),initial_text="" , manager=manager)
                            done4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((310, 260), (70, 30)), text='Done', manager=manager)
                        else:
                            print("Wrong User ID")
                    else:
                        print('Invalid')

                if event.ui_element == done4:   #Clicked done button - password
                    pc=dbm.password_check(pin,usn)
                    if(pc):
                        print('Successfully Signed in as',usn)
                        return 1
                    else:
                        print('Wrong Password')
                
            manager.process_events(event)
        manager.update(dt)
        screen.fill((0,0,0))
        manager.draw_ui(screen)
        pygame.display.update()
        
def opening():
    screen = pygame.display.set_mode((800,800))
    manager = pygame_gui.UIManager((800, 800))

    clock = pygame.time.Clock()
    bot_rating = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 100), (200, 30)),initial_text="400" , manager=manager)

    Bot = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (200, 30)), text='Bot', manager=manager)
    color =  pygame_gui.elements.UIDropDownMenu(options_list=["White", "Black","Random"], starting_option="White", relative_rect=pygame.Rect((100, 150), (200, 30)), manager=manager)
    pick = {"White": 'b', "Black": "w"}

    PvP = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 600), (200, 30)), text='PvP', manager=manager)

    while True:
        dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == PvP:
                    return "p&p",'null',0
                if event.ui_element == Bot:
                    if color.selected_option[0]=='R':
                        import random
                        pic = random.choice(['w','b'])
                        return "bot", pic, int(bot_rating.get_text())
                    return "bot", pick[color.selected_option[0]], int(bot_rating.get_text())
            manager.process_events(event)
        manager.update(dt)
        screen.fill((0,0,0))
        manager.draw_ui(screen)
        pygame.display.update()
    
