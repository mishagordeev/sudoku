from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_full_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_diagonal_squares(board)
    solve_sudoku(board)
    return board

def fill_diagonal_squares(board):
    for i in range(0, 9, 3):
        fill_square(board, i, i)

def fill_square(board, row, col):
    nums = random.sample(range(1, 10), 9)
    index = 0
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums[index]
            index += 1

def remove_numbers(board, num_holes):
    count = num_holes
    while count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            count -= 1

def generate_sudoku(board, num_holes=2):
    # board = generate_full_sudoku()
    remove_numbers(board, num_holes)
    return board

@app.route('/')
def index():
    
    solved_board = generate_full_sudoku() 
    solved_board_copy = [row[:] for row in solved_board]
    remove_numbers(solved_board_copy,10)
    sudoku_board = solved_board_copy
    return render_template('index.html', sudoku_board=sudoku_board, solved_board=solved_board)

if __name__ == '__main__':
    app.run(debug=True)
