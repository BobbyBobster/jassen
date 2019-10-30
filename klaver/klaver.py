import random
import numpy as np

#TODO: Implement a way to be able to play against the computer 

class Card:
    """Standard playing card."""
    SUITS = (0,1,2,3)
    RANKS = (0,1,2,3,4,5,6,7)
    # Note that we use the No-Trump ordering of cards
    SUITSstr = tuple('s h c d'.split())
    RANKSstr = tuple('7 8 9 J Q K X A'.split())

    __slots__ = ['suit', 'rank']

    def __init__(self, suit, rank):
        self.suit, self.rank = suit, rank

    def __repr__(self):
        return 'Card({},{})'.format(self.suit, self.rank)

    def __str__(self):
        return '({}, {})'.format(self.SUITSstr[self.suit], self.RANKSstr[self.rank])

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __eq__(self, other):
        """Return true when suit and rank are same of two cards.
        Needed so we can create dicts with Card objects as keys."""
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False


class Deck:
    """Deck of cards, which holds 32 Card objects."""

    __slots__ = ['cards']

    def __init__(self):
        self.cards = [Card(s, r) for s in Card.SUITS for r in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        """Deal cards to players in the fashion of Klaverjas.

        It is up to the caller to order the players list in the correct way.
        """
        position = 0

        for i in [3, 2, 3]:
            for j in range(4):
                for _ in range(i):
                    # players[j].hand.append(self.cards.pop(0))
                    players[j].hand.append(self.cards[position])
                    print('Player {} gets {}'.format(j, self.cards[position]))
                    position += 1


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

class Tree:
    def __init__(self):
        pass

class Round:
    def __init__(self):
        pass

class Trick:
    def __init__(self):
        pass


class Belief:
    """Probability distribution over all players per card.

    Since each card is dealt to some player (including the beliefholder) we can view this as a pmf.

    Members:
        self.beliefHolder : The Player object whose beliefs we model.
        self.pmf : A 4x8x5 NumPy Array which holds te probability values for cards in the hands of players. Dimensions are suit x rank x player, where player0 is the beliefholder and player4 is the discard pile.


    Methods:
        resetBelief : At the start of a new round each player knows the cards in their hands and hence knows the probabilities of those cards. As there is no information about any other cards, those are set to be uniformly distributed.
        normalize :



    NOTE: There are actually 2 beliefs, the one about the current state of the game and which player has which card during play. And one about the starting state of the game, this belief also evolves as cards are being played and is a way to backwards deduce why players have bid as they did.
    """

    deck = Deck()

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

    def normalize(self):
        """Change probability values such that they add up to one but keep their ratio."""
        s = np.sum(self.pmf, axis=2)
        for card in self.deck.cards:
            for player in range(5):
                self.pmf[card.suit, card.rank, player] /= s[card.suit, card.rank]
        self.rowsumTest()

    # TODO: Create tester decorator which checks whether all appropriate row and column sums are 1
    
    # TODO: Create setBelief method to change manually change a probability in pmf
    # TODO: Create setCardProbabilities method which takes not a Card object but just rank and suit
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

    def toDiscard(self, card=None):
        """When a Card is played that Card will go to the discard pile so is not in any Players hand."""
        self.setCardProbabilities(card=card, values=(0,0,0,0,1))
    
    def notFollowed(self, playerIndex=None, suit=None):
        """When a player doesnt follow suit, this means that they for certain do not have any more cards in that suit."""
        if suit is not None and playerIndex is not None and isinstance(playerIndex, int):
            self.pmf[suit,:,playerIndex] = (0,0,0,0,0,0,0,0)


if __name__ == "__main__":

    d = Deck()
    # d.shuffle()

    p = Player()
    p.hand = d.cards[0:8]
    # print(p.hand)

    b = Belief(p)
    # print(p.belief.pmfs)
    for i in range(4):
        for j in range(8):
            b.setCardProbabilities(Card(i,j), (1,2,3,4,5))
    
    b.normalize()
   # p.belief.pmfs[Card(1,2)] = [1,2,1]
   # p.belief.normalize()
   # print(p.belief.pmfs)

