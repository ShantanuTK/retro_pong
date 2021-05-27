from math import trunc
import pygame
import sys, os
import colours
import random

pygame.init()

# GAME VARIABLES
WIDTH = 700
HEIGHT = 500
clock = pygame.time.Clock()
FPS = 45

#TEXT VARIABLES
gameFont = pygame.font.Font("freesansbold.ttf", 20)

# BG COLOUR
bgColour = pygame.Color(colours.GREY12)

# IMPORTING SOUND FILES
pongSound = pygame.mixer.Sound(os.path.join("assets", "pong.ogg"))
scoreSound = pygame.mixer.Sound(os.path.join("assets", "score.ogg"))

# GAME RECTANGLES
player = pygame.Rect(WIDTH - 12, (HEIGHT / 2 - 50), 7, 100)
opponent = pygame.Rect(5, (HEIGHT / 2 - 50), 7, 100)
ball = pygame.Rect((WIDTH / 2 - 8), (HEIGHT / 2 - 8), 16, 16)

# MAINWINDOW SET UP 
mainWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")
icon = pygame.image.load(os.path.join('assets', 'icon.png'))
pygame.display.set_icon(icon)

def ball_animation(ballXSpeed, ballYSpeed, playerScore, opponentScore, scoreTime):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        pygame.mixer.Sound.play(pongSound)
        ballYSpeed *= -1

    if ball.left <= 0:
        playerScore += 1
        scoreTime = pygame.time.get_ticks()
        pygame.mixer.Sound.play(scoreSound)

    if ball.right >= WIDTH:
        opponentScore += 1
        scoreTime = pygame.time.get_ticks()
        pygame.mixer.Sound.play(scoreSound)

    if ball.colliderect(player) and ballXSpeed > 0:
        if abs(ball.right - player.left) < 10:
            ballXSpeed *= -1
            pygame.mixer.Sound.play(pongSound)
        
        if abs(ball.top - player.bottom) < 10 and ballYSpeed < 0:
            ballXSpeed *= - 1

        if abs(ball.bottom - player.top) < 10 and ballYSpeed > 0:
            ballYSpeed *= - 1
    
    if ball.colliderect(opponent):
        if abs(ball.left - opponent.right) < 10:
            ballXSpeed *= -1
            pygame.mixer.Sound.play(pongSound)
        
        if abs(ball.top - opponent.bottom) < 10 and ballYSpeed < 0:
            ballXSpeed *= - 1

        if abs(ball.bottom - opponent.top) < 10 and ballYSpeed > 0:
            ballYSpeed *= - 1
    
    return ballXSpeed, ballYSpeed, playerScore, opponentScore, scoreTime

def player_animation():
    if player.top <= 0:
        player.top = 0

    if player.bottom >= HEIGHT - 10:
        player.bottom = HEIGHT - 10

def opponent_animation():
    speed = 7
    if opponent.bottom > ball.y:
        opponent.bottom -= speed

    if opponent.top < ball.y:
        opponent.top += speed

    if opponent.top <= 0:
        opponent.top = 0

    if opponent.bottom >= HEIGHT - 10:
        opponent.bottom = HEIGHT - 10

def ball_start(ballXSpeed, ballYSpeed, scoreTime):
    ball.center = (WIDTH / 2, HEIGHT / 2)
    currentTime = pygame.time.get_ticks()

    if currentTime - scoreTime < 700:
        # print("inside three second block")
        numberThreeLabel = gameFont.render("3", True, colours.LIGHTGREY)
        print(numberThreeLabel)
        mainWindow.blit(numberThreeLabel, (WIDTH / 2 - 5, HEIGHT / 2 + 25))

    if 700 < currentTime - scoreTime < 1400:
        # print("inside 2 second block")
        numberTwoLabel = gameFont.render("2", True, colours.LIGHTGREY)
        print(numberTwoLabel)
        mainWindow.blit(numberTwoLabel, (WIDTH / 2 - 5, HEIGHT / 2 + 25))

    if 1400 < currentTime - scoreTime < 2100:
        # print("inside 1 second block")
        numberOneLabel = gameFont.render("1", True, colours.LIGHTGREY)
        print(numberOneLabel)
        mainWindow.blit(numberOneLabel, (WIDTH / 2 - 5, HEIGHT / 2 + 25))
    
    if currentTime - scoreTime < 2100:
        ballXSpeed, ballYSpeed = 0, 0
    else:
        ballXSpeed = 5 * random.choice((1, -1))
        ballYSpeed = 5 * random.choice((1, -1))
        scoreTime = None

    return ballXSpeed, ballYSpeed, scoreTime



def main():
     
    run = True
    ballXSpeed = 5 * random.choice((1, -1))
    ballYSpeed = 5 * random.choice((1, -1))
    playerSpeed = 0
    playerScore = 0
    opponentScore = 0
    scoreTime = True

    while run:  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerSpeed += 5
                if event.key == pygame.K_UP:
                    playerSpeed -= 5
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    playerSpeed -= 5
                if event.key == pygame.K_UP:
                    playerSpeed += 5

        # BALL ANIMATION
        ball.x += ballXSpeed
        ball.y += ballYSpeed
        ballXSpeed, ballYSpeed, playerScore, opponentScore, scoreTime = ball_animation(ballXSpeed, ballYSpeed, playerScore, opponentScore, scoreTime)
        
        # PLAYER ANIMATION
        player.y += playerSpeed
        player_animation()

        # OPPONENT ANIMATION
        opponent_animation()


        # DRAWINGS 
        mainWindow.fill(bgColour)
        pygame.draw.aaline(mainWindow, colours.LIGHTGREY, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
        pygame.draw.rect(mainWindow, colours.LIGHTGREY, player)
        pygame.draw.rect(mainWindow, colours.LIGHTGREY, opponent)
        pygame.draw.ellipse(mainWindow, colours.LIGHTGREY, ball)

        playerScoreLabel = gameFont.render(f"{playerScore}", True, colours.LIGHTGREY)
        mainWindow.blit(playerScoreLabel, (360, 250))

        opponentScoreLabel = gameFont.render(f"{opponentScore}", True, colours.LIGHTGREY)
        mainWindow.blit(opponentScoreLabel, (330, 250))

        if scoreTime:
            ballXSpeed, ballYSpeed, scoreTime = ball_start(ballXSpeed, ballYSpeed, scoreTime)


        # UPDATE WINDOW
        pygame.display.update()
        clock.tick(FPS)

    

if __name__ == '__main__':
    main()