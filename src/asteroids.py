# https://www.pygame.org/docs/#

import pygame
import os
import math 

# import Sprite2


main_dir = os.path.split(os.path.abspath(__file__))[0]
print(main_dir)

assets_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'assets'))


SCREENRECT = pygame.Rect(0, 0, 1280, 720)

screen = pygame.display.set_mode((SCREENRECT.size))


background = pygame.Surface(SCREENRECT.size)

background.fill("blue")


class Sprite2(pygame.sprite.Sprite, ):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        # print("sprite created")

    def Init(self, **kwargs):
        # print(kwargs['path'])

        # check if we shouldn't add a sprite to the all group (for player to control it's own rendering)
        if(not "dont_add_to_group" in kwargs):
            kwargs["render_group"].add(self)
        #
        self.image = pygame.image.load( os.path.join(self.asset_dir, kwargs['path']+".png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=SCREENRECT.topleft)
        #rectangle used int- so rounds out position/ velocity when moving things/ slowing down
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)

        # for allowing rotation
        self.img_original=self.image #to store the original image to allow rotating from it
        self.rect_original = self.rect

        self.scale = 1.0
        self.angle=0.0
        self.angle_rads=0.0


        self.drag=.99
        self.speed=0.0
        self.max_speed=10
        


        #for "physics"

        self.vel= pygame.math.Vector2(0.0,0.0)
        return self
    
    # for auto setting the radians with the angle in degrees being set
    def SetAngle(self, angle):
        self.angle=angle
        self.angle_rads=math.radians(self.angle)

    def Rotate(self, degrees):

        # print("rotating degrees: ",degrees)
        self.SetAngle(self.angle+degrees)


        # self.image = pygame.transform.rotate(self.img_original, self.rotation)

        # MUCH less jagged / aliased than normal rotate

        # self.rect_original.x=self.pos.x
        # self.rect_original.y=self.pos.y

        # self.image = pygame.transform.rotozoom(self.img_original, self.angle, 1)
        # self.rect = self.image.get_rect(center = self.rect_original.center)
    
    # percent in decimal/ 0.0-1.0
    def ResizePercentOriginal(self, percent):
        
        self.scale = percent
        # new_width = percent*self.img_original.get_rect().width
        # new_height = percent*self.img_original.get_rect().height
        # self.image = pygame.transform.scale(self.img_original, (new_width, new_height))
        # self.rect.width = new_width
        # self.rect.height = new_height
        # print("resized asteroid, w, h: ", new_width, new_height, "percent: ",percent)


    #for after updating a rect- since using position for being able to position based on floats/ no rounding errors, we have to update position after changing rect
    def RectUpdated(self):
        self.rect_original.x=self.rect.x
        self.rect_original.y=self.rect.y
        self.pos.x=self.rect_original.x
        self.pos.y=self.rect_original.y
    

    def update(self):

        # print("updating sprite")

        self.pos.x+=self.vel.x
        self.pos.y+=self.vel.y

        self.rect_original.x=self.pos.x
        self.rect_original.y=self.pos.y
        
        self.image = pygame.transform.rotozoom(self.img_original, self.angle, self.scale)
        self.rect = self.image.get_rect(center = self.rect_original.center)

        self.WrapIfApplicable()



        # self.rect_original.y+=self.vel.y


        # self.rect.x+=self.vel.x

        # self.rect_original.x+=self.vel.x


        # if(self.speed>0):

        
        

        # print("angle rads: ", self.angle_rads, "angle: ", self.angle, "speed:", self.speed, "velocity: ",self.vel)
    def WrapIfApplicable(self):
        if(self.pos.x>SCREENRECT.width):
            self.rect.x=0-self.rect.width
            self.RectUpdated()

        elif(self.pos.x+self.rect.width<0):
            self.rect.x=SCREENRECT.width
            self.RectUpdated()


        if(self.pos.y>SCREENRECT.height):
            self.rect.y=0-self.rect.height
            self.RectUpdated()

        elif(self.pos.y+self.rect.height<0):
            self.rect.y=SCREENRECT.height
            self.RectUpdated()






class Player(Sprite2):
    def __init__(self):
        Sprite2.__init__(self)     
        self.thrusting=False
        
        

    def InitHitArea(self):

        # for having more fair hit area for the player
        self.hit_area_reduction=.7
        # self.rect_hit_area = self.rect_original
        # self.rect_hit_area = pygame.Rect(0, 0, self.rect.width*self.hit_area_reduction, self.rect.height*self.hit_area_reduction)
        # self.rect_hit_area.center=self.rect
        print("player created")


    #for giving the ship thrust/ moving it forward /backwards in the direction its facing

    def Thrust(self, amount):

        amount*=10
        # print("thrust acheieved! ", amount)
        #should figure out the amount of thrust to go in the x and y direction, depending on the angle the ship is facing
        self.thrusting=True
        self.speed+=(amount*dt)

        if(self.speed>0):
            if(self.speed>self.max_speed):
                self.speed= self.max_speed
        elif(self.speed<0):
            if(self.speed<-self.max_speed):
                self.speed= -self.max_speed
        
        # print("speed: ", self.speed)

        self.vel.x=math.sin(self.angle_rads)*(-self.speed)
        self.vel.y=math.cos(self.angle_rads)*(-self.speed)

    def update(self):
        self.speed*=self.drag
        self.vel.x*=self.drag
        self.vel.y*=self.drag

        Sprite2.update(self)

        # update hit area
        # self.rect_hit_area.x=self.rect.x
        # self.rect_hit_area.y=self.rect.y
        
        # self.rect_hit_area.center=self.rect

    def Reset(self):
        self.rect.center=SCREENRECT.center
        self.angle=0
        self.RectUpdated()
        self.vel.x=0
        self.vel.y=0



class Bullet(Sprite2):

    # static vars
    max_life=0.65

    def __init__(self, render_group):
        Sprite2.__init__(self)
        self.Init(path="bullet", render_group=render_group)

        self.lifetime=0
        # self.vel.x=5
        # self.vel.y=5
    
    def update(self):
        Sprite2.update(self)
        self.lifetime+=dt
        if(self.lifetime>self.max_life):
            self.kill()

        # if(not SCREENRECT.contains(self.rect)):
            # print("killing bullet")
            # self.kill()

class Asteroid(Sprite2):
    # static variables

    # asteroids sizes- from 1 to 4 - using 1 instead of 0 to make dividing by size not be dived by zero (or would have to add a 1 each time)

    asteroid_sizes = [.5, 1, 1.5, 2.5]
    asteroid_scores = [200, 100, 50, 25]


    # We'll set size from 1 being the smallest/ half default size to 5 being the largest
    def __init__(self, render_group, size, angle):
        Sprite2.__init__(self)
        self.Init(path="asteroid_basic", render_group=render_group)

        self.SetupAsteroid(size, angle)

    def SetupAsteroid(self, size, angle):
        

        if(size>self.asteroid_sizes.__len__()):
            size = self.asteroid_sizes.__len__()
        self.size=size
        # print("asteroid size: ", size)
        self.SetAngle(angle)
        self.SetupFromSize()
        
    
    def SetupFromSize(self):
        self.ResizePercentOriginal(self.asteroid_sizes[self.size-1])
        self.speed = (1/self.size) *5
        self.vel.x=math.cos(self.angle_rads)*self.speed
        self.vel.y=math.sin(self.angle_rads)*self.speed

    def update(self):
        Sprite2.update(self)
        self.SetAngle(self.angle+ (1/self.size)*3 )

    
    def AsteroidHit(self):
        # should make itself smaller (or destroy if smallest size), and spawn a new asteroid, and increase score
        # print("asteroid hit")

        AddScore(self.asteroid_scores[self.size-1])
        self.size-=1

        
        if(self.size<1):
            self.kill()
        else:
            self.SetupFromSize()
            # spawn new asteroid in opposite angle
            asteroid = Asteroid(all, size=self.size, angle=self.angle+180)
            asteroid.rect.center=self.rect.center
            asteroid.RectUpdated()
            asteroids.add(asteroid)




# ------------------Game functions ---------------------
lives_original=3
lives=3
game_over=False
player_dead=False
player_invincible= False


spawn_delay=0.25
spawn_timer=1.0

def SpawnBullet():
    global spawn_timer
    # print("spawn_delay", spawn_delay)
    # print("spawn_timer", spawn_timer)
    if(spawn_timer>spawn_delay):
        # print("spawning bullet")
        spawn_timer=0.0
        bullet = Bullet(all)
        # all.add(bullet)
        bullets_player.add(bullet)

        # need to spawn bullet on top of ship, and moving in the same angle ship is facing
        bullet.pos.x=player.rect_original.centerx -math.sin(player.angle_rads)*player.rect.width*.5
        bullet.pos.y=player.rect_original.centery -math.cos(player.angle_rads)*player.rect.height*.5

        bullet.vel.x = -math.sin(player.angle_rads)*5 + player.vel.x
        bullet.vel.y = -math.cos(player.angle_rads)*5 + player.vel.y

def PlayerInjured():
    # need to stop rendering player temporarily
    global player_dead
    player_dead=True

    # decrease lives
    global lives
    lives-=1



    # Reste player angle and position
    player.Reset()


    # end game if lives <0
    if(lives<0):
        GameOver()

player_respawn_timer=0
player_respawn_delay=2
player_respawn_visible=.5

player_blink_timer=0
player_blink_delay = .2
player_blinking=False # for if not visible / blinking for a second when injured
def ReSpawnPlayer():
    global player_respawn_timer
    global player_dead
    global player_invincible
    global player_blink_timer
    global player_blink_delay
    global player_blinking

    player_respawn_timer+=dt

    if(not player_invincible):
        if(player_respawn_timer>player_respawn_visible):                    
            player_invincible=True            

    elif(player_respawn_timer>player_respawn_delay):
        player_respawn_timer=0 
        player_blink_timer=0
        player_invincible=False
        player_dead=False
        player_blinking=False
    else: # player is invincible, not not fully spawned
        player_blink_timer+=dt
        if(player_blink_timer>player_blink_delay):
            player_blinking= not player_blinking
            player_blink_timer=0


    # print(player_respawn_timer)

def GameOver():
    print("game over man!")
    global game_over
    game_over=True

def RestartGame():
    global lives
    global lives_original
    global score
    lives=lives_original
    ResetScore()

    global game_over
    game_over=False

    player.Reset()

    # clear out asteroids and restart at level 1
    global asteroids
    asteroids.empty()
    all.empty()
    LoadLevel(0)


def LoadLevel(num):

    global asteroids

    if(num==0):
        asteroid = Asteroid(all, size=5, angle=125)
        asteroid.rect.centerx=SCREENRECT.centerx
        asteroid.RectUpdated()
        asteroids.add(asteroid)

        asteroid2 = Asteroid(all, size=5, angle=0)
        asteroid2.rect.centerx=SCREENRECT.width*.25
        asteroid2.rect.centery=SCREENRECT.height*.25
        asteroid2.RectUpdated()
        asteroids.add(asteroid2)

        asteroid3 = Asteroid(all, size=5, angle=45)
        asteroid3.rect.centerx=SCREENRECT.width*.75
        asteroid3.rect.centery=SCREENRECT.height*.75
        asteroid3.RectUpdated()
        asteroids.add(asteroid3)


# pygame setup
pygame.init()
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
running = True
dt = 0





all = pygame.sprite.Group()
bullets_player = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Player.containers = all



#for all sprites to use the same asset dir- set as a static var

Sprite2.asset_dir = assets_dir +"/"

player = Player()
player_img = pygame.image.load( os.path.join(Sprite2.asset_dir, "spaceship_basic.png")).convert_alpha()
# print("player rect: ",player.rect)
# player.InitHitArea()

player.Init(path="spaceship_basic", dont_add_to_group=True)

player.rect.center=SCREENRECT.center
player.RectUpdated()

# asteroid1 = Sprite2()
# asteroid1.Init(path="asteroid_basic", render_group=all)


# all.add(player)
# all.add(asteroid1)

LoadLevel(0)





# UI stuff

score=0
score_font = pygame.font.Font(None, 60)
score_txt = score_font.render("Score: "+str(score), True, (255,255,255))

game_over_txt1 = score_font.render("Game Over Man!", True, (255,255,255))
game_over_txt2 = score_font.render("Score: "+str(score), True, (255,255,255))
game_over_txt3 = score_font.render(" Press 'Space' to restart", True, (255,255,255))



def AddScore(points):
    global score
    global score_txt
    score+=points
    # print("added to score", points)
    score_txt = score_font.render("Score: "+str(score), True, (255,255,255))

def ResetScore():
    global score
    global score_txt
    score=0
    score_txt = score_font.render("Score: "+str(score), True, (255,255,255))

# asteroids.add(all)


# player2 = Player()

# player2.rect = player2.image.get_rect(midbottom=SCREENRECT.center)




# def CreatePlayer():

#     print("create player")

#     player_sprite = Sprite2.Sprite2()








# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)





# asteroid1 = pygame.image.load(assets_dir+'/asteroid_basic.png').convert_alpha()

# asteroid2 = pygame.image.load(assets_dir+'/asteroid2.png').convert_alpha()


spaceship = pygame.image.load(assets_dir+'/spaceship_basic.png').convert_alpha()
pygame.display.set_icon(spaceship)

# rescales images permenantly...

# spaceship = pygame.transform.scale(spaceship, (50, 75))

# spaceship = pygame.transform.scale(spaceship, (300, 300))


# spaceship_rect = spaceship.get_rect(center =((screen.get_width()/2,screen.get_height()/2)))


# rotation=0


while running:

    # poll for events

    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # else if event.type ==pygame.


    # fill the screen with a color to wipe away anything from last frame

    screen.fill("black")


    # clear/erase the last drawn sprites

    # all.clear(screen, background)


    # update all the sprites

    # all.update()


    # all.draw(screen)


    # draw the scene

    # dirty = all.draw(screen)

    # pygame.display.update(dirty)

    

    # screen.blit(player.image, player.rect.midbottom)

    

    if(not game_over):
        if(not player_dead):
            screen.blit(player.image, player.rect)
            player.update()
        else:
            ReSpawnPlayer()
            if (player_invincible):
                if(not player_blinking):
                    screen.blit(player.image, player.rect)
                player.update()

    all.draw(screen)
    all.update()

    # for asteroid in pygame.sprite.spritecollide(bullets_player, asteroids, 0):
    #     print("bullet hit asteroid!")

    # Collisions
    for bullet in bullets_player:
        for asteroid in asteroids:
            if(bullet.rect.colliderect(asteroid.rect)):
                # print("bullet hit asteroid!")
                bullet.kill()

                # should actually spawn another asteroid, and shrink this one, if above a certain size
                asteroid.AsteroidHit()

                #should also spawn a explosion animation

    if(not player_dead and not player_invincible):
        for asteroid in asteroids:
            if(player.rect.colliderect(asteroid.rect)):
                asteroid.AsteroidHit()
                PlayerInjured()


    keys_down = pygame.key.get_pressed()
    # key_repeat = pygame.key.get_repeat()

    if(not game_over):
        if(not player_dead or player_invincible):

            if(keys_down[pygame.K_RIGHT]):
                player.Rotate(-5.0)
            elif(keys_down[pygame.K_LEFT]):
                player.Rotate(5.0)

            if(keys_down[pygame.K_UP]):
                player.Thrust(1)
            elif(keys_down[pygame.K_DOWN]):
                player.Thrust(-1)
            else:
                player.thrusting=False

            if(keys_down[pygame.K_SPACE] and not player_invincible):
                SpawnBullet()
    else:
       if(keys_down[pygame.K_SPACE]):
            RestartGame()


    spawn_timer+=dt

    # if(bullets_player.__len__()>0):
    #     print("num bullets: ", bullets_player.__len__())

    # print("spawn timer: ", spawn_timer)



    #where things are drawn

    # screen.blit(asteroid1, (100,100))

    # screen.blit(asteroid2, (200,200))

    # asteroid1.rect.centerx=pygame.mouse.get_pos()[0]
    # asteroid1.rect.centery=pygame.mouse.get_pos()[1]

    # rect_asteroid = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], asteroid1.rect.width, asteroid1.rect.height)

    # rect_asteroid = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 100, 100)


    # screen.blit(asteroid1, (pygame.mouse.get_pos()[0]-asteroid1.get_rect().center[0], pygame.mouse.get_pos()[1]-asteroid1.get_rect().center[1]))

    # screen.blit(asteroid1, (pygame.mouse.get_pos()))



    # collide = pygame.Rect.colliderect(player.rect, asteroid1.rect)

    # if(collide):
    #     print("collision!! player rect: ", player.rect, ", rect_asteroid: ",asteroid1.rect)

    


    #https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

    # rotated_image = pygame.transform.rotate(spaceship, rotation)

    # new_rect = rotated_image.get_rect(center = spaceship_rect.center)


    # spaceship2 = pygame.transform.rotate(spaceship, rotation)

    # rotation+=5

    # spaceship_rect.x+=1;

    # spaceship_rect.y+=1;



    # screen.blit(rotated_image, new_rect)

    # screen.blit(spaceship, spaceship_rect)

    # UI stuff
    screen.blit(score_txt, (20,20))

    if(not game_over):
        screen.blit(score_txt, (20,20))
    else:
        screen.blit(game_over_txt1, (450,200))
        screen.blit(game_over_txt2, (550,250))
        screen.blit(game_over_txt3, (400,400))
    

    for i in range(lives):
        screen.blit(player_img, (20+i*50,60))


    # flip() the display to put your work on screen
    pygame.display.flip()


    # limits FPS to 60

    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()