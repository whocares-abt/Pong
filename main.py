import pygame
from sys import exit
from random import choice, random


# initializing game
pygame.init()
screen = pygame.display.set_mode((800, 400))
background_surf = pygame.Surface((800, 400))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
Game_active = False
Mode_selector = False

# title screen
test_font = pygame.font.Font('font/Pixeltype.ttf', 100)
title_font = test_font.render('PONG', False, 'White')
title_rect = title_font.get_rect(center=(400, 100))
play_button = pygame.image.load('IMAGE/Play button.png')
play_button_scaled = pygame.transform.scale2x(play_button)
play_button_rect = play_button_scaled.get_rect(center=(400, 300))

# Number of player selector
single_player = test_font.render('One Player', None, 'White')
single_player_rect = single_player.get_rect(center = (200, 200))
two_player = test_font.render('Two Players', None, 'White')
two_player_rect = two_player.get_rect(center = (600, 200))

# Score tracker
left_score = 0
right_score = 0
Ball_reset = True

# BGM
bgm = pygame.mixer.Sound('Music/BGM.mp3')
bgm.play(-1)

# A sprite for the 1st Player's Paddle
class Player_Paddle1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill('White')
        self.rect = self.image.get_rect(center=(100, 200))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if not ball_collision_paddles()[0]:
            if keys[pygame.K_UP] and self.rect.top >= 0:
                self.rect.y -= 5.0
            elif keys[pygame.K_DOWN] and self.rect.bottom <= 400:
                self.rect.y += 5.0

    def update(self):
        self.player_input()


# A sprite for the 2nd Player's Paddle
class Player_Paddle2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill('White')
        self.rect = self.image.get_rect(center= (700, 200))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if not ball_collision_paddles()[0]:
            if keys[pygame.K_w] and self.rect.top >= 0:
                self.rect.y -= 5.0
            elif keys[pygame.K_s] and self.rect.bottom <= 400:
                self.rect.y += 5.0

    def update(self):
        self.player_input()


# A sprite for the AI's paddle
class AI_Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill('White')
        self.rect = self.image.get_rect(center=(700, 200))

    def AI_input(self):
        Ball_y = Balls.sprite.rect.y
        Paddle_y = self.rect.center[1]
        if Ball_y >= Paddle_y and self.rect.bottom <= 400:
            self.rect.y += min(5, abs(Paddle_y-Ball_y))
        elif Ball_y <= Paddle_y and self.rect.top >= 0:
            self.rect.y -= min(5, abs(Paddle_y-Ball_y))

    def update(self):
        self.AI_input()


class Paddle_Ball(pygame.sprite.Sprite):
    def __init__(self, v_x, v_y):
        super().__init__()
        self.image = pygame.image.load('IMAGE/Ball.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 200))
        self.v_x = v_x
        self.v_y = v_y


    def position_update(self):
        self.rect.x += self.v_x
        self.rect.y += self.v_y


    def velocity_update(self):
        y = ball_collision_paddles()
        if y[0]:
            if self.v_x >= 0:
                self.v_x = -(self.v_x + random()/2)
            else:
                self.v_x = -(self.v_x - random()/2)
            if self.v_y >= 0:
                self.v_y = min((self.v_y*y[1]+random()), 10)
            else:
                self.v_y = max(self.v_y*y[1]-random(), -10)
            if self.rect.x<400:
                self.rect.x+=2
            else:
                self.rect.x-=2
        if ball_collision_walls():
            self.v_y = -self.v_y


    def restart(self):
        if self.rect.x >= 900 or self.rect.x <= -100:
            self.rect = self.image.get_rect(center=(400, 200))
            self.v_x = choice([-5, -4, -3, 3, 4, 5])
            self.v_y = choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])


    def update(self):
        self.position_update()
        self.velocity_update()
        self.restart()


def ball_collision_paddles():
    if pygame.sprite.spritecollide(Balls.sprite, Paddles, False):
        Ball_y = Balls.sprite.rect.center[1]
        for i in pygame.sprite.spritecollide(Balls.sprite, Paddles, False):
            Paddle_y = i.rect.center[1]
            x = abs(Paddle_y - Ball_y)
        return (True, 0.5+(x/50))
    else:
        return (False, 0, 0)


def ball_collision_walls():
    return Balls.sprite.rect.y <= 0 or Balls.sprite.rect.bottom >= 400

 
def score_update(left_score, right_score, Ball_reset):
    if 300 <= Balls.sprite.rect.x <= 500:
        Ball_reset = True
    if Ball_reset:
        if Balls.sprite.rect.x < 0:
            right_score += 1
            Ball_reset = False
        elif Balls.sprite.rect.x > 800:
            left_score += 1
            Ball_reset = False
    return (left_score, right_score, Ball_reset)

Balls = pygame.sprite.GroupSingle()
Balls.add(Paddle_Ball(-5, 0))

Paddles = pygame.sprite.Group()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if Game_active:
            # Code for exiting the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game_active = False
                    Mode_selector = False
                    Paddles.empty()
                    Balls.empty()
                    left_score = 0
                    right_score = 0
                    Ball_reset = True
        if not Game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    Mode_selector = True
        if Mode_selector:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and single_player_rect.collidepoint(pygame.mouse.get_pos()):
                    Game_active = True
                    Paddles.add(Player_Paddle1(), AI_Paddle())
                    Balls.add(Paddle_Ball(-5, 0))
                if pygame.mouse.get_pressed()[0] and two_player_rect.collidepoint(pygame.mouse.get_pos()):
                    Game_active = True
                    Paddles.add(Player_Paddle1(), Player_Paddle2())
                    Balls.add(Paddle_Ball(-5, 0))



    # Updating screen
    if Game_active:
        # Updating score
        left_score_text = test_font.render(f'{left_score}', False, 'white')
        right_score_text = test_font.render(f'{right_score}', False, 'white')
        screen.blit(background_surf, (0, 0))
        screen.blit(left_score_text, (175, 75))
        screen.blit(right_score_text, (575, 75))
        left_score, right_score, Ball_reset =score_update(left_score, right_score, Ball_reset)
        
        # Updating paddles and ball
        Balls.draw(screen)
        Balls.update()
        Paddles.draw(screen)
        Paddles.update()
        pygame.draw.line(screen, 'White', (400,0), (400,400), 2)

    elif Mode_selector:
        screen.blit(background_surf, (0, 0))
        screen.blit(single_player, single_player_rect)
        screen.blit(two_player, two_player_rect)

    else:
        screen.blit(background_surf, (0, 0))
        screen.blit(title_font, title_rect)
        screen.blit(play_button_scaled, play_button_rect)

    # Updating display and capping fps
    pygame.display.update()
    clock.tick(60)