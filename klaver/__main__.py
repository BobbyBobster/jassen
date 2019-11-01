import klaver.common.deckscards as dc
import klaver.player.player as pl
import klaver.game.divisions as div

import klaver.devtools.beliefplot as bplot

import random

if __name__ == "__main__":
    d = dc.Deck()
    # d.shuffle()

    players = [pl.Player(name) for name in ['zuid', 'west', 'nord', 'oost']] 
    tree = div.Tree(players)

    tree.play()

   # position = 0
   # for jdx in range(4):
   #     for _ in range(8):
   #         players[jdx].hand.append(d.cards[position])
   #         print('Player {} gets {}'.format(jdx, d.cards[position]))
   #         position += 1
   #     
   #    
   # 
   # for idx in range(4):
   #     players[idx].belief.resetBelief()

   # for _ in range(15):
   #     suit = random.randint(0, 3)
   #     rank = random.randint(0, 7)
   #     players[0].belief.toDiscard(dc.Card(suit, rank))
   #     print("played ", dc.Card(suit, rank))
   # 
   # players[0].belief.notFollowed(1,1)
   # players[0].belief.notFollowed(2,1)
   # 
   # bplot.beliefPlotter(players[0])
