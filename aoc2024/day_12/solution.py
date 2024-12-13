from pathlib import Path


class Solution:
    neighbour_offsets = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    outer_corner_neighbours_offsets = {((-1, 0), (0, -1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((1, 0), (0, 1))}
    inner_corner_neighbours_offsets = {((-1, 0), (0, -1), (-1, -1)), ((1, 0), (0, -1), (1, -1)), ((-1, 0), (0, 1), (-1, 1)), ((1, 0), (0, 1), (1, 1))}

    def solve_part1(self, input_file_path: Path) -> int:
        matrix = self._read_map(input_file_path)
        rows = len(matrix)
        cols = len(matrix[0])
        all_connected_components = self._get_all_connected_components(matrix, rows, cols)
        return sum((len(area_components) * len(self._get_component_perimeter_part_1(area_components, rows, cols, set())) for area_components in all_connected_components))

    def solve_part2(self, input_file_path: Path) -> int:
        matrix = self._read_map(input_file_path)
        rows = len(matrix)
        cols = len(matrix[0])
        all_connected_components = self._get_all_connected_components(matrix, rows, cols)
        return sum((len(area_components) * self._get_component_perimeter_part_2(area_components) for area_components in all_connected_components))

    @staticmethod
    def _read_map(input_file_path: Path) -> list[list[str]]:
        matrix = []
        with open(input_file_path, 'r') as file:
            for line in file:
                line_as_str = line.strip("\n")
                matrix.append(list(line_as_str))
        return matrix

    @staticmethod
    def _get_all_connected_components(matrix: list[list[str]], rows: int, cols: int):
        visited_components = set()
        all_connected_components = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) not in visited_components:
                    connected_component = set()
                    Solution._get_connected_component(matrix, r, c, rows, cols, visited_components, connected_component)
                    all_connected_components.append(connected_component)
        return all_connected_components

    @staticmethod
    def _get_connected_component(matrix: list[list[str]], current_row: int, current_col: int, rows: int, cols: int, visited: set[tuple[int, int]], component: set[tuple[int, int]]) -> None:
        visited.add((current_row, current_col))
        component.add((current_row, current_col))
        current_char = matrix[current_row][current_col]
        all_neighbours = ((n_r + current_row, n_c + current_col) for n_r, n_c in Solution.neighbour_offsets)
        valid_neighbours = [(n_r, n_c) for n_r, n_c in all_neighbours if (0 <= n_r < rows) and (0 <= n_c < cols) and matrix[n_r][n_c] == current_char and (n_r, n_c) not in visited]

        for (nr, nc) in valid_neighbours:
            Solution._get_connected_component(matrix, nr, nc, rows, cols, visited, component)

    @staticmethod
    def _get_component_perimeter_part_1(component: set[tuple[int, int]], rows: int, cols: int, visited: set[tuple[int, int]]) -> list[tuple[int, int]]:
        perimeter_coordinates = list()
        for r, c in component:
            all_neighbours = ((n_r + r, n_c + c) for n_r, n_c in Solution.neighbour_offsets)
            valid_neighbours = [(n_r, n_c) for n_r, n_c in all_neighbours if (n_r < 0 or n_r >= rows) or (n_c < 0 or n_c >= cols) or (n_r, n_c) not in component and (n_r, n_c) not in visited]
            visited.union(valid_neighbours)
            [perimeter_coordinates.append(neighbour) for neighbour in valid_neighbours]
        return perimeter_coordinates

    @staticmethod
    def _get_component_perimeter_part_2(component: set[tuple[int, int]]) -> int:
        perimeter_len = 0
        for r, c in component:
            outer_corner_neighbours = [((n1_r + r, n1_c + c), (n2_r + r, n2_c + c)) for ((n1_r, n1_c), (n2_r, n2_c)) in
                                       Solution.outer_corner_neighbours_offsets if (n1_r + r, n1_c + c) not in component and (n2_r + r, n2_c + c) not in component]

            inner_corner_neighbours = [((n1_r + r, n1_c + c), (n2_r + r, n2_c + c), (n3_r + r, n3_c + c)) for ((n1_r, n1_c), (n2_r, n2_c), (n3_r, n3_c)) in
                                       Solution.inner_corner_neighbours_offsets if (n1_r + r, n1_c + c) in component and (n2_r + r, n2_c + c) in component and (n3_r + r, n3_c + c) not in component]

            perimeter_len += len(outer_corner_neighbours) + len(inner_corner_neighbours)

        return perimeter_len
