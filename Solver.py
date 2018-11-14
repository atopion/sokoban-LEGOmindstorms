#   Solver class, to be started

import Map as GameMap
import StateTree
import TranspositionTable

level = open("level.txt", "r").read()

game_map = GameMap.Map(level)

game_map.mapProduction()
game_map.mapPrinting()

states = StateTree.StateTree(game_map.getBoxArray(), game_map.getPlayerPosition())

table = TranspositionTable.TranspositionTable(game_map.width, game_map.height, game_map.getBoxCount())

table.insert(game_map.getBoxArray(), game_map.getPlayerPosition())
