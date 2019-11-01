import klaver.player.belief as belief 
import klaver.calculator.calculator as calc

import random

class Player:
    """Player of the game."""
    def __init__(self, name='P'):
        self.name = name
        self.hand = []
        self.belief = belief.Belief(self)
    
    def __str__(self):
        return '{}'.format(self.name)

    def playCard(self, playedCards, trumpSuit):
        playable = calc.selectPlayable(playedCards, trumpSuit, self.hand)
        c = random.choice(playable) # Now throws random cards 
        self.hand.remove(c)
        return c
