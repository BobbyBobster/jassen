# jassen

## TODO
Hij kan kleurbekennen maar gooit dan wel een random kaart van die kleur op.

* Player.playCard
    * Introeven
    * Overtroeven
        * Of dit in een aparte functie plaatsen

* PEP 8 compatibility

* Welk object doet welke actie?
    * Delen
    * Spelen
    * Puntentelling bijhouden
    * NAT / gehaald / PIT bepalen

* Use more decorators (function wrappers)


## Design choices
### Algemeen
Normale kleuren worden aangeduid met getallen, sans wordt aangeduid met None

### Trick
In een slag kunnen de gespeelde kaarten worden opgeslagen in een list met vaste plaatsing (dus Zuid altijd op plaats 0) of relatieve plaatsing (elke speler zet de eerst gespeelde kaart op plek 0).

**Vaste plaatsing** is makkelijker op de manier dat we niet de startpositie van de slag hoeven mee te sturen.

**Relatieve plaatsing** is makkelijker op de manier dat we denken als de speler zelf.


### Beliefs and valuation function
Elke speler moet constant zijn beliefs aanpassen op wat er is gespeeld en wat voor kaarten elke speler heeft. Een idee om dit te implementeren is om elk `Player` object een lijst te geven met probability distributions van welke kaarten de andere spelers hebben. Dus speler 0 heeft aparte beliefs over de kaarten van spelers 1, 2, en 3.
Dan kunnen deze beliefs samen met de kaarten van de speler zelf worden gebruikt om een valuation te geven aan welke kaart moet worden gespeeld.
