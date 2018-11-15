import numpy as np


class Map:

    clear     = lambda self, x : x if x != 1 or x != 2 else 5
    box       = lambda self, x : x == 2
    targets   = lambda self, x : x == 3
    playerpos = lambda self, x : x == 1

    def __init__(self, mapString):
        self.mapString = mapString
        self.map = []
        self.width = 0
        self.height = 0
        self.mapProduction()
        self.clearedMap = map(self.clear, self.map)
        self.boxArray = list(filter(self.box, self.map))
        self.targetArray = list(filter(self.targets, self.map))
        self.player = list(filter(self.playerpos, self.map))[0]

    def mapProduction(self):
        self.map = []
        tmp = 0
        width = 0
        for c in self.mapString:
            tmp += 1
            if c == "$":  # Player
                self.map.append(1)
            if c == "@":  # Box
                self.map.append(2)
            if c == ".":  # Target
                self.map.append(3)
            if c == "#":  # Wall
                self.map.append(4)
            if c == " ":  # Empty
                self.map.append(5)

            if c == "\n":
                if tmp > width +1:
                    width = tmp -1
                tmp = 0

        self.width  = width
        self.height = len(self.map) / width

    def mapPrinting(self):
        tmp = ""
        count = 0
        for c in self.map:
            if c == 1:
                tmp += "$"
            elif c == 2:
                tmp += "@"
            elif c == 3:
                tmp += "."
            elif c == 4:
                tmp += "#"
            elif c == 5:
                tmp += " "
            count += 1
            if count == self.width:
                print(tmp)
                tmp = ""
                count = 0

#   Normalize the players position by finding the top left cell the player can reach without moving a box.
#   This decreases the memory usage of the solution tree a lot, but makes a new algorithm necessary to connect
#   the solution paths.
#
#   one_dim: boolean whether x contains the player position in one dimension or x,y contain it in two dimensions
#            if one_dim is true, the y argument will be ignored

    def normalizedPlayerPosition(self, x, y, one_dim):

        if one_dim:
            y = x // self.width
            x = x % self.width
        if x > self.width or y > self.height:
            return None

        tmp_map = np.empty(len(self.map), dtype=int)
        changes = []
        label = 1
        for i in range(0, len(self.map), 1):
            if self.isUnpassable(i):
                tmp_map[i] = 0
            elif (i-1 < 0 or self.isUnpassable(i-1)) and (i-self.width < 0 or self.isUnpassable(i-self.width)):
                tmp_map[i] = label
                label += 1
            elif i-self.width < 0 or self.isUnpassable(i-self.width):
                tmp_map[i] = tmp_map[i-1]
            elif i-1 < 0 or self.isUnpassable(i-1):
                tmp_map[i] = tmp_map[i-self.width]
            else:
                if tmp_map[i-1] < tmp_map[i-self.width]:
                    tmp_map[i] = tmp_map[i-1]
                    changes.append([tmp_map[i-1], tmp_map[i-self.width]])
                else:
                    tmp_map[i] = tmp_map[i-self.width]
                    changes.append([tmp_map[i-self.width], tmp_map[i-1]])

        # Normalize Changes
        for i in range(0, len(changes), 1):
            for j in range(0, len(changes), 1):
                if changes[i][1] == changes[j][0]:
                    changes[j][0] = changes[i][0]

        for i in range(0, len(tmp_map), 1):
            for c in changes:
                if(tmp_map[i] == c[1]):
                    tmp_map[i] = c[0]

        playerLabel = tmp_map[y * self.width + x]

        # Calculate left-top corner with label: playerLabel
        # IMPORTANT: left goes before top
        for i in range(0, len(tmp_map), 1):
            if tmp_map[int((i % self.height) * self.width + i // self.height)] == playerLabel:
                if one_dim:
                    return int((i % self.height) * self.width + i // self.height)
                else:
                    return [int((i % self.height) * self.width + i // self.height) % self.width,
                            int((i % self.height) * self.width + i // self.height) // self.width]

    def getBoxArray(self):
        return np.array(self.boxArray, dtype=int)

    def getBoxCount(self):
        return len(self.boxArray)

    def getPlayerPosition(self):
        return self.player

    def getClearedMap(self):
        return self.clearedMap

    def getTargetsArray(self):
        return self.targetArray

    def getGameMap(self):
        return self.map



#   Helpers
    def isUnpassable(self, x):
        return self.map[x] == 4 or self.map[x] == 2


# mapObj = Map("######\n#   .#\n# $  #\n#@   #\n######\n")
# print("Width:  ", mapObj.width)
# print("Height: ", mapObj.height)
# mapObj.mapPrinting()

# pr = cProfile.Profile()
# pr.run('mapObj.normalizedPlayerPosition(4, 3, False)')
# pr.print_stats()
