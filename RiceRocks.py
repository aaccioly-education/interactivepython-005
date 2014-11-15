# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
INITIAL_LIVES = 3
MAX_NUMBER_OF_ROCKS = 12
SAFE_DISTANCE = 150
SCORE_TO_SPEED_RATIO = 20.0
score = 0
lives = 0
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(sprites, canvas):
    """ Call the update and draw methods for each sprite in the group. 
        Sprites with age greater than or equal to its lifespan are also removed. """
    for sprite in set(sprites):
        sprite.draw(canvas)
        ## if sprite aged beyhond its lifespan
        if sprite.update():
            ## remove object from the original set
            sprites.remove(sprite)
            
 
def group_collide(group, other_object):
    """ Detect collisions between a group and a sprite. 
        Colliding object are removed from the group.
        Return True or False depending on whether there was a collision. """
    has_collided = False
    ## Iterate over a copy of the set
    for sprite in set(group):
        if sprite.collide(other_object):
            ## remove object from the original set
            group.remove(sprite)
            ## creates explosion sprite
            a_explosion = Sprite(sprite.get_position(), (0,0), 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)
            has_collided = True
    
    return has_collided 

def group_group_collide(group1, group2):
    """ Detect collisions between two groups of sprites. 
        Colliding object are removed from the first group.
        Return the number of elements in the first group that collide with the second group"""
    n_collisions = 0;
    ## Iterate over a copy of the first set
    for sprite in set(group1):
        ## if the current sprite collided with a sprite from group 2
        if group_collide(group2, sprite): 
            ## remove object from first group
            group1.remove(sprite)
            n_collisions += 1
    
    return n_collisions 

def new_game():
    """ Starts a new game. """
    global started, lives, score, my_ship, missile_group
    
    lives = INITIAL_LIVES
    score = 0
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    missile_group = set()
    soundtrack.play()
    started = True

def game_over():
    """ Remove sprites, rewind soundtrack. """
    global started, rock_group, missile_group, explosion_group 

    started = False
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    soundtrack.rewind()
    
# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_position(self):
        """ Returns the ship position. """
        return self.pos
    
    def get_radius(self):
        """ Returns the ship radius. """
        return self.radius
    
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.dim = ()
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        center = list(self.image_center)
        if self.animated:
            index = self.age % self.lifespan
            center[0] += index * self.image_size[0]
            
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age
        self.age += 1
        
        # true if sprite hit its lifespan, false otherwise
        return self.age >= self.lifespan
     
    def collide(self, other_object):
        """  Detect collisions. """   
        distance = dist(self.pos, other_object.get_position())  
        return distance <= self.radius + other_object.get_radius()       

    def get_position(self):
        """ Returns the sprite position. """
        return self.pos
    
    def get_radius(self):
        """ Returns the sprite radius. """
        return self.radius
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        new_game()


def draw(canvas):
    global time, started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI

    # draw and update ship
    my_ship.draw(canvas)
    my_ship.update()
    # draw and update rocks
    process_sprite_group(rock_group, canvas)
    # draw and update missiles
    process_sprite_group(missile_group, canvas)
    # draw and update explosions
    process_sprite_group(explosion_group, canvas)
    
    # Draw scores
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # if the ship hit any of the rocks
    if group_collide(rock_group, my_ship): 
        # decrease the number of lives by one
        lives -= 1
        # game over
        if lives <= 0:
            game_over()
    
    # Detect collisions between missiles and rocks.
    # Increment the score each time a missile collides with a rock.
    score += group_group_collide(missile_group, rock_group)

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

   
def rock_spawner():
    """ Timer handler that spawns a rock. """ 
    if (started and len(rock_group) <= MAX_NUMBER_OF_ROCKS):
        rock_pos = []
        distance_to_ship = 0
        
        ## prevents rocks from spawning too close to the ship
        while distance_to_ship < SAFE_DISTANCE:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            distance_to_ship = dist(rock_pos, my_ship.get_position())
        
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        ### Every rock hit increases the average rock speed by 5%
        ### Every 20 score doubles the average speed
        score_boost = 1 + score / SCORE_TO_SPEED_RATIO
        rock_vel = [score_boost * rock_vel[0], score_boost * rock_vel[1]]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
