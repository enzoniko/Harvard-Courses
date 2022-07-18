"""
Tic Tac Toe Player
"""

import math
import random
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

def getSpacesInfo(board):

    # Start with vars to count the empty spaces number in the board and the positions of them
    # Start with a var that counts the filled spaces positions too
    empty_spaces_number = 0
    empty_spaces_positions = []
    filled_spaces_positions = []

    # Loop through each cell in the board and if the cell is empty increment empty_spaces var and add its position to the empty_spaces_positions List
    # If the cell isn't empty add its position to the filled_spaces_positions list
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                empty_spaces_number += 1
                empty_spaces_positions.append((row, cell))
            else:
                filled_spaces_positions.append((row, cell))


    # Returns a List with the number of empty spaces in the first element, each empty position in the second element
    # and each filled position in the third element
    return [empty_spaces_number, empty_spaces_positions, filled_spaces_positions]

def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Get the number of empty spaces in the board
    empty_spaces_number = getSpacesInfo(board)[0]
    # If the number of empty spaces is odd it's X's turn, else it's O's turn
    return O if empty_spaces_number % 2 == 0 else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Get the positions of the empty spaces in the board (A List of tuples(row, cell))
    empty_spaces_positions = getSpacesInfo(board)[1]

    # Returns a set of empty spaces positions
    return set(empty_spaces_positions)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception

    # Make a deep copy of the original input board
    new_board = copy.deepcopy(board)

    # Apply the input action to the deep copied board
    new_board[action[0]][action[1]] = player(board)

    # Return it
    return new_board        
    

def checkForMacthes(filled_spaces_positions):

    # If the legth of the list received (filled spaces positions) is greater or equal to 3 (it's possible to match 3)
    if len(filled_spaces_positions) < 3:
        return False
    # First option for calculating matches(longest):
    """
        # Horizontal and vertical count var
        rowAndCell = 0

        # Main diagonal and secondary diagonal position to compare later
        main_diagonal = [(0, 0), (1, 1), (2, 2)]
        secondary_diagonal = [(2, 0), (1, 1), (0, 2)]

        # Item count to iterate over filled spaces positions list
        item = 0

        # Vars for filled spaces that are in the same row, cell, main diagonal or secondary diagonal
        filled_spaces_in_same_row = 0
        filled_spaces_in_same_cell = 0
        filled_spaces_in_main_diagonal = 0
        filled_spaces_in_secondary_diagonal = 0

        # Loop through each row and cell (0, 1, 2) trying to find horizontal or vertical matches
        while rowAndCell < 3:

            # Loop through each item in the list
            while item < len(filled_spaces_positions):

                # If the item's row is the same as the row we are checking increment the var for filled spaces in the same row
                if filled_spaces_positions[item][0] == rowAndCell:
                    filled_spaces_in_same_row += 1

                # If the item's cell is the same as the cell we are checking increment the var for filled spaces in the same cell
                if filled_spaces_positions[item][1] == rowAndCell:
                    filled_spaces_in_same_cell += 1

                # Check in the next item
                item += 1
            
            # If the var for filled spaces in the same row or cell is 3 return True(victory)
            if filled_spaces_in_same_row == 3 or filled_spaces_in_same_cell == 3:
                return True
            
            # Else, reset item and filled spaces vars and increment the row and cell we are checking
            else:   
                item = 0
                filled_spaces_in_same_row = 0
                filled_spaces_in_same_cell = 0
                rowAndCell += 1
        
        # If there isn't a horizontal or vertical match try to find diagonal matches
        # Loop through each item in the filled spaces positions list
        for item_pos in filled_spaces_positions:

            # If the item is in main_diagonal List, increase filled spaces in main diagonal var
            if item_pos in main_diagonal:
                filled_spaces_in_main_diagonal += 1

            # If the item is in secondary_diagonal List, increase filled spaces in secondary diagonal var
            if item_pos in secondary_diagonal:
                filled_spaces_in_secondary_diagonal += 1
            
            # If the var for filled spaces in the main or secondary diagonal is 3 return True(victory) 
            if filled_spaces_in_main_diagonal == 3 or filled_spaces_in_secondary_diagonal == 3:
                return True
        
        # If no horizontal, vertical and diagonal match was found return False(no victory)
        if filled_spaces_in_same_row != 3 and filled_spaces_in_same_cell != 3 and filled_spaces_in_main_diagonal != 3 and filled_spaces_in_secondary_diagonal != 3:
            return False
        """
    # Second option to calculate matches(cleaner, faster and smaller):

    # Horizontal and vertical count var
    rowAndCell = 0

    # Main diagonal and secondary diagonal position to compare later
    main_diagonal = [(0, 0), (1, 1), (2, 2)]
    secondary_diagonal = [(2, 0), (1, 1), (0, 2)]

    # Loop through each row and cell (0, 1, 2) trying to find horizontal or vertical matches
    while rowAndCell < 3:

        # First method option for vertical and horizontal matches(cleaner, less complicated, faster and uses comprehension):

        # Create lists formed by elements that have been filtered by having the same row or cell as the row or cell we are checking. If the length of these lists is 3 it returns True (vertical or horizontal match found)
        if len([item for item in filled_spaces_positions if item[0] == rowAndCell]) == 3 or len([item for item in filled_spaces_positions if item[1] == rowAndCell]) == 3:
            return True

        # If no match was found in the row or cell we are checking go to the next row or cell
        else:   
            rowAndCell += 1

        # Second method option for vertical and horizontal matches(complicated, slower, elegant and uses filter function and lambda expressions):
        """"

            # Create lists formed by elements that have been filtered by having the same row or cell as the row or cell we are checking. If the length of these lists is 3 it returns True (vertical or horizontal match found)
            if len(list(filter(lambda x: x[0] == rowAndCell, filled_spaces_positions))) == 3 or len(list(filter(lambda x: x[1] == rowAndCell, filled_spaces_positions))) == 3:
                return True

            # If no match was found in the row or cell we are checking go to the next row or cell
            else:
                rowAndCell += 1
            """

    # Faster and cleaner method to calculate diagonal matches:

    # Creates sets of common elements between the list of filled spaces positions and the main and secondary diagonal lists. If the length of these sets is 3, it returns True (diagonal match found)
    if len(set(filled_spaces_positions).intersection(main_diagonal)) == 3 or len(set(filled_spaces_positions).intersection(secondary_diagonal)) == 3:
        return True


    # If no diagonal matches were found and we checked all rows and cells on the board and found no vertical or horizontal matches, returns False
    elif rowAndCell == 3:
        return False   

def getFilledPositionsForEachPlayer(board):

    # Get the positions of the filled spaces in the board
    filled_spaces_positions = getSpacesInfo(board)[2]

    # Start with two lists, one for X's and the other for O's filled positions
    x_spaces_positions = []
    o_spaces_positions = []

    # Populate both lists with the correct touples from filled_spaces_positions List
    for position in filled_spaces_positions:
        if board[position[0]][position[1]] == X:
            x_spaces_positions.append(position)
        else:
            o_spaces_positions.append(position)

    return [x_spaces_positions, o_spaces_positions]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Get two lists, one for X's and the other for O's filled positions
    x_spaces_positions = getFilledPositionsForEachPlayer(board)[0]
    o_spaces_positions = getFilledPositionsForEachPlayer(board)[1]
    
    # Use checkForMatches function to return who won if someone has won, else return None
    if checkForMacthes(x_spaces_positions) == True:
        return X
    elif checkForMacthes(o_spaces_positions) == True:
        return O
    else:
        return None
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Get the number of empty spaces of the board 
    empty_spaces_number = getSpacesInfo(board)[0]

    # If someone has won or if all cells have been filled (tie) return True (the game is over), else return false (game in progress)
    return winner(board) != None or empty_spaces_number == 0

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # If the winner is X return 1
    if winner(board) == X:
        return 1
    
    # If the winner is O return -1
    elif winner(board) == O:
        return -1

    # Else return 0 (tie)
    else:
        return 0

def min_value(board):

    # If the board is in a terminal state returns the utility of the board
    if terminal(board) == True:
        return utility(board)
    
    # Initialize the best score var as 2 (the same as infinite)
    best_score = 2

    # For each possible action 
    for action in actions(board):

        # Update the best score by getting the minimum value between the current best score and the max_value() of each result achieved with each action
        best_score = min(best_score, max_value(result(board, action)))
    
    # Returns the final best score
    return best_score

def max_value(board):
    
    # If the board is in a terminal state returns the utility of the board
    if terminal(board) == True:
        return utility(board)

    # Initialize the best score var as -2 (the same as negative infinite)
    best_score = -2

    # For each possible action 
    for action in actions(board):

        # Update the best score by getting the minimum value between the current best score and the max_value() of each result achieved with each action
        best_score = max(best_score, min_value(result(board, action)))
    
    # Returns the final best score
    return best_score

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # First option of minimax (creates a list and filtrates the list until we get the optimal action)(not the cleanest and more complex):
    # If the board is in a terminal state return None
    if terminal(board) == True:
        return None
    elif board == initial_state():
        optimal_action_candidates = list(actions(board))
        return random.choice(optimal_action_candidates)
    else:

        # List of optimal action candidates
        optimal_action_candidates = []

        # Loop through each possible action in the board
        for action in actions(board):

            # If the player is trying to maximize the score 
            if player(board) == X:

                # Itialize best score var as -2 (The same as negative infinite)
                best_score = -2

                # Update the best score by getting the maximum value between the current best score and the min_value() of each result achieved with each action
                best_score = max(best_score, min_value(result(board, action)))

            # If the player is trying to minimize the score 
            elif player(board) == O:

                # Itialize best score var as 2 (The same as infinite)
                best_score = 2

                # Update the best score by getting the minimum value between the current best score and the max_value() of each result achieved with each action
                best_score = min(best_score, max_value(result(board, action)))

            # Append to the list of optimal action candidates a list that contains the action and the best score for this action
            optimal_action_candidates.append([action, best_score])

        # If the player is trying to maximize the score get the highest score from all the actions in the optimal action candidates list
        if player(board) == X:
          optimal_action = max(map(lambda candidate: candidate[1], optimal_action_candidates))

        # If the player is trying to minimize the score get the lowest score from all the actions in the optimal action candidates list
        if player(board) == O:
          optimal_action = min(map(lambda candidate: candidate[1], optimal_action_candidates))

        # Return a random choice of a list made of elements that contains the score of an optimal action (var above) from the optimal action candidates list
        return random.choice(list(filter(lambda x: x[1] == optimal_action, optimal_action_candidates)))[0]
                
