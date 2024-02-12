import itertools
import time
import random
import os
import sys

def read_file(filename):
    with open(filename, 'r') as file:
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

def manual_input():
    buffer_size = int(input("Enter buffer size: "))
    rows, cols = map(int, input("Enter matrix size (rows cols): ").split())
    matrix = [list(input().split()) for _ in range(rows)]
    
    num_seqs = int(input("Enter the number of sequences: "))
    sequences = [input().strip().split() for _ in range(num_seqs)]
    points = [int(input()) for _ in range(num_seqs)]

    return buffer_size, matrix, sequences, points

def find_all_patterns(matrix, step):
    rows, cols = len(matrix), len(matrix[0])
    all_paths = []

    for indices in itertools.product(range(cols), range(rows)):
        x, y = indices
        path = []
        visited = []

        def generate_paths(x, y, steps):
            if steps == 0:
                all_paths.append(path.copy())
                return
            visited.append((x, y))
            path.append((matrix[y][x], (x, y)))

            for dx, dy in [(0, 1), (1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < cols and 0 <= next_y < rows and (next_x, next_y) not in visited:
                    generate_paths(next_x, next_y, steps - 1)

            visited.pop()
            path.pop()

        generate_paths(x, y, step)

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

def optimal_pattern(matrix, buffer_size, sequences, points):
    max_points = float('-inf')
    optimal_path = []

    all_paths = find_all_patterns(matrix, buffer_size)
    for path in all_paths:
        path_reward = calculate_point(matrix, path, sequences, points)
        if path_reward > max_points:
            max_points = path_reward
            optimal_path = path

    return max_points, optimal_path

def save_results(max_points, optimal_path, final_time):
    filename = input("Enter the filename to save the results: ")
    with open(filename, 'w') as file:
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