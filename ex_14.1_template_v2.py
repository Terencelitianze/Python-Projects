import random

SUITES=["♠","\033[91m♥\033[0m","\033[92m♣\033[0m","\033[94m♦\033[0m"]
RANKS = ['A','2','3','4','5','6','7','8','9','X','J','Q','K']
VALUES = [11,2,3,4,5,6,7,8,9,10,10,10,10]

class Card:

    def __init__(self, suit, rank):
        #initialize attributes here
        self.suit = suit
        self.rank = rank
        self.value = VALUES[RANKS.index(rank)]


    def __str__(self):
        return f'┌───────┐\n│{self.rank}      │\n│{self.suit}      │\n│       │\n│       │\n│      {self.suit}│\n│      {self.rank}│\n└───────┘\n'


# Example of instantiating and printing an ace of spades card
'''ace_spades = Card("♠", "A")
print(ace_spades)'''


class Deck(list):

    def __init__(self):
        super().__init__(self)
        for i in SUITES:
            for j in RANKS:
                self.append(Card(i,j))

    def shuffle(self):
        random.shuffle(self)

    def __str__(self):
        result = ""
        for cards in self:
            result += str(cards)
        return result
    
    def deal(self):
        deal_card = self.pop()
        return deal_card


'''deck = Deck()
deck.shuffle()
print(deck)'''

class Hand(Deck):

    def __init__(self,name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.name}:\n{super().__str__()}'

deck = Deck()
deck.shuffle()
Terence = Hand("Terence")
for i in range(2):
    card = deck.deal()
    Terence.append(card)
print(Terence)



