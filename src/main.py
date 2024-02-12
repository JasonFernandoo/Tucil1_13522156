import itertools
import time
import random
import os
import sys

def read_file(filename):
    with open(f'tes/{filename}', 'r') as file:
        buffer_size = int(file.readline())
        rows, cols = map(int, file.readline().split()) 
        matrix = [list(file.readline().split()) for _ in range(rows)]
        num_seqs = int(file.readline())
        sequences = []
        points = []
        for _ in range(num_seqs):
            sequences.append(file.readline().strip().split())
            points.append(int(file.readline()))
    return buffer_size, matrix, sequences, points

def generate_random_input(rows, cols, num_seqs):
    buffer_size = random.randint(1, 5)
    matrix_size = (rows, cols)

    matrix = [[chr(random.randint(65, 90)) for _ in range(cols)] for _ in range(rows)]
    
    sequences = [[''.join(chr(random.randint(65, 90)) for _ in range(random.randint(1, 5)))] for _ in range(num_seqs)]

    points = [random.randint(1, 10) for _ in range(num_seqs)]

    print("Randomly Generated Input:")
    print(f"Buffer Size: {buffer_size}")
    print("Matrix:")
    for row in matrix:
        print(" ".join(row))
    print(f"Number of Sequences: {num_seqs}")
    print("Sequences:")
    for seq in sequences:
        print(" ".join(seq))
    print("Points:")
    print(" ".join(map(str, points)))

    return buffer_size, matrix, sequences, points

def find_all_patterns(
    matrix: list[list[str]], step: int
) -> list[list[tuple[str, tuple[int, int]]]]:
    num_rows: int = len(matrix)
    num_cols: int = len(matrix[0])
    all_paths: list[list[tuple[str, tuple[int, int]]]] = []

    def explore_paths(
        current_x: int,
        current_y: int,
        current_path: list[tuple[str, tuple[int, int]]] = [],
        visited_cells: set[tuple[int, int]] = set(),
        current_direction: str = "vertical",
        remaining_steps: int = step,
    ) -> None:
        if remaining_steps == 0:
            all_paths.append(current_path.copy())
            return
        if current_direction == "vertical":
            for next_y in range(num_rows):
                if (current_x, next_y) not in visited_cells: 
                    explore_paths(
                        current_x,
                        next_y,
                        current_path + [
                            (matrix[next_y][current_x], (current_x, next_y))
                        ],  
                        visited_cells | {(current_x, next_y)}, 
                        "horizontal",
                        remaining_steps - 1,
                    )
        else: 
            for next_x in range(num_cols):
                if (next_x, current_y) not in visited_cells: 
                    explore_paths(
                        next_x,
                        current_y,
                        current_path + [
                            (matrix[current_y][next_x], (next_x, current_y))
                        ],  
                        visited_cells | {(next_x, current_y)},  
                        "vertical",
                        remaining_steps - 1,
                    )

    for x in range(num_cols):
        explore_paths(
            x,
            0,
            current_path=[(matrix[0][x], (x, 0))],
            visited_cells={(x, 0)},
            current_direction="vertical",
            remaining_steps=step,
        )

    return all_paths

def calculate_point(matrix, path, sequences, points):
    total_reward = 0
    buffer_tokens = []
    for token, _ in path:
        buffer_tokens.append(token)
        for seq, reward in zip(sequences, points):
            if all(t in buffer_tokens for t in seq):
                total_reward += reward
                buffer_tokens = [t for t in buffer_tokens if t not in seq]
    return total_reward

def compare_path_with_sequence(
    path: list[tuple[str, tuple[int, int]]], sequence: list[str],
) -> bool:
    for i in range(0, len(path)-len(sequence)+1):
        if all(path[i+j][0] == sequence[j] for j in range(len(sequence))):
            return True
    return False

def point_path(path: list[tuple[str, tuple[int, int]]], rewards: list[int], sequences: list[list[str]]) -> int:
    for i in range(len(sequences)):
        if compare_path_with_sequence(path, sequences[i]):
            return rewards[i]
    return 0

def compare_paths(
    all_paths: list[list[tuple[str, tuple[int, int]]]],
    sequences: list[list[str]],
    rewards: list[int],
) -> tuple[list[list[tuple[str, tuple[int, int]]]], int]:
    result = []
    total_points = 0
    current_points = 0
    for path in all_paths:
        for i in range(len(sequences)):
            if compare_path_with_sequence(path, sequences[i]):
                current_points += rewards[i]
        if not result:
            result = path
            total_points = current_points
        else:
            if current_points > total_points:
                result = path
                total_points = current_points
        current_points = 0

    return result, total_points

def optimal_pattern(matrix, buffer_size, sequences, points):
    all_paths = find_all_patterns(matrix, buffer_size)
    optimal_path, max_points = compare_paths(all_paths, sequences, points)
    return max_points, optimal_path[:-1]

def save_results(max_points, optimal_path, final_time):
    filename = input("Enter the filename to save the results: ")
    with open(f'tes/{filename}.txt', 'w') as file:
        file.write("RESULT:\n")
        file.write(f"Points obtained: {max_points}\n")
        file.write(f"Path: {' '.join(token for token, _ in optimal_path)}\n")
        file.write("Selected Path Coordinates:\n")
        for _, (x, y) in optimal_path:
            file.write(f"{x + 1}, {y + 1}\n")
        file.write(f"{final_time * 1000} ms\n")
        loader()
        clear_terminal()
    print(f"Results saved to {filename}")

def initial_display():
    print_ascii_main()
    print("Select Input Method:")
    print("1. Read from txt file")
    print("2. Generate Random Input")
    print("3. Exit")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_main():
    print('''                                                                                  
                                                                                                                                    
  .g8"""bgd `YMM'   `MM'`7MM"""Yp, `7MM"""YMM  `7MM"""Mq.  `7MM"""Mq. `7MMF'   `7MF'`7MN.   `7MF'`7MMF' `YMM' 
.dP'     `M   VMA   ,V    MM    Yb   MM    `7    MM   `MM.   MM   `MM.  MM       M    MMN.    M    MM   .M'   
dM'       `    VMA ,V     MM    dP   MM   d      MM   ,M9    MM   ,M9   MM       M    M YMb   M    MM .d"     
MM              VMMP      MM"""bg.   MMmmMM      MMmmdM9     MMmmdM9    MM       M    M  `MN. M    MMMMM.     
MM.              MM       MM    `Y   MM   Y  ,   MM  YM.     MM         MM       M    M   `MM.M    MM  VMA    
`Mb.     ,'      MM       MM    ,9   MM     ,M   MM   `Mb.   MM         YM.     ,M    M     YMM    MM   `MM.  
  `"bmmmd'     .JMML.   .JMMmmmd9  .JMMmmmmMMM .JMML. .JMM..JMML.        `bmmmmd"'  .JML.    YM  .JMML.   MMb.    
                                                                                                    
        ''')
    loader()
    print("\033c", end="")

def print_ascii_result():
    print("\033c", end="")
    print('''                                                                                  
                                                                         
`7MM"""Mq.  `7MM"""YMM   .M"""bgd `7MMF'   `7MF'`7MMF'      MMP""MM""YMM 
  MM   `MM.   MM    `7  ,MI    "Y   MM       M    MM        P'   MM   `7 
  MM   ,M9    MM   d    `MMb.       MM       M    MM             MM      
  MMmmdM9     MMmmMM      `YMMNq.   MM       M    MM             MM      
  MM  YM.     MM   Y  , .     `MM   MM       M    MM      ,      MM      
  MM   `Mb.   MM     ,M Mb     dM   YM.     ,M    MM     ,M      MM      
.JMML. .JMM..JMMmmmmMMM P"Ybmmd"     `bmmmmd"'  .JMMmmmmMMM    .JMML.    
                                                                                                    
        ''')
    
def loader():
    chars = "/—\\|"
    for _ in range(5):
        for char in chars:
            sys.stdout.write('\r' + 'Loading ' + char)
            sys.stdout.flush()
            time.sleep(0.1)
    print()

def main():
    initial_display()
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        filename = input("Enter the file name: ")
        loader()
        print_ascii_result()
        buffer_size, matrix, sequences, points = read_file(filename)
    elif choice == '2':
        rows = int(input("Enter the number of rows: "))
        cols = int(input("Enter the number of columns: "))
        num_seqs = int(input("Enter the number of sequences: "))
        print_ascii_result()
        buffer_size, matrix, sequences, points = generate_random_input(rows, cols, num_seqs)
    elif choice == '3':
        clear_terminal()
        return
    else:
        print("Invalid choice. Exiting.")
        return

    start_time = time.time()
    max_points, optimal_path = optimal_pattern(matrix, buffer_size, sequences, points)
    end_time = time.time()
    final_time = end_time - start_time
    print("Points obtained:", max_points)
    print("Path:", ' '.join(token for token, _ in optimal_path))
    print("Selected Path Coordinates:")
    for _, (x, y) in optimal_path:
        print(f"{x + 1}, {y + 1}")
    print(final_time * 1000, "ms")
    
    save_option = input("Do you want to save the results to a text file? (yes/no): ").lower()
    if save_option == 'yes':
        save_results(max_points, optimal_path, final_time)
    else:
        clear_terminal()

if __name__ == "__main__":
    main()