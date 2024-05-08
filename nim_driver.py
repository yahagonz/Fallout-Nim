#Calculates the nim sum of a board
def nimSum(board):
    result = 0;
    #XOR all elements in pile for nim sum
    for pile in board: 
        result ^= pile
    return result

def computerMove(board):
    n_sum = nimSum(board)
    #If nim sum is zero, only 1 stick will be removed
    if n_sum == 0:
        max_index = board.index(max(board))
        board[max_index] -= 1
    else: #it will XOR the first largest available pile (that does not add sticks back into pile) 
        for i, pile in enumerate(board):
            if pile ^ n_sum <= pile:
                board[i] ^= n_sum
                break
    return board