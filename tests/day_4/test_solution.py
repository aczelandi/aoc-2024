from pathlib import Path
import pytest

from aoc2024.day_4.solution import Solution

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample.txt", 18),
    ("input_sample.txt", 2644),
])
def test_solution_part1(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part1(input_file_path = input_file_path)
    assert result == expected

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample.txt", 9),
    ("input_sample.txt", 1952),
])
def test_solution_part2(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part2(input_file_path = input_file_path)
    assert result == expected
