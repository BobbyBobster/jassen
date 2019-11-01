class Player:
    """Player of the game."""
    def __init__(self, name='P'):
        self.name = name
        self.hand = []
        self.belief = Belief(self)

    def playCard(self, playedCards, trumpSuit):
        playable = calc.selectPlayable(playedCards, trumpSuit, self.hand)
        c = random.choice(playable) # Now throws random cards 
        self.hand.remove(c)
        return c
