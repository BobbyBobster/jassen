"""Klaverjas calculator

This module is used to calculate different aspects of the Klaverjas card game. 
These include point totals, finding a highest card, and roem calculations.
"""

TRUMPRANKS = (0,1,6,7,2,3,4,5)
ROEMRANKS = (0,1,2,4,5,6,3,7)

POINTS = (0,0,0,2,3,4,10,11)
TRUMPPOINTS = (0,0,14,20,3,4,10,11)

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
        #cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, hand))
        cardsInTrump = [card for card in hand if card.suit == trumpSuit]
        
        if not cardsInTrump:
            # No cards in trump suit hence play a card
            # Also works for sans trump
            return None
        
        #playedTrumps = list(filter(lambda card: card.suit == trumpSuit, playedCards))
        playedTrumps = [card for card in playedCards if card.suit == trumpSuit]
        if playedTrumps:
            highestPlayedTrump = max(playedTrumps, key=lambda card: card.rank)
            #higherTrumps = list(filter(lambda card: card.trumpRank > highestPlayedTrump.trumpRank, cardsInTrump))
            #higherTrumps = list(filter(lambda card: TRUMPRANKS[card.rank] > TRUMPRANKS[highestPlayedTrump.rank], cardsInTrump))
            higherTrumps = [card for card in cardsInTrump if TRUMPRANKS[card.rank] > TRUMPRANKS[highestPlayedTrump.rank]]

            if higherTrumps:
                # We need to trump-over
                return higherTrumps
        
            # Cannot trump-over, check if we can play a non-trump otherwise trump-under
            #nonTrumps = list(filter(lambda card: card not in cardsInTrump, hand))
            nonTrumps = [card for card in hand if card not in cardsInTrump]
            return nonTrumps if nonTrumps else cardsInTrump
        else:
            # playedTrumps empty
            return cardsInTrump
        if selectTrumpOver():
            return selectTrumpOver()
        else:
            #nonTrumps = list(filter(lambda card: card not in cardsInTrump, hand))
            nonTrumps = [card for card in hand if card not in cardsInTrump]
            return nonTrumps if nonTrumps else cardsInTrump

    
    def selectTrumpOver():
        #playedTrumps = list(filter(lambda card: card.suit == trumpSuit, playedCards))
        #cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, hand))
        playedTrumps = [card for card in playedCards if card.suit == trumpSuit]
        cardsInTrump = [card for card in hand if card.suit == trumpSuit]
        try:
            highestPlayedTrump = max(playedTrumps, key=lambda card: card.rank)
            #higherTrumps = list(filter(lambda card: card.trumpRank > highestPlayedTrump.trumpRank, cardsInTrump))
            #higherTrumps = list(filter(lambda card: TRUMPRANKS[card.rank] > TRUMPRANKS[highestPlayedTrump.rank], cardsInTrump))
            higherTrumps = [card for card in cardsInTrump if TRUMPRANKS[card.rank] > TRUMPRANKS[highestPlayedTrump.rank]]
            return higherTrumps
        except ValueError:
            return cardsInTrump
        
        
    # Function starts here
    if not playedCards:
    # playedCards empty, hence can play any card
        return hand
    
    startSuit = playedCards[0].suit
    #cardsInSuit = list(filter(lambda card: card.suit == startSuit, hand))
    cardsInSuit = [card for card in hand if card.suit == startSuit]
    
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
    #cardsInTrump = list(filter(lambda card: card.suit == trumpSuit, cards))
    cardsInTrump = [card for card in cards if card.suit == trumpSuit]

    if cardsInTrump:
        #highTrump = max(cardsInTrump, key=lambda card: card.trumpRank)
        highTrump = max(cardsInTrump, key=lambda card: TRUMPRANKS[card.rank])
        return highTrump
    else:
        #cardsInStartSuit = list(filter(lambda card: card.suit == cards[0].suit, cards))
        cardsInStartSuit = [card for card in cards if card.suit == cards[0].suit]
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
        #points += card.points if card.suit != trumpSuit else card.trumpPoints
        points += POINTS[card.rank] if card.suit != trumpSuit else TRUMPPOINTS[card.rank]
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
        #trumpKing = list(filter(lambda c: c.suit == trumpSuit and c.rank == 4, cards))
        #trumpQueen = list(filter(lambda c: c.suit == trumpSuit and c.rank == 5, cards))
        trumpKing = [card for card in cards if card.suit == trumpSuit and card.rank == 4]
        trumpQueen = [card for card in cards if card.suit == trumpSuit and card.rank == 5]
        if trumpKing and trumpQueen:
            roem += 20

    # Normal roem
    # For each suit we check whether there are 3 cards in that suit, if so there is chance for roem
    for i in range(4):
        #cardsInSuit = list(filter(lambda c: c.suit == i, cards))
        cardsInSuit = [card for card in cards if card.suit == i]
        if len(cardsInSuit) >= 3:
            cards = cardsInSuit

            # We sort the list and check the difference between consecutive cards
            cards.sort(key=lambda c: c.rank)
            subtractList = []
            for i in range(len(cards) - 1):
                #subtract = abs(cards[i].roemRank - cards[i+1].roemRank)
                subtract = abs(ROEMRANKS[cards[i].rank] - ROEMRANKS[cards[i].rank])
                subtractList.append(subtract)

            # If more than 1 difference equals 1, we know at least 3 cards have consecutive ranks
            #lenOfOnes = len(list(filter(lambda x: x == 1, subtractList)))
            lenOfOnes = len([x for x in subtractList if x == 1])
            if lenOfOnes == 2:
                roem += 20
            elif lenOfOnes == 3:
                roem += 50

    return roem
