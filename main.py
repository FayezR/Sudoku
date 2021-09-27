import numpy as np
from colorama import Back, Fore, Style
from collections import Counter


# Function checks whether sudoku board is valid (each row,col,sub-grid meets constraints)
def is_valid_board(sudoku):
    subgrids = split_into_subgrids(sudoku)

    for i in range(9):
        duplicates_row = [x for x, c in Counter(sudoku[i, :]).items() if c > 1]
        duplicates_col = [x for x, c in Counter(sudoku[:, i]).items() if c > 1]
        duplicates_3x3 = [x for x, c in Counter(subgrids[i]).items() if c > 1]

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


# Function checks whether a number can put be in a cell on the sudoku board
def is_valid_move(grid, row, col, n):
    s_row = (row // 3) * 3
    s_col = (col // 3) * 3

    for i in range(0, 9):
        # checks a row for presence of n
        if grid[row, i] == n:
            return False

        # checks a column for presence of n
        if grid[i, col] == n:
            return False

        # checks 3x3 sub-grid for presence of n
        if grid[s_row + (i // 3), s_col + (i % 3)] == n:
            return False
    return True


def possible_candidates(board, row, col):
    s_row = (row // 3) * 3
    s_col = (col // 3) * 3
    num = set(range(10))

    used_row_digits = set(board[row, :])
    used_col_digits = set(board[:, col])
    used_3x3_digits = set()
    for i in range(9):
        used_3x3_digits.add(board[s_row + (i // 3), s_col + (i % 3)])

    unused_row_digits = used_row_digits.symmetric_difference(num)
    unused_col_digits = used_col_digits.symmetric_difference(num)
    unused_3x3_digits = used_3x3_digits.symmetric_difference(num)

    unused_digits = (unused_col_digits.intersection(unused_row_digits, unused_3x3_digits))

    # print(f"Used row digits: {used_row_digits}")
    # print(f"unused row digits: {unused_row_digits}\n")
    # print(f"Used col digits: {used_col_digits}")
    # print(f"unused col digits: {unused_col_digits}\n")
    # print(f"Used 3x3 digits: {used_3x3_digits}")
    # print(f"Unused 3x3 digits: {unused_3x3_digits}")
    # print(f"Unused: {unused_digits}")

    return unused_digits


def make_move(board):
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                candidates = possible_candidates(board, row, col)
                for num in candidates:
                    if is_valid_move(board, row, col, num):
                        board[row, col] = num
                        if make_move(board):
                            return True
                        board[row, col] = 0
                return False
    return True


# Returns a sudoku board with all cells filled with -1
def invalid_board_marker(sudoku):
    sudoku[sudoku >= 0] = -1
    return sudoku


def sudoku_solver(sudoku):
    if is_valid_board(sudoku):
        if make_move(sudoku):
            return sudoku
        else:
            return invalid_board_marker(sudoku)
    else:
        return invalid_board_marker(sudoku)


def tests():
    import time
    difficulties = ['hard']

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


if __name__ == '__main__':

    def get_input():
        x = input(f"{Back.WHITE}{Fore.BLACK} Welcome! Please choose an option from the menu:"
                  f"\n1. Test code against all the tests"
                  f"\n2. Run custom code"
                  f"\n3. Test code against hard sudoku puzzles"
                  f"\n0. Exit"
                  f"\n{Back.CYAN}{Fore.BLACK}Your input -> {Style.RESET_ALL}")

        # Run all tests
        if x == "1":
            tests()
            get_input()

        if x == "2":
            # load puzzle to test
            sudoku = np.load("data/medium_puzzle.npy")
            print(f"Board {5} - medium_puzzle:\n {sudoku[5].copy()} \n")

            # Get subgrids of board
            print("Here are the subgrids of this board: \n")
            print(split_into_subgrids(sudoku[5].copy()))

            # checks for validity of board
            print(f"Board Valid? :  {is_valid_board(sudoku[5].copy())}")

            # solves board
            print(sudoku_solver(sudoku[5].copy()))

            get_input()

        # Test multiple sudokus
        if x == "3":
            sudoku = np.load("data/hard_puzzle.npy")
            print(f"Board {0} - hard_puzzle:\n {sudoku[0].copy()} \n")
            print(possible_candidates(sudoku[0].copy(), 0, 0))

            get_input()

        if x == "0":
            print("you have exited the program!")
            exit(0)


    get_input()
