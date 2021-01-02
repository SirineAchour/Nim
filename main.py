import sys
import time
from random import randrange


class State:

    def __init__(self, stacks):
        # maybe lenna check e list ken feha 1s w 2s w clear them ?
        self.stacks = stacks  # a list of stacks
        self.score = 0  # initialize e score fl 0
        self.next_states = []
        if not stacks:
            self.isTerminal = True
        else:
            self.isTerminal = False
        self.generate_next_states()

    # this works i checked
    def generate_next_states(self):
        if self.isTerminal:
            print("uh oh nowhere to go from here")
            return None
        # first we loop through e stacks li 3anna lkol
        for stack in self.stacks:
            # this is for saving e stacks mt3 e next states bch mayebdech 3andi duplicate next states
            next_stacks = []
            # then f kol stack i look to fin l possible ways to divide it
            # i stop at stack/2 5atr zeyed
            for i in range(1, int(stack / 2) + 1):
                # if (i) w (stack - i) 9add b3adhhom then we dont add them 5atr we cant
                # if (i) w (stack - i) 7ajet mayzidouch yet9asmou zeda we dont add them
                # e5er if yroddna ken nouslou l 7aja terminal that means li we won
                if ((stack - i) == i) or ((i in [0, 1, 2]) and ((stack - i) in [0, 1, 2])):
                    continue

                # we copy e stack li 3anna 5atr e child one is gonna be very similar
                new_stack = self.stacks.copy()
                # if it already exists f e stacks then we just remove the one n7ebbou na9smouh w go on
                # if i in self.stacks and (stack-i) in self.stacks:
                new_stack.remove(stack)

                if (not (stack - i) in self.stacks) and (not (stack - i) in [1, 2]):
                    new_stack.append(stack - i)
                if (not i in self.stacks) and (not i in [1, 2]):
                    new_stack.append(i)
                if not check_if_exists(new_stack, next_stacks):
                    next_stacks.append(new_stack)
                    self.next_states.append(State(new_stack))

        if not self.next_states:
            self.isTerminal = True

    def set_up_tree(self, min_or_max):
        print(min_or_max)

    def draw_stacks(self):
        print("Currently we have :")
        for e in self.stacks:
            print(str(e) + "|", end="")

        print("")
        print("Choose your next move:")
        for index, stack in enumerate(self.next_states):
            print(str(index) + ") " + str(stack.stacks))
        check, index = 0, 0
        while check == 0:
            try:
                index = int(input().strip())
                if len(self.next_states) > index >= 0:
                    check = 1
                else:
                    print("That doesnt exist. Please pick again (one that exists this time)")
            except:
                print("That's not even a number... Try again")
        return self.next_states[index]


#     def actions(self, state):
#         return state.moves
#
#     def result(self, state, move):
#         if move not in state.moves:
#             return Struct(to_move=if_(state.to_move == 'H', 'M', 'H'), utility=state.utility, sticks=state.sticks,
#                           moves=state.moves)
#         moves = if_(state.sticks - move > 3, [x for x in range(1, 4)], [x for x in range(1, state.sticks - move)])
#         return Struct(to_move=if_(state.to_move == 'H', 'M', 'H'), utility=self.compute_utility(state, move),
#                       sticks=state.sticks - move,
#                       moves=moves)
#
#     def compute_utility(self, state, move):
#         if state.sticks - move == 1:
#             return if_(state.to_move == 'M', 1, -1)
#         else:
#             return 0
#
#     def terminal_test(self, state):
#         return state.utility != 0 or len(state.moves) == 0
#
#     def utility(self, state, player):
#         return if_(player == 'M', state.utility, -state.utility)
#
#     def display(self, state):
#         print
#         '( %s, %d )' % (state.to_move, state.sticks)
#
#
#
# def minimax(position, depth, maximizingPlayer):
#     if depth == 0 or "game over" in position:
#         return "static evaluation of position"
#
#     if maximizingPlayer:
#         maxEval = int('-inf')
#         for each_child of position.next_states()
#             eval = minimax(child, depth - 1, false)
#             maxEval = max(maxEval, eval)
#         return maxEval
#
#     else
#         minEval = +infinity
#         for each child of position
#             eval = minimax(child, depth - 1, true)
#             minEval = min(minEval, eval)
#         return minEval
#
def check_if_exists(e, list):
    for el in list:
        if len(el) != len(e):
            continue
        i = 0
        for ee in e:
            if not ee in el:
                break
            else:
                i = i + 1
        if i == len(e):
            return True
    return False


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
    print("flipping coin", end="", flush=True)
    for i in range(3):
        sys.stdout.flush()
        time.sleep(1)
        print(".", end="", flush=True)
    print("")
    n = 0
    if coin == "t":
        n = 1
    # machine = 0 and user = 1
    max_player, min_player = 0, 0
    if randrange(10) % 2 == n:
        print("You play first. Good luck!")
        maxi_player = 1
        State([number_of_tokens]).draw_stacks().set_up_tree(0)
    else:
        print("Looks like i play first. Good luck!")
        mini_player = 1
        State([number_of_tokens]).set_up_tree(1)
    next_turn(name, stacks, max_player, min_player)


def next_turn(name, stacks, maxi_player, mini_player):
    print("____Player " + str(name) + "____")
    print("available stacks : ")
    for stack in stacks:
        print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    s = State([7, 8, 9])
    State([7, 8, 9]).draw_stacks().set_up_tree(0)
