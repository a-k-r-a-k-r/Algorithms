# Sudoku solver

A GUI application made with tkinter to visualize the solving of a sudoku grid, using a backtracking algorithm.

### Backtracking
[From wikipedia:](https://en.wikipedia.org/wiki/Backtracking)

> Backtracking is a general algorithm for finding all (or some) solutions to some computational problems, notably constraint satisfaction problems, that incrementally builds candidates  to the solutions, and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution.

### Utilisation
> python \PATH_TO_FILE\sudoku_gui.py

Click 'solve board' to start the visualization with the prebuilt sudoku grid. You can also create a new grid from scratch ('Create grid'), enter a few numbers if you want and then solve it when you are done.

### Screenshots

* Initial board:

![initial_grid](https://user-images.githubusercontent.com/69766734/105037870-eb894680-5a5e-11eb-9cbc-c0330bb1e61c.png)

* Solving:
Here the algorithm is backtracking from the cell circled in black to the one circled in green, which is the first number that makes the board unsolvable as-is. The next possible number will be tried and the program will continue to try this solution for the following cells.

![solving](https://user-images.githubusercontent.com/69766734/105037872-ec21dd00-5a5e-11eb-81d4-b592851d7d7d.png)

* Solution:

![solved](https://user-images.githubusercontent.com/69766734/105037871-ec21dd00-5a5e-11eb-9845-564b451eefa2.png)
