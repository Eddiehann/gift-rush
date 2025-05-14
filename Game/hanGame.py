# Name: Eddie Han
# Date: Oct.28, 2020
# Class: ICS3U1-01
# Description: A top-down puzzle game

import pygame
pygame.init()

#colours -----------------------------------------------------------------------
WHITE = (223, 246, 245)
GREY = (48, 44, 46)
L_GREY = (160, 147, 142)
SILVER = (207, 198, 184)
RED = (230, 72, 46)
D_RED = (169, 59, 59)
GREEN = (113, 170, 52)
D_GREEN = (57, 123, 68)
L_BLUE = (138, 235, 241)
BLUE = (40, 204, 223)
D_BLUE = (57, 120, 168)
BROWN = (160, 91, 83)
D_BROWN = (122, 68, 74)
SKIN = (238, 161, 96)
D_SKIN = (191, 121, 88)
YELLOW = (244, 180, 27)

# variables & lists ------------------------------------------------------------
#player info
player_x = 80
player_y = 240
can_move = 0
health = 10000
movement_enabled = True
movement_time = 0
invincible = False
damaged_time = 0

#wall locations
wall_pos = [[80,192],[128,192],[176,192],[224,192],[272,192],[320,192],[368,192],[416,192],[464,192],[512,192],[560,192],[80,288],[128,288],[176,288],[224,288],[272,288],[320,288],[368,288],[416,288],[464,288],[512,288],[560,288],[32,240],[608,240]]

#spike info
spike_pos = [[272,240]]
start_state = [1]
next_state = 0
extend_time = 0

# gift locations
gift_pos = [[320,240]]

# exit locations
exit_pos = [560,240]

gifts_collected = 0
gift_active = [True, True] #determines if a gift has been collected
enter_exit = False

# screen setup -----------------------------------------------------------------
width = 640
height = 360
SIZE = (width, height)
screen = pygame.display.set_mode(SIZE)
screen.fill(GREY)
font = pygame.font.SysFont("Arial", 20)
endScore = pygame.font.SysFont("Arial", 30)

# images -----------------------------------------------------------------------
menu_image = pygame.image.load("hanMenu.png")
level0 = pygame.image.load("hanInstructionLevel.png")
level1 = pygame.image.load("hanLevel1.png")
level2 = pygame.image.load("hanLevel2.png")
level3 = pygame.image.load("hanLevel3.png")
win = pygame.image.load("hanWon.png")
lose = pygame.image.load("hanLost.png")

# sounds -----------------------------------------------------------------------
switch_tab = pygame.mixer.Sound("switchTab.wav")
select = pygame.mixer.Sound("select.wav")
step = pygame.mixer.Sound("step.wav")
hurt = pygame.mixer.Sound("hurt.wav")
pickup = pygame.mixer.Sound("pickup.wav")
bgm = pygame.mixer.Sound("winterSnow.wav")

level_image = level0
level1_gifts = 0
level2_gifts = 0
level3_gifts = 0

# sprites ----------------------------------------------------------------------
def playerSprite(x,y): # draws the player
    # outline
    pygame.draw.rect(screen, GREY, pygame.Rect(x-9, y-12, 18, 24))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-6, y-15, 15, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+9, y-12, 3, 12))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+9, y-12, 3, 12))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+12, y-9, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-15, y-9, 6, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-12, y-3, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-12, y+3, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+9, y+3, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-6, y+12, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+3, y+12, 3, 3))

    # body
    pygame.draw.rect(screen, GREEN, pygame.Rect(x-6, y, 9, 6))
    pygame.draw.rect(screen, D_GREEN, pygame.Rect(x+3, y, 3, 6))
    pygame.draw.rect(screen, BROWN, pygame.Rect(x-6, y+6, 6, 3))
    pygame.draw.rect(screen, D_BROWN, pygame.Rect(x, y+6, 6, 3))
    pygame.draw.rect(screen, D_SKIN, pygame.Rect(x, y, 3, 3))
    pygame.draw.rect(screen, D_SKIN, pygame.Rect(x+6, y+3, 3, 3))
    pygame.draw.rect(screen, SKIN, pygame.Rect(x-9, y+3, 3, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x-6, y+9, 3, 3))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x+3, y+9, 3, 3))

    # head
    pygame.draw.rect(screen, D_GREEN, pygame.Rect(x-6, y-12, 6, 9))
    pygame.draw.rect(screen, SKIN, pygame.Rect(x-3, y-9, 12, 9))
    pygame.draw.rect(screen, GREY, pygame.Rect(x, y-6, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+6, y-6, 3, 3))
    pygame.draw.rect(screen, SKIN, pygame.Rect(x-6, y-6, 3, 3))
    pygame.draw.rect(screen, D_GREEN, pygame.Rect(x-9, y-6, 3, 3))
    pygame.draw.rect(screen, D_SKIN, pygame.Rect(x-9, y-9, 3, 3))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-12, y-6, 3, 3))
    pygame.draw.rect(screen, BROWN, pygame.Rect(x-3, y-9, 3, 6))
    pygame.draw.rect(screen, BROWN, pygame.Rect(x, y-12, 6, 3))
    pygame.draw.rect(screen, BROWN, pygame.Rect(x+3, y-9, 6, 3))
    pygame.draw.rect(screen, D_BROWN, pygame.Rect(x+6, y-12, 3, 3))
    pygame.draw.rect(screen, D_BROWN, pygame.Rect(x+3, y-12, 6, 3))
    pygame.draw.rect(screen, D_BROWN, pygame.Rect(x+9, y-9, 6, 3))

def giftSprite(x,y): # draws the gift
    pygame.draw.rect(screen, GREY, pygame.Rect(x-12, y-9, 24, 18))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-9, y-12, 18, 24))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-6, y-15, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+3, y-15, 3, 3))
    pygame.draw.rect(screen, GREEN, pygame.Rect(x-9, y-9, 18, 9))
    pygame.draw.rect(screen, D_GREEN, pygame.Rect(x-9, y, 18, 9))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-6, y-6, 12, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x-3, y-9, 6, 9))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-3, y, 6, 9))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-9, y+3, 18, 3))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-3, y, 6, 9))
    pygame.draw.rect(screen, RED, pygame.Rect(x-9, y-9, 3, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x+6, y-9, 3, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x-6, y-12, 3, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x+3, y-12, 3, 3))
    
def spikeBase(x,y): # draws the sprite for the retracted spike
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-21, y-21, 42, 42))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-21, y-18, 42, 36))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-18, y-21, 36, 42))
    pygame.draw.rect(screen, L_BLUE, pygame.Rect(x-18, y-18, 36, 33))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x-12, y-15, 24, 27))
    pygame.draw.rect(screen, BLUE, pygame.Rect(x-15, y-12, 30, 21))
    pygame.draw.rect(screen, D_BLUE, pygame.Rect(x-18, y+15, 36, 3))
    pygame.draw.rect(screen, D_BLUE, pygame.Rect(x-6, y-3, 12, 12))
    pygame.draw.rect(screen, D_BLUE, pygame.Rect(x-9, y, 18, 6))
    pygame.draw.rect(screen, L_BLUE, pygame.Rect(x-6, y, 12, 6))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-6, y, 6, 3))

def spikeExtend(x,y): # draws the sprite for the extended spike
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-6, y-9, 6, 9))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-6, y-6, 3, 6))
    pygame.draw.rect(screen, L_BLUE, pygame.Rect(x, y-6, 3, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-9, y-3, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-6, y-9, 3, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-3, y-12, 6, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x, y-9, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+3, y-6, 3, 6))

def exitSprite(x,y): # draws the sprite for the exit (santa's sleigh)
    # outline
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-21, y-21, 42, 42))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-18, y+18, 33, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-21, y+12, 39, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-18, y+9, 39, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-21, y, 39, 9))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-21, y-3, 36, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-18, y-6, 30, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-12, y-15, 24, 9))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-15, y-15, 3, 6))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-9, y-18, 21, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-6, y-21, 15, 3))

    # sleigh
    pygame.draw.rect(screen, RED, pygame.Rect(x-18, y, 9, 9))
    pygame.draw.rect(screen, RED, pygame.Rect(x-9, y+3, 24, 6))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-15, y+9, 27, 3))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-18, y+6, 3, 3))
    pygame.draw.rect(screen, D_RED, pygame.Rect(x+12, y+6, 3, 3))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x-9, y, 3, 3))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x+12, y, 3, 3))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x-6, y+3, 18, 3))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x-18, y-3, 9, 3))
    pygame.draw.rect(screen, L_GREY, pygame.Rect(x-12, y+12, 3, 3))
    pygame.draw.rect(screen, L_GREY, pygame.Rect(x+6, y+12, 3, 3))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x+15, y+12, 3, 3))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x-18, y+15, 33, 3))

    # santa
    pygame.draw.rect(screen, D_RED, pygame.Rect(x-6, y-6, 6, 6))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x, y-6, 9, 6))
    pygame.draw.rect(screen, RED, pygame.Rect(x-3, y-3, 6, 3))
    pygame.draw.rect(screen, SKIN, pygame.Rect(x-3, y-15, 12, 9))
    pygame.draw.rect(screen, GREY, pygame.Rect(x, y-12, 3, 3))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+6, y-12, 3, 3))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x-3, y-15, 3, 6))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x, y-18, 6, 3))
    pygame.draw.rect(screen, SILVER, pygame.Rect(x+3, y-15, 6, 3))
    pygame.draw.rect(screen, L_GREY, pygame.Rect(x+6, y-18, 3, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x-6, y-18, 6, 3))
    pygame.draw.rect(screen, RED, pygame.Rect(x-9, y-15, 6, 6))
    pygame.draw.rect(screen, SKIN, pygame.Rect(x-6, y-12, 3, 3))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-12, y-12, 3, 3))
    
def selectLeft(x,y):
    # top bracket
    pygame.draw.rect(screen, GREY, pygame.Rect(x+4, y, 16, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x, y+4, 8, 16))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+8, y+8, 4, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+8, y+8, 8, 4))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x+4, y+4, 12, 4))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x+4, y+4, 4, 12))    
    
    # bottom bracket
    pygame.draw.rect(screen, GREY, pygame.Rect(x, y+44, 8, 16))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+4, y+56, 16, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+8, y+48, 4, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x+8, y+52, 8, 4))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x+4, y+48, 4, 12))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x+4, y+56, 12, 4))     
    
def selectRight(x,y):
    # top bracket    
    pygame.draw.rect(screen, GREY, pygame.Rect(x-19, y, 16, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-7, y+4, 8, 16))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-15, y+8, 8, 4))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-11, y+8, 4, 8))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-15, y+4, 12, 4))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-7, y+4, 4, 12))
    
    # bottom bracket    
    pygame.draw.rect(screen, GREY, pygame.Rect(x-7, y+40, 8, 16))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-19, y+52, 16, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-11, y+44, 4, 8))
    pygame.draw.rect(screen, GREY, pygame.Rect(x-15, y+48, 8, 4))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-7, y+44, 4, 12))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x-15, y+52, 12, 4))
    
# functions --------------------------------------------------------------------
# draws the player, main function
def drawPlayer(x,y):
    global gifts_collected
    global spike_pos
    
    screen.blit(level_image, pygame.Rect(0, 0, width, height))
    drawExit(exit_pos[0], exit_pos[1])    
    
    for gift in range(len(gift_pos)):
        drawGift(gift_pos[gift][0], gift_pos[gift][1], gift+1)
    
    for spike in range(len(spike_pos)):
        drawSpikes(spike_pos[spike][0],spike_pos[spike][1],start_state[spike])
    
    playerSprite(x,y) # player
    
    # score
    text = font.render(str(gifts_collected), 1, GREY)
    screen.blit(text, pygame.Rect(216,20,15,21))
    
    if health < 3:
        pygame.draw.rect(screen, BLUE, pygame.Rect(141,14,36,33))
        if health < 2:
            pygame.draw.rect(screen, BLUE, pygame.Rect(96,14,36,33))
                 
    
    pygame.display.update()

#draws the gifts
def drawGift(x,y, gift_num):
    global gifts_collected
    global gift_active
    global level1_gifts
    global level2_gifts
    global level3_gifts
    
    if gift_active[gift_num-1]: 
        if player_x != x or player_y != y:
            giftSprite(x,y)
        else:
            pickup.play()
            if level == 0:
                gifts_collected += 1
            if level == 1:
                level1_gifts += 1
            if level == 2:
                level2_gifts += 1
            if level == 3:
                level3_gifts += 1
            if level == 1 or level == 2 or level == 3:
                gifts_collected = level1_gifts + level2_gifts + level3_gifts
            gift_active[gift_num-1] = False
            
# draws the spikes
def drawSpikes(x,y,state):
    global next_state
    spikeBase(x,y)
    if next_state % 4 == 2 and state == 2:
        spikeExtend(x,y)  
    elif next_state % 4 == 0 and state == 1:
        spikeExtend(x,y)

# draws the exit (end of the level)        
def drawExit(x,y):
    global enter_exit
    
    if enter_exit == False:
        if player_x != x or player_y != y:
            exitSprite(x,y)
        else:
            enter_exit = True
            
# game -------------------------------------------------------------------------
running = True
in_menu = True
start_music = True
selected = 10
level = 0
myClock = pygame.time.Clock()

while running:
    # start playing the bgm
    if start_music:
        bgm.play(-1)
        start_music = False
        
    # start in the menu screen
    while in_menu:
        screen.blit(menu_image, pygame.Rect(0, 0, width, height)) 
        
        # selects an option determined by the keys pressed
        if selected % 2 == 0:
            selectLeft(240,176)
            selectRight(399,176)
        elif selected % 2 == 1:
            selectLeft(248,232)
            selectRight(395,232)
        pygame.display.flip()
        
        # get the event
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()

            # check if the player pressed enter/return
            if evnt.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP] or pressed[pygame.K_DOWN]:
                    switch_tab.play()
                    selected += 1
                if selected % 2 == 0 and pressed[pygame.K_RETURN]:
                    select.play()
                    in_menu = False
                elif selected % 2 == 1 and pressed[pygame.K_RETURN]:
                    select.play()
                    pygame.quit()        
                
    # get the current tick
    ticks = pygame.time.get_ticks()    

# no keys pressed --------------------------------------------------------------
    screen.blit(level_image, pygame.Rect(0, 0, width, height)) 
    text = font.render(str(gifts_collected), 1, GREY)
    screen.blit(text, pygame.Rect(216,20,15,21))    
    drawExit(exit_pos[0], exit_pos[1]) 
    for gift in range(len(gift_pos)):
        drawGift(gift_pos[gift][0], gift_pos[gift][1], gift+1)
    for spike in range(len(spike_pos)):
        drawSpikes(spike_pos[spike][0],spike_pos[spike][1],start_state[spike])    
    drawPlayer(player_x, player_y)
    
    
# player movement --------------------------------------------------------------
    # enable the player's movement 0.15 seconds after last moved
    if ticks - movement_time > 150:
        movement_enabled = True    
        
    # disable the player's invincibility after 1 second
    if ticks - damaged_time > 1000:
        invincible = False    
        
    if ticks - extend_time > 350:
        next_state += 1
        extend_time = ticks

    # quit the game when the user clicks the red cross 
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            running = False
        
        # check if any keys are pressed
        if evnt.type == pygame.KEYDOWN and movement_enabled:
            pressed =  pygame.key.get_pressed()
            
            # move the player towards the location determined by the key pressed
            if pressed[pygame.K_LEFT]:
                dest_x = player_x - 48
                dest_y = player_y
                
                step.play()
                
                # check for walls
                for wall in range(len(wall_pos)):
                    if dest_x == wall_pos[wall][0] and dest_y == wall_pos[wall][1]:
                        can_move += 1
                
                # move the player        
                if can_move == 0:
                    for steps in range(24):
                        player_x -= 2
                        drawPlayer(player_x, player_y)       
                can_move = 0
                            
            elif pressed[pygame.K_RIGHT]:
                dest_x = player_x + 48
                dest_y = player_y
                
                step.play()
            
                for wall in range(len(wall_pos)):
                    if dest_x == wall_pos[wall][0] and dest_y == wall_pos[wall][1]:
                        can_move += 1                
                
                if can_move == 0:
                    for steps in range(24):
                        player_x += 2
                        drawPlayer(player_x, player_y)  
                can_move = 0
                        
            elif pressed[pygame.K_UP]:
                dest_x = player_x 
                dest_y = player_y - 48
                
                step.play()
            
                for wall in range(len(wall_pos)):
                    if dest_x == wall_pos[wall][0] and dest_y == wall_pos[wall][1]:
                        can_move += 1                
                
                if can_move == 0:                
                    for steps in range(24):
                        player_y -= 2
                        drawPlayer(player_x, player_y)
                can_move = 0
                        
            elif pressed[pygame.K_DOWN]:
                dest_x = player_x 
                dest_y = player_y + 48
                
                step.play()
            
                for wall in range(len(wall_pos)):
                    if dest_x == wall_pos[wall][0] and dest_y == wall_pos[wall][1]:
                        can_move += 1                
                
                if can_move == 0: 
                    for steps in range(24):
                        player_y += 2
                        drawPlayer(player_x, player_y) 
                can_move = 0
                    
            # determine the time the player moved and lock its movement
            movement_time = ticks
            movement_enabled = False
            
    # player collision with spikes ---------------------------------------------
    for spike in range(len(spike_pos)):
        if player_x == spike_pos[spike][0] and player_y == spike_pos[spike][1] and invincible == False:
            if (next_state % 4 == 2 and start_state[spike] == 2) or (next_state % 4 == 0 and start_state[spike] == 1):
                hurt.play()
                health -= 1 
                invincible = True
                damaged_time = ticks
                
    # player collision with exit -----------------------------------------------
    #check if the player entered the exit           
    if enter_exit:
        if health > 0:
            pickup.play()
        level += 1
        enter_exit = False
        
        #switch levels
        if level == 1:
            gifts_collected = 0
            level_image = level1
            
            # wall pos
            wall_pos = [[80,48],[272,48],[320,48],[368,48],[464,48],[512,48],[560,48],[80,336],[128,336],[176,336],[272,336],[320,336],[368,336],[560,336],[32,96],[32,144],[32,192],[32,240],[32,288],[608,96],[608,144],[608,192],[608,240],[608,288],[128,96],[128,144],[128,192],[128,240],[176,144],[224,144],[176,144],[224,96],[224,288],[224,240],[320,144],[320,240],[416,96],[416,144],[416,288],[416,240],[464,240],[512,288],[512,240],[512,192],[512,144]]
            
            # spike pos
            spike_pos = [[80,144],[80,192],[80,240],[176,192],[224,192],[272,144],[368,144],[320,192],[272,240],[368,240],[416,192],[464,192],[560,96],[560,144],[560,192]]
            start_state = [1,2,1,1,2,1,1,2,1,1,1,2,1,2,1]
            
            # gift pos
            gift_pos = [[128,288],[272,288],[368,96]]
            gift_active = [True, True, True]
            
            # player pos
            health = 3
            player_x = 80
            player_y = 96
            
            #exit_pos
            exit_pos = [560,288]
            
        elif level == 2:
            level_image = level2
            
            wall_pos = [[80,48],[224,48],[272,48],[320,48],[368,48],[416,48],[464,48],[512,48],[560,48],[80,336],[128,336],[176,336],[224,336],[272,336],[320,336],[416,336],[464,336],[512,336],[560,336],[32,96],[32,144],[32,240],[32,288],[608,96],[608,144],[608,192],[608,240],[608,288],[128,96],[176,96],[80,192],[128,192],[224,240],[272,240],[272,144],[320,144],[368,144],[368,288],[368,240],[368,192],[416,240],[464,240]]

            spike_pos = [[128,144],[176,144],[224,96],[272,96],[128,240],[176,240],[176,288],[224,288],[272,192],[320,192],[464,96],[560,96],[416,144],[512,144],[464,192],[560,192],[512,240],[464,288]]
            start_state = [1,2,1,2,1,2,1,2,1,2,1,1,1,1,1,1,1,2]

            gift_pos = [[320,96],[80,288],[320,288],[416,288]] 
            gift_active = [True, True, True, True]
            
            health = 3
            player_x = 80
            player_y = 96
            
            exit_pos = [560,288]
            
        elif level == 3:
            level_image = level3
            
            wall_pos = [[80,48],[128,48],[224,48],[272,48],[320,48],[368,48],[416,48],[512,48],[560,48],[80,336],[128,336],[224,336],[272,336],[320,336],[368,336],[416,336],[512,336],[560,336],[32,96],[32,144],[32,192],[32,240],[32,288],[608,96],[608,144],[608,192],[608,240],[608,288],[176,96],[464,288],[176,288],[176,240],[128,240],[464,96],[464,144],[512,144],[272,144],[320,144],[368,144],[272,240],[320,240],[368,240]]

            spike_pos = [[80,192],[128,192],[80,240],[80,288],[176,144],[224,144],[224,96],[224,240],[224,288],[272,192],[320,192],[368,192],[416,96],[416,144],[464,240],[416,240],[416,288],[512,192],[560,192],[560,144],[560,96]]
            start_state = [1,1,2,1,1,2,1,1,2,1,2,1,2,1,1,2,1,1,1,2,1]

            gift_pos = [[128,288],[512,96],[320,96],[320,288]] 
            gift_active = [True, True, True, True]
            
            health = 3
            player_x = 80
            player_y = 96
            
            exit_pos = [560,288]
    
        # if the player reached the end  
        if level == 4:
            screen.blit(win, pygame.Rect(0, 0, width, height))
            text = endScore.render(str(gifts_collected), 1, WHITE)
            screen.blit(text, pygame.Rect(348,196,20,28))
            pygame.display.flip()
            gameWon = True
            
            while gameWon:
            # check if the player wants to restart
                pygame.init()
                for evnt in pygame.event.get():
                    if evnt.type == pygame.QUIT:
                        pygame.quit()                    
                    if evnt.type == pygame.KEYDOWN:
                        pressed =  pygame.key.get_pressed()
                        if pressed[pygame.K_RETURN]:
                            select.play()
                            in_menu = True
                            level = 0
                            level1_gifts = 0
                            level2_gifts = 0
                            level3_gifts = 0
                            
                            gameWon = False
                            
    # player death -------------------------------------------------------------                        
    if health <= 0:
            pygame.draw.rect(screen, BLUE, pygame.Rect(51,14,36,33))        

            screen.blit(lose, pygame.Rect(0, 0, width, height))
            text = endScore.render(str(gifts_collected), 1, WHITE)
            screen.blit(text, pygame.Rect(348,196,20,28))
            pygame.display.flip()
            gameLost = True       
            
            while gameLost:
                pygame.init()              
                
                # check the user input
                for evnt in pygame.event.get():
                    if evnt.type == pygame.QUIT:
                        pygame.quit()                    
                    if evnt.type == pygame.KEYDOWN:
                        pressed =  pygame.key.get_pressed()
                        if pressed[pygame.K_RETURN]:
                            select.play()
                            enter_exit = True
                            
                            # check which level the player died on and removes gifts collected in that level from the total
                            if level == 1:
                                level1_gifts = 0
                            if level == 2:
                                level2_gifts = 0
                            if level == 3:
                                level3_gifts = 0
                            gifts_collected = level1_gifts + level2_gifts + level3_gifts
                            level -= 1    
                            gameLost = False            
                      
    pygame.display.flip()
    myClock.tick(60)

pygame.quit()