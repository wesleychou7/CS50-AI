"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1

    # terminal state            
    if x_count == 5 and o_count == 4:
        return None

    if x_count > o_count:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.add((i,j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    board2 = copy.deepcopy(board)

    i = action[0]
    j = action[1]

    if board2[i][j] is None:
        if current_player == "X":
            board2[i][j] = "X"
        elif current_player == "O":
            board2[i][j] = "O"
        return board2

    raise RuntimeError("Invalid action.")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x_count = 0
    o_count = 0

    # check rows
    for row in board:
        if row[0] == row[1] and row[1] == row[2]:
            return row[0]

    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]

    # check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell is None:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    return 0


def max_value(board):

    v = -999
    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):

    v = 999
    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    moves = {}

    if player(board) == "X":
        for action in actions(board):
            moves[action] = min_value(result(board, action))
        print(moves)
        return max(moves, key=moves.get)

    if player(board) == "O":
        for action in actions(board):
            moves[action] = max_value(result(board, action))
        print(moves)
        return min(moves, key=moves.get)














