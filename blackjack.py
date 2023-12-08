import os
import random
import time

from ascii_art import *


def initialize_cards():
    """
    return a complete set of 52 cards
    :return:
    """
    list_of_cards = []
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    card_values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    for s in suits_name:
        for v in card_values:
            list_of_cards.append(Card(s, v))
    return list_of_cards


def get_a_card(list_cards):
    """
    return a random card in list_card and remove it from the list
    :param list_cards: list of Card
    :return: a random card of the list of Card
    """
    index = random.randint(0, len(list_cards) - 1)
    c = list_cards[index]
    list_cards.remove(c)
    return c


def display_cards(list_cards, mode=0):
    """
    Display the cards in the list
    mode = 0 : no hidden card. mode = 1 : first card hidden
    :return:
    """
    if mode == 0:
        print(ascii_version_of_card(*list_cards))
    else:
        print(ascii_version_of_hidden_card(*list_cards))


def score(list_of_cards):
    """
    Return the total value of the cards in list_of_cards
    :param list_of_cards: list of Card
    :return: the total score of card. If total > 21, change value of Ace to 1 and recalculate total.
    """
    total_score = 0
    for card in list_of_cards:
        total_score += card.points
    for card in list_of_cards:
        if card.rank == "Ace" and total_score > 21:
            total_score -= 10
    return total_score


def display_game(list1, list2, mode):
    """
    Display first list1 : list of computer Card with mode = 1 if one hidden card.
    Display message and score if mode != 1
    Then display second list2 : list of user Card with message and score
    :param list1:
    :param list2:
    :param mode:
    :return:
    """
    message_sup = ""
    if mode != 1:
        message_sup = f"(score : {score(list1)})"
    print("Computer cards are :", message_sup)
    display_cards(list1, mode)
    print(f"Your cards are : (score : {score(list2)})")
    display_cards(list2)


def save_credit(a):
    """
    save the ammount a of player in bankroll.txt
    :param a: value of bet
    :return: 
    """
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "bankroll.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, "w")
    f.write(str(a))
    f.close()

def load_credit():
    """
    load the ammount a of player in bankroll.txt
    :return: the value of the bankroll of player
    """
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "bankroll.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, "r")
    a = int(f.read())
    f.close()
    return a


continue_playing = True

while continue_playing:

    # initialise cards, computer cards and user cards
    cards = initialize_cards()
    mode = 1  # one computer card hidden
    cards_user = []
    cards_computer = []
    for i in range(0, 2):
        cards_user.append(get_a_card(cards))
        cards_computer.append(get_a_card(cards))

    # Display title look if bankroll is too low.
    print(title)
    amount = load_credit()
    if amount < 100:
        print("You're have a low bankroll. We give you a new amount of 1000$ !")
        amount = 1000
        save_credit(amount)

    while True:
        try:
            my_bet = int(input(f"You have {amount}$. Choose your bet for this game : "))
            if my_bet > amount:
                print("You exceed your credit. Enter a valid bet.")
            else:
                break
        except:
            print("Enter a valid bet...")

    # Display computer and user cards
    display_game(cards_computer, cards_user, mode)

    # User want a card ?
    want_a_card = True
    while want_a_card and score(cards_user) <21:
        choice = input("Do you want another card 'Y' for Yes or 'N' for No ? ")
        if choice.lower() != 'y':
            want_a_card = False
        else:
            cards_user.append(get_a_card(cards))
        display_game(cards_computer, cards_user, mode)

    game_ended = False

    # end of game BlackJack with 2 cards
    if score(cards_user) == 21 and mode == 1 and len(cards_user) == 2:
        print(f"BLACKJACK, you win {my_bet}$ !")
        amount += my_bet
        save_credit(amount)
        game_ended = True

    # end of game score exceeds
    elif score(cards_user) > 21:
        print(f"You loose {my_bet}$ !")
        amount -= my_bet
        save_credit(amount)
        game_ended = True

    # Computer get cards while score < 17
    else:
        mode = 0
        display_game(cards_computer, cards_user, mode)
        while score(cards_computer) < 17:
            print()
            print("Computer get a new card...\n")
            time.sleep(5)
            cards_computer.append(get_a_card(cards))
            display_game(cards_computer, cards_user, mode)

    # Who win the game ?
    if not game_ended:
        if score(cards_computer) > 21 or score(cards_user) > score(cards_computer):
            print(f"You win {my_bet}$ !")
            amount += my_bet
            save_credit(amount)
        elif score(cards_computer) == score(cards_user):
            print("This is a draw !")
        else:
            print(f"You loose {my_bet}$ :(")
            amount -= my_bet
            save_credit(amount)

    # Restart the game ?
    choice = input("Do you want to play again 'Y' for Yes or 'N' for No ? ")
    if choice.lower() != "y":
        continue_playing = False











