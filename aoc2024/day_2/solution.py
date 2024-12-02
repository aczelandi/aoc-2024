import re
from pathlib import Path
from typing import Optional


class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        reports = self._read_input(input_file_path)
        return sum(1 for r in reports if self._is_fully_valid(r))

    def solve_part2(self, input_file_path: Path) -> int:
        reports = self._read_input(input_file_path)
        return sum(1 for r in reports if self._is_partially_valid(r))

    @staticmethod
    def _read_input(input_file_path: Path) -> (list[list[int]]):
        reports = []
        with open(input_file_path, 'r') as file:
            for report in file:
                levels = [int(level) for level in (re.split(r"\s", report.strip("\n")))]
                reports.append(levels)

        return reports

    @staticmethod
    def _is_fully_valid(report: list[int]) -> bool:
        if len(report) == 0 or len(report) == 1:
            return True

        diffs = []
        positive_count = 0
        negative_count = 0
        for i in range(1, len(report)):
            diff = report[i] - report[i - 1]
            if abs(diff) < 1 or abs(diff) > 3:
                return False
            diffs.append(diff)
            if diff >= 0:
                positive_count += 1
            else:
                negative_count += 1

        return positive_count == len(diffs) or negative_count == len(diffs)

    @staticmethod
    def _is_partially_valid(levels: list[int]) -> bool:
        if len(levels) == 0 or len(levels) == 1:
            return True
        is_valid = Solution._is_fully_valid(levels)
        if is_valid:
            return True

        for i in range(0, len(levels)):
            is_valid = Solution._remove_and_check_fully_valid(levels, i)
            if is_valid:
                return True

        return False

    @staticmethod
    def _remove_and_check_fully_valid(levels: list[int], index_to_remove: Optional[int] = None) -> bool:
        copy_of_levels = list(levels)
        if index_to_remove is not None:
            del copy_of_levels[index_to_remove]

        return Solution._is_fully_valid(copy_of_levels)
