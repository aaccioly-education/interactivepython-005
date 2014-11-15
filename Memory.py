# implementation of card game - Memory

import simplegui
import random

CARD_SIZE = (50, 100)
TEXT_DISPLACEMENT = (13, 65)
DECK_SIZE = 16

deck = None
exposed = None
state = None
first_card_idx = None
second_card_idx = None
turns = None

# helper function to initialize globals
def new_game():
    """ Start a new game. """
    global deck
    global exposed
    global state
    global turns
    
    # builds deck
    deck = range(DECK_SIZE / 2) + range(DECK_SIZE / 2)
    # and shuffles
    random.shuffle(deck)
    
    # every card starts hidden
    exposed = [False] * DECK_SIZE
    state = 0
    turns = 0
    
    label.set_text("Turns = " + str(turns))
    
def memory_state_machine(card_idx):
    """ Flip cards and check for pairs."""
    
    global state
    global first_card_idx
    global second_card_idx
    global turns
    
    # first click
    if state == 0:
        # register first exposed card
        first_card_idx = card_idx
        state = 1
    # even clicks 
    elif state == 1:
        # register second exposed card
        second_card_idx = card_idx
        # update the number of turns
        turns += 1
        label.set_text("Turns = " + str(turns))
        state = 2
    # odd clicks  
    else:
        # if the two last exposed cards have different values
        if deck[first_card_idx] != deck[second_card_idx]:
            # turn previous cards down
            exposed[first_card_idx] = False
            exposed[second_card_idx] = False  
        # register the first exposed card    
        first_card_idx = card_idx
        state = 1
   
    # always flip current card    
    exposed[card_idx] = True      
     
# define event handlers
def mouseclick(pos):
    """ Pick a card. """
        
    select_card_idx = pos[0] / CARD_SIZE[0]
    
    # ignore clicks on exposed cards
    if not exposed[select_card_idx]:
        # flip card and check for pairs
        memory_state_machine(select_card_idx)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    """ Draw the game board. """
    
    # card position
    pos = (0,0)
    
    # display cards
    for card_index in range(DECK_SIZE):
        card = deck[card_index]
        if exposed[card_index]:
            # exposed card
            canvas.draw_text(
                str(card), 
                (pos[0]+ TEXT_DISPLACEMENT[0], pos[1] + TEXT_DISPLACEMENT[1]), 
                40, 
                'White')	
        else:
            # hidden card
            canvas.draw_polygon([
                pos, 
                (pos[0], pos[1] +  CARD_SIZE[1]),
                (pos[0] + CARD_SIZE[0], pos[1] + CARD_SIZE[1]),
                (pos[0] + CARD_SIZE[0], pos[1])], 
                1, 
                'Brown', 
                'Green')        
        #updates card position
        pos = (pos[0] + CARD_SIZE[0], pos[1])                        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()