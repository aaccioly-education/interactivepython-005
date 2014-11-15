# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# import the modules
import simplegui
import random
import math

# define global variables (program state)
player_guess = None
secret_number = None
max_range = 100
allowed_guesses = None

# helper functions

def new_game():
    """ Helper function to start and restart the game. """
    
    # initialize global variables used in the code
    global secret_number
    global max_range
    global allowed_guesses
    
    # compute allowed guessess
    allowed_guesses = int(math.ceil(math.log(max_range, 2)))
    # chooses a new secret number
    secret_number = random.randrange(max_range)
    
    print "New game. Range is from 0 to", max_range
    print "Number of remaining guesses is", allowed_guesses, "\n" 

# define event handlers for control panel

def range100():
    """ Changes the range to [0,100) and starts a new game. """ 
    global max_range
    
    max_range = 100
    
    new_game()

def range1000():
    """ Changes the range to [0,1000) and starts a new game  """    
    global max_range
    
    max_range = 1000
    
    new_game()
    
def input_guess(guess):
    """ Main game logic. """ 
    global player_guess
    global allowed_guesses

    # local variables
    finished = False
    result = None
    
    # convert play guess to int
    player_guess = int(guess)
    # updates allowed number of guessess
    allowed_guesses-= 1
    
    print "Guess was", player_guess
    print "Number of remaining guesses is", allowed_guesses
 
    # logic to check the guess
    if player_guess < secret_number:
        result = "Higher!"
    elif player_guess > secret_number:
        result = "Lower!"
    else:
        result = "Correct!"
        finished = True
     
    # print results for the round
    if allowed_guesses == 0 and not finished:
        print "You ran out of guesses.  The number was",  secret_number
        finished = True
    else:
        print result
    
    print
    
    # automatically restarts the game when it finished
    if finished:
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess The Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_input("Input", input_guess, 25)
button_reset = frame.add_button("Reset", new_game)
button_range100 = frame.add_button("Range: 0 - 100", range100)
button_range1000 = frame.add_button("Range: 0 - 1000", range1000)

# call new_game 
new_game()