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

    num_empty = 9
    
    for row in board:
        num_empty -= sum(item is not EMPTY for item in row)
        
    if num_empty == 0:
        next_player = None
    elif num_empty%2 == 0:
        next_player = O 
    else:
        next_player = X
    
    return next_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves = set()
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] is EMPTY:
                possible_moves.add((i,j))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i,j = action
    if board[i][j] is not EMPTY:
        raise NameError('NotValidAction')
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if (board[1][1] == board[0][0] == board[2][2]) or \
    (board[1][1] == board[0][1] == board[2][1]) or \
    (board[1][1] == board[0][2] == board[2][0]) or \
    (board[1][1] == board[1][0] == board[1][2]):
        winner = board[1][1]
    elif (board[0][0] == board[1][0] == board[2][0]) or \
    (board[0][0] == board[0][1] == board[0][2]):
        winner = board[0][0]
    elif (board[2][2] == board[2][1] == board[2][0]) or \
    (board[2][2] == board[1][2] == board[0][2]):
        winner = board[2][2]
    else:
        winner = None
        
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    terminal = (winner(board) is not None) or (player(board) is None)
    
    return terminal


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == X:
        util = 1
    elif winner(board) == O:
        util = -1
    else:
        util = 0
    
    return util


def score(board, alpha, beta):
    """
    Returns the end score for the current player on the board.
    """
    if terminal(board) == True:
        return utility(board)
    
    if player(board) == X:
        best_value = -float('inf')
        for action in actions(board):
            new_board = result(board, action)
            value = score(new_board, alpha, beta)
            best_value = max(value, best_value )
            alpha = max(best_value, alpha)
            if beta <= alpha:
                break
        return best_value

    if player(board) == O:
        best_value = float('inf')
        for action in actions(board):
            new_board = result(board, action)
            value = score(new_board, alpha, beta)
            best_value = min(value, best_value)
            beta = min(best_value, beta)
            if beta <= alpha:
                break
        return best_value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    
    best_action = None
    alpha = -float('inf')
    beta = float('inf')
    
    if player(board) == X:
        best_value = -float('inf')
        for action in actions(board):
            new_board = result(board, action)
            v = score(new_board,alpha,beta)
            if v > best_value:
                best_action = action
                best_value = v
        return best_action

    if player(board) == O:
        best_value = float('inf')
        for action in actions(board):
            new_board = result(board, action)
            v = score(new_board,alpha, beta)
            if v < best_value:
                best_action = action
                best_value = v
                
        return best_action