import klaver.common.deckscards as dc

import numpy as np

class Belief:
    """Probability distribution over all players per card.

    Since each card is dealt to some player (including the beliefholder) we can 
    view this as a pmf.

    Members:
        self.beliefHolder : The Player object whose beliefs we model.
        self.pmf : A 4x8x5 NumPy Array which holds te probability values for 
        cards in the hands of players. Dimensions are suit x rank x player, 
        where player0 is the beliefholder and player4 is the discard pile.


    Methods:
        resetBelief : At the start of a new round each player knows the cards 
        in their hands and hence knows the probabilities of those cards. 
        As there is no information about any other cards, those are set to be 
        uniformly distributed.
        normalize :



    NOTE: There are actually 2 beliefs, the one about the current state of the 
    game and which player has which card during play. 
    And one about the starting state of the game, this belief also evolves as 
    cards are being played and is a way to backwards deduce why players have 
    bid as they did.
    """

    deck = dc.Deck()

    def __init__(self, beliefHolder):
        self.beliefHolder = beliefHolder
        self.pmf = np.zeros((4,8,5))

    def clearProbabilities(self, card):
        self.pmf[card.suit, card.rank] = [0,0,0,0,0]

    def rowsumTest(self):
        if (np.sum(self.pmf, axis=2) == 1).all():
            print("rowsum is fine")
        else:
            raise Exception("function changed probabilities such that rowsum != 1")

    def resetBelief(self):
        for card in self.deck.cards:
            if card in self.beliefHolder.hand:
                self.pmf[card.suit, card.rank] = [1,0,0,0,0]
            else:
                self.pmf[card.suit, card.rank] = [0,1/3,1/3,1/3,0]
        self.rowsumTest()

    # NOTE(bb20191030): I have a feeling this doesnt work as intended
    def normalize(self):
        """Change probability values such that they add up to one but keep 
        their ratio."""
        s = np.sum(self.pmf, axis=2)
        for card in self.deck.cards:
            for player in range(5):
                self.pmf[card.suit, card.rank, player] /= s[card.suit, card.rank]
        self.rowsumTest()

    # TODO: Create setBelief method to change manually change a 
    #       probability in pmf
    def setCardProbabilities(self, card=None, values=None, suit=None, rank=None):
        if card is not None:
            suit = card.suit
            rank = card.rank
        
        if not isinstance(values, (list, tuple)) or len(values) != 5:
            raise Exception("values must be a 5-tuple or list with 5 elements")

        self.pmf[suit, rank] = values
#        self.rowsumTest() 

    def getCardProbabilities(self, card=None, suit=None, rank=None):
        if card is not None:
            return self.pmf[card.suit, card.rank]
        if suit is not None and rank is not None:
            return self.pmf[suit, rank]

    # NOTE(bb20191031): Choose between toDiscard method and cardPlayed method
    #   both are doing the same(?) now
    def toDiscard(self, card=None):
        """When a Card is played that Card will go to the discard pile so is 
        not in any Players hand."""
        self.setCardProbabilities(card, (0,0,0,0,1))
        
    def notFollowed(self, playerIndex=None, suit=None):
        """When a player doesnt follow suit, this means that they for certain 
        do not have any more cards in that suit."""
        if suit is not None and playerIndex is not None and isinstance(playerIndex, int):
            self.pmf[suit,:,playerIndex] = (0,0,0,0,0,0,0,0)
            self.normalize()
