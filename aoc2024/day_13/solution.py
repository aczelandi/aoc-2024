import dataclasses
import re
import sys
from functools import cache
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Button:
    x_offset: int = 0
    y_offset: int = 0
    cost: int = 0


@dataclasses.dataclass(frozen=True)
class Position:
    x: int = 0
    y: int = 0

    def apply(self, button: Button) -> "Position":
        return Position(self.x + button.x_offset, self.y + button.y_offset)


class Solution:
    button_regex = r"Button\s[AB]:\sX\+(\d+),\sY\+(\d+)"
    prize_regex = r"Prize: X=(\d+), Y=(\d+)"

    def solve_part1(self, input_file_path: Path) -> int:
        machines = self._read_input(input_file_path)
        return sum(
            (cost for cost in (self._compute_min_cost_part_1(machine_setup=machine_setup[0], current_position=Position(0, 0), target_position=machine_setup[1], cost=0) for machine_setup in machines)
             if cost != sys.maxsize))

    def solve_part2(self, input_file_path: Path) -> int:
        machines = self._read_input(input_file_path, offset=10000000000000)
        return sum(
            (cost for cost in (
                self._compute_min_cost_part_2(machine_setup=machine_setup[0],
                                              target_position=Position(x=machine_setup[1].x, y=machine_setup[1].y),
                                              presses_b=machine_setup[1].x // machine_setup[0][1].x_offset) for machine_setup in machines)
             if cost != sys.maxsize))

    def _read_input(self, input_file_path: Path, offset: int = 0) -> list[tuple[tuple[Button, Button], Position]]:
        machines = []

        with open(input_file_path, 'r') as file:
            blocks = file.read().strip().split("\n\n")
            for b in blocks:
                lines = b.split("\n")
                button_a_match = re.match(self.button_regex, lines[0]).groups()
                button_a = Button(x_offset=int(button_a_match[0]), y_offset=int(button_a_match[1]), cost=3)
                button_b_match = re.match(self.button_regex, lines[1]).groups()
                button_b = Button(x_offset=int(button_b_match[0]), y_offset=int(button_b_match[1]), cost=1)
                prize_match = re.match(self.prize_regex, lines[2]).groups()
                prize = Position(x=int(prize_match[0]) + offset, y=int(prize_match[1]) + offset)
                machines.append(((button_a, button_b), prize))

        return machines

    @cache
    def _compute_min_cost_part_1(self, machine_setup: tuple[Button, Button], current_position: Position, target_position: Position, cost: int) -> int:
        if current_position.x == target_position.x and current_position.y == target_position.y:
            return cost

        if current_position.x > target_position.x or current_position.y > target_position.y:
            return sys.maxsize

        return min([self._compute_min_cost_part_1(machine_setup, current_position.apply(button), target_position, cost + button.cost) for button in machine_setup])

    ## https://www.reddit.com/r/adventofcode/comments/1hd4wda/comment/m1vrand/
    @cache
    def _compute_min_cost_part_2(self, machine_setup: tuple[Button, Button], target_position: Position, presses_b: int) -> int:
        total_cost = sys.maxsize
        while presses_b >= 0:
            presses_a = (target_position.x - presses_b * machine_setup[1].x_offset) / machine_setup[0].x_offset
            presses_a_rest = (target_position.x - presses_b * machine_setup[1].x_offset) % machine_setup[0].x_offset
            if presses_a_rest == 0 and presses_a * machine_setup[0].y_offset + presses_b * machine_setup[1].y_offset == target_position.y:
                total_cost = min(total_cost, int(presses_a) * machine_setup[0].cost + presses_b * machine_setup[1].cost)
            presses_b -=1

        return total_cost
