import sys, pygame

pygame.init()

size = width, height = 1000, 800

speed = [2, 2]
speed2 = [-4, 4]
black = 0, 0, 0

screen=pygame.display.set_mode(size)

ball1=pygame.image.load("assets/intro_ball.gif").convert()
ball2=pygame.image.load("assets/intro_ball.gif").convert()
ball1rect=ball1.get_rect()
ball2rect=pygame.Rect(500, 500, 111, 111)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ball1rect=ball1rect.move(speed)
    if ball1rect.left < 0 or ball1rect.right > width:
        speed[0]=-speed[0]

    if ball1rect.top < 0 or ball1rect.bottom > height:
        speed[1] = -speed[1]

    ball2rect=ball2rect.move(speed)
    if ball2rect.left < 0 or ball2rect.right > width:
        speed2[0]=-speed2[0]

    if ball2rect.top < 0 or ball2rect.bottom > height:
        speed2[1] = -speed2[1]

    screen.fill(black)
    screen.blit(ball1, ball1rect)
    screen.blit(ball2, ball2rect)
    pygame.display.flip()

