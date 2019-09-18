import pygame
import sys
import time
import random
from pygame.locals import *
from pygame.math import Vector2

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 700
WINDOWHEIGHT = 300
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('pong no walls')

WHITE = (255, 255, 255)
collisonSound = pygame.mixer.Sound('bounce.wav')
pygame.mixer.music.load('fade.wav')
pygame.mixer.music.play(-1, 0)

moveRight = False
moveLeft = False
moveUp = False
moveDown = False
SPEED = 2


# this part of the code is your box class
def vector2(xySpeed, scale):
    velocity = Vector2()
    velocity[0], velocity[1] = xySpeed[0], xySpeed[1]
    return velocity * scale


class Box:
    def __init__(self, rect, bg_color, velocity, scale=1):
        self.bg_color_ = Color(bg_color)  # convert hex color string to Color
        self.rect_ = pygame.Rect(rect)  # convert rect tuple to pyGame.Rect
        self.velocity_ = vector2(velocity, scale)

    def __str__(self):
        return 'Box: clr={}, rect={}, velocity={}'.format(self.bg_color_, self.rect_, self.velocity_)

    def get_velocity(self):
        return self.velocity_

    def get_color(self):
        return self.bg_color_

    def get_rect(self):
        return self.rect_

    def move_box(self):
        self.rect_.left += self.velocity_[0]
        self.rect_.top += self.velocity_[1]


def play():
    global moveUp, moveLeft, moveRight, moveDown

    musicPlaying = True
    playerTotal: int = 0
    playerScore: int = 0
    aiTotal: int = 0
    aiScore: int = 0

    ball = Box(rect=pygame.draw.circle(windowSurface, (0, 0, 0), (350, 150), 10),
               bg_color='#FF0000', velocity=(1.5, 1.5), scale=SPEED)
    ballImage = pygame.image.load('player.png')
    ballStretchedImage = pygame.transform.scale(ballImage, (20, 20))

    playerWall = Box(rect=(690, 130, 10, 70), bg_color='#00FF00', velocity=(0, 0), scale=SPEED)
    playerWallImage = pygame.image.load('sidewall.png')
    stretchedPlayerWallImage = pygame.transform.scale(playerWallImage, (10, 70))

    playerTopWall = Box(rect=(500, 0, 70, 10), bg_color='#00ff00', velocity=(0, 0), scale=SPEED)
    playerTopWallImage = pygame.image.load('topBotwall.png')
    stretchedPlayerTopWallImage = pygame.transform.scale(playerTopWallImage, (70, 10))

    playerBotWall = Box(rect=(500, 290, 70, 10), bg_color='#00ff00', velocity=(0, 0), scale=SPEED)
    playerBotWallImage = pygame.image.load('topBotwall.png')
    stretchedPlayerBotWallImage = pygame.transform.scale(playerBotWallImage, (70, 10))

    aiWall = Box(rect=(0, 130, 10, 70), bg_color='#0000ff', velocity=(0, 1), scale=SPEED)
    aiWallImage = pygame.image.load('sidewall.png')
    stretchedAiWallImage = pygame.transform.scale(aiWallImage, (10, 70))

    aiTopWall = Box(rect=(100, 0, 70, 10), bg_color='#0000ff', velocity=(1, 0), scale=SPEED)
    aiTopWallImage = pygame.image.load('topBotwall.png')
    stretchedAiTopWallImage = pygame.transform.scale(aiTopWallImage, (70, 10))

    aiBotWall = Box(rect=(100, 290, 70, 10), bg_color='#0000ff', velocity=(1, 0), scale=SPEED)
    aiBotWallImage = pygame.image.load('topBotwall.png')
    stretchedAiBotWallImage = pygame.transform.scale(aiBotWallImage, (70, 10))

    Balls = [ball]
    Walls = [playerWall, playerTopWall, playerBotWall,
             aiWall, aiTopWall, aiBotWall]

    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = True
                    moveUp = False
                if event.key == K_p:
                    pygame.mixer.music.play(-1, 0)

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                if event.key == K_m:
                    pygame.mixer.music.stop()
                else:

                    musicPlaying = not musicPlaying

        for event in pygame.event.get():  # quit?
            if event.type == QUIT:
                quit_game = True

        windowSurface.fill(Color('#303030'))  # draw background

        # move down
        if moveDown and playerWall.rect_.bottom < WINDOWHEIGHT:
            playerWall.rect_.top += SPEED
        # move up
        if moveUp and playerWall.rect_.top > 0:
            playerWall.rect_.top -= SPEED
        # move left until u hit the middle point
        if moveLeft and playerTopWall.rect_.left > 350:
            playerTopWall.rect_.left -= SPEED
            playerBotWall.rect_.left -= SPEED
        # move right until u hit the right side of the window
        if moveRight and playerTopWall.rect_.right < WINDOWWIDTH:
            playerTopWall.rect_.left += SPEED
            playerBotWall.rect_.left += SPEED

        # ai wall limits
        if aiWall.rect_.top <= 0 or aiWall.rect_.bottom >= WINDOWHEIGHT:
            aiWall.velocity_[1] *= -1
        if aiTopWall.rect_.left <= 0 or aiTopWall.rect_.right >= 350:
            aiTopWall.velocity_[0] *= -1
            aiBotWall.velocity_[0] *= -1

        windowSurface.blit(ballStretchedImage, ball.get_rect())
        windowSurface.blit(stretchedPlayerWallImage, playerWall.get_rect())
        windowSurface.blit(stretchedPlayerTopWallImage, playerTopWall.get_rect())
        windowSurface.blit(stretchedPlayerBotWallImage, playerBotWall.get_rect())

        windowSurface.blit(stretchedAiWallImage, aiWall.get_rect())
        windowSurface.blit(stretchedAiTopWallImage, aiTopWall.get_rect())
        windowSurface.blit(stretchedAiBotWallImage, aiBotWall.get_rect())

        # draw first ball
        for ball in Balls:
            c = ball.get_rect()
            vel = ball.get_velocity()
            c.left += vel[0]
            c.top += vel[1]

        # draw the walls
        for wall in Walls[:]:
            r = wall.get_rect()
            v = wall.get_velocity()
            r.left += v[0]
            r.top += v[1]

            # change in velocity due to collision
            if ball.rect_.colliderect(wall.get_rect()):
                # y velocity
                if (ball.rect_.top < 0 + 10
                        or ball.rect_.bottom > WINDOWHEIGHT - 10):
                    ball.velocity_[1] *= -1
                    collisonSound.play()

                # x velocity
                if (ball.rect_.left < 0 + 10
                        or ball.rect_.right > WINDOWWIDTH - 10):
                    ball.velocity_[0] *= -1
                    collisonSound.play()

                # if ball gets off screen
            if ball.rect_.left < 0 or ball.rect_.right > WINDOWWIDTH \
                    or ball.rect_.top < 0 or ball.rect_.bottom > WINDOWHEIGHT:

                print('yourScore: ', playerScore, sep='\n')
                print('player won games', playerTotal, sep='\n')
                print('ai Score', aiScore, sep='\n')
                print('ai won games', aiTotal, sep='\n')

                # player points
                if ball.rect_.left <= WINDOWWIDTH / 2:
                    playerScore = 1 + playerScore

                    # give player a point if he has 11
                    if playerScore > 11:
                        playerTotal = 1 + playerTotal
                        playerScore = 0
                        aiScore = 0

                    # quit since player has 3 points
                    if playerTotal >= 3:
                        pygame.quit()
                        sys.exit()

                # ai Points
                if ball.rect_.right >= WINDOWWIDTH / 2:
                    aiScore = 1 + aiScore
                    # give ai point if it has 11
                    if aiScore > 11:
                        aiTotal = 1 + aiTotal
                        aiScore = 0
                        playerScore = 0

                    # quit since ai has 3 wins
                    if aiTotal >= 3:
                        pygame.quit()
                        sys.exit()

                for ball in Balls:
                    Balls.remove(ball)
                    newBall = Box(rect=(350, 150, 20, 20), bg_color='#FF0000',
                                  velocity=(random.randint(-3, 3), random.randint(-3, 3)), scale=SPEED)
                    vel = newBall.get_velocity()
                    if vel[1] == 0 and vel[0] == 0:
                        vel[1] += 1
                        vel[0] += 1
                    else:
                        c.left = vel[1]
                        c.top = vel[0]
                    c = ball.get_rect()

                    Balls.append(newBall)

        pygame.display.update()  # blit all updates to screen at once
        mainClock.tick(100)
        time.sleep(.02)  # pause slightly

    pygame.quit()
    sys.exit()


play()
