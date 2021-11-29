import copy

#Return the best play for the AI to make
def ai_make_play(b, playing_as):
    depth = 3
    alpha = -1000
    beta = 1000
    
    if playing_as == b.p1:
        b = ai_make_play_1(b, depth, alpha, beta)
    else:
        b = ai_make_play_2(b, depth, alpha, beta)

    return b

#If the AI is player 2 return the best play for player 2. Player 2 wants to minimize
def ai_make_play_2(b, depth, alpha, beta):
    possible_next_states = next_states(b)               #A list of all possible next states
    
    optimal_state = possible_next_states[0]             #The current optimal state
    optimal_value = 1000                                #The value of the current optimal state
            
    for state in possible_next_states:                  #For every possible next state
        value = alphabeta(state, depth, alpha, beta)    #The value of the state

        if value < optimal_value:                       #If the value is better
            optimal_value = value                       #Update
            optimal_state = state

    return optimal_state                                #Return the optimal next play

#If the AI is player 1 return the best play for player 1. Player 1 wants to maximize
def ai_make_play_1(b, depth, alpha, beta):
    possible_next_states = next_states(b)
    
    optimal_state = possible_next_states[0]
    optimal_value = -1000
            
    for state in possible_next_states:
        value = alphabeta(state, depth, alpha, beta)

        if value > optimal_value:
            optimal_value = value
            optimal_state = state

    return optimal_state

#Player 1 wants to maximize
#Player 2 wants to minimize
def alphabeta(board, depth, alpha, beta):

    if board.game_over() or depth == 0:         #Base condition
        value = heuristic(board)

    else:
        possible_next_states = next_states(board)
        
        if board.turn == 1:                                                 #Player 1
            value = -1000                                                   #The current best option
            for state in possible_next_states:                              #For every possible next state
                value = max(value, alphabeta(state, depth-1, alpha, beta))  #The value of this state is the value of the next state
                alpha = max(alpha, value)                                   #Update Alpha

                if beta <= alpha:                                           #Beta prune
                    break

        else:                                                               #Player 2
            value = 1000                                                    #The current best option
            for state in possible_next_states:                              #For every possible next state
                value = min(value, alphabeta(state, depth-1, alpha, beta))  #The value of this state is the value of the next state
                beta = min(beta, value)                                     #Update Beta

                if beta <= alpha:                                           #Alpha prune
                    break

    return value




#Player 1 wants to maximize
#Player 2 wants to minimize

#The heuristic function scores a board state
def heuristic(board):
    rows, columns, diagonals = board.board_state()
    lines = rows + columns + diagonals

    score = 0
    
    for line in lines:                          #For every line
        markers_p1 = 0                          #The number of p1 markers in the line
        markers_p2 = 0                          #The number of p2 markers in the line
        
        for slot in line:                       #For every slot in the line
            if slot == board.p1:                #If the slot is taken by a p1 marker
                markers_p1 = markers_p1 + 1     #Add one to the p1 counter
            elif slot == board.p2:              #If the slot is taken by a p2 marker
                markers_p2 = markers_p2 + 1     #Add one to the p2 counter

        if markers_p1 > 0 and markers_p2 > 0:   #If the line is dead
            score = score + 0                   #Score it as 0


        elif markers_p1 == board.winning_in_a_row:  #If p1 has won
            return 1000                             #Return a lot
        elif markers_p2 == board.winning_in_a_row:  #If p2 has won
            return -1000                            #Return negative a lot
        
        elif markers_p1 > 0:                    #If p1 can win on the line
            score = score + markers_p1          #Score it as positive
        elif markers_p2 > 0:                    #If p2 can win on the line
            score = score - markers_p2          #Score it as negative
    
    return score

#Takes a board and returns all possible boards after one move
def next_states(board):
    possible_next_states = []

    column_nr = 0
    for column in board.board:                          #For every column
        if board.check_valid_column(column) == 1:       #If it is not full
            next_state = ai_drop_piece(board, column_nr)#The result of dropping the piece in the column
            possible_next_states.append(next_state)     #Add the result to the list
        column_nr = column_nr + 1

    return possible_next_states

#Takes a board and a column and returns the result of when a piece has been dropped in the column
def ai_drop_piece(board, column):
    potential_board = copy.deepcopy(board)
    
    deepest = potential_board.find_deepest(board.board[column])
    potential_board.board[column][deepest] = potential_board.turn
    potential_board.next_turn()

    return potential_board
