from pygame import color
from main import WIDTH
from math import trunc
from random import random, triangular
import pygame, colours, os, sys
from pygame import event
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(xPos, yPos))

class Player(Block):
    def __init__(self, path, xPos, yPos, speed):
        super().__init__(path, xPos, yPos)
        self.speed = speed
        self.movement = 0
    
    def constraints(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        
        if self.rect.top <= 0:
            self.rect.top = 0

    def update(self, ballGroup):
        self.rect.y += self.movement
        self.constraints()

class Opponent(Block):
    def __init__(self, path, xPos, yPos, speed):
        super().__init__(path, xPos, yPos)
        self.speed = speed

    def constraints(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        
        if self.rect.top <= 0:
            self.rect.top = 0

    def update(self, ballGroup):
        if self.rect.bottom > ballGroup.sprite.rect.y:
            self.rect.bottom -= self.speed

        if self.rect.top < ballGroup.sprite.rect.y:
            self.rect.top += self.speed
        self.constraints()
    

class Ball(Block):
    def __init__(self, path, xPos, yPos, speed, paddleGroup):
        super().__init__(path, xPos, yPos)
        self.speedX = speed * random.choice((-1, 1))
        self.speedY = speed * random.choice((-1, 1))
        self.active = False
        self.scoreTime = 0
        self.paddles = paddleGroup

    def update(self):
        if self.active:
            self.rect.x += self.speedX
            self.rect.y += self.speedY
            self.collision()

        else:
            self.restart_counter()

    def reset_ball(self):
        self.active = False
        self.speedX *= random.choice((-1,1))
        self.speedY *= random.choice((-1,1))
        self.scoreTime = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        pygame.mixer.Sound.play(scoreSound)

    def collision(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            pygame.mixer.Sound.play(pongSound)
            self.speedY *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            collisionPaddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect

            if abs(self.rect.right - collisionPaddle.left) < 10 and self.speedX > 0:
                pygame.mixer.Sound.play(pongSound)
                self.speedX *= -1
            
            if abs(self.rect.left - collisionPaddle.right) < 10 and self.speedX < 0:
                pygame.mixer.Sound.play(pongSound)
                self.speedX *= -1
            
            if abs(self.rect.top - collisionPaddle.bottom) < 10 and self.speedY < 0:
                self.rect.top = collisionPaddle.bottom
                self.speedY *= -1 

            if abs(self.rect.bottom - collisionPaddle.top) < 10 and self.speedY > 0:
                self.rect.bottom = collisionPaddle.top
                self.speedY *= -1 

    def restart_counter(self):
        currentTime = pygame.time.get_ticks()
        countDown = 3

        if currentTime - self.scoreTime <= 700:
            countDown = 3

        if 700 < currentTime - self.scoreTime <= 1400:
            countDown = 2

        if 1400 < currentTime - self.scoreTime <= 2100:
            countDown = 1

        if currentTime - self.scoreTime >= 2100:
            self.active = True

        countDownLabel = gameFont.render(str(countDown), True, colours.ACCENT)
        countDownRect = countDownLabel.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 50))
        pygame.draw.rect(mainWindow, backgroundColor, countDownRect)
        mainWindow.blit(countDownLabel, countDownRect)


class GameManager():
    def __init__(self, ballGroup, paddleGroup):
        self.playerScore = 0
        self.opponentScore = 0
        self.ballGroup = ballGroup
        self.paddleGroup = paddleGroup

    def run_game(self):
        self.ballGroup.draw(mainWindow)
        self.paddleGroup.draw(mainWindow)

        self.ballGroup.update()
        self.paddleGroup.update(self.ballGroup)
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ballGroup.sprite.rect.right >= WIDTH:
            self.opponentScore += 1
            self.ballGroup.sprite.reset_ball()
        
        if self.ballGroup.sprite.rect.left <= 0:
            self.playerScore += 1 
            self.ballGroup.sprite.reset_ball()


    def draw_score(self):
        playerScoreLabel = gameFont.render(str(self.playerScore), True, colours.ACCENT)
        playerScoreRect = playerScoreLabel.get_rect(midleft = (WIDTH / 2 + 40, HEIGHT/2))

        opponentScoreLabel = gameFont.render(str(self.opponentScore), True, colours.ACCENT)
        opponentScoreRect = opponentScoreLabel.get_rect(midright = (WIDTH / 2 - 40, HEIGHT/2))
        
        mainWindow.blit(playerScoreLabel, playerScoreRect)
        mainWindow.blit(opponentScoreLabel, opponentScoreRect)


# initialize pygame
pygame.init()

# paths
ballPath = 'assets/ball.png'
pongSoundPath = 'assets/pong.ogg'
scoreSoundPath = 'assets/score.ogg'
gameIconPath = 'assets/icon.png'
paddlePath = 'assets/paddle.png'

# global variables
run = True
FPS = 60
WIDTH = 800
HEIGHT = 500
clock = pygame.time.Clock()

gameFont = pygame.font.Font("freesansbold.ttf", 20)
pongSound = pygame.mixer.Sound(pongSoundPath)
scoreSound = pygame.mixer.Sound(scoreSoundPath)

backgroundColor = pygame.Color(colours.SPACE)
accent_color = colours.ACCENT
middleStrip = pygame.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT)

# display set up
mainWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pong")
gameIcon = pygame.image.load(os.path.join("assets", "icon.png"))
pygame.display.set_icon(gameIcon)

# game objects
player = Player(paddlePath, WIDTH - 20, HEIGHT / 2, 5)
opponent = Opponent(paddlePath, 20, HEIGHT / 2, 5)
paddleGroup = pygame.sprite.Group()
paddleGroup.add(player)
paddleGroup.add(opponent)

ball = Ball(ballPath, WIDTH / 2, HEIGHT / 2, 5, paddleGroup)
ballSprite = pygame.sprite.GroupSingle()
ballSprite.add(ball)

gameManager = GameManager(ballSprite, paddleGroup)
# game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed

            if event.key == pygame.K_DOWN:
                player.movement += player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed

            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    mainWindow.fill(backgroundColor)
    pygame.draw.rect(mainWindow, accent_color, middleStrip)

    # run the game
    gameManager.run_game()
    #render screen
    pygame.display.update()
    clock.tick(FPS)
