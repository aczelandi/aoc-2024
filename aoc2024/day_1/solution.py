from heapq import heappop
from pathlib import Path
import re
import heapq

class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        (left, right) = self._read_input(input_file_path)

        if len(left) != len(right):
            raise ValueError("invalid input data provided")

        heapq.heapify(left)
        heapq.heapify(right)

        return sum(abs(heappop(left) - heappop(right)) for _ in range(0, len(left)))

    def solve_part2(self, input_file_path: Path) -> int:
        (left, right) = self._read_input(input_file_path)
        right_by_count = {number : right.count(number) for number in set(right)}

        return sum(n * right_by_count.get(n, 0) for n in left)

    @staticmethod
    def _read_input(input_file_path: Path) -> (list[int], list[int]):
        left = []
        right = []
        with open(input_file_path, 'r') as file:
            for line in file:
                (left_val, right_val) = re.split(r"\s+", line.strip("\n"))
                left.append(int(left_val))
                right.append(int(right_val))

        return left, right

