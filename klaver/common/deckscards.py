import random

class Card:
    """Standard playing card."""
    SUITS = (0,1,2,3)
    RANKS = (0,1,2,3,4,5,6,7)
    # Note that we use the No-Trump ordering of cards
    SUITSstr = tuple('s h c d'.split())
    RANKSstr = tuple('7 8 9 J Q K X A'.split())

    SUITSlongstr = tuple('Hearts Diamonds Spades Clubs'.split())
    RANKSlongstr = tuple('7 8 9 Jack Queen King 10 Ace'.split())  

    __slots__ = ['suit', 'rank']

    def __init__(self, suit, rank):
        self.suit, self.rank = suit, rank

    def __repr__(self):
        return 'Card({},{})'.format(self.suit, self.rank)

    def __str__(self):
        return '({}, {})'.format(self.suit, self.rank)
#        return '{} of {}'.format(self.RANKSlongstr[self.rank], 
#                self.SUITSlongstr[self.suit])

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
                    players[j].hand.append(self.cards[position])
                    print('Player {} gets {}'.format(j, self.cards[position])) #DEBUG
                    position += 1
