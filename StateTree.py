class StateTree:

    def __init__(self, box_array, player_pos):
        self.current_node = Node(box_array, player_pos, None, None)
        self.root_node = self.current_node

    def add_node(self, box_array, player_pos, move):
        self.current_node.add_node(box_array, player_pos, move)

    def refuse_node(self):
        if self.current_node == self.root_node:
            return
        else:
            self.current_node = self.current_node.farther


class Node:

    def __init__(self, box_array, player_pos, farther, move):
        self.box_array = box_array
        self.player_pos = player_pos
        self.farther = farther
        self.move = move
        self.sons = []

    def add_node(self, box_array, player_pos, move):
        self.sons.append(Node(box_array, player_pos, self, move))


class Move:

    def __init__(self, box_nr, old_pos, new_pos):
        self.box_nr = box_nr
        self.old_pos = old_pos
        self.new_pos = new_pos
