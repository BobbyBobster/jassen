# Klaverjas 

## TODO
- Why not let TrumpCard be subclass of Card so we can implement data model
methods (dunder methods)
  - This would mean we need Deck class to just be a container of Cards (or TrumpCards)
  - rank and suit should remain the same only interactions between cards should differ
- Is there a place for generators?
  - Perhaps in the calculator?
- Rewrite README to English
- Implement a way to play against the computer
- Write a How to play guide

## How to play
Klaverjas is a trick taking card game in which four players play in two teams against eachother. A game of klaverjas ends when one of the teams scores 1500 points. The game is played in rounds (on average 16 needed to reach 1500 points for one of the teams) in which players are dealt 8 cards from a piket deck of cards (from a standard deck of 52 cards, remove all cards of rank 2 through 6). 

### Dealing
Cards are dealt from a piket deck of cards. This means there are 32 cards to be dealt. The dealer shuffles the deck and starting from the player to his/her left, deals clockwise. Dealing occurs in 3-2-3 fashion, first each player recieves 3 cards from the deck, then 2 cards, and lastly 3 cards again.

### Bidding
After the cards are dealt, the bidding round starts. Here players will announce how many points they expect to win this round. The player to the left of the dealer starts the bidding. After this the bidding goes clockwise. 
# EXPAND ON BIDDING

### Point scoring
`

## Design choices
### Trick

### Beliefs and valuation function
A Belief is a probability distribution over all players and discard pile per card. 
