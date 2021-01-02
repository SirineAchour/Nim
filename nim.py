from anytree import Node, RenderTree, findall


class Tree(object):
    def __init__(self, root_value, first_player):
        self.root_value = root_value
        self.first_player = first_player  # first_player: True = Human, False = Computer
        self.tree = [Node(0, node_value=[self.root_value], is_final=False, evaluator_value=None)]
        self.render_tree()

    def render_tree(self):
        current_state, check_state = 0, True
        while check_state:
            count_final = 0
            for node in findall(self.tree[0], filter_=lambda n: n.depth == current_state):
                if not node.is_final:
                    for list_ in self.set_all_child(node):
                        self.tree.append(Node(len(self.tree), parent=self.tree[node.name],
                                              node_value=list_[0], is_final=True if list_[1] == 1 else False,
                                              evaluator_value=None))
                else:
                    count_final += 1
                if count_final == self.count_siblings(current_state):
                    check_state = False
            current_state += 1
        self.set_evaluator_value()

    def set_all_child(self, node):
        result_list = []
        if max(node.node_value) == 2:
            result_list.append([self.set_child_value(node.node_value, 2, 1), 1])
        else:
            for value in node.node_value:
                number_of_children = self.count_children(value)
                if value > 2:
                    for i in range(number_of_children):
                        result_list.append([self.set_child_value(node.node_value, value, i + 1), 0])
        return self.check_duplicate(result_list)

    def count_children(self, current_value):
        return (int(current_value / 2) - 1) if current_value % 2 == 0 else int(current_value / 2)

    def check_duplicate(self, list_):
        result_list = []
        for value in list_:
            if value not in result_list:
                result_list.append(value)
        return result_list

    def set_child_value(self, list_, current_value, deduction):
        result_list = []
        is_already_split = True
        for value in list_:
            if value == current_value and is_already_split:
                result_list.append(current_value - deduction)
                result_list.append(deduction)
                is_already_split = False
            else:
                result_list.append(value)
        # result_list.sort(reverse=True)  # Uncomment for sorted list
        return result_list

    def set_evaluator_value(self):
        current_state, current_player = self.get_tree_height(), self.first_player
        while current_state >= 0:
            for node in findall(self.tree[0], filter_=lambda n: n.depth == current_state):
                node.evaluator_value = self.calculate_evaluator_value(node, current_player, current_state)
            current_player = not current_player
            current_state -= 1

    def calculate_evaluator_value(self, node, current_player, current_state):
        if node.is_final and current_state % 2 == 0:
            return -1 if current_player else 1
        elif node.is_final and current_state % 2 != 0:
            return 1 if not current_player else -1
        else:
            value = []
            for child in node.children:
                value.append(child.evaluator_value)
            if current_state % 2 == 0:
                return min(value) if current_player else max(value)
            else:
                return max(value) if not current_player else min(value)

    def count_siblings(self, current_state):
        return len(findall(self.tree[0], filter_=lambda n: n.depth == current_state))

    def get_tree(self):
        print("Total node: " + str(len(self.tree)), end="\n\n")
        # Choose between 2 type of return, simple or details
        return RenderTree(self.tree[0]).by_attr(lambda n: ("-".join(map(str, n.node_value)) +
                                                           "  [" + str(n.evaluator_value) + "]"))
        # return RenderTree(self.tree[0])

    def get_tree_height(self):
        return self.tree[0].height

class Game:
    def __init__(self):
        self.number_of_sticks = None
        self.is_play_first = None
        self.tree = None
        self.current_player = None
        self.play()

    def play(self):
        self.show_insert_number_of_stick()
        self.show_turn_choice()
        self.creating_tree()
        current_node = self.tree.tree[0]
        while not current_node.is_leaf:
            if not self.available_moving_point(current_node):
                break
            if self.current_player:
                current_node = self.get_human_moving_choice(current_node)
            else:
                current_node = self.get_comp_moving_choice(current_node)
            self.current_player = not self.current_player
            print("---------------------------------------------------\n\n")
        print("\n---------------------------------------------------\n\n")
        self.show_winner()

    def available_moving_point(self, current_node):
        print("---------------------------------------------------")
        print(("\t\t(^_^)/ YOUR" if self.current_player else "\t     ['-']/ COMPUTER'S") + " TURN")
        print("---------------------------------------------------")
        print("Available Moving Point")
        count_child = 0
        for child in current_node.children:
            if child.is_leaf:
                print("\nThere are no available moving point T____T", end="")
                return False
            else:
                print(str(count_child + 1) + ". [" + ("-".join(map(str, child.node_value)))+"]")
            count_child += 1
        print("")
        return True

    def get_comp_moving_choice(self, current_node):
        choice_child = self.check_comp_moving_choice(current_node)
        current_child = 0
        for child in current_node.children:
            if current_child == choice_child:
                print("Computer move\t: [" + ("-".join(map(str, child.node_value)))+"]")
                return child
            current_child += 1
        print("---------------------------------------------------")

    def check_comp_moving_choice(self, current_node):
        child_choice = 0
        for child in current_node.children:
            if child.evaluator_value == 1:
                return child_choice
            child_choice += 1
        return child_choice / child_choice - 1

    def get_human_moving_choice(self, current_node):
        while True:
            count_child = 0
            moving_choice = int(input("Choose your move\t: "))
            for child in current_node.children:
                if moving_choice - 1 == count_child:
                    print("Your move\t\t: [" + ("-".join(map(str, child.node_value))) + "]")
                    return child
                count_child += 1
            print("Invalid move\n")


    def show_insert_number_of_stick(self):
        print("---------------------------------------------------")
        while True:
            self.number_of_sticks = int(input("Insert number of sticks\t: "))
            if self.number_of_sticks % 2 != 0 and self.number_of_sticks != 1:
                break
            print("Must be odd and not 1.\n")
        print("---------------------------------------------------\n\n")

    def show_turn_choice(self):
        print("---------------------------------------------------")
        print("\t\t  FIRST PLAYER")
        print("---------------------------------------------------")
        self.is_play_first = int(input("1. You\n2. Computer\n\nInsert your choice\t: "))
        self.is_play_first = True if self.is_play_first == 1 else False
        print("---------------------------------------------------\n\n")

    def creating_tree(self):
        print("---------------------------------------------------")
        print("Creating tree....")
        self.tree = Tree(self.number_of_sticks, self.is_play_first)
        print("Tree created.")
        self.current_player = self.tree.first_player
        print("---------------------------------------------------\n\n")

    def show_rendered_tree(self):
        print("---------------------------------------------------")
        is_show_tree = input("View rendered tree [y/n]? ")
        print("---------------------------------------------------")
        if is_show_tree == "y" or is_show_tree == "Y":
            print(self.tree.get_tree())
        print("---------------------------------------------------\n\n")

    def show_winner(self):
        print("---------------------------------------------------")
        print(("\t    Y O U   " if not self.current_player else "\tC O M P U T E R   ") + "W I N !")
        self.current_player = not self.current_player
        print(("\t    Y O U   " if not self.current_player else "\tC O M P U T E R   ") + "L O S E !")
        print("---------------------------------------------------\n\n")


Game()