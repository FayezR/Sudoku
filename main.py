import numpy as np
from colorama import Back, Fore, Style
from collections import Counter


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


# Function finds a single empty cell in a 3x3 subgrid
def find_single_cell(sudoku):
    arr = split_into_subgrids(sudoku)
    for i in range(9):
        if len(np.unique(arr[i, :])) == 9:
            for j in range(9):
                if arr[i, j] == 0:

                    box_row = j
                    box_col = i
                    # row=
                    #             for col in range(3):
                    #                 i = box_row//3 + row
                    #                 j = box_col//3 - col
                    # return True, i, j


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
    # if find_single_cell(board):
    #     bool, row, col = find_single_cell(board)
    #     for num in range(1, 10):
    #         if is_valid_move(board, row, col, num):
    #             board[row, col] = num
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


if __name__ == '__main__':
    print


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
            sudoku = np.load("data/easy_puzzle.npy")
            board = sudoku.copy()
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
            for i in range(15):
                # load puzzle to test
                sudoku = np.load("data/hard_puzzle.npy")
                board = sudoku.copy()
                print(f"Board {i} - hard puzzle:\n {board[i]} \n")

                # checks for validity of board
                print(f"Board Valid? :  {is_valid_board(board[i])}")

                # solves board
                print(sudoku_solver(board[i]))
            get_input()

        if x == "0":
            print("you have exited the program!")
            exit(0)


    get_input()
