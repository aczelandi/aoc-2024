from pathlib import Path
import pytest

from aoc2024.day_3.solution import Solution

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample_part1.txt", 161),
    ("input_sample.txt", 184576302),
])
def test_solution_part1(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part1(input_file_path = input_file_path)
    assert result == expected

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample_part2.txt", 48),
    ("input_sample.txt", 118173507),
])
def test_solution_part2(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part2(input_file_path = input_file_path)
    assert result == expected
