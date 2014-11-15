# "Stopwatch: The Game"

# Import modules
import simplegui

# Define global variables (program state)
elapsed_time = 0
rounds = 0
score = 0

# Define "helper" functions
def format(t):
    """ Helper function format that converts time 
        in tenths of seconds into formatted string A:BC.D """
    
    tenths_of_seconds = t % 10
    t /= 10
    seconds = t % 60
    minutes = t / 60
    
    # Format String: http://www.codeskulptor.org/docs.html#string-formatting
    formatted_time = '%(minutes)0d:%(seconds)02d.%(ts)0d' % \
        {
         "minutes": minutes, 
         "seconds": seconds, 
         "ts": tenths_of_seconds
        }
    
    return formatted_time

def score_board(): 
    """ Helper function that formats the score board. """
    
    return str(score) + "/" + str(rounds)                
    
# Define event handler functions
def start_handler():
    """ Event handler for the Start button. """
    timer.start()
    
def stop_handler():
    """ Event handler for the Stop button. """
    
    global rounds
    global score
    
    if timer.is_running():
        timer.stop()
        # Increases the number of rounds
        rounds += 1
        # If the timmer stoped in a whole second
        if elapsed_time % 10 == 0:
            # Increases the score
            score += 1        
    
def reset_handler():
    """ Event handler for the Reset button. """
    
    global elapsed_time
    global rounds
    global score
    
    # In the Video Lecture the Reset Button stops the time
    # https://class.coursera.org/interactivepython-005/lecture/29
    timer.stop()
    
    elapsed_time = 0
    rounds = 0
    score = 0

def timer_handler():
    """ Event handler for timer with 0.1 sec interval. """
    
    global elapsed_time
    elapsed_time += 1

def draw_handler(canvas):
    """ Draws the score board and timer. """
    
    # Draw Score Board
    canvas.draw_text(score_board(), (155, 25), 25, 'Green')
    # Draw timer
    canvas.draw_text(format(elapsed_time), (50, 90), 40, 'White')
    
# Create a frame
frame = simplegui.create_frame('Stopwatch: The Game', 200, 150)

# Register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
start_button = frame.add_button('Start', start_handler, 100)
stop_button = frame.add_button('Stop', stop_handler, 100)
reset_handler = frame.add_button('Reset', reset_handler, 100)

# Start frame 
frame.start()
