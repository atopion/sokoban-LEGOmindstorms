import AssignmentAlgorithms
import DeadlockDetection
import numpy as np


class Execution:

    def __init__(self, state_tree, transposition_table, game_map):
        self.state_tree = state_tree
        self.transposition_table = transposition_table
        self.game_map = game_map
        self.width = game_map.width
        self.height = game_map.height
        self.assignment_algorithms = AssignmentAlgorithms.AssignmentAlgorithms(game_map.width, game_map.height, game_map.getTargetsArray(), game_map.getClearedMap)
        self.deadlock_detection = DeadlockDetection.DeadlockDetection(game_map.getGameArray(), game_map.getTargetsArray(), self.width, self.height)

    def possibleMoves(self, state, box):
        result = []
        # Move to the right
        if box +1 != 4 and box +1 != 2 and self.deadlock_detection.deadlock_array[box +1] == 0 and (box) % self.width != 0:
            result.append([box, box+1])
        # Move to the left
        if box -1 != 4 and box -1 != 2 and self.deadlock_detection.deadlock_array[box -1] == 0 and (box) % self.width != 1:
            result.append([box, box-1])
        # Move down
        if box + self.width != 4 and box + self.width != 2 and self.deadlock_detection.deadlock_array[box + self.width] == 0 and (box + self.width) <= len(self.game_map.map):
            result.append([box, box+ self.width])
        # Move up
        if box - self.width != 4 and box - self.width != 2 and self.deadlock_detection.deadlock_array[box - self.width] == 0 and (box - self.width) >= 0:
            result.append([box, box- self.width])
        return result

    def execute(self, state):
        box_array = state.get_current_node().box_array
        for b in box_array:


