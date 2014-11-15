# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
# constants for direction
LEFT = -1
RIGHT = 1
# constants for thrusters
ON = True
OFF = False
# Math constants
MAX_RAD = math.pi * 2 
# constants for score and lives
lives_pos = (50, 50)
score_pos = (WIDTH - 104, 50)
font_size = 24

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
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def update_position(pos, vel):
    """ Updates the positon according to the velocity. """
    pos[0] = (pos[0] + vel[0]) % WIDTH
    pos[1] = (pos[1] + vel[1]) % HEIGHT
 
def normalize_angle(angle):
    """ Angles are normalizaded between 0 and 2*pi rad. """
    return angle % MAX_RAD
            
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.acc_constant = 0.3
        self.friction_constant = 0.02
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0.0
        self.angle_constant = 0.05
        self.missile_constant = 5
        self.image = image
        self.image_size = info.get_size()
        self.image_center_off = info.get_center()
        self.image_center_on = [self.image_center_off[0] + self.image_size[0], 
                                self.image_center_off[1]]
        self.radius = info.get_radius()
        
    def steer(self, direction):
        """ Control ship. """
        self.angle_vel += self.angle_constant * direction
        
    def set_thrusters(self, state):
        """ Turn thrusters on and off. """
        
        # play the thrust sound
        if state == ON:
            ship_thrust_sound.play();
        # rewind the sound when the thrust turns off
        elif state == OFF:
            ship_thrust_sound.rewind();
                    
        self.thrust = state
                
    def update(self):
        """ Update ship position, angle and velocities. """
        
        # update the ship position, wraps around the screen when it goes off the edge
        update_position(self.pos, self.vel)
        # update angle
        self.angle = normalize_angle(self.angle + self.angle_vel)
        # compute the forward vector
        forward = angle_to_vector(self.angle)
        # friction update
        self.vel[0] *= (1 - self.friction_constant)
        self.vel[1] *= (1 - self.friction_constant)
        # when the ship is thrusting
        if self.thrust:
            # accelerate the ship in the direction of the forward vector
            self.vel[0] += forward[0] * self.acc_constant
            self.vel[1] += forward[1] * self.acc_constant
        
    def shoot(self):
        """ Shoot missiles. """
        global a_missile
        
        forward = angle_to_vector(self.angle)
        # tip of the ship's "cannon".
        missile_pos = (self.pos[0] + self.radius * forward[0], 
                       self.pos[1] + self.radius * forward[1]) 
        # sum of the ship's velocity and a multiple of the
        # ship's forward vector 
        missile_velocity = (self.vel[0] + forward[0] * self.missile_constant,
                            self.vel[1] + forward[1] * self.missile_constant)
        a_missile = Sprite(missile_pos, 
                           missile_velocity, 
                           self.angle, 
                           0, 
                           missile_image,
                           missile_info, 
                           missile_sound)
    def draw(self,canvas):
        image_center = self.image_center_on if self.thrust else self.image_center_off
        # draw ship without thrusters  
        canvas.draw_image(self.image, 
                          image_center, 
                          self.image_size, 
                          self.pos, 
                          self.image_size, 
                          self.angle)     
    
    
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
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, 
                          self.image_center, 
                          self.image_size, 
                          self.pos, 
                          self.image_size, 
                          self.angle) 
    
    def update(self):
        """ Update sprite position, angle and velocities. """
        
        update_position(self.pos, self.vel)     
        # update angle
        self.angle = normalize_angle(self.angle + self.angle_vel)

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile is not None:
        a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile is not None:
        a_missile.update()
    
    # draw lives
    canvas.draw_text("Lives", lives_pos, font_size, "White")
    canvas.draw_text(str(lives), 
                     (lives_pos[0], lives_pos[1] + font_size), 
                     font_size, 
                     "White")
    # draw scores
    canvas.draw_text("Score", score_pos, font_size, "White")
    canvas.draw_text(str(score), 
                     (score_pos[0], score_pos[1] + font_size), 
                     font_size, 
                     "White")
    
def keydown_handler(key):
    """ Handle key presses. """
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.steer(LEFT)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.steer(RIGHT)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrusters(ON) 
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        

def keyup_handler(key):
    """ Handle key releases. """
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.steer(RIGHT) 
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.steer(LEFT)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrusters(OFF)    
               
def rock_spawner():
    """ Timer handler that spawns a rock. """ 
    global a_rock
    
    rock_pos = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    rock_velocity = (random.randrange(-4, 5), random.randrange(-4, 5))
    # Angle between 0 and 2r
    rock_angle = random.random() * MAX_RAD
    rock_angle_vel = random.choice((-0.1, 0.1)) * random.random()
    
    a_rock = Sprite(rock_pos, rock_velocity, rock_angle, rock_angle_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = None

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
