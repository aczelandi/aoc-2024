from pathlib import Path
import pytest

from aoc2024.day_6.solution import Solution

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample.txt", 41),
    ("input_sample.txt", 4602),
])
def test_solution_part1(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part1(input_file_path = input_file_path)
    assert result == expected

@pytest.mark.parametrize("input_file, expected", [
    ("small_sample.txt", 6),
    ("input_sample.txt", 1703),
])
def test_solution_part2(input_file, expected):
    input_file_path = Path(__file__).parent / input_file
    solution = Solution()
    result = solution.solve_part2(input_file_path = input_file_path)
    assert result == expected
