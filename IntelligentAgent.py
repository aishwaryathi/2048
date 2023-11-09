import time
import math
from BaseAI import BaseAI
import time


class IntelligentAgent(BaseAI):
    def __init__(self):
        self.max_depth = 4
        self._max_move_depth = 0
        self.time_limit = 0.2

    def getMove(self, grid):
        best_move = None
        max_val = -math.inf

        start_time = time.process_time()
        depth = 1

        while depth <= self.max_depth:
            alpha = max_val
            beta = math.inf
            for move, moved_grid in grid.getAvailableMoves():
                temp_grid = moved_grid
                val = self.min(temp_grid, alpha, beta, depth - 1)
                alpha = max(val, alpha)
                if val > max_val:
                    max_val = val
                    best_move = move

                if alpha >= beta:
                    break

            end_time = time.process_time()
            if end_time - start_time >= self.time_limit:
                break

            depth += 1

        return best_move


    def max(self, grid, alpha, beta, depth):
        self._max_move_depth = min(depth, self._max_move_depth)
        if depth <= 0:
            return self.evaluate(grid)
        max_val = -math.inf
        children = self.get_max_children(grid)
        if len(children) ==0:
            return self.evaluate(grid)
        for next_move, next_grid in children:
            max_val = max(max_val, self.min(next_grid, alpha, beta, depth - 1))
            alpha = max(max_val, alpha)
            if alpha >= beta:
                return max_val
        return max_val

    def min(self, grid, alpha, beta, depth):
        if depth > self._max_move_depth:
            self._max_move_depth = depth

        if depth <= 0:
            return self.evaluate(grid)

        min_val = math.inf
        children = self.get_min_children(grid)
        if len(children) ==0:
            return self.evaluate(grid)
        for next_move, next_grid in children:
            min_val = min(min_val, self.max(next_grid, alpha, beta, depth - 1))
            beta = min(min_val, beta)
            if beta <= alpha:
                return min_val
        return min_val

    def get_max_children(self, grid):
        children = []
        for move, moved_grid in grid.getAvailableMoves():
            children.append((move, moved_grid))
        return children

    def get_min_children(self, grid):
        children = []
        for cell in grid.getAvailableCells():
            for tile_val in [2, 4]:
                next_grid = grid.clone()
                next_grid.setCellValue(cell, tile_val)
                children.append((None, next_grid))
        return children


    def mergeHeuristic(self, grid):
        directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
        score = 0
        size = grid.size
        for x in range(size):
            for y in range(size):
                tile = grid.map[x][y]
                if tile:
                    for direction in range(4):
                        move = directionVectors[direction]
                        next_x, next_y = x + move[0], y + move[1]
                        if grid.crossBound((next_x, next_y)):
                            next_tile = grid.map[next_x][next_y]
                            if tile == next_tile:
                                score += tile
        return score

    def monotonic(self, grid):
        score = 0
        grid_val = [[4096,1024,256,64],
                        [1024,256,64,16],
                        [256,64,16,4],
                        [64,16,4,1]]
        for r in range(3):
            for c in range(3):
                score += grid.map[r][c] * grid_val[r][c]
        return score

    def blankTiles(self, grid):
        return len(grid.getAvailableCells())

    def smoothness(self, grid):
        score = 0
        for r in range(grid.size):
            for c in range(grid.size - 1):
                curr_val = grid.map[r][c]
                next_val = grid.map[r][c + 1]
                if curr_val != 0 and next_val != 0:
                    score -= abs(curr_val - next_val)

        for c in range(grid.size):
            for r in range(grid.size - 1):
                curr_val = grid.map[r][c]
                next_val = grid.map[r + 1][c]
                if curr_val != 0 and next_val != 0:
                    score -= abs(curr_val - next_val)

        return score
    def snakeHeuristic(self, grid):

        weights = [[12, 11, 4, 3], 
        [13, 10, 5, 2], 
        [14, 9, 6, 1], 
        [15, 8, 7, 0]]

        score = 0
        max_tile = grid.getMaxTile()

        for x in range(grid.size):
            for y in range(grid.size):
                tile = grid.map[x][y]
                if tile:
                    score += weights[x][y] * tile
        score -= max_tile
        return score
    def evaluate(self, grid):
        weights = {
            'blankTiles': 1000,
            'monotonic': 10,
            'snakeHeuristic': 100,
            'smoothness': -1,
            'mergeHeuristic': 1000,
        }

        heuristics = {
            'blankTiles': self.blankTiles(grid),
            'monotonic': self.monotonic(grid),
            'snakeHeuristic': self.snakeHeuristic(grid),
            'smoothness': self.smoothness(grid),
            'mergeHeuristic': self.mergeHeuristic(grid),
        }

        total_score = sum(weights[heuristic] * heuristics[heuristic] for heuristic in weights)
        return total_score




