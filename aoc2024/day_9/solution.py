from pathlib import Path


class Solution:

    def solve_part1(self, input_file_path: Path) -> int:
        disk_map = self._read_map(input_file_path)
        decoded_map = self._decode_map(disk_map)
        compacted_map = self._compact_map_part_1(decoded_map)
        return self._get_checksum(compacted_map)

    def solve_part2(self, input_file_path: Path) -> int:
        disk_map = self._read_map(input_file_path)
        decoded_map = self._decode_map(disk_map)
        compacted_map = self._compact_map_part_2(decoded_map)
        return self._get_checksum(compacted_map)

    @staticmethod
    def _read_map(input_file_path: Path) -> list[int]:
        with open(input_file_path, 'r') as file:
            disk_map = [int(nr) for nr in list(file.readline().strip("\n"))]

        return disk_map

    @staticmethod
    def _decode_map(disk_map: list[int]) -> list[str]:
        file_index = 0
        is_free_space = False
        decoded = []

        for nr in disk_map:
            if not is_free_space:
                decoded.extend([file_index] * nr)
                file_index += 1
            else:
                decoded.extend(['.'] * nr)
            is_free_space = not is_free_space

        return decoded

    @staticmethod
    def _compact_map_part_1(disk_map: list[str]) -> list[str]:
        start = 0
        end = len(disk_map) - 1
        compacted = list(disk_map)

        while start <= end:
            current_start = compacted[start]
            current_end = compacted[end]
            if current_start != '.':
                start += 1
            elif current_end == '.':
                end -= 1
            else:
                compacted[start] = compacted[end]
                compacted[end] = '.'
                start += 1
                end -= 1

        return compacted

    @staticmethod
    def _compact_map_part_2(disk_map: list[str]) -> list[str]:
        start = 0
        end = len(disk_map) - 1
        compacted = list(disk_map)
        free_spaces = Solution._get_free_space_intervals(disk_map)

        while start <= end:
            current_start = compacted[start]
            current_end = compacted[end]
            if current_start != '.':
                start += 1
            elif current_end == '.':
                end -= 1
            else:
                end_snapshot = end
                while compacted[end_snapshot] == current_end:
                    end_snapshot -= 1

                block_length = end - end_snapshot
                (valid_slot_index, (valid_start, valid_end)) = next(
                    ((valid_slot_index, (valid_start, valid_end)) for (valid_slot_index, (valid_start, valid_end)) in
                     enumerate(free_spaces) if (valid_end - valid_start + 1) >= block_length), (None, (None, None)))
                if valid_slot_index is None or valid_start > end - block_length + 1:
                    end = end_snapshot
                else:
                    compacted[valid_start:valid_start + block_length] = [current_end] * block_length
                    compacted[end - block_length + 1: end + 1] = ['.'] * block_length
                    if valid_end - valid_start + 1 == block_length:
                        free_spaces.pop(valid_slot_index)
                    else:
                        free_spaces[valid_slot_index] = (valid_start + block_length, valid_end)

        return compacted

    @staticmethod
    def _get_checksum(compacted_map: list[str]) -> int:
        return sum((int(nr) * index for index, nr in enumerate(compacted_map) if nr != '.'))

    @staticmethod
    def _get_free_space_intervals(disk_map: list[str]) -> list[tuple[int, int]]:
        free_spaces = [i for i, val in enumerate(disk_map) if val == '.']
        intervals = []
        start = free_spaces[0]

        for prev, curr in zip(free_spaces, free_spaces[1:]):
            if curr != prev + 1:
                intervals.append((start, prev))
                start = curr
        intervals.append((start, free_spaces[-1]))  # Add the last interval

        return intervals
