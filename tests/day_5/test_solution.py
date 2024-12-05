from pathlib import Path
import pytest

from aoc2024.day_5.solution import Solution

@pytest.mark.parametrize("input_file_rules, input_file_updates,, expected", [
    ("small_sample_rules.txt", "small_sample_updates.txt", 143),
    ("input_sample_rules.txt", "input_sample_updates.txt", 4774),
])
def test_solution_part1(input_file_rules, input_file_updates, expected):
    input_file_path_rules = Path(__file__).parent / input_file_rules
    input_file_path_updates = Path(__file__).parent / input_file_updates
    solution = Solution()
    result = solution.solve_part1(input_file_path_rules = input_file_path_rules, input_file_path_updates = input_file_path_updates)
    assert result == expected

@pytest.mark.parametrize("input_file_rules, input_file_updates,, expected", [
    ("small_sample_rules.txt", "small_sample_updates.txt", 123),
    ("input_sample_rules.txt", "input_sample_updates.txt", 6004),
])
def test_solution_part2(input_file_rules, input_file_updates, expected):
    input_file_path_rules = Path(__file__).parent / input_file_rules
    input_file_path_updates = Path(__file__).parent / input_file_updates
    solution = Solution()
    result = solution.solve_part2(input_file_path_rules = input_file_path_rules, input_file_path_updates = input_file_path_updates)
    assert result == expected
