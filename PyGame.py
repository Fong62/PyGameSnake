import random
import pygame
import pygame.display
from pygame.font import Font
from pygame.math import Vector2
import sys
class Snake:
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(1,0)
        self.new_block=False
        #Head
        self.Head_Left = pygame.image.load("Resources/HeadLeft1.png").convert_alpha()
        self.Head_Left = pygame.transform.scale(self.Head_Left, (cell_size, cell_size))
        self.Head_Right = pygame.image.load("Resources/HeadRight1.png").convert_alpha()
        self.Head_Right = pygame.transform.scale(self.Head_Right, (cell_size, cell_size))
        self.Head_Up = pygame.image.load("Resources/HeadUp1.png").convert_alpha()
        self.Head_Up = pygame.transform.scale(self.Head_Up, (cell_size, cell_size))
        self.Head_Down = pygame.image.load("Resources/HeadDown1.png").convert_alpha()
        self.Head_Down = pygame.transform.scale(self.Head_Down, (cell_size, cell_size))
        #Tail
        self.Tail_Left = pygame.image.load("Resources/TailLeft1.png").convert_alpha()
        self.Tail_Left = pygame.transform.scale(self.Tail_Left, (cell_size, cell_size))
        self.Tail_Right = pygame.image.load("Resources/TailRight1.png").convert_alpha()
        self.Tail_Right = pygame.transform.scale(self.Tail_Right, (cell_size, cell_size))
        self.Tail_Up = pygame.image.load("Resources/TailUp1.png").convert_alpha()
        self.Tail_Up = pygame.transform.scale(self.Tail_Up, (cell_size, cell_size))
        self.Tail_Down = pygame.image.load("Resources/TailDown1.png").convert_alpha()
        self.Tail_Down = pygame.transform.scale(self.Tail_Down, (cell_size, cell_size))
        #Body
        self.Horizontal = pygame.image.load("Resources/Horizontal1.png").convert_alpha()
        self.Horizontal = pygame.transform.scale(self.Horizontal, (cell_size, cell_size))
        self.Vertical = pygame.image.load("Resources/Vertical1.png").convert_alpha()
        self.Vertical = pygame.transform.scale(self.Vertical, (cell_size, cell_size))
        self.TL = pygame.image.load("Resources/TL1.png").convert_alpha()
        self.TL = pygame.transform.scale(self.TL, (cell_size, cell_size))
        self.TR = pygame.image.load("Resources/TR1.png").convert_alpha()
        self.TR = pygame.transform.scale(self.TR, (cell_size, cell_size))
        self.BL = pygame.image.load("Resources/BL1.png").convert_alpha()
        self.BL = pygame.transform.scale(self.BL, (cell_size, cell_size))
        self.BR = pygame.image.load("Resources/BR1.png").convert_alpha()
        self.BR = pygame.transform.scale(self.BR, (cell_size, cell_size))
    
    def draw_snake(self):
        for index,block in enumerate(self.body):
            x_pos=block.x*cell_size
            y_pos=block.y*cell_size
            Block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            self.caculate_head()
            self.caculate_tail()
            if index==0:
                screen.blit(self.Head,Block_rect)
            elif index==len(self.body)-1:
                screen.blit(self.Tail,Block_rect)
            else:
                pre_block=self.body[index+1]-block
                next_block=self.body[index-1]-block
                if pre_block.y==next_block.y:
                    screen.blit(self.Horizontal,Block_rect)
                elif pre_block.x==next_block.x:
                    screen.blit(self.Vertical,Block_rect)
                else:
                    if pre_block.x==-1 and next_block.y==-1 or pre_block.y==-1 and next_block.x==-1:
                     screen.blit(self.TL,Block_rect)
                    if pre_block.x==-1 and next_block.y==1 or pre_block.y==1 and next_block.x==-1:
                     screen.blit(self.BL,Block_rect)
                    if pre_block.x==1 and next_block.y==-1 or pre_block.y==-1 and next_block.x==1:
                     screen.blit(self.TR,Block_rect)
                    if pre_block.x==1 and next_block.y==1 or pre_block.y==1 and next_block.x==1:
                     screen.blit(self.BR,Block_rect)
            
    def caculate_head(self):
        head_res=self.body[0]-self.body[1]
        if head_res==Vector2(1,0):
            self.Head=self.Head_Right
        if head_res==Vector2(-1,0):
            self.Head=self.Head_Left
        if head_res==Vector2(0,1):
            self.Head=self.Head_Down
        if head_res==Vector2(0,-1):
            self.Head=self.Head_Up

    def caculate_tail(self):
        tail_res=self.body[-2]-self.body[-1]
        if tail_res==Vector2(1,0):
            self.Tail=self.Tail_Left
        if tail_res==Vector2(-1,0):
            self.Tail=self.Tail_Right
        if tail_res==Vector2(0,1):
            self.Tail=self.Tail_Up
        if tail_res==Vector2(0,-1):
            self.Tail=self.Tail_Down

    def move_snake(self):
        if self.new_block==True:
         body_copy=self.body[:]
         new_head = self.body[0] + self.direction 
         body_copy.insert(0, new_head)  
         self.body=body_copy[:]
         self.new_block=False
        else:
         body_copy=self.body[:-1]
         new_head = self.body[0] + self.direction 
         body_copy.insert(0, new_head)  
         self.body=body_copy[:]

    def lengthen(self):
        self.new_block=True

class Bullet:
    def __init__(self, pos, direction):
        self.pos = Vector2(pos)  
        self.direction = Vector2(direction).normalize()
        self.speed = 20  
        self.size = 5  

    def move(self):
       self.pos += self.direction * self.speed

    def draw(self, screen):
       pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.size)

    def is_off_screen(self):
       return not (0 <= self.pos.x < cell_number * cell_size and 0 <= self.pos.y < cell_number * cell_size)


class Prey:
    def __init__(self):
        self.randompos()
        self.Prey1 = pygame.image.load("Resources/Prey1.png").convert_alpha()
        self.Prey1 = pygame.transform.scale(self.Prey1, (cell_size, cell_size))
        self.bullets = [] 
        self.shoot_interval = 2000 
        pygame.time.set_timer(pygame.USEREVENT + 2, self.shoot_interval) 

    def draw_prey(self):
        Prey_rect=pygame.Rect(self.pos.x*cell_size,self.pos.y*cell_size,cell_size,cell_size)
        screen.blit(self.Prey1,Prey_rect)

        for bullet in self.bullets:
            bullet.draw(screen)
       

    def randompos(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)
        self.pos=Vector2(self.x,self.y)

    def shoot(self):
        direction = Vector2(random.choice([-1, 1]), random.choice([-1, 1]))  
        new_bullet = Bullet(self.pos * cell_size, direction)  
        self.bullets.append(new_bullet)
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.prey = Prey()
        self.game_win_sound=pygame.mixer.Sound("Sounds\\win_sound.wav")
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.Draw_Grass()
        self.Draw_Score()
        self.prey.update_bullets() 
        self.check_bullet_collision()  
        # Adjust level win screen
        global menu_selection
        score=5
        if menu_selection <1:
         self.check_win(score)
        elif menu_selection>=1:
         score+=menu_selection
         self.check_win(score)

    def draw_element(self):
        self.snake.draw_snake()
        self.prey.draw_prey()
    
    def game_over(self):
        Fail_Text = "Game Over! Your score: " + str(len(self.snake.body) - 3)
        Play_Again_Text = "Press Enter to play again and X for Stage Selection or Esc to quit."
        Fail_surface = game_font.render(Fail_Text, True, (56, 74, 12))
        Play_Again_surface = game_font.render(Play_Again_Text, True, (56, 74, 12))
    
        Fail_rect = Fail_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))
        Play_Again_rect = Play_Again_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size * 2 // 3))
    
        screen.blit(Fail_surface, Fail_rect)
        screen.blit(Play_Again_surface, Play_Again_rect)
        pygame.display.flip()  

    def reset_game(self):
        self.snake = Snake()
        self.prey = Prey()
    
    def check_collision(self):
        if self.prey.pos == self.snake.body[0]:
            self.prey.randompos()
            self.snake.lengthen()
            for block in self.snake.body[1:]:
             if block==self.prey.pos:
                 self.prey.randompos()

    def check_fail(self):
        global game_active, game_over
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            game_active = False
            game_over = True
        '''for block in self.snake.body[1:]:
            if block == self.snake.body[0]:  # Collision with self
                game_active = False
                game_over = True'''
    
    def check_win(self,score):
        global game_win,game_active
        if len(self.snake.body)==score+3:
           self.game_win_sound.play()
           game_win = True
           game_active= False
           

    def notice(self,text):
        text_surface=menu_font.render(text,True,(56,74,12))
        text_rect = text_surface.get_rect()
        screen_center = (cell_number * cell_size // 2, cell_number * cell_size // 2)
        text_rect.center = screen_center
        screen.blit(text_surface,text_rect)
        pygame.display.flip()


    def check_bullet_collision(self):
     global game_active, game_over
     for segment in self.snake.body:
        snake_segment_rect = pygame.Rect(segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
        for bullet in self.prey.bullets:
            bullet_rect = pygame.Rect(bullet.pos.x, bullet.pos.y, bullet.size, bullet.size)
            if snake_segment_rect.colliderect(bullet_rect):
                game_active = False
                game_over = True  
                
    
    def handle_shoot_event(self, event):
       if event.type == pygame.USEREVENT + 2 and menu_selection>=2:
            self.prey.shoot()

    def Draw_Grass(self):
        grass_color_light = (124, 252, 0)
        grass_color_dark = (110, 220, 0)
        for i in range(cell_number):
            for j in range(cell_number):
                grass_color = grass_color_light if (i + j) % 2 == 0 else grass_color_dark
                grass_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, grass_color, grass_rect)

    def Draw_Score(self):
        score_text = "Score: " + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect()
        score_rect.topright = (cell_number * cell_size - 10, 10)
        screen.blit(score_surface, score_rect)


menu_selection = 0
level_texts = [f"Level {i + 1}" for i in range(20)]
level_colors = [(0, 0, 0) for _ in range(20)]
visible_levels = 6
scroll_offset = 0



def draw_menu(screen, font):
    global blink_show
    title_text = font.render("Snake game", True, (250, 0, 0))
    start_text = font.render("Press Enter !", True, (250, 0, 0))
    back_ground = pygame.image.load("Resources\\Back_Ground.png")
    back_ground = pygame.transform.scale(back_ground, (cell_size * cell_number, cell_size * cell_number))
    back_ground_rect = back_ground.get_rect(topleft=(0, 0))

    title_rect = title_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 6))
    start_rect = start_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size * 5 // 6))

    screen.blit(back_ground, back_ground_rect)
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

    for i in range(visible_levels):
        level_index = scroll_offset + i
        if level_index >= len(level_texts):
            break
        color = (255, 0, 0) if level_index == menu_selection else level_colors[level_index]
        level_surface = font.render(level_texts[level_index], True, color)
        level_rect = level_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3 + i * 40))
        screen.blit(level_surface, level_rect)

# Initialize pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_number = 20
cell_size = 40
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)
game_font = pygame.font.SysFont("Arial", 24, bold=True)
menu_font = pygame.font.SysFont("RockWell", 45, bold=True)

main = Main()
running = True
game_active = False
game_over = False
game_win = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        main.handle_shoot_event(event)
        if game_active:
            if event.type == screen_update:
                main.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)
        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    main.reset_game()
                    game_active = True
                    game_over = False
                    game_win=False
                elif event.key == pygame.K_x:
                    game_active=False
                    game_over=False
                    game_win=False
                    main.reset_game()
                    draw_menu(screen,menu_font)
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()
        elif game_win:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    menu_selection+=1
                    main.reset_game()
                    game_active = True
                    game_over = False
                   
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if menu_selection > 0:
                        menu_selection -= 1
                    if menu_selection < scroll_offset:
                        scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    if menu_selection < len(level_texts) - 1:
                        menu_selection += 1
                    if menu_selection >= scroll_offset + visible_levels:
                        scroll_offset += 1
                elif event.key == pygame.K_RETURN:
                    game_active = True
                    
                    if menu_selection < 7:
                        pygame.time.set_timer(screen_update, 200)
                    elif menu_selection < 14:
                        pygame.time.set_timer(screen_update, 150)
                    else:
                        pygame.time.set_timer(screen_update, 100)

    # Drawing
    if game_active:
        pygame.display.set_caption("Level " + str(menu_selection + 1))
        main.draw_element()
    elif game_over:
        pygame.display.set_caption(":(")
        back_ground_fail = pygame.image.load("Resources\\Level_Failed.png")
        back_ground_fail = pygame.transform.scale(back_ground_fail, (cell_size * cell_number, cell_size * cell_number))
        back_ground_failrect = back_ground_fail.get_rect(topleft=(0, 0))
        screen.blit(back_ground_fail, back_ground_failrect)
        main.game_over()
    elif game_win:
        screen.fill((173, 216, 230))
        main.notice("You win ! Press Enter to continue !")
    
    else:
        pygame.display.set_caption("Menu")
        draw_menu(screen, menu_font)

    pygame.display.update()
    clock.tick(60)

pygame.quit()