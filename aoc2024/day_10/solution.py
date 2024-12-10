from pathlib import Path


class Solution:
    neighbour_offsets = ((0, -1), (0, 1), (-1, 0), (1, 0))

    def solve_part1(self, input_file_path: Path) -> int:
        topo_map = self._read_topo_map(input_file_path)
        total_rows = len(topo_map)
        total_cols = len(topo_map[0])
        trailheads = [(row, col) for row in range(0, total_rows) for col in range(0, total_cols) if topo_map[row][col] == 0]
        return sum((len(self._find_routes_from_source_to_target_part_1(topo_map, t_row, t_col, total_rows, total_cols, 9)) for t_row, t_col in trailheads))

    def solve_part2(self, input_file_path: Path) -> int:
        topo_map = self._read_topo_map(input_file_path)
        total_rows = len(topo_map)
        total_cols = len(topo_map[0])
        trailheads = [(row, col) for row in range(0, total_rows) for col in range(0, total_cols) if topo_map[row][col] == 0]
        return sum((self._find_routes_from_source_to_target_part_2(topo_map, t_row, t_col, total_rows, total_cols, 9)) for t_row, t_col in trailheads)

    @staticmethod
    def _read_topo_map(input_file_path: Path) -> list[list[int]]:
        topo_map = []
        with open(input_file_path, 'r') as file:
            for line in file:
                line_as_str = line.strip("\n")
                topo_map.append([int(height) for height in list(line_as_str)])
        return topo_map

    @staticmethod
    def _find_routes_from_source_to_target_part_1(topo_map: list[list[int]], row: int, col: int, total_rows: int,
                                                  total_cols: int, target_val: int) -> set[tuple[int, int]]:
        current = topo_map[row][col]
        if current == target_val:
            return {(row, col)}

        all_neighbours = ((row + n_row, col + n_col) for (n_row, n_col) in Solution.neighbour_offsets)
        valid_neighbours = [(n_row, n_col) for (n_row, n_col) in all_neighbours if
                            0 <= n_row < total_rows and 0 <= n_col < total_cols and topo_map[n_row][
                                n_col] == current + 1]

        if valid_neighbours is None:
            return set()

        return set().union(*[
            Solution._find_routes_from_source_to_target_part_1(topo_map, n_row, n_col, total_rows, total_cols,
                                                               target_val) for n_row, n_col in valid_neighbours])

    @staticmethod
    def _find_routes_from_source_to_target_part_2(topo_map: list[list[int]], row: int, col: int, total_rows: int, total_cols: int, target_val: int) -> int:
        current = topo_map[row][col]
        if current == target_val:
            return 1

        all_neighbours = ((row + n_row, col + n_col) for (n_row, n_col) in Solution.neighbour_offsets)
        valid_neighbours = [(n_row, n_col) for (n_row, n_col) in all_neighbours if
                            0 <= n_row < total_rows and 0 <= n_col < total_cols and topo_map[n_row][
                                n_col] == current + 1]

        if valid_neighbours is None:
            return 0

        return sum((Solution._find_routes_from_source_to_target_part_2(topo_map, n_row, n_col, total_rows, total_cols, target_val) for n_row, n_col in valid_neighbours))
