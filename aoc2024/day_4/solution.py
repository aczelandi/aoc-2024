from pathlib import Path


class Solution:
    xmas_word = "XMAS"
    positions_on_all_directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    first_diagonal_positions = ((-1, -1), (1, 1))
    second_diagonal_positions = ((-1, 1), (1, -1))

    def solve_part1(self, input_file_path: Path) -> int:
        matrix = self._read_input(input_file_path)
        row_count = len(matrix)
        col_count = len(matrix[0])
        total_sum = 0
        for i in range(0, row_count):
            for j in range(0, col_count):
                if matrix[i][j] == 'X':
                    total_sum += self._count_all_part_1(matrix, "", i, j, set())

        return total_sum

    def solve_part2(self, input_file_path: Path) -> int:
        matrix = self._read_input(input_file_path)
        row_count = len(matrix)
        col_count = len(matrix[0])
        total_sum = 0
        for i in range(0, row_count):
            for j in range(0, col_count):
                if matrix[i][j] == 'A':
                    total_sum += self._count_all_part_2(matrix, i, j)

        return total_sum

    @staticmethod
    def _read_input(input_file_path: Path) -> (list[list[str]]):
        lines = []
        with open(input_file_path, 'r') as file:
            for line in file:
                lines.append(list(line.strip("\n")))

        return lines

    def _count_all_part_1(self, matrix: list[list[str]], acc: str, row: int, col: int,
                          visited: set[tuple[int, int]], direction: tuple[int, int] = None) -> int:
        current = matrix[row][col]

        if acc + current == self.xmas_word:
            return 1

        if not self.xmas_word.startswith(acc + current):
            return 0

        visited.add((row, col))
        result = 0
        next_positions = self.positions_on_all_directions if direction is None else [direction]
        for (next_row, next_col) in next_positions:
            new_row = row + next_row
            new_col = col + next_col
            if (new_row, new_col) not in visited and 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
                result += self._count_all_part_1(matrix, acc + current, new_row, new_col, visited, (next_row, next_col))

        return result

    def _count_all_part_2(self, matrix: list[list[str]], row: int, col: int) -> int:
        first_diagonal_elements = []
        second_diagonal_elements = []

        for (first_diagonal_row, first_diagonal_column) in self.first_diagonal_positions:
            next_row = row + first_diagonal_row
            next_col = col + first_diagonal_column

            if 0 > next_row or next_row >= len(matrix) or 0 > next_col or next_col >= len(matrix[0]):
                return 0
            first_diagonal_elements.append(matrix[next_row][next_col])

        for (second_diagonal_row, second_diagonal_column) in self.second_diagonal_positions:
            next_row = row + second_diagonal_row
            next_col = col + second_diagonal_column

            if 0 > next_row or next_row >= len(matrix) or 0 > next_col or next_col >= len(matrix[0]):
                return 0
            second_diagonal_elements.append(matrix[next_row][next_col])

        if len(first_diagonal_elements) != 2 and len(second_diagonal_elements) != 2:
            return 0

        first_diagonal_elements = sorted(first_diagonal_elements)
        second_diagonal_elements = sorted(second_diagonal_elements)

        return 1 if first_diagonal_elements[0] == 'M' and second_diagonal_elements[0] == 'M' and \
                    first_diagonal_elements[1] == 'S' and second_diagonal_elements[1] == 'S' else 0
