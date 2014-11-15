# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = None
player_hand = None
dealer_hand = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
CARD_BACK_COLORS = ('Blue', 'Red')
# offsets
PANEL_TEXT_H_OFFSET = 150
PANEL_HAND_V_OFFSET = 30
HAND_H_SPACE = 30
# canvas elements positions
TITLE_TEXT_POS = (100, 100)
SCORE_POS = (400, 100)
DEALER_PANEL_POS = (60, 200)
PLAYER_PANEL_POS = (60, 400)
CARD_BACK_POS = (DEALER_PANEL_POS[0], DEALER_PANEL_POS[1] + PANEL_HAND_V_OFFSET);

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        """ Create Hand object. """
        self.cards = []

    def __str__(self):
        """ Return a string representation of a hand. """
        hand_string = "Hand contains"
        for card in self.cards:
            hand_string += " " + str(card)
        return hand_string        

    def add_card(self, card):
        " Add a card object to a hand. """
        self.cards.append(card)

    def get_value(self):
        """ Value of a hand. """
        hasAces = False;
        value = 0;
        for card in self.cards:
            if card.get_rank() == 'A':
                hasAces = True
            value +=  VALUES[card.get_rank()]
        # add 10 to hand value if it doesn't bust    
        if hasAces and value <= 11:
            value += 10;
        
        return value;
    
    def is_busted(self):
        """ Check if hand is busted. """
        return self.get_value() > 21
   
    def draw(self, canvas, pos):
        """ Draw a hand on the canvas. """
        # use the draw method for cards
        card_h_pos = pos[0]
        for card in self.cards:
            card.draw(canvas, (card_h_pos, pos[1]))
            card_h_pos += CARD_SIZE[0] + HAND_H_SPACE
            
# define deck class 
class Deck:
    def __init__(self, color):
        """ Create a Deck object. """
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.color = color
        
    def shuffle(self):
        """ Shuffle the deck. """ 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        if len(self.cards) > 0:
            return self.cards.pop()
    
    def get_color(self):
        return self.color
    
    def __str__(self):
        """ Return a string representation of a deck. """
        hand_string = "Deck contains"
        for card in self.cards:
            hand_string += " " + str(card)
        return hand_string  
    
def draw_planel(canvas, text1, text2, hand, pos): 
    """ Draw a card panel for the dealer or the player. """
    
    canvas.draw_text(text1, pos, 30, "Black", "sans-serif")
    text2_pos = (pos[0] + PANEL_TEXT_H_OFFSET, pos[1])
    canvas.draw_text(text2, text2_pos, 30, "Black", "sans-serif")
    hand_pos = (pos[0],  pos[1] + PANEL_HAND_V_OFFSET)
    hand.draw(canvas, hand_pos)
    
def draw_back_of_card(canvas, pos, color):
    """ Draw the back of a card on the desired position. """
    
    card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0] * 
                CARD_BACK_COLORS.index(color), CARD_BACK_CENTER[1])

    canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, 
                      [pos[0] + CARD_BACK_CENTER[0], 
                       pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

#define event handlers for buttons
def deal():
    """ Start a new game. """
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    # if player forfeit, update score 
    if in_play:
        outcome = "Forfeit. You lose."
        score -= 1
        in_play = False
        return;
        
    # random deck color
    deck_color = random.choice(CARD_BACK_COLORS)
        
    # create and shuffle deck
    deck = Deck(deck_color)
    deck.shuffle()
    
    # player starts with two cards
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    # dealer starts with two cards
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # print hands
    # print "Player hand", player_hand
    # print "Dealer hand", dealer_hand
    
    outcome = ""
    in_play = True

def hit():
    """ Hit player. """
    global in_play, outcome, score
 
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        #print "Player ", player_hand, "-", player_hand.get_value() 
        if player_hand.is_busted():
            outcome = "You went bust and lose."
            score -= 1
            in_play = False
    
    #print outcome
       
def stand():
    """ Stand and compute scores. """
    global in_play, outcome, score
   
    # if hand is in play, 
    if in_play:
        # repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        #print "Dealer ", dealer_hand, "-", dealer_hand.get_value() 
        # updates outcome and score
        if dealer_hand.is_busted(): 
            outcome = "Dealer went bust. You win."
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "You lose."
            score -= 1
        else:
            outcome = "You win."
            score += 1
        # ends round
        in_play = False
    
    # print outcome
    
# draw handler    
def draw(canvas):
    """ Draw game. """
 
    # draw title
    canvas.draw_text("Black Jack", TITLE_TEXT_POS, 45, "Cyan", "sans-serif") 
    # draw score
    canvas.draw_text("Score: " + str(score), SCORE_POS, 30, "Black", "sans-serif") 
    # draw dealer's panel
    draw_planel(canvas, "Dealer", outcome, dealer_hand, DEALER_PANEL_POS)   
    # draw the back of the dealer's first card
    if in_play:
        draw_back_of_card(canvas, CARD_BACK_POS, deck.get_color())
    # draw player's panel
    hint = "Hit or Stand?" if in_play else "New Deal?"
    draw_planel(canvas, "Player", hint, player_hand, PLAYER_PANEL_POS)


# frame initialization
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()