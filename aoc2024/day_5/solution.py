from collections import deque
from pathlib import Path

from mypy.binder import defaultdict


class Solution:

    def solve_part1(self, input_file_path_rules: Path, input_file_path_updates: Path) -> int:
        rules = self._read_rules(input_file_path_rules)
        updates = self._read_updates(input_file_path_updates)
        rules_as_dict = self._get_rules_as_dict(rules)
        valid_updates = self._find_valid_updates(rules_as_dict, updates)
        return sum((sublist[len(sublist) // 2] for sublist in valid_updates))

    def solve_part2(self, input_file_path_rules: Path, input_file_path_updates: Path) -> int:
        rules = self._read_rules(input_file_path_rules)
        updates = self._read_updates(input_file_path_updates)
        rules_as_dict = self._get_rules_as_dict(rules)
        fixed_updates = self._get_fixed_updates(rules_as_dict, updates)
        return sum((sublist[len(sublist) // 2] for sublist in fixed_updates))

    @staticmethod
    def _read_rules(input_file_path: Path) -> list[tuple[int, int]]:
        rules = []
        with open(input_file_path, 'r') as file:
            for line in file:
                rules_as_str = line.strip("\n").split("|")
                rules.append((int(rules_as_str[0]), int(rules_as_str[1])))

        return rules

    @staticmethod
    def _read_updates(input_file_path: Path) -> list[list[int]]:
        rules = []
        with open(input_file_path, 'r') as file:
            for line in file:
                rules_as_str = line.strip("\n").split(",")
                rules.append([int(nr) for nr in rules_as_str])

        return rules

    @staticmethod
    def _get_rules_as_dict(rules: list[tuple[int, int]]) -> dict[int, set[int]]:
        result = defaultdict(set)
        for (start, end) in rules:
            result[start].add(end)
        return result

    @staticmethod
    def _find_valid_updates(rules_as_dict: dict[int, set[int]], updates: list[list[int]]) -> list[list[int]]:
        def _is_update_valid(_update: list[int]) -> bool:
            current_level = 0
            topo_sort_by_level = Solution._sort_topologically(rules_as_dict, _update)
            for nr in _update:
                nr_level = topo_sort_by_level[nr]
                if nr_level < current_level:
                    return False
                current_level = nr_level
            return True

        return [update for update in updates if _is_update_valid(update)]

    @staticmethod
    def _get_fixed_updates(rules_as_dict: dict[int, set[int]], updates: list[list[int]]) -> list[list[int]]:
        result = []
        for update in updates:
            current_level = 0
            topo_sort_by_level = Solution._sort_topologically(rules_as_dict, update)
            is_invalid = False
            for nr in update:
                nr_level = topo_sort_by_level[nr]
                if nr_level < current_level:
                    is_invalid = True
                    break
                current_level = nr_level

            if is_invalid:
                result.append(Solution._get_sorted_by_level(topo_sort_by_level))

        return result

    @staticmethod
    def _sort_topologically(rules_as_dict: dict[int, set[int]], pages: list[int]) -> dict[int, int]:
        if not rules_as_dict:
            return {}

        in_degree = defaultdict(int)

        for node in pages:
            if node not in in_degree:
                in_degree[node] = 0
            for neighbour in rules_as_dict[node]:
                in_degree[neighbour] += 1

        queue = deque([node for node in in_degree if in_degree[node] == 0])
        if len(queue) == 0:
            queue.append(list(rules_as_dict.keys())[0])

        level = 0
        node_by_level = {}

        while queue:
            for _ in range(len(queue)):
                current = queue.popleft()
                node_by_level[current] = level
                for neighbour in rules_as_dict[current]:
                    if neighbour in pages:
                        in_degree[neighbour] -= 1
                        if in_degree[neighbour] == 0:
                            queue.append(neighbour)
            level += 1

        return node_by_level

    @staticmethod
    def _get_sorted_by_level(topo_sort_by_level: dict[int, int]) -> list[int]:
        values = []
        for nr, level in topo_sort_by_level.items():
            values.insert(level, nr)

        return values

