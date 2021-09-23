import numpy as np
from colorama import Back, Fore, Style
from collections import Counter

SKIP_TESTS = True

def sudoku_solver(sudoku):
    return False


def is_valid_board(sudoku):
    subgrids = split_into_subgrids(sudoku)

    for i in range(9):
        duplicates_row = [item for item, c in Counter(sudoku[i, :]).items() if c > 1]
        duplicates_col = [item for item, c in Counter(sudoku[:, i]).items() if c > 1]
        duplicates_3x3 = [item for item, c in Counter(subgrids[i]).items() if c > 1]

        # Checks rows for duplicates
        if len(np.unique(sudoku[i, :])) < 9:
            if 0 in duplicates_row:
                return True
            else:
                return False

        # Checks columns for duplicates
        if len(np.unique(sudoku[:, i])) < 9:
            if 0 in duplicates_col:
                return True
            else:
                return False

            # Checks 3x3 for duplicates
        if len(np.unique(subgrids[i])) < 9:
            if 0 in duplicates_3x3:
                return True
            else:
                return False
    return True


# Function divides sudoku board into 3x3 subgrids, from top-left to bottom right
def split_into_subgrids(sudoku):
    subgrids = []
    for box_row in range(3):
        for box_col in range(3):
            subgrid = []
            for row in range(3):
                for col in range(3):
                    subgrid.append(sudoku[3 * box_row + row][3 * box_col + col])
            subgrids.append(subgrid)
    return np.array(subgrids)


def is_valid_move(grid, row, col, n):
    # variables used to check presence of n in 3x3 square
    s_row = (row // 3) * 3
    s_col = (col // 3) * 3

    for i in range(0, 9):
        # checks a row for presence of n
        if grid[row, i] == n:
            return False

        # checks a column for presence of n
        if grid[i, col] == n:
            return False

        # checks 3x3 square for presence of n
        if grid[s_row + (i // 3), s_col + (i % 3)] == n:
            return False
    return True


def make_move(board):
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row, col] = num

                        # Trouble shooting code

                        # print("\n")
                        # print(board)

                        if make_move(board):
                            return True
                        board[row, col] == 0
                return False
    return True


def tests():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"{Back.BLACK}{Fore.WHITE}This is {difficulty} sudoku number ", i, f"{Style.RESET_ALL}")
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print("\n")
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            # print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print(f"{Back.GREEN} Yes! Correct solution.{Style.RESET_ALL}")
                count += 1
            else:
                print(f"{Back.RED}+ No, the correct solution is: {Style.RESET_ALL}")
                print(solutions[i])

            print(f" {Fore.CYAN}This sudoku took", end_time - start_time, f"seconds to solve.\n {Style.RESET_ALL}")

        print(f"{Fore.BLACK}{Back.YELLOW}{count}/{len(sudokus)} {difficulty} sudokus correct {Style.RESET_ALL}")
        if count < len(sudokus):
            break


if not SKIP_TESTS:
    tests()

if __name__ == '__main__':
    def get_input():
        x = input(f"{Back.CYAN}{Fore.BLACK}Choose 1 to run tests or 2 to run main: \n"
                  f"Your input: {Style.RESET_ALL}")

        # Run all tests
        if x == "1":
            tests()
            get_input()

