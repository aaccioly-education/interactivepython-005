# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
HALF_BALL_RADIUS = BALL_RADIUS / 2
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_ACC = 5
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = None
ball_vel = None
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

def update_pos(paddle_pos, velocity):
    """ Update paddle's vertical position, keep paddle on the screen. """
   
    next_paddle_v_pos = paddle_pos[1] + velocity
    
    if next_paddle_v_pos >= 0 and  next_paddle_v_pos <= HEIGHT - PAD_HEIGHT:
        paddle_pos[1] = next_paddle_v_pos

def is_striking_a_paddle(paddle_pos):
    """ Checks is the ball is striking a paddle. """
   
    # The ball is not striking a paddle if
    # A. ball vertical position > paddle vertical position
    # B. ball horizontal position < paddle vertical position
    
    a = (ball_pos[1] >= (paddle_pos[1] + PAD_HEIGHT - 1) + HALF_BALL_RADIUS)
    b = (ball_pos[1] <= paddle_pos[1] - HALF_BALL_RADIUS)
      
    # It is strinking the paddle if:
    #  NOT(A) AND NOT(B)
    return not(a) and not(b)
        
def spawn_ball(direction):
    """ Initialize ball_pos and ball_vel for new bal in middle of table
        if direction is RIGHT, the ball's velocity is upper right, else upper left. """
    
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    # 120 to 240 pixels per second
    horizontal_speed = random.randrange(2, 4)
    # 60 to 180 pixels per second
    vertical_speed = random.randrange(1, 3)
    
    if direction == RIGHT:
        ball_vel = [horizontal_speed, -vertical_speed]
    else:
        ball_vel = [-horizontal_speed, -vertical_speed]    
        
# define event handlers
def new_game():
    """ Starts a new game. """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    starting_direction = random.choice([LEFT, RIGHT])
    
    spawn_ball(starting_direction)

def draw(canvas):
    """ Draw the shapes of the game. """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's position
    update_pos(paddle1_pos, paddle1_vel);
    update_pos(paddle2_pos, paddle2_vel);
    
    # Detect collisions with gutters and paddles
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        # Striking left paddle
        if is_striking_a_paddle(paddle1_pos):
            ball_vel[0] = -ball_vel[0] * 1.1	
        # Strking left gutter
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - 1) - BALL_RADIUS:
        # Striking right paddle
        if is_striking_a_paddle(paddle2_pos):
            ball_vel[0] = - ball_vel[0] * 1.1	
        # Strking right gutter
        else:
            score1 += 1
            spawn_ball(LEFT)
        
    # draw paddles
    paddle1_pos_two = (paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT)
    canvas.draw_line(paddle1_pos, paddle1_pos_two, PAD_WIDTH, 'White')
    paddle2_pos_two = (paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT)
    canvas.draw_line(paddle2_pos, paddle2_pos_two, PAD_WIDTH, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4 - 10, 50), 40, 'White')
    canvas.draw_text(str(score2), (WIDTH / 4 * 3 -10, 50), 40, 'White')
    
def keydown(key):
    """ Controls paddles velocity. """
    global paddle1_vel, paddle2_vel
 
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PAD_ACC
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PAD_ACC
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PAD_ACC
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PAD_ACC
   
def keyup(key):
    """ Make the paddles stand still when control keys
        are released. """
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button_reset = frame.add_button('Restart', new_game, 100)


# start frame
new_game()
frame.start()
