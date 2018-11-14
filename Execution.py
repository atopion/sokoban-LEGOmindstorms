import AssignmentAlgorithms
import DeadlockDetection


class Execution:

    def __init__(self, state_tree, transposition_table, game_map):
        self.state_tree = state_tree
        self.transposition_table = transposition_table
        self.game_map = game_map
        self.assignment_algorithms = AssignmentAlgorithms.AssignmentAlgorithms(game_map.width, game_map.height, game_map.getTargetsArray(), game_map.getClearedMap)
        self.deadlock_detection = DeadlockDetection.DeadlockDetection()

