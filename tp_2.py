import sys
import time
from collections import defaultdict
from copy import deepcopy
from itertools import chain
from operator import itemgetter
from random import randrange

count = 0

#Classe représentant l'état d'un noeud
class Noeud:
    #Constructeur de la classe
    #On a un nombre de cartes = 10 par défaut, mais l'utilisateur peut entrer une autre valeur pendant l'execution
    def __init__(self, stack=10):
        self.stack = stack
        self.data = defaultdict(lambda: 0)
        self.data[self.stack] = 1

    #Fonction permettant de trouver les actions résultant en les nodes suivantes de l'état courant
    def actions(self):
        results = []
        for key, value in self.data.items():
            #On vérifie qu'on a bien plus de 3 cartes dans notre stack
            if key >= 3 and value > 0:
                for i in range(1, int((key - 1) / 2) + 1):
                    action = deepcopy(self)
                    action.data[key] = value - 1
                    action.data[i] = action.data[i] + 1
                    action.data[key - i] = action.data[key - i] + 1
                    results.append(action)
        return results
    
    #Fonction vérifiant si le noeud courant est terminal (si aucune autre action n'est possible)
    def is_terminal(self):
        return len(self.actions()) == 0

    #Fonction permettant d'afficher l'état du noeud sous forme de chaine
    def __str__(self):
        values = list(chain.from_iterable([str(key) for _ in range(value)] for key, value in self.data.items()))
        return " ".join(values)

    #Fonction permettant au joueur, s'il est humain, de choisir une action à effectuer pour avancer le jeu
    def choose_action(self):
        actions = self.actions()
        if self.is_terminal():
            return None
        print("Choose your next move:")
        i = 0
        #Imprime dans la console toutes les actions possibles du joueur
        for index, action in enumerate(self.actions()):
            print(str(index) + ") " + str(action))
            i = index
        check, index = 0, 0
        while check == 0:
            try:
                index = int(input().strip())
                if i >= index >= 0:
                    check = 1
                else:
                    print("That doesnt exist. Please pick again (one that exists this time)")
            except:
                print("That's not even a number... Try again")
        return actions[index]


#Fonction Minimax permettant de retourner le résultat
def minimax(node, maximizing_player):
    global count
    count = count + 1
    #Si l'état est terminal, on retourne le résultat, dépendant de qui joue
    if node.is_terminal():
        return 0 if maximizing_player else 1
    #Sinon on applique Minimax sur les états suivants de l'état courant
    if maximizing_player:
        value = float('-inf')
        for child in node.actions():
            value = max(value, minimax(child, False))
        return value
    else:
        value = float('inf')
        for child in node.actions():
            value = min(value, minimax(child, True))
        return value

#Fonction permettant à l'ordinateur de choisir sa prochaine action
def minimax_decision(node, maximizing_player):
    if node.is_terminal():
        return None
    if maximizing_player:
        max_value, max_action = float('-inf'), None
        for action in node.actions():
            max_value, max_action = max(
                (max_value, max_action),
                (minimax(action, False), action),
                key=itemgetter(0)
            )
        return max_action
    else:
        min_value, min_action = float('inf'), None
        for action in node.actions():
            min_value, min_action = min(
                (min_value, min_action),
                (minimax(action, True), action),
                key=itemgetter(0)
            )
        return min_action

#Fonction permettant de ne pas vérifier des branches de l'arbre inutilement
def minimax_pruning(node, maximizing_player, alpha, beta):
    global count
    count = count + 1
    if node.is_terminal():
        return 0 if maximizing_player else 1
    if maximizing_player:
        value = float('-inf')
        for child in node.actions():
            value = max(value, minimax_pruning(child, False, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
    else:
        value = float('inf')
        for child in node.actions():
            value = min(value, minimax_pruning(child, True, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

#Fonction de décision de l'ordinateur qui n'utilise pas le pruning
def minimax_decision_pruning(node, maximizing_player):
    if node.is_terminal():
        return None
    if maximizing_player:
        max_value, max_action = float('-inf'), None
        for action in node.actions():
            max_value, max_action = max(
                (max_value, max_action),
                (minimax_pruning(action, False, float('-inf'), float('inf')), action),
                key=itemgetter(0)
            )
        return max_action
    else:
        min_value, min_action = float('inf'), None
        for action in node.actions():
            min_value, min_action = min(
                (min_value, min_action),
                (minimax_pruning(action, True, float('-inf'), float('inf')), action),
                key=itemgetter(0)
            )
        return min_action


def start_game():
    number_of_tokens = 0
    print("Hi player.. what's your name ?")
    name = input()
    print("Okay then " + str(name) + ", let's play.")
    print("How many cards in the stack do you want there to be? (make sure you input an integer)")
    check = 0
    while check == 0:
        try:
            number_of_tokens = int(input().strip())
            check = 1
        except:
            print("Integer please")
            
    #On décide du joueur grace à un pile ou face
    print("Now we flip a coin to see who gets to play first")
    print("Heads or tails ? (h or t)")
    coin = input().strip()
    while (not coin == "h") and (not coin == "t"):
        print("h or t please")
        coin = input().strip()
    print("flipping coin", end="", flush=True)
    for i in range(3):
        sys.stdout.flush()
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("")
    n = 0
    if coin == "t":
        n = 1
    current = Noeud(stack=number_of_tokens)
    #Si le joueur commence:
    if randrange(10) % 2 == n:
        print("You play first. Good luck!")
        print("Initially we have "+str(current)+" elements")
        maximizing_player = True
        while True:
            if maximizing_player:
                #Il choisit l'action qu'il compte entreprendre
                current = current.choose_action()
                if current is not None:
                    print(" You played : "+str(current))
            else:
                #L'ordinateur joue ensuite
                current = minimax_decision(current, maximizing_player)
                if current is not None:
                    print(" I played : " + str(current))
            if not current:
                if maximizing_player:
                    print("Boohoo you lost.")
                else:
                    print("Congrats "+name+"! You won!")
                break
            maximizing_player = not maximizing_player
    #Si la machine commence:
    else:
        print("Looks like i play first. Good luck!")
        print("Initially we have "+str(current)+" elements")
        maximizing_player = True
        while True:
            if not maximizing_player:
                current = current.choose_action()
                if current is not None:
                    print(" You played : "+str(current))
            else:
                current = minimax_decision(current, maximizing_player)
                if current is not None:
                    print(" I played : " + str(current))
            if not current:
                if maximizing_player:
                    print("Congrats "+name+"! You won!")
                else:
                    print("Boohoo you lost.")
                break
            maximizing_player = not maximizing_player

start_game()
print("Number of nodes visited:", count)