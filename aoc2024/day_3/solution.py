import re
from pathlib import Path


class Solution:

    row_pattern_part1 = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    row_pattern_part2 = r"mul\([0-9]{1,3},[0-9]{1,3}\)|don\'t\(\)|do\(\)"
    mul_pattern = r"([0-9]{1,3}),([0-9]{1,3})"

    def solve_part1(self, input_file_path: Path) -> int:
        input_lines = self._read_input(input_file_path)
        total_sum = 0

        for line in input_lines:
            mul_match = re.findall(self.row_pattern_part1, line)
            for mm in mul_match:
                numbers = re.findall(self.mul_pattern, mm)
                mul = 1
                for n in numbers[0]:
                    mul *= int(n)
                total_sum += mul

        return total_sum

    def solve_part2(self, input_file_path: Path) -> int:
        input_lines = self._read_input(input_file_path)
        total_sum = 0

        include_next = True
        for line in input_lines:
            match = re.findall(self.row_pattern_part2, line)
            for mm in match:
                if mm.startswith("mul") and include_next:
                    numbers = re.findall(self.mul_pattern, mm)
                    mul = 1
                    for n in numbers[0]:
                        mul *= int(n)
                    total_sum += mul
                elif mm == "don't()":
                    include_next = False
                elif mm =="do()":
                    include_next = True

        return total_sum

    @staticmethod
    def _read_input(input_file_path: Path) -> (list[str]):
        lines = []
        with open(input_file_path, 'r') as file:
            for line in file:
                lines.append(line.strip("\n"))

        return lines