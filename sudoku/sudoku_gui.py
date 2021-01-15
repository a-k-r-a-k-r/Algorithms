from tkinter import *
import time

# --- TO DO:
#
# - put play mode and solve on the same board
# - reset stops solver
# - empty play board before solving
# - add color for play mode (check vs board of vs solved?)
# - modif mode for creating a board to solve
# - no solution exists


class Sudo_App(Frame):
    def __init__(self, board, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.board = board
        self.starting_board = []
        self.modified_board = \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        for line in self.board:
            self.starting_board.append(line)

        self.board_frame = None
        self.button_frame = None
        self.empty_pos = []
        self.string_vars = []
        self.pos_entry = []
        self.start_gui()

    # --- GUI functions ---
    def start_gui(self):

        # Frame inside main one where board is displayed
        self.board_frame = Frame(self, borderwidth=2, relief=SUNKEN, bg='black')
        self.board_frame.grid(padx=10, pady=(10, 0), row=1)

        # Frame inside main one where buttons are displayed
        self.button_frame = Frame(self)
        self.button_frame.grid(row=2)

        # Buttons for button_frame
        button_solve = Button(self.button_frame, text='Solve board', relief=RAISED, width=10, command=self.solve_gui)
        button_solve.grid(row=1, column=1, padx=20, pady=10)

        button_restart = Button(self.button_frame, text='↺', relief=RAISED, width=5, command=self.reset_board)
        button_restart.grid(row=1, column=2, padx=10, pady=10)

        button_modify = Button(self.button_frame, text='Create grid', relief=RAISED, width=10, command=self.board_creator)
        button_modify.grid(row=1, column=3, padx=10, pady=10)

        # Create a label for each element in board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    num = ' '
                    elt = len(self.string_vars)
                    self.string_vars.append(StringVar())
                    self.pos_entry.append((i,j))

                    label = Entry(self.board_frame, text=num, justify='center', width=4, bd=0, bg='white',
                                  textvariable=self.string_vars[elt],
                                  validate='focus')
                    label.grid(row=i, column=j, padx=1, pady=1, ipady=9, ipadx=4)

                    self.string_vars[elt].trace("w", lambda name, index, mode, var=self.string_vars,
                                                           elt=elt: self.entry_update(var, elt))

                else:
                    num = self.board[i][j]
                    label = Label(self.board_frame, text=num, width=4, height=2, bg='lavender')
                    label.grid(row=i, column=j, padx=1, pady=1)

                if i % 3 == 0 and i != 0:  # Add a bigger line after third and sixth row
                    label.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:  # Add a bigger line after third and sixth column
                    label.grid(padx=(3, 1))

    def solve_gui(self):
        self.reset_board()

        # Create a label for each element in board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    num = " "
                    color = 'white'
                else:
                    num = self.board[i][j]
                    color = 'lavender'

                label = Label(self.board_frame, text=num, width=4, height=2, bg=color)
                label.grid(row=i, column=j, padx=1, pady=1)

                if i % 3 == 0 and i != 0:  # Add a bigger line after third and sixth row
                    label.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:  # Add a bigger line after third and sixth column
                    label.grid(padx=(3, 1))

        self.solve_board()
        time.sleep (0.2)
        for pos in self.empty_pos:
            label = self.board_frame.grid_slaves(int(pos[0]), int(pos[1]))
            label[0].config(bg='green')

    def reset_board(self):
        Frame.destroy(self)
        for pos in self.empty_pos:
            self.board[pos[0]][pos[1]] = 0
        self.__init__(self.starting_board)

    def update_gui(self, pos, i, color):
        if color == 'red': i = " "
        label = self.board_frame.grid_slaves(pos[0], pos[1])
        label[0].config(text=i, bg=color)
        time.sleep(0.001)

    # --- Board creator functions ---
    def board_creator(self):
        Frame.destroy (self)
        for pos in self.empty_pos:
            self.board[pos[0]][pos[1]] = 0
        self.__init__ (self.modified_board)

        self.button_frame.grid_slaves()[0].config(text='Done', command= self.modify_board)

    def modify_board(self):
        Frame.destroy (self)
        for pos in self.empty_pos:
            self.board[pos[0]][pos[1]] = 0
        self.__init__ (self.modified_board)

    # --- Sudoku solve functions ---
    def solve_board(self):
        pos = self.find_next_0()

        if not pos:
            return True

        for i in range(1, 10):
            if self.possible(pos, i):
                self.board[pos[0]][pos[1]] = i

                if self.solve_board():
                    return True

                self.board[pos[0]][pos[1]] = 0

        return False

    def find_next_0(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.empty_pos.append((i, j))
                    return i, j  # Return row and column of the first zero found

        return None

    def possible(self, pos, num):
        list_impossible = []
        for i in range(pos[0] // 3 * 3, pos[0] // 3 * 3 + 3):
            for j in range(pos[1] // 3 * 3, pos[1] // 3 * 3 + 3):
                list_impossible.append((self.board[i][j]))  # add number of each position in square

        for i in range(len(self.board)):
            list_impossible.append(self.board[pos[0]][i])  # add number of each position in row
            list_impossible.append(self.board[i][pos[1]])  # add number of each position in column

        if num not in list_impossible:

            self.update_gui(pos, num, color='yellow')
            self.update()
            return True

        self.update_gui(pos, num, color='red')
        self.update()

        return False

    # --- Sudoku play functions

    # get solved sudoku

    # when input display red or green color
    def entry_update(self, sv, elt):
        pos = self.pos_entry[elt]
        label = self.board_frame.grid_slaves(pos[0], pos[1])


        try:
            num = int(sv[elt].get())
        except ValueError:
            label[0].config(bg='white')
            sv[elt].set('')
            self.modified_board[pos[0]][pos[1]] = 0
            self.board[pos[0]][pos[1]] = 0

        else:
            if self.play_possible(pos, num):
                color = 'green'
            else:
                color = 'red'

            if self.button_frame.grid_slaves()[0]['text'] == 'Done':
                self.modified_board[pos[0]][pos[1]] = num

            else:
                self.board[pos[0]][pos[1]] = num


            label[0].config(bg=color)
            sv[elt].set(num)
            self.starting_board[pos[0]][pos[1]] = 0

    def play_possible(self, pos, num):

        if self.button_frame.grid_slaves ()[0]['text'] == 'Done':
            board = self.modified_board

        else:
            board = self.board

        list_impossible = []
        for i in range (pos[0] // 3 * 3, pos[0] // 3 * 3 + 3):
            for j in range (pos[1] // 3 * 3, pos[1] // 3 * 3 + 3):
                list_impossible.append ((board[i][j]))  # add number of each position in square

        for i in range(len(board)):
            list_impossible.append(board[pos[0]][i])  # add number of each position in row
            list_impossible.append(board[i][pos[1]])  # add number of each position in column

        if num not in list_impossible:
            return True

        return False


if __name__ == '__main__':
    board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
             [5, 2, 0, 0, 0, 0, 0, 0, 0],
             [0, 8, 7, 0, 0, 0, 0, 3, 1],
             [0, 0, 3, 0, 1, 0, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 0, 6, 0, 0],
             [1, 3, 0, 0, 0, 0, 2, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    root = Tk()
    app = Sudo_App(board, master=root)
    app.mainloop()
    root.destroy()

    # print_board(board)
    #
    # if solve_board(board):
    #     print('\n\n')
    #     print_board(board)
    #
    # else:
    #     print('No solution exists for this board')