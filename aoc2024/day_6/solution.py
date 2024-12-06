import sys
from functools import cache
from pathlib import Path

from enum import Enum

sys.setrecursionlimit(10000)

class Orientation(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    def __init__(self, val):
        self.next = None


Orientation.NORTH.next = Orientation.EAST
Orientation.EAST.next = Orientation.SOUTH
Orientation.SOUTH.next = Orientation.WEST
Orientation.WEST.next = Orientation.NORTH

class Solution:
    next_moves_mapping = {
        Orientation.NORTH: (-1, 0),
        Orientation.EAST: (0, 1),
        Orientation.SOUTH: (1, 0),
        Orientation.WEST: (0, -1),
    }

    def solve_part1(self, input_file_path: Path) -> int:
        matrix = self._read_map(input_file_path)
        (start_cell_row, start_cell_col) = next((row, col) for row in range(0, len(matrix)) for col in range(0, len(matrix[0])) if matrix[row][col] == '^')
        matrix[start_cell_row][start_cell_col] = "."
        visited_cells = self._walk_map(matrix, start_cell_row, start_cell_col, Orientation.NORTH)
        return len(visited_cells) + 1

    def solve_part2(self, input_file_path: Path) -> int:
        matrix = self._read_map(input_file_path)
        (start_cell_row, start_cell_col) = next((row, col) for row in range(0, len(matrix)) for col in range(0, len(matrix[0])) if matrix[row][col] == '^')
        matrix[start_cell_row][start_cell_col] = "."
        blocking_position_count = 0
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                if i == start_cell_row and j == start_cell_col:
                    continue
                if matrix[i][j] != '.':
                    continue
                matrix[i][j] = "#"
                has_cycle = self._search_cycle_in_map(matrix, start_cell_row, start_cell_col, Orientation.NORTH, set())
                if has_cycle:
                    blocking_position_count += 1
                matrix[i][j] = "."

        return blocking_position_count

    @staticmethod
    def _read_map(input_file_path: Path) -> list[list[str]]:
        rules = []
        with open(input_file_path, 'r') as file:
            for line in file:
                rules_as_str = line.strip("\n")
                rules.append(list(rules_as_str))

        return rules

    def _walk_map(self, matrix: list[list[str]], row: int, col: int, orientation: Orientation) -> set[tuple[int, int]]:

        (next_row_offset, next_col_offset) = self.next_moves_mapping[orientation]
        next_row, next_col = row + next_row_offset, col + next_col_offset
        if next_row < 0 or next_row >= len(matrix) or next_col < 0 or next_col >= len(matrix[0]):
            return set()

        next_cell = matrix[next_row][next_col]
        if next_cell == ".":
            return {(row, col)} | self._walk_map(matrix, next_row, next_col, orientation)
        if next_cell == "#":
            return {(row, col)} | self._walk_map(matrix, row, col, orientation.next)

        return set()

    def _search_cycle_in_map(self, matrix: list[list[str]], row: int, col: int, orientation: Orientation, visited: set[tuple[int,int,int]]) -> bool:

        if (row, col, orientation.value) in visited:
            # we already arrived once to this position from the same direction
            return True

        visited.add((row, col, orientation.value))
        (next_row_offset, next_col_offset) = self.next_moves_mapping[orientation]
        next_row, next_col = row + next_row_offset, col + next_col_offset
        if next_row < 0 or next_row >= len(matrix) or next_col < 0 or next_col >= len(matrix[0]):
            return False

        next_cell = matrix[next_row][next_col]
        if next_cell == ".":
            return self._search_cycle_in_map(matrix, next_row, next_col, orientation, visited)
        if next_cell == "#":
            return self._search_cycle_in_map(matrix, row, col, orientation.next, visited)

        return False
