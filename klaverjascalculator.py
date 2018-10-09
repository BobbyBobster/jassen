
# coding: utf-8

"""Klaverjas calculator

This module is used to calculate different aspects of the Klaverjas card game by the same author. These include point totals, finding a highest card, and roem calculations.
This module only expects to recieve inputs from the Klaverjas card game. As such it will freely use attributes of for example the Card class as defined there.
"""

import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug



def orderPlayers(players=[], startingPlayerPosition=None):
    """Needs a better name
    Returns the list of players with Player at startingPlayerPosition on index 0
    """
    if not isinstance(startingPlayerPosition, int):
        raise IndexError('startingPlayerPosition must be an integer')
    
    ordered = players[startingPlayerPosition::] + players[:startingPlayerPosition:]
    return ordered


def selectPlayable(playedCards=[], trumpSuit=None, hand=[]):
    
    def selectPlayableTrump():
        cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, hand))
        
        if not cardsInTrump:
            # No cards in trump suit hence play a card
            # Also works for sans trump
            return None
        
        playedTrumps = list(filter(lambda card: card.suit == trumpSuit, playedCards))
        if playedTrumps:
            highestPlayedTrump = max(playedTrumps, key=lambda card: card.rank)
            higherTrumps = list(filter(lambda card: card.trumpRank > highestPlayedTrump.trumpRank, cardsInTrump))

            if higherTrumps:
                # We need to trump-over
                return higherTrumps
        
            # Cannot trump-over, check if we can play a non-trump otherwise trump-under
            nonTrumps = list(filter(lambda card: card not in cardsInTrump, hand))
            return nonTrumps if nonTrumps else cardsInTrump
        else:
            # playedTrumps empty
            return cardsInTrump
        if selectTrumpOver():
            return selectTrumpOver()
        else:
            nonTrumps = list(filter(lambda card: card not in cardsInTrump, hand))
            return nonTrumps if nonTrumps else cardsInTrump

    
    def selectTrumpOver():
        playedTrumps = list(filter(lambda card: card.suit == trumpSuit, playedCards))
        cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, hand))
        try:
            highestPlayedTrump = max(playedTrumps, key=lambda card: card.rank)
            higherTrumps = list(filter(lambda card: card.trumpRank > highestPlayedTrump.trumpRank, cardsInTrump))
            return higherTrumps
        except ValueError:
            return cardsInTrump
        
        
    # Function starts here
    if not playedCards:
    # playedCards empty, hence can play any card
        return hand
    
    startSuit = playedCards[0].suit
    cardsInSuit = list(filter(lambda card: card.suit == startSuit, hand))
    
    if startSuit == trumpSuit and selectTrumpOver():
        return selectTrumpOver()
    
    if cardsInSuit:
        # Able to follow suit
        return cardsInSuit
    elif selectPlayableTrump():
        # Not able to follow suit hence must trump-in or trump-over
        return selectPlayableTrump()
    else:
        # Not able to trump-in or trump-over hence able to play any card
        return hand


def highestCard(cards, trumpSuit=None):
    """Returns the highest Card object
    """
    cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, cards))

    if cardsInTrump:
        highTrump = max(cardsInTrump, key=lambda card: card.trumpRank)
        return highTrump
    else:
        cardsInStartSuit = list(filter(lambda card: card.suit == cards[0].suit, cards))
        highCard = max(cardsInStartSuit, key=lambda card: card.rank)
        return highCard


def countPoints(cards, trumpSuit=None):
    """Counts amount of points in a list of cards

    Args:


    Returns:
    integer value how many points the cards are in total
    """
    points = 0
    for card in cards:
        points += card.points if card.suit != trumpSuit else card.trumpPoints
    return points


def countRoem(cards, trumpSuit=None):
    """Counts the amount of roem (additional points) in a list of cards

    Args:


    Returns:
        Integer value how many points of roem are in the cards in total
    """
    roem = 0
    # Stuk
    # Without a trumpSuit, stuk is impossible
    if trumpSuit is not None:
        trumpKing = list(filter(lambda c: c.suit == trumpSuit and c.rank == 4, cards))
        trumpQueen = list(filter(lambda c: c.suit == trumpSuit and c.rank == 5, cards))
        if trumpKing and trumpQueen:
            roem += 20

    # Normal roem
    # For each suit we check whether there are 3 cards in that suit, if so there is chance for roem
    for i in range(4):
        cardsInSuit = list(filter(lambda c: c.suit == i, cards))
        if len(cardsInSuit) >= 3:
            cards = cardsInSuit

            # We sort the list and check the difference between consecutive cards
            cards.sort(key=lambda c: c.rank)
            subtractList = []
            for i in range(len(cards) - 1):
                subtract = abs(cards[i].roemRank - cards[i+1].roemRank)
                subtractList.append(subtract)

            # If more than 1 difference equals 1, we know at least 3 cards have consecutive ranks
            lenOfOnes = len(list(filter(lambda x: x == 1, subtractList)))
            if lenOfOnes == 2:
                roem += 20
            elif lenOfOnes == 3:
                roem += 50

    return roem