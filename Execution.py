from AssignmentAlgorithms import AssignmentAlgorithms
import TranspositionTable
from DeadlockDetection import DeadlockDetection
from StateTree import StateTree, Node
import Map
import numpy as np


class Execution:

    def __init__(self, transposition_table: TranspositionTable, game_map: Map):
        self.transposition_table = transposition_table
        self.game_map = game_map
        self.width = game_map.width
        self.height = game_map.height
        self.assignment_algorithms = AssignmentAlgorithms(game_map.width, game_map.height, game_map.getTargetsArray(), game_map.getClearedMap())
        self.deadlock_detection = DeadlockDetection(game_map.getGameMap(), game_map.getTargetsArray(), self.width, self.height)

    def possible_moves(self, box):
        result = []
        # Move to the right
        if box +1 != 4 and box +1 != 2 and self.deadlock_detection.deadlock_array[box +1] == 0 and (box) % self.width != 0:
            result.append([box, box+1])
        # Move to the left
        if box -1 != 4 and box -1 != 2 and self.deadlock_detection.deadlock_array[box -1] == 0 and (box) % self.width != 1:
            result.append([box, box-1])
        # Move down
        if box + self.width != 4 and box + self.width != 2 and self.deadlock_detection.deadlock_array[box + self.width] == 0 and (box + self.width) <= len(self.game_map.map):
            result.append([box, box + self.width])
        # Move up
        if box - self.width != 4 and box - self.width != 2 and self.deadlock_detection.deadlock_array[box - self.width] == 0 and (box - self.width) >= 0:
            result.append([box, box - self.width])
        return result

    def analyse_state(self, node):
        # Produces followup states of the given state and sort's them ascending by their new lower bound
        # Also a deadlock detection is performed on every new state.
        # The new states are checked in the transposition table.
        # player_position is the normalized position of the box before moving.
        #
        #
        box_array = node.box_array
        # result = []
        for i in range(0, len(box_array), 1):
            moves = self.possible_moves(box_array[i])
            for m in moves:
                if self.deadlock_detection.deadlock_array[m[1]] == 1:
                    print("Deadlock: ", m[1])
                    continue

                pos = self.game_map.normalizedPlayerPositionMove(m)
                print("Move", m)
                print("Posititon: ", (m[0] - (m[1] - m[0])))
                print("Reachable: ", self.game_map.is_reachable(m[0] - (m[1] - m[0])))
                print(self.game_map.print_reachableArray())
                if not self.game_map.is_reachable(m[0] - (m[1] - m[0])):
                    print("Not reachable: ", m[1])
                    continue
                new_box_array = np.array(box_array, dtype=int)
                new_box_array[i] = m[1]
                # new_box_array = box_array[:i].append(m[1]) + box_array[i + 1:]
                if self.transposition_table.lookup(new_box_array, pos):
                    print("Already visited: ", m[1])
                    continue
                print("")
                print("New Box Array: ", new_box_array)
                bound = self.assignment_algorithms.greedyAssignment(new_box_array)
                print("BOUND: ", bound)
                if bound == 0:
                    # Target found
                    return Node(new_box_array, pos, node, m, 0)
                f = True
                for j in range(0, len(node.sons), 1):
                    if bound < node.sons[i].lower_bound:
                        node.sons.insert(j, Node(new_box_array, pos, node, m, bound))
                        # result.insert(j, Node(new_box_array, pos, node, m, bound))
                        print("Smaller: ", node.sons)
                        f = False
                        break
                if f:
                    node.sons.append(Node(new_box_array, pos, node, m, bound))
                    print("Last: ", node.sons)
                    # result.append(Node(new_box_array, pos, node, m, bound))

        return None

    def execute(self, current_node, depth=0):
        res = self.analyse_state(current_node)
        print("Sons: ", current_node.sons)
        print("Result: ", res)
        if res is not None:
            return res
        if not current_node.sons:
            return None
        if depth >= 1000:
            print("Depth reached")
            return None

        for s in current_node.sons:
            r = self.execute(s, depth+1)
            if r is not None:
                return r
        return None
