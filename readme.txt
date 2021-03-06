This is python program is an algorithm to solve sudoku puzzles. This is a graded assingment as part of my Masters in Computer Science - Artificial intelligence module.

-------

The agent that I have implemented is a backtracking depth-first search algorithm. I have chosen to implement this type of algorithm as it is best suited in solving a puzzle like sudoku. This is because a sudoku board has constraints on the positioning of a number in the grid, much like the eight-queens puzzle. These constraints help define states that are valid, eventually leading to a goal state.  The algorithm uses these constraints to test numbers by inserting them into an empty cell. This is in contrast to an uninformed search in which no additional information is used in traversing the search tree. 

I have chosen to implement a depth-first as opposed to a breadth-first search algorithm as it has a lower space complexity. This is because depth-first search offers ability to disregard previously explored nodes, once all the children of a node is explored and expanded.

Code explanation:

A helper function first looks to check if a sudoku board is valid by splicing each row, column and 3x3 grid as separate numpy arrays, and thereafter checking for duplicate values. This is based on the constraint Ð rows, columns and 3x3 grids must only contain one occurrence of a number between 1 and 9.  The function has been programmed to ignore duplicate values of Ô0Õ as these are the empty cells and it is expected that a sudoku board will have more than one empty cell in a given row, column or  3x3 grid.

Once the validity of a sudoku board has been determined, the algorithm begins to solve the sudoku board. A helper function locates an empty cell, and a series of values from 1-9 are tried in this empty cell and the validity of the placement checked by another helper function. If this new state with the addition of the number is consistent (conforms to the constraints), the number is placed, and the state updated. If later on, a state is encountered that is not consistent, the algorithm backtracks and tries placing another number in the cell. This function loops and continues to fill in the board until no empty cell is left. 

