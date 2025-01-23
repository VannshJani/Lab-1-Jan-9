'''
This code is used to create an animation of a sudoku being solved.
'''
import matplotlib.pyplot as plt # type: ignore
import matplotlib.animation as animation # type: ignore

test_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
total_boards = []

def is_valid(board, row, col, num):
    '''
    Check if the number can be placed in the cell
    '''
    for i in range(9):
        if num in (board[row][i], board[i][col]):
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_mrv(board):
    '''
    Find the cell with the minimum remaining values
    '''
    min_count = 10
    mrv_position = (-1, -1)
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                count = sum(is_valid(board, row, col, num) for num in range(1, 10))
                if count < min_count:
                    min_count = count
                    mrv_position = (row, col)

    # print("MRV Position:", mrv_position)
    return mrv_position

def solve_sudoku(board):
    '''
    Solve the Sudoku board using backtracking
    '''
    total_boards.append([row[:] for row in board])
    empty = find_mrv(board)
    if empty == (-1, -1):
        return True

    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def print_board(board):
    '''
    Print the Sudoku board
    '''
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

if solve_sudoku(test_board):
    print("Solved Sudoku Board:")
    print_board(test_board)
    print("Number of boards:", len(total_boards))
else:
    print("No solution exists.")


def animate_sudoku(all_boards):
    '''
    Function to animate the Sudoku board
    '''
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.set_xticks([i + 0.5 for i in range(9)], minor=True)
        ax.set_yticks([i + 0.5 for i in range(9)], minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        ax.imshow([[5]*9]*9, cmap="Blues", vmin=0, vmax=9)
        for i in range(9):
            for j in range(9):
                num = all_boards[frame][i][j]
                if num != 0:
                    ax.text(j, i, str(num), ha="center", va="center", color="black")
        ax.set_xticks([])
        ax.set_yticks([])

    ani = animation.FuncAnimation(fig, update, frames=len(all_boards), interval=500, repeat=False)
    ani.save("sudoku_animation.gif", writer="imagemagick")
    plt.show()

animate_sudoku(total_boards)
