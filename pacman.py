from map import boards
import pygame
import math

pygame.init()

#inital stats of games
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = boards
color = 'red'
PI = math.pi
player_images = []
#import image player
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'add-on/player_images/{i}.png'), (45, 45)))

#import ghost image
blinky_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'add-on/ghost_images/dead.png'), (45, 45))
######
player_x = 450
player_y = 663
counter = 0
direction = 0
#ghost blinky
blinky_x = 56
blinky_y = 58
blinky_direction = 0
#ghost inky
inky_x = 440
inky_y = 388
inky_direction = 2
#ghost pinky
pinky_x = 440
pinky_y = 438
pinky_direction = 2 
#ghost clyde
clyde_x = 440
clyde_y = 438
clyde_direction = 2

flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
moving = False
ghost_speed = [2, 2, 2, 2]
startup_counter = 0
lives = 3

#Font
font = pygame.font.Font('freesansbold.ttf', 20)

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions() # use this to cheaking player
        self.rect = self.draw()# draw rectangle
    
    def draw(self):
        #this line is make for regular ghost
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead): 
            screen.blit(self.img, (self.x_pos, self.y_pos))
        #this line is make a ghost when a player power up    
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        #we draw a rectangle this variable:
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 3))    
        return ghost_rect
    
    #Check for a ghost valid pathing and turn checking
    def check_collisions(self):
        #R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3 )// num1][self.center_x // num2] < 3 \
                or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3 )// num1][self.center_x // num2] < 3 \
                or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                self.in_box or self.dead)):
                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[2] = True
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[0] = True
            
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[2] = True
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                            self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False                         
        return self.turns, self.in_box
    
    def move_clyde(self):
        # r ,l, u ,d
        #clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]: #it mean in this line if ghost turns right and find player in right that he turn
                self.x_pos += self.speed # going right 
            elif not self.turns[0]: #ghost collide turn in to obstacle
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]: 
                # if the ghost able to turns right and the target is not over there ghost will sitll walkthrough that direction
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed
                else:
                    self.x_pos += self.speed   
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]: #it mean in this line if ghost turns left and find player in right that he turn
                self.x_pos -= self.speed # going left
            elif not self.turns[1]: #ghost collide turn in to obstacle(left)
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]: 
                # if the ghost able to turns right and the target is not over there ghost will sitll walkthrough that direction
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed
                else:
                    self.x_pos -= self.speed  
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]: #it mean in this line if ghost turns up and find player in right that he turn
                self.y_pos -= self.speed # going up
            elif not self.turns[2]: #ghost collide turn in to obstacle(left)
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]: 
                # if the ghost able to turns up and the target is not over there ghost will sitll walkthrough that direction
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos += self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]: #it mean in this line if ghost turns up and find player in right that he turn
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]: 
                # if the ghost able to turns right and the target is not over there ghost will sitll walkthrough that direction
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
                    
                    
                    
#display score
def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup: # make a powerup status of pac-man
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))  

#update eating board dot
#changing the score
def check_collisions(scor, power, power_count, eaten_ghost):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:# this part is using for make a animation of pac-man eating dot when opening mouth
        if level[center_y // num1][center_x // num2] == 1:# small dot
            level[center_y // num1][center_x // num2] = 0
            scor += 10 #you can change score once per piece
        if level[center_y // num1][center_x // num2] == 2: #big dot
            level[center_y // num1][center_x // num2] = 0
            scor += 50 #score change
            power = True
            power_count = 0
            eaten_ghost = [False, False, False, False]
            
    return scor, power, power_count, eaten_ghost

#drawing map
def draw_board():
    num1 = ((HEIGHT - 50) // 32) 
    num2 = (WIDTH // 30)
    for i in range(len(level)):# iterate every single row in level
        for j in range(len(level[i])):#iterate every single columns inside specific row
            if level[i][j] == 1: #white small dot in direction of the space map
                pygame.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker: #white big dot in direction of the space map and it flicker
                pygame.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:# line in vertical
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),(j * num2 + (0.5 * num2), i*num1 + num1),3)
            if level[i][j] == 4:# line in horizontal
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),(j * num2 + num2, i*num1 + (0.5 * num1)),3)
            if level[i][j] == 5:# make an right arc lines
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:# make an left arc lines
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],PI/2, PI, 3)
            if level[i][j] == 7:# make an right down arc lines
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI/2, 3)
            if level[i][j] == 8:# make an left down arc lines
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI/2, 2 * PI, 3)    
            if level[i][j] == 9:# line in horizontal in white color
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),(j * num2 + num2, i*num1 + (0.5 * num1)),3)

#player modifying
def draw_player():
    #0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0: #make direction to player
        screen.blit(player_images[counter // 5], (player_x, player_y))# this thing is make a picture do a animation in 3 frame per sec
    elif direction == 1: #make direction to player
        screen.blit(pygame.transform.flip(player_images[counter // 5],True, False), (player_x, player_y))
    elif direction == 2: #make direction to player
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3: #make direction to player
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))
#check position of the player             
def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d 
    if direction == 0 and turns_allowed[0]:# if player go right and turn allowed to go right
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y    

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        

    return [blink_target, ink_target, pink_target, clyd_target]
        
       
running = True
while running:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving =True
    
    screen.fill('black')
    draw_board()
    center_x = player_x + 23 # in this part we make a collision of the code 
    center_y = player_y + 24
    if powerup:
        ghost_speed = [1, 1, 1, 1]
    else:
        ghost_speed = [2, 2, 2, 2]
    if blinky_dead:
        ghost_speed[0] = 4
    if inky_dead:
        ghost_speed[1] = 4
    if pinky_dead:
        ghost_speed[2] = 4
    if clyde_dead:
        ghost_speed[3] = 4
            
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)
    
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    #add to if not  power up to check eaten ghost
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
            (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                    (player_circle.colliderect(clyde) and not clyde.dead):
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            counter = 0
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 440
                            pinky_y = 438
                            pinky_direction = 2 
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False    
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            counter = 0
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 440
                            pinky_y = 438
                            pinky_direction = 2 
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False 
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            counter = 0
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 440
                            pinky_y = 438
                            pinky_direction = 2 
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False 
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            counter = 0
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 440
                            pinky_y = 438
                            pinky_direction = 2 
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False 
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 450
                            player_y = 663
                            counter = 0
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 440
                            pinky_y = 438
                            pinky_direction = 2 
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False 
    if powerup and (player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]):
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100 #score for eaten ghost
    if powerup and (player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]):
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and (player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]):
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and (player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]):
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    
    #use for loop for make everything happening in computer ex like keyboard mouse...
    for event in pygame.event.get():
        # we use this for exit and out infinite while loop 
        if event.type == pygame.QUIT:
            running = False
        #managing a keyboard setting:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        # this code is for when we pressing the button together It will work on direction that we current want.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction    
        
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
    
    # this condition is use for when players out of range of size game it return player back to the screen in the other way        
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897
    
    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False    
    
            
    pygame.display.flip()

pygame.quit()