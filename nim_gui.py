import pygame
import sys #to quit from the game
import nim_driver #implementation of AI

pygame.init() #initialize everything (display, mixer, etc...)

#Images
title_screen = pygame.image.load("./Assets/title.png") #background title 
p_wait = pygame.image.load("./Assets/please_wait.png") #background for PC move
bg = pygame.image.load("./Assets/bg.png") #background for play
item_image = pygame.image.load("./Assets/cap.png") #item image for CollectableItem Class
cursor_image = pygame.image.load("./Assets/pip_boy.png")#cursor image for Cursor Class

bg_size = (640, 360) #size of game window
item_width_height = (80, 80) #size of item icon
cursor_width_height = (60, 60) #size of cursor icon

bg = pygame.transform.scale(bg, bg_size) #transforming scale will help to fill game window
title_screen = pygame.transform.scale(title_screen, bg_size)
item_image = pygame.transform.scale(item_image, item_width_height) #resizing 
cursor_image = pygame.transform.scale(cursor_image, cursor_width_height)

#Game window setup
pygame.display.set_caption("*** Nim ***") #window title
screen = pygame.display.set_mode(bg_size) #creating window
screen.blit(title_screen, title_screen.get_rect()) #sets background image
pygame.display.flip() #updates the display

class CollectableItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(CollectableItem, self).__init__()
        self.image = item_image
        self.rect = pygame.Rect(((x, y), item_width_height))

class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Cursor, self).__init__()
        self.image = cursor_image
        self.rect = pygame.Rect(((x, y), cursor_width_height))

def play_sound_effect():
    sound = pygame.mixer.Sound("./Assets/cap.mp3") #create sound obj
    sound.play()

def play_bg_music():
    pygame.mixer.music.load("./Assets/bg_music.mp3") #put on queue
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1) #-1 for infinite loop

def resetBG(board):
    screen.blit(bg, bg.get_rect()) #apply background
    printitems(board) #reprint items over background

cursors = pygame.sprite.Group() #needed to draw() cursor 
def printcursor(r):
    cursors.empty() #no more than one cursor in cursors
    cursor = Cursor(565, 96 * r) #r = row num
    cursors.add(cursor) #add cursor to cursors group
    cursors.draw(screen) #print group (one cursor)

items = pygame.sprite.Group() #collection of items
def printitems(board):
    items.empty() #remove all previous items
    for r, pile in enumerate(board):
        for i in range(pile):
            it = CollectableItem(80 * i, 92 * r) #i = item pos in row & r = row num
            items.add(it) #add it to collection
    items.draw(screen) #draw all items

play_bg_music() #plays infinitely
pygame.time.wait(20000) #pause for title screen

#start game
board = [1, 3, 5, 7] #starting board
temp_board = board[:] #helpful for switching rows
row = 3 #starting row
items_collected = 0 #keeps track of player's turn
pc_lost = False
resetBG(board) #sets game area background and displays items
pygame.display.flip()
printcursor(row) #display cursor 

while (True):
    for event in pygame.event.get():
        if sum(board) <= 0: #Game Over
            final = pygame.image.load("./Assets/lost.png") #player lost
            if pc_lost: 
                final = pygame.image.load("./Assets/won.png") #player won

            final = pygame.transform.scale(final, bg_size)
            screen.blit(final, final.get_rect())
            pygame.display.flip()
            pygame.time.wait(5000) #wait on Game Over screen
            
            #restart game
            board = [1, 3, 5, 7]
            temp_board = board[:]
            row = 3
            items_collected = 0
            pc_lost = False
            resetBG(board)
            printcursor(row)

        if event.type == pygame.QUIT:
            pygame.quit() #uninitialize everything 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and items_collected > 0: #player confirmed turn
                play_sound_effect()
                board[row] -= items_collected #remove selected items
                items_collected = 0 #reset items
                
                if sum(board) <= 0: #check if player lost
                    pc_lost = False
                    break #to get to Game Over conditional

                screen.blit(p_wait, p_wait.get_rect()) #set background for PC turn
                pygame.display.flip()
                pygame.time.wait(3000) #waiting for PC turn
                
                temp_board = nim_driver.computerMove(board) #update to new state
                board = temp_board[:]
                if sum(board) <= 0: #check if PC lost
                    pc_lost == True
                    break

                resetBG(board)
            elif event.key == pygame.K_UP: #moving cursor up
                items_collected = 0
                temp_board = board[:] #reset temp board
                resetBG(board) #reset items displayed
                if row > 0:
                    row -= 1
            elif event.key == pygame.K_DOWN: #moving cursor down
                items_collected = 0
                temp_board = board[:]
                resetBG(board)
                if row < 3:
                    row += 1
            elif event.key == pygame.K_LEFT: #taking items
                if board[row] > 0 and items_collected < board[row]:
                    items_collected += 1
                    temp_board[row] -= 1
                resetBG(temp_board) #updates display when items collected
            elif event.key == pygame.K_RIGHT: #putting back items
                if items_collected > 0:
                    items_collected -= 1
                    temp_board[row] += 1
                resetBG(temp_board) #updates display when items put back
        
        printcursor(row) #display cursor 
        pygame.display.flip() #update screen