from functools import cache
from math import floor, log10
from pathlib import Path


class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        arrangements = self._read_arrangement(input_file_path)
        return len(self._blink(arrangements, 25))

    def solve_part2(self, input_file_path: Path) -> int:
        arrangements = self._read_arrangement(input_file_path)
        return sum((self._blink_with_cache(nr, 75) for nr in arrangements))

    @staticmethod
    def _read_arrangement(input_file_path: Path) -> list[int]:
        with open(input_file_path, 'r') as file:
            return [int(nr) for nr in file.read().strip("/n").split(" ")]

    def _blink(self, arrangements: list[int], blink_count: int) -> list[int]:
        if blink_count == 0:
            return arrangements

        result = []
        for nr in arrangements:
            length = len(str(nr))
            if nr == 0:
                result.append(1)
            elif length % 2 == 0:
                first_half = int(str(nr)[0: length // 2])
                second_half = int(str(nr)[length // 2: length])
                result.append(first_half)
                result.append(second_half)
            else:
                result.append(nr * 2024)

        return self._blink(result, blink_count - 1)

    @cache
    def _blink_with_cache(self, nr: int, blink_count: int) -> int:
        if blink_count == 0:
            return 1
        if nr == 0:
            return self._blink_with_cache(1, blink_count - 1)

        l = floor(log10(nr)) + 1
        if l % 2:
            return self._blink_with_cache(nr * 2024, blink_count - 1)

        return (self._blink_with_cache(nr // 10 ** (l // 2), blink_count - 1) +
                self._blink_with_cache(nr % 10 ** (l // 2), blink_count - 1))
