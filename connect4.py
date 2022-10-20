import random
import math
from typing import List, Tuple

'''
NOTE 1: The `board` list that represents board state will have 7 * c elements,
        where `c` is the number of columns.

        The first 7 elements in the list represent the **bottom** row of the board,
        the next 7 represent the row above it, and so on.

NOTE 2: Since all functions are immutable/have no side effects, this should be a
        purely functional solution, i.e. no global mutable variables are required.
'''

# Enumerating player color and number.
# Yellow goes first.
YELLOW = 1
RED = 2

COLS = 7 # There's always 7 columns according to implementation notes.

def check_move(board: List[int], turn: int, col: int, pop: bool) -> bool:
    '''
    Checks if a certain move is valid given a `board` state. Returns whether or not move is valid.

    ### Arguments
        - `board`: the board state
        - `turn`: which player makes this move
        - `col`: the column to drop/pop the piece. This is zero-indexed (first col is 0).
        - `pop`: `True` if pop, `False` if drop
    
    ### Returns
        `True` if move is valid, `False` otherwise
    '''
    return True

def apply_move(board: List[int], turn: int, col: int, pop: bool) -> List[int]:
    '''
    Applies a given move to the board. Returns the new board state.

    This is an **immutable** function with NO SIDE EFFECTS, i.e. the list
    referred to by the `board` variable is not modified.

    ### Arguments
        - `board`: the board state
        - `turn`: which player makes this move
        - `col`: the column to drop/pop the piece. This is zero-indexed (first col is 0).
        - `pop`: `True` if pop, `False` if drop

    ### Returns
        The new board state (list of ints)
    '''
    return board.copy()

def check_victory(board: List[int], who_played: int) -> int:
    '''
    Checks if a player has won the game. Returns the player who won, or 0 if no one has won.

    ||----------------------------------------------------------------------------------||
    ||NOTE: According to telegram chat, if some player somehow makes a move such that   ||
    ||the board would be in a winning position for BOTH players (e.g. via a pop move),  ||
    ||the player that made the move LOSES.                                              ||
    ||----------------------------------------------------------------------------------||

    ### Arguments
        - `board`: the board state
        - `who_played`: the player who just made a move

    ### Returns
        The player number of the player who won, or 0 if no one has won.
        If the board is in a position that is winning for both players, then return
        the OPPONENT player. The player who just made such a move loses.

        I.e. you lose if you make a move that would win the game for your opponent, even
        if it is also winning for yourself.
    '''

    # NOTE: these two have to be separate variables as we have to consider
    #       the case where both players win and we have to confer the win to the
    #       opponent of `who_played`.
    #
    #       this also means we cannot do early termination unless we reach a case where
    #       both players wins, then the result is fully certain.
    yellow_wins = False
    red_wins = False
    num_rows = len(board) // COLS

    # Check horizontals (left to right)
    for row in range(num_rows):
        # Check if there are 4 consecutive pieces of the same color
        # in a row.

        streak_piece = 0 # the current player number which has N pieces in a row. 0 means no player.
        index_of_streak_start = 0 # the beginning index of the N pieces in a row

        for col in range(COLS):
            piece = board[row * 7 + col]
            if piece != streak_piece: # streak is broken
                if streak_piece != 0 and col - index_of_streak_start + 1 == 4:
                    if streak_piece == YELLOW:
                        yellow_wins = True
                    elif streak_piece == RED: # redundant elif, but here for future-proofing multiplayers if needed.
                        red_wins = True
                index_of_streak_start = col # reset streak index
                streak_piece = piece
        
        # Check if row ended with a winning streak:
        if streak_piece != 0 and 6 + 1 - index_of_streak_start == 4:
            if streak_piece == YELLOW:
                yellow_wins = True
            elif streak_piece == RED:
                red_wins = True
    
    # Checking verticals and diagonals only make sense if num_rows >= 4
    if num_rows >= 4:
        # Check verticals (bottom to top)
        for col in range(COLS):
            # Check if there are 4 consecutive pieces of the same color
            # in a column.

            streak_piece = 0
            index_of_streak_start = 0

            for row in range(num_rows):
                piece = board[row * 7 + col]
                if piece != streak_piece:
                    if streak_piece != 0 and row - index_of_streak_start + 1 == 4:
                        if streak_piece == YELLOW:
                            yellow_wins = True
                        elif streak_piece == RED:
                            red_wins = True
                    index_of_streak_start = row
                    streak_piece = piece

            # Check if end of column has a winning streak:
            if streak_piece != 0 and 5 + 1 - index_of_streak_start == 4:
                if streak_piece == YELLOW:
                    yellow_wins = True
                elif streak_piece == RED:
                    red_wins = True

        # Check up-left diagonals (bottom-right to top-left)
        
        # contains all starting bottom-right points such that diagonals have at least
        # 4 pieces in them.
        starting_coords = [(0, x) for x in range(3, COLS)]
        starting_coords += [(x, COLS - 1) for x in range(1, num_rows - 3)]

        # traverse one diagonal at a time from the above starting points
        for row, col in starting_coords:
            streak_piece = 0
            index_of_streak_start = 0
            diagonal_idx = 0 # The (n+1)th piece of the current diagonal

            while row + diagonal_idx < num_rows and col - diagonal_idx >= 0:
                piece = board[(row + diagonal_idx) * 7 + col - diagonal_idx]
                if piece != streak_piece:
                    if streak_piece != 0 and diagonal_idx - index_of_streak_start + 1 == 4:
                        if streak_piece == YELLOW:
                            yellow_wins = True
                        elif streak_piece == RED:
                            red_wins = True
                    index_of_streak_start = diagonal_idx
                    streak_piece = piece
                diagonal_idx += 1

            # Check if the last few pieces are a winning streak:
            if streak_piece != 0 and num_rows - row - index_of_streak_start == 4:
                if streak_piece == YELLOW:
                    yellow_wins = True
                elif streak_piece == RED:
                    red_wins = True

        # Check up-right diagonals (top-right to bottom-left)

        # similar to above, contains all starting bottom-left points such that diagonals have at least
        # 4 pieces in them.

        starting_coords = [(0, x) for x in range(COLS - 4, -1, -1)]
        starting_coords += [(x, 0) for x in range(1, num_rows - 3)]

        for row, col in starting_coords:
            streak_piece = 0
            index_of_streak_start = 0
            diagonal_idx = 0

            while row + diagonal_idx < num_rows and col + diagonal_idx < COLS:
                piece = board[(row + diagonal_idx) * 7 + col + diagonal_idx]
                if piece != streak_piece:
                    if streak_piece != 0 and diagonal_idx - index_of_streak_start + 1 == 4:
                        if streak_piece == YELLOW:
                            yellow_wins = True
                        elif streak_piece == RED:
                            red_wins = True
                    index_of_streak_start = diagonal_idx
                    streak_piece = piece
                diagonal_idx += 1

            # Check if the last few pieces are a winning streak:
            if streak_piece != 0 and num_rows - row - index_of_streak_start == 4:
                if streak_piece == YELLOW:
                    yellow_wins = True
                elif streak_piece == RED:
                    red_wins = True

    if yellow_wins and red_wins:
        # returns the opponent of `who_played`, if 2 => 1, if 1 => 2.
        # XXX: This won't work for >= 3 player mode
        return 3 - who_played
    elif yellow_wins:
        return YELLOW
    elif red_wins:
        return RED
    
    return 0

def computer_move(board: List[int], turn: int, level: int) -> Tuple[int, bool]:
    '''
    Evaluates the 'best' move to make for a given `turn` (i.e. player), depending on `level` of
    difficulty and `board` state.

    ### Arguments
        - `board`: the board state
        - `turn`: the player number of which the computer is supposed to make a move for.
        - `level`: the difficulty level of the computer.
            - 1: Trivial. 

    ### Returns
        A tuple of the form `(col, pop)`, where `col` is the column to drop/pop the piece,
        and `pop` is `True` if pop, `False` if drop.
    '''
    return (0,False)
    
def display_board(board: List[int]):
    '''
    Takes in the board state and displays it by any means.
    '''
    pass

def menu():
    '''
    Game menu. 
    
    User to select between PvP or PvAI.

    -----
    
    If PvP, implementation is straightforward.

    1. `display_board()`

    2. Allow player 1 to make a move.

    3. Go through move-making subroutine
        - Sanitize the input, make sure column is not out of bounds, 
          and that a truthy/falseyy value is given for `pop`.
        - Check if move is valid using `check_move()`.
        - If neither of the above passed, ask for input again.
        - Retrieve the move to make
    
    4. Apply the obtained move using `apply_move()`

    5. Repeat the 1-4 for player 2, then alternate between the 2 players, 
      until `check_victory()` returns a non-zero value.

    -----

    If PvAI, user is prompted to select difficulty level, 
    and choose whether or not player or computer goes first.

    1. `display_board()`
    2. Allow player/computer to make a move.
    3. If computer's turn, evaluate `computer_move()` to obtain the best move to make.
    4. If player's turn, go through move-making subroutine to obtain move from player.
    5. Apply the obtained move using `apply_move()`
    6. Repeat 1-5 until `check_victory()` returns a non-zero value.
    '''
    pass

if __name__ == "__main__":
    menu()
    print("Hello World")
