#   Solver class, to be started

import Map as GameMap
from StateTree import Node
from Execution import Execution
import TranspositionTable
import AssignmentAlgorithms

level = open("level.txt", "r").read()

game_map = GameMap.Map(level)
game_map.mapProduction()
game_map.mapPrinting()

assignment = AssignmentAlgorithms.AssignmentAlgorithms(game_map.width, game_map.height, game_map.getTargetsArray(), game_map.getClearedMap())
# states = StateTree.StateTree(game_map.getBoxArray(), game_map.getPlayerPosition(), assignment)

table = TranspositionTable.TranspositionTable(game_map.width, game_map.height, game_map.getBoxCount())

table.insert(game_map.getBoxArray(), game_map.getPlayerPosition())

root = Node(game_map.getBoxArray(), game_map.getPlayerPosition(), None, None, assignment.greedyAssignment(game_map.getBoxArray()))
execution = Execution(table, game_map)

solution = execution.execute(root)
result = []
node = solution
if node is None:
    print("No Solution found")
else:
    while node.farther is not None:
        result.append(node.move)
        #n = node.move[1] - node.move[0]
        #if n == 1: result.append(" right,")
        #elif n == -1: result.append(" left,")
        #elif n > 0: result.append(" up,")
        #elif n < 0: result.append(" down,")
        node = node.farther
    print(result)

