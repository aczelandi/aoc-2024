from itertools import combinations
from pathlib import Path

from mypy.binder import defaultdict


class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        antenna_map = self._read_map(input_file_path)
        rows = len(antenna_map)
        cols = len(antenna_map[0])
        antenna_dict = self._get_map_as_dict(antenna_map)
        antinode_positions = []
        for frequency in antenna_dict:
            antinode_positions.extend(Solution._add_possible_antinodes_for_frequency_part_1(antenna_dict[frequency], rows, cols))
        return len(set(antinode_positions))

    def solve_part2(self, input_file_path: Path) -> int:
        antenna_map = self._read_map(input_file_path)
        rows = len(antenna_map)
        cols = len(antenna_map[0])
        antenna_dict = self._get_map_as_dict(antenna_map)
        antinode_positions = []
        for frequency_letter, frequency_positions in antenna_dict.items():
            antinodes_for_freq = Solution._add_possible_antinodes_for_frequency_part_2(antenna_dict[frequency_letter], rows, cols)
            antinodes_for_freq = antinodes_for_freq | frequency_positions
            antinode_positions.extend(antinodes_for_freq)
        return len(set(antinode_positions))

    @staticmethod
    def _read_map(input_file_path: Path) -> list[list[str]]:
        antenna_map = []
        with open(input_file_path, 'r') as file:
            for line in file:
                antenna_map.append(list(line.strip("\n")))

        return antenna_map

    @staticmethod
    def _get_map_as_dict(antennas_map: list[list[str]]) -> dict[str, set[tuple[int, int]]]:
        row = len(antennas_map)
        col = len(antennas_map[0])

        antennas_dict = defaultdict(set)
        for i in range(0, row):
            for j in range(0, col):
                frequency = antennas_map[i][j]
                if frequency != ".":
                    antennas_dict[frequency].add((i,j))

        return antennas_dict

    @staticmethod
    def _add_possible_antinodes_for_frequency_part_1(positions: set[tuple[int, int]], rows: int, cols: int) -> set[tuple[int, int]]:
        position_pairs_for_frequency = list(combinations(positions, 2))
        valid_antinode_positions = []
        for pos1, pos2 in position_pairs_for_frequency:
            diff_row, diff_col = pos1[0] - pos2[0], pos1[1] - pos2[1]
            all_antinode_positions = [(pos1[0] + diff_row, pos1[1] + diff_col), (pos2[0] - diff_row, pos2[1] - diff_col)]
            valid_antinode_positions.extend([pos for pos in all_antinode_positions if 0 <= pos[0] < rows and 0 <= pos[1] < cols])
        return set(valid_antinode_positions)

    @staticmethod
    def _add_possible_antinodes_for_frequency_part_2(positions: set[tuple[int, int]], rows: int, cols: int) -> set[tuple[int, int]]:
        position_pairs_for_frequency = list(combinations(positions, 2))
        valid_antinode_positions = []
        for pos1, pos2 in position_pairs_for_frequency:
            diff_row, diff_col = pos1[0] - pos2[0], pos1[1] - pos2[1]
            all_antinode_positions = []
            antinode_row = pos1[0]
            antinode_col = pos1[1]
            while 0 <= antinode_row < rows and 0 <= antinode_col < cols:
                antinode_row, antinode_col =  antinode_row + diff_row, antinode_col + diff_col
                all_antinode_positions.append((antinode_row, antinode_col))

            antinode_row = pos2[0]
            antinode_col = pos2[1]
            while 0 <= antinode_row < rows and 0 <= antinode_col < cols:
                antinode_row, antinode_col =  antinode_row - diff_row, antinode_col - diff_col
                all_antinode_positions.append((antinode_row, antinode_col))

            valid_antinode_positions.extend([pos for pos in all_antinode_positions if 0 <= pos[0] < rows and 0 <= pos[1] < cols])
        return set(valid_antinode_positions)
