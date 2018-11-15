import numpy as np


class DeadlockDetection:

    # TODO Missing bounds at self.width

    def __init__(self, game_array, target_array, width, height):
        self.game_array = game_array
        self.target_array = target_array
        self.width = width
        self.height = height
        self.deadlock_array = np.zeros(self.width*self.height, dtype=int)

    # Self designed deadlock detection.
    # Sets every corner as deadlocked and then uses the recursive property of deadlocks
    def detect(self):
        for i in range(0, len(self.game_array)):
            # Wall
            if self.game_array[i] == 4:
                self.deadlock_array[i] = 1
            # Player or Empty (Boxes can not be on deadlocks from start and a corner with target is not a deadlock)
            elif self.game_array[i] == 1 or self.game_array[i] == 5:
                # Top-left corner
                if (self.game_array[i-1] == 4 or i-1 < 0) and (self.game_array[i-self.width] == 4 or i-self.width < 0):
                    self.deadlock_array[i] = 1
                # Top-right corner
                elif (self.game_array[i+1] == 4 or i+1 > len(self.game_array)) and (self.game_array[i-self.width] == 4 or i-self.width < 0):
                    self.deadlock_array[i] = 1
                # Bottom-left corner
                elif (self.game_array[i-1] == 4 or i-1 < 0) and (self.game_array[i+self.width] == 4 or i+self.width > len(self.game_array)):
                    self.deadlock_array[i] = 1
                # Bottom-right corner
                elif (self.game_array[i+1] == 4 or i+1 > len(self.game_array)) and (self.game_array[i+self.width] == 4 or i+self.width > len(self.game_array)):
                    self.deadlock_array[i] = 1

        for i in range(0, len(self.game_array), 1):
            self.deadlock_array[i] = self._reku_deadlock(i)

    def _reku_deadlock(self, a):
        if a < 0 or a >= len(self.game_array) or self.game_array[a] == 4: return 0
        elif self.deadlock_array[a] == 1:
            return 1
        elif not self._walls_around(a):
            return 0
        else:
            r = 1
            if a+1 < len(self.game_array): r = r & self._reku_deadlock(a+1)
            if a-1 > 0: r = r & self._reku_deadlock(a-1)
            if a+self.width < len(self.game_array): r = r & self._reku_deadlock(a+self.width)
            if a-self.width > 0: r = r & self._reku_deadlock(a-self.width)
            return r

    # Pull Deadlock detection
    def detect_pull(self):
        visited = np.zeros(self.width*self.height, dtype=int)
        for t in range(0, len(self.target_array), 1):
            self._reku_pull(t, visited)
        for a in range(0, len(visited), 1):
            if visited[a] == 0:
                self.deadlock_array[a] = 1

    def _reku_pull(self, a, visited):
        if visited[a] == 1: return
        if a < 0 or self.game_array[a] == 4 or a >= len(self.game_array): return
        visited[a] = 1
        if a+1 < len(self.game_array) and self.game_array[a+1] != 4: self._reku_pull(a+1, visited)
        if a-1 > 0 and self.game_array[a+1] == 4: self._reku_pull(a-1, visited)
        if a+self.width < len(self.game_array) and self.game_array[a+self.width] != 4: self._reku_pull(a+self.width, visited)
        if a-self.width > 0 and self.game_array[a-self.width] != 4: self._reku_pull(a-self.width, visited)

    # Helpers
    def _walls_around(self, a):
        b = self.game_array[a-1] == 4 or self.game_array[a+1] == 4 or self.game_array[a-self.width] == 4 or self.game_array[a+self.width] == 4
        c = a-1 < 0 or a-self.width < 0 or a+1 > len(self.game_array) or a+self.width > len(self.game_array)
        return b or c
