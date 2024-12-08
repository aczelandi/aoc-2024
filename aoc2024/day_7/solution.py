from pathlib import Path


class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        rules = self._read_rules(input_file_path)
        return sum((rule[0] for rule in rules if Solution._is_solvable_part_1(rule[0], rule[1][1:], rule[1][0])))

    def solve_part2(self, input_file_path: Path) -> int:
        rules = self._read_rules(input_file_path)
        return sum((rule[0] for rule in rules if Solution._is_solvable_part_2(rule[0], rule[1][1:], rule[1][0])))

    @staticmethod
    def _read_rules(input_file_path: Path) -> list[(int, list[int])]:
        rules = []
        with open(input_file_path, 'r') as file:
            for line in file:
                rules_as_str = line.strip("\n")
                result, components = rules_as_str.split(": ", 2)
                rules.append((int(result), [int(nr) for nr in list(components.split(" "))]))

        return rules

    @staticmethod
    def _is_solvable_part_1(result: int, components: list[int], acc: int) -> bool:
        if result == acc and not components:
            return True

        if not components:
            return False

        return (Solution._is_solvable_part_1(result, components[1:], acc + components[0])
                or Solution._is_solvable_part_1(result, components[1:], acc * components[0]))

    @staticmethod
    def _is_solvable_part_2(result: int, components: list[int], acc: int) -> bool:
        if result == acc and not components:
            return True

        if not components:
            return False

        return (Solution._is_solvable_part_2(result, components[1:], acc + components[0])
                or Solution._is_solvable_part_2(result, components[1:], acc * components[0])
                or Solution._is_solvable_part_2(result, components[1:], int(f"{acc}{components[0]}")))