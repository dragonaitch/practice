import random
from termcolor import colored

suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':10}

playing = True

class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+' of '+self.suit

class Deck():

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_list = ''
        for card in self.deck:
            deck_list += '\n'+card.__str__()
        return 'Deck has: '+deck_list

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():

    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input(f"How many chips would you like to bet (your total = {chips.total}): "))
        except ValueError:
            print("Sorry, a bet must be an integer.")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't be excced {chips.total}")
            else:
                break

def hit(deck,hand):
    new_card = deck.deal()
    hand.add_card(new_card)
    print(new_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:

        x = input("\nWould you like to hit or stand? Enter 'h' or 's': ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("\nPlayer stands. Dealer is playing.")
            playing = False
        else:
            print("Please try again.")
            continue
        break

def show_some(player,dealer):
    print(colored("\nDealer's Hand:","green"))
    print("<card didden>")
    print(dealer.cards[1])
    print(colored("\nPlayer's Hand: ","blue"), *player.cards, sep='\n')
    print(colored("\n# Player's Value: ","red"), player.value)

def show_all(player,dealer):
    print(colored("\nDealer's Hand: ","green"), *dealer.cards, sep='\n')
    print(colored("\n# Dealer's Value: ","red"), dealer.value)
    print(colored("\nPlayer's Hand: ","blue"), *player.cards, sep='\n')
    print(colored("\n# Player's Value: ","red"), player.value)

def player_busts(player,dealer,chips):
    print("\nPlayer Busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("\nPlayer Wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("\nDealer Busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("\nDealer Wins!")
    chips.lose_bet()

def push():
    print("\nPlayer and Dealer Tie!")


player_chips = Chips()

while True:
    print(colored("\nWelcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.","red"))

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())


    take_bet(player_chips)


    show_some(player_hand, dealer_hand)


    while playing:

        hit_or_stand(deck, player_hand)


        show_some(player_hand, dealer_hand)


        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value <= 17:
            print("\n *Dealer Hit!")
            hit(deck, dealer_hand)


        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push()

    print("\nPlayer's winnings stand at",player_chips.total)

    new_game = input("\nWould you like to play another hand? Enter 'y' or 'n': ")

    if new_game[0].lower() == 'y' and player_chips.total != 0:
        playing = True
        continue
    elif player_chips.total == 0:
        print("\nYou don't have enough chip for playing.")
        break
    else:
        print("\nThanks for playing.")
        break
