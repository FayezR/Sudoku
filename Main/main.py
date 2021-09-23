import numpy as np
from colorama import Back, Fore, Style
from collections import Counter

SKIP_TESTS = True

def sudoku_solver(sudoku):
    return False


def is_valid_board(sudoku):
    for i in range(9):
        duplicates_row = [item for item, c in Counter(sudoku[i, :]).items() if c > 1]
        duplicates_col = [item for item, c in Counter(sudoku[:, i]).items() if c > 1]

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

