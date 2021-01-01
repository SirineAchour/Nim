import sys
import time
from random import randrange


def start_game():
    number_of_tokens = 0
    print("Hi player.. what's your name ?")
    name = input()
    print("Okay then " + str(name) + ", let's play.")
    print("How many things in the stack do you want there to be? (make sure you input an integer)")
    check = 0
    while check == 0:
        try:
            number_of_tokens = int(input().strip())
            check = 1
        except:
            print("Integer please")
    stacks = {number_of_tokens: 0}

    print("Now we flip a coin to see who gets to play first")
    print("Heads or tails ? (h or t)")
    coin = input().strip()
    while (not coin == "h") and (not coin == "t"):
        print("h or t please")
        coin = input().strip()
    print("flipping coin.", end="", flush=True)
    sys.stdout.flush()
    time.sleep(1)
    print(".", end="", flush=True)
    sys.stdout.flush()
    time.sleep(1)
    print(".", flush=True)
    n = 0
    if coin == "t":
        n = 1
    maxi_player, mini_player = 0, 0
    if randrange(10) % 2 == n:
        print("You play first. Good luck!")
        maxi_player = 1
    else:
        print("Looks like i play first. Good luck!")
        mini_player = 1
    next_turn(name, stacks, maxi_player, mini_player)


def next_turn(name, stacks, maxi_player, mini_player):
    print("____Player " + str(name) + "____")
    print("available stacks : ")
    for stack in stacks:
        print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_game()
