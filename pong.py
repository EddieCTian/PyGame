# Adapted from https://www.pygame.org/docs/tut/MakeGames.html

try:
    # always import
    import sys
    import os
    import pygame
    from import_ import *
    # game specific

    import random
    import math
    import getopt

    #for convenience using rect() and others 

    from pygame.locals import *
except ImportError as err:
    print ("Couldn't load module. %s" % (err))
    sys.exit(2)

class Ball(pygame.sprite.Sprite): #pygame.sprite.Sprite means it inherits that class' attributes
    # A ball goes across the screen
    # returns ball object
    # functions: update, calcnewpos
    # attributes: area, vector, image, rect, reinit
    def __init__(self, xy, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ball.png')
        self.center=xy
        self.rect.center=self.center
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0

    def update(self):
        out=False
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos
        [angle,z] = self.vector
        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            if tl and bl:
                out=2
            if tr and br:
                out=1
        else:
            # Deflate the rectangles so you can't catch a ball behind the bat
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)

            # self.hit added to prevent ball getting stuck in bat

            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = self.bat_hit(angle, player1.rect.centery, 0)
                # angle = math.pi-angle
                print(angle)
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = self.bat_hit(angle, player2.rect.centery, 1)
                print(angle)
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = [angle,z]
        return out
    
    def bat_hit(self, angle, bat_center, side):
        diff=self.rect.centery-bat_center
        if side==0:
            return_=float(math.pi)-angle+float(diff)/100*2
        if side==1:
            return_=float(math.pi)-angle-float(diff)/100*2
        return return_

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(int(dx),int(dy))

    def reinit(self, speed):
        self.rect.center=self.center
        self.vector=speed
    

class Bat(pygame.sprite.Sprite):
    # Moveable bat which hits the ball.
    # returns: bat obj
    # functions: reinit (reset after round), update, moveup, movedown
    # attributes: side, speed, state, score

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bat.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = bat_speed
        self.state = "still"
        self.score = 0
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0,0]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed)
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] = self.movepos[1] + (self.speed)
        self.state = "movedown"

def main():
    # define ball and player speeds

    global ball_speed, bat_speed, angle

    angle=0.0
    ball_speed=3.0
    bat_speed=5.0

    # init screen
    pygame.init()
    screen=pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("Pong")

    # background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # init font
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 60)

    # init clock
    clock = pygame.time.Clock()

    # Intro text
    title=big_font.render("Welcome to pong!", 1, (255, 255, 255))
    title_box=title.get_rect(center=(int(background.get_width()/2), int(background.get_height()/2)))

    controls=font.render("P1 uses a, z to move, P2 uses Up, Down to move. Press any movement key to begin", 1, (255, 255, 255))
    controls_box=controls.get_rect(center=(int(background.get_width()/2), title_box.bottom+10))

    change_speed=font.render("Use o, p to change the ball speed", 1, (255, 255, 255))
    change_speed_box=change_speed.get_rect(center=(int(background.get_width()/2), controls_box.bottom+10))

    background.blit(title, title_box)
    background.blit(controls, controls_box)
    background.blit(change_speed, change_speed_box)

    screen.blit(background, (0, 0))

    pygame.display.flip()

    menu = True

    while menu:
        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN:
                if event.key == K_EQUALS:
                    ball_speed +=1
                    if ball_speed>20:
                        ball_speed=20
                elif event.key == K_MINUS:
                    ball_speed -=1
                    if ball_speed<1:
                        ball_speed=1
                elif event.key == K_a or event.key == K_z or event.key == K_UP or event.key == K_DOWN:
                    menu = False
        
        current_speed=font.render("Ball speed: "+str(ball_speed), 1, (255, 255, 255))
        current_speed_box=current_speed.get_rect(center=(int(background.get_width()/2), change_speed_box.bottom+10))

        pygame.draw.rect(background, (0, 0, 0), current_speed_box.inflate(14, 0))
        background.blit(current_speed, current_speed_box)

        screen.blit(background, (0, 0))

        pygame.display.flip()
    
    # clear screen
    bigrect = Rect.union(title_box, controls_box)
    bigrect = Rect.union(bigrect, current_speed_box)

    pygame.draw.rect(background, (0, 0, 0), bigrect)

    # init players
    global player1, player2
    player1=Bat('left')
    player2=Bat('right')

    # init ball
    speed = ball_speed*[-1.0, 1.0][random.randint(0, 1)] 
    ball = Ball((int(background.get_width()/2), int(background.get_height()/2)), [angle, speed])

    # init sprites
    playersprites = pygame.sprite.RenderPlain((player1, player2))
    ballsprite = pygame.sprite.RenderPlain(ball)

    # init scores
    score_player_1 = font.render(str(player1.score), 1, (255, 255, 255))
    score_player_2 = font.render(str(player2.score), 1, (255, 255, 255))

    text_player_1 = score_player_1.get_rect(centerx=int(background.get_width()/4))
    text_player_2 = score_player_2.get_rect(centerx=int(background.get_width()*3/4))

    # blitting 
    background.blit(score_player_1, text_player_1)
    background.blit(score_player_2, text_player_2)

    screen.blit(background, (0, 0))

    pygame.display.flip()

    # event loop
    while player1.score<10 and player2.score<10:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    player1.moveup()
                if event.key == K_z:
                    player1.movedown()
                if event.key == K_UP:
                    player2.moveup()
                if event.key == K_DOWN:
                    player2.movedown()
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_z:
                    player1.movepos = [0, 0]
                    player1.state= "still"
                if event.key == K_UP or event.key == K_DOWN:
                    player2.movepos = [0, 0]
                    player2.state= "still"

        # clear out old positions
        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)

        # score checking
        hello=ball.update()
        if type(hello) == int:
            if hello == 1:
                player1.score+=1
                score_player_1 = font.render(str(player1.score), 1, (255, 255, 255))
                text_player_1 = score_player_1.get_rect(centerx=int(background.get_width()/4))
                pygame.draw.rect(background, (0, 0, 0), text_player_1.inflate(2, 2))
                background.blit(score_player_1, text_player_1)

            elif hello == 2:
                player2.score+=1
                score_player_2 = font.render(str(player2.score), 1, (255, 255, 255))
                text_player_2 = score_player_2.get_rect(centerx=int(background.get_width()*3/4))
                pygame.draw.rect(background, (0, 0, 0), text_player_2.inflate(2, 2))
                background.blit(score_player_2, text_player_2)

            screen.blit(background, (0, 0))

            speed=float(ball_speed*[-1.0, 1.0][random.randint(0, 1)])
            ball.reinit([angle, speed])

        # update ball position
        ballsprite.update()

        # update players
        playersprites.update()

        ballsprite.draw(screen)
        playersprites.draw(screen)

        # flip screen
        pygame.display.flip()
    
    if player1.score == 10: 
        winner = 'Player 1'
        score = player1.score
    else:
        winner = 'Player 2'
        score = player2.score
    final_message=font.render("The winner is "+winner+" with a score of "+ str(score), 1, (255, 255, 255))
    final_message_box=final_message.get_rect(center=(int(background.get_width()/2), int(background.get_height()/2)))
    background.blit(final_message, final_message_box)

    screen.blit(background, (0, 0))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return True

if __name__=='__main__': main()