class Tree:
    """A tree is the main unit of a Klaverjas game,
    it consists of as many hands it takes to get one team to 1500 points (about 16 hands)
    """
    def __init__(self, names):
        self.players = [Player(name) for name in names]
        self.deck = Deck()
        self.wijPoints, self.zijPoints = 0, 0
        self.handNum = 0
        self.startPlayPos = 0


    def newHandSetup(self):
        for player in self.players:
            player.hand.clear()
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(self.players)
        self.startPlayPos = (self.startPlayPos + 1)%4

    def bidding(self):
        """Starts a round of bidding

        Returns:
        Tuple containing
            Suit which will be trump next hand
            Amount of points which needs to be gotten by the winning team
            Position of player with the highest bid
        """
        return (random.randint(0, 3), 80, random.randint(0, 3))


    def play(self):
        # while (self.wijPoints < 1500 or self.zijPoints < 1500):
        print(' --- Nieuwe hand --- ')
        self.newHandSetup()
        trumpSuit, bidMark, bidWinner = self.bidding()
        hand = Hand(self.players, self.startPlayPos, trumpSuit, bidMark, bidWinner)
        wijHandPoints, zijHandPoints, wijTrickWins, zijTrickWins = hand.play()
        
        if bidWinner % 2 == 0:
            # Wij spelen
            if wijHandPoints < bidMark:
                # Wij zijn NAT
                print('Wij is NAT')
                self.zijPoints += 162
            elif wijTrickWins == 8:
                # Wij hebben PIT
                print('Wij hebben PIT')
                self.wijPoints += 262
            else:
                # Wij hebben het gehaald
                print('Wij hebben gehaald')
                self.wijPoints += wijHandPoints
                self.zijPoints += zijHandPoints
        else:
            # Zij spelen
            if zijHandPoints < bidMark:
                # Zij zijn NAT
                print('Zij is NAT')
                self.wijPoints += 162
            elif zijTrickWins == 8:
                # Zij hebben PIT
                print('Zij hebben PIT')
                self.zijPoints += 262
            else:
                # Zij hebben het gehaald
                print('Zij hebben gehaald')
                self.wijPoints += wijHandPoints
                self.zijPoints += zijHandPoints
        print('Hand wij: {}'.format(wijHandPoints))
        print('Hand zij: {}'.format(zijHandPoints))
        print('Totaal Punten: {}'.format(wijHandPoints + zijHandPoints))

class Hand:
    """Consists of 8 tricks
    """
    def __init__(self, players, startPlayPos, trumpSuit, bidMark=0, bidWinner=0):
        self.players, self.startPlayPos, self.trumpSuit = players, startPlayPos, trumpSuit
        self.bidMark, self.bidWinner = bidMark, bidWinner
        self.wijPoints, self.zijPoints = 0, 0
        self.wijTrickWins, self.zijTrickWins = 0, 0


    def play(self):
        """Plays a Hand consisting of 8 Tricks.

        Returns:
        Tuple containing
            Amount of points won by Wij
            Amount of points won by Zij
            Amount of tricks won by Wij
            Amount of tricks won by Zij
        """
        for i in range(4):
            self.players[i].resetBelief()

        # Per trick calculate winners and points and roem
        for trickNum in range(8):
            print('Slagnummer:', trickNum, '; Beginspeler:', self.players[self.startPlayPos], '(' + str(self.startPlayPos) + ')', '; Biedwinnaar:', self.bidWinner, self.bidMark, '; Troef:', Card.SUITSlongstr[self.trumpSuit])
            trick = Trick(self.players, self.startPlayPos, self.trumpSuit)
            highCard, posHighCard, points, roem = trick.play()
            self.startPlayPos = posHighCard

            if self.startPlayPos % 2 == 0:
                self.wijPoints += points if trickNum != 7 else points + 10
                self.wijPoints += roem
                self.wijTrickWins += 1
            else:
                self.zijPoints += points if trickNum != 7 else points + 10
                self.zijPoints += roem
                self.zijTrickWins += 1

        return (self.wijPoints, self.zijPoints, self.wijTrickWins, self.zijTrickWins)


class Trick:
    """Perhaps use an ordered list of players in this class?
    
    A trick is the smallest unit of play, it consists of one card per player
    """
    def __init__(self, players, startingPlayerPosition, trumpSuit):
        self.players, self.startingPlayerPosition, self.trumpSuit = players, startingPlayerPosition, trumpSuit
        self.cards = []

    def __str__(self):
        return 'Players: {} \n Starting player: {} \n Trump suit: {}'.format(self.players, self.startingPlayerPosition, self.trumpSuit)

    def __repr__(self):
        return 'Trick({},{},{})'.format(self.players, self.startingPlayerPosition, self.trumpSuit)


    def play(self):
        """Zorgt dat spelers een kaart spelen,checkt dan welke kaart het hoogste is.

        Returns:
        tuple containing
            tuple containing the winning card (Card object) and the position of the winner (absolute position)
            integer of total amount of points in the Trick
            integer of total amount of roem in the Trick
        """
        
        
        orderedPlayers = calc.orderPlayers(self.players, self.startingPlayerPosition)
        
        for i in range(4):
            orderedPlayers[i].valuate(self.cards)
            print(orderedPlayers[i].name, *orderedPlayers[i].hand)
            c = orderedPlayers[i].playCard(self.cards, self.trumpSuit)
            self.cards.append(c)
            

        print('Cards list: {} {} {} {}'.format(*self.cards))
        map(lambda player: player.valuate(self.cards), orderedPlayers)

        highCard = calc.highestCard(self.cards, self.trumpSuit)
        posHighCard = (self.cards.index(highCard) + self.startingPlayerPosition)%4
        
        points = calc.countPoints(self.cards, self.trumpSuit)
        roem = calc.countRoem(self.cards, self.trumpSuit)
        
        # if highCard not in self.players[posHighCard].hand:
        #     raise Exception('wrong player has been selected as winner')
        
        print('Highest card: {}, from player: {} ({}), {}th card'.format(highCard, self.players[posHighCard], posHighCard, self.cards.index(highCard)+1))
        print('Points total: {}'.format(points), '; Roem total: {}'.format(roem))

        return (highCard, posHighCard, points, roem)
