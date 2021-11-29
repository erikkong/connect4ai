import pygame
import sys
import math
import time
from pygame import mixer
import ai


#The board and the things affecting the board
class Board():
    def __init__(self):
        self.size = 7                           #The size of the board
        self.winning_in_a_row = 4               #The number of marks in a row required to win
        self.empty = 0                          #The sign of an empty slot
        self.p1 = 1                             #The sign of player one
        self.p2 = 2                             #The sign of player 2
        self.turn = 1                           #The current player
        self.board = self.create_empty_board()  #The board
        self.color1 = (0,0,255)                 #Blue color
        self.color2 = (255,255,255)             #White color
        self.color3 = (255,0,0)                 #Red color
        self.color4 = (255,255,0)               #Yellow color

    #Creates an empty board on the format board[column][row]
    def create_empty_board(self):
        board = []
        for col in range(self.size):
            board.append([])
            for row in range(self.size):
                board[col].append(self.empty)
        
        return board

    #Checks if the game is over
    def game_over(self):
        rows, columns, diagonals = self.board_state()                                   #The board state

        win, winning_player = self.check_lines_for_win(rows + columns + diagonals)      #Check if anybody has won
        if win:                                                                         #If somebody won:
            #self.print_board()                                                          #-Print out the board
            #print(winning_player, "vann!")                                              #-Print the winner
            
            return True                                                                  #-Return true (game is over)
        
        draw = self.check_draw()                                                        #Check if it is a draw
        if draw:                                                                        #If it is a draw:
            #print("Oavgjort!")                                                          #-Print out "tie"   
            
            return True                                                                 #-Return true (game is over)

        return False                                                            #If the game has not ended return false

    def game_over_player(self, game_screen):
        rows, columns, diagonals = self.board_state()                                   #The board state

        win, winning_player = self.check_lines_for_win(rows + columns + diagonals)      #Check if anybody has won
        if win:                                                                         #If somebody won:
    #self.print_board()                                                          #-Print out the board
    #print(winning_player, "vann!")                                              #-Print the winner
            self.draw_winner(game_screen, winning_player)
            return True                                                                  #-Return true (game is over)

        draw = self.check_draw()                                                        #Check if it is a draw
        if draw:                                                                        #If it is a draw:
    #print("Oavgjort!")                                                          #-Print out "tie"   
            self.draw_draw(game_screen)
            return True                                                                 #-Return true (game is over)

        return False                             
    #Checks if the board is full
    def check_draw(self):
        #Flattens the list of lists
        flat_board = []                         
        for col in self.board:
            flat_board = flat_board + col

        
        if flat_board.count(self.empty) == 0:   #If there are no empty slots
            return True                         #Return true (it is a draw)
        else:                                   #Else
            return False                        #Return false (it is not a draw)

    #Checks all of the "lines" for won line
    def check_lines_for_win(self, lines):
        #Check each line
        for line in lines:
            win, winning_player = self.check_line_for_win(line)

            if win:                             #If the line has four in a row
                return win, winning_player      #Return true (somebody has won) and the player that won
            
        return False, winning_player            #If nobody has won, return False and "Ingen"

    #Checks a line for a win
    def check_line_for_win(self, line):
        winning_player = "Ingen"
        
        if line.count(self.p1) == self.winning_in_a_row:    #If player 1 has four in a row
            winning_player = self.p1                        #The winning player is p1
        elif line.count(self.p2) == self.winning_in_a_row:  #If player 2 has four in a row
            winning_player = self.p2                        #The winning player is p2
        else:                                               #If nobody has won
            return False, winning_player                    #Return False and "Ingen"
        
        return True, winning_player                         #If somebody has won, return True and the winning player

    #Returns all of the possible lines you can win on
    def board_state(self):
        transposed_board = self.transpose_board()

        columns = self.possible_straight_windows(self.board)        #All possible columns you can win on
        rows = self.possible_straight_windows(transposed_board)     #All possible rows you can win on
        diagonals = self.possible_diagonal_windows()                #All possible diagonals you can win on

        return rows, columns, diagonals


    #Returns all possible diagonal lines you can win on
    def possible_diagonal_windows(self):
        diagonal_windows = []                                                       #All diagonal lines you can win on
        diagonals = []                                                              #All of the diagonals (including the diagonal board[1][1])
        #Upper left half and bottom left half
        for row in range(0, len(self.board[0])):                                    #For every row to the left
            top_left_to_bottom_right = True                                         #Simply a flag to know what type of diagonal we are looking at
            current_diagonal = self.get_diagonal(row, top_left_to_bottom_right)     #Retrieves the diagonal line of that type that intersects the current slot
            diagonals.append(current_diagonal)                                      #Append the diagonal to the list of diagonals

            top_left_to_bottom_right = False
            current_diagonal = self.get_diagonal(row, top_left_to_bottom_right)
            diagonals.append(current_diagonal)

        #Bottom right half
        for col in range(1, len(self.board)):                                       #For every row remaining row to the right
            current_diagonal = self.get_diagonal2(col)                              #Retrieves the diagonal line of that type that intersects the current slot
            diagonals.append(current_diagonal)                                      #Append the diagonal to the list of diagonals

        #Top right half
        for col in range(1, len(self.board)):                                       #For every row remaining row to the right
            current_diagonal = self.get_diagonal3(col)                              #Retrieves the diagonal line of that type that intersects the current slot
            diagonals.append(current_diagonal)                                      #Append the diagonal to the list of diagonals


        for diagonal in diagonals:                                                          #For every diagonal
            if len(diagonal) == self.winning_in_a_row:                                      #If the diagonal is of length 4
                diagonal_windows.append(diagonal)                                           #Add it to the diagonal lines
                
            elif len(diagonal) > self.winning_in_a_row:                                     #If the diagonal is longer than 4
                diagonal_windows = diagonal_windows + self.get_windows_from_line(diagonal)  #Split it up into windows

        return diagonal_windows

    #Given a starting position returns the diagonal of one type intersecting that position            
    def get_diagonal(self, row, top_left_to_bottom_right):
        r = row                                         #The input is the starting row
        c = 0                                           #The column always starts at the top
        current_diagonal = []                           #Where the diagonal is stored
        
        allowed = list(range(0, self.size))             #A list containing the boards existing number

        while r in allowed and c in allowed:            #While the iterators are inside the board
            current_diagonal.append(self.board[c][r])   #Append the current indices
            c = c + 1                                   #Move the column one step to the right
            
            if top_left_to_bottom_right:                #If the diagonal goes from top left to bottom right
                r = r + 1                               #Move the row one step down
            else:                                       #If not
                r = r - 1                               #Move the row one step up
                
        return current_diagonal                         #Return the diagonal

    #Bottom left to top right of the bottom right corner
    def get_diagonal2(self, col):
        r = len(self.board) - 1                         #It starts at the bottom row
        c = col                                         #The column is the input
        current_diagonal = []                           #Where the diagonal is stored
        
        allowed = list(range(0, self.size))             #A list containing the boards existing number

        while r in allowed and c in allowed:            #While the iterators are inside the board
            current_diagonal.append(self.board[c][r])   #Append the current indices
            c = c + 1                                   #Move the column one step to the right
            r = r - 1                                   #Move the row one step up
                
        return current_diagonal                         #Return the diagonal

    #Bottom left to top right of the top right corner
    def get_diagonal3(self, col):
        r = 0                                           #It starts at the top row
        c = col                                         #The column is the input
        current_diagonal = []                           #Where the diagonal is stored
        
        allowed = list(range(0, self.size))             #A list containing the boards existing number

        while r in allowed and c in allowed:            #While the iterators are inside the board
            current_diagonal.append(self.board[c][r])   #Append the current indices
            c = c + 1                                   #Move the column one step to the right
            r = r + 1                                   #Move the row one step down
                
        return current_diagonal                         #Return the diagonal


    #Given a line (row, column or diagonal) splits it up into permutations of four consecutive slots 
    def get_windows_from_line(self, line):
        possible_windows = []                                   #The windows of a given line
        number_of_windows = len(line) - self.winning_in_a_row   #The number of possible windows on a line

        for window in range(number_of_windows + 1):             #For every possible window
            #Get a slice of length 4 and append it to the possible windows
            lower_bound = window                                
            upper_bound = lower_bound + self.winning_in_a_row
            current_window = line[lower_bound : upper_bound]
            possible_windows.append(current_window)

        return possible_windows                                 #Return the possible windows

    #The function returns a list of all possible windows of either all rows or all columns
    #instanced_board may or may not be transposed
    def possible_straight_windows(self, instanced_board):
        possible_straight_windows = []
        
        for col in instanced_board:
            possible_straight_windows = possible_straight_windows + self.get_windows_from_line(col)
        return possible_straight_windows
                
    #Transposes the board
    def transpose_board(self):
        transposed = self.create_empty_board()
    
        for col in range(len(self.board)):
           for row in range(len(self.board[0])):
              transposed[col][row] = self.board[row][col]

        return transposed

    #Prints the board
    def print_board(self):
        transposed = self.transpose_board() #Transpose for it to be readable
        self.print_column_names()           #Print helping names of columns
        for row in transposed:
            print(row)

    #Prints the name of all the columns to make it easier to see which one is which
    def print_column_names(self):               
        names = list(range(1, (self.size + 1))) #A list of all column numbers
        names = [str(i) for i in names]         #Aplly the function str on all members of names
        print(names, "\n")

    #Takes a player input
    def choose_column(self):
        while True:
            time.sleep(1)
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    sys.exit

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    column = int(math.floor(posx/120))
                    return column
                                                            

    #Drops the piece into a column
    def drop_piece_player(self, game_screen):
        column = self.choose_column()
        #Choose the column
        valid_column = self.check_valid_column(self.board[column])
        if valid_column == 1:
            deepest = self.find_deepest_player(self.board[column],column, game_screen)
        #Find the deepest
            self.board[column][deepest] = self.turn         #Place the marker
        else:
            print('Columnen är full. Välj en annan!')
            self.drop_piece_player(game_screen)
            
        
    #Finds the slot where the piece will be dropped
    def find_deepest_player(self, column, column_index, game_screen):
        mixer.music.load("marker.ogg")
        mixer.music.play()
        for row in range(len(column)):#For every row of the column
            
            if column[row] != self.empty:   #If the slot is occupied   
                break                       #Break
            self.animate_marker(row, column_index, game_screen)
            deepest = row                   #If not: select as slot
        return deepest
    
    def drop_piece(self):
        column = self.choose_column()
        #Choose the column
        valid_column = self.check_valid_column(self.board[column])
        if valid_column == 1:
            deepest = self.find_deepest(self.board[column])
        #Find the deepest
            self.board[column][deepest] = self.turn         #Place the marker
        else:
            print('Columnen är full. Välj en annan!')
            self.drop_piece()

    def find_deepest(self, column): 
        for row in range(len(column)):      #For every row of the column
            if column[row] != self.empty:   #If the slot is occupied   
                break                       #Break
            deepest = row                   #If not: select as slot
        return deepest
            

    #Next turn
    def next_turn(self):
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1
            
    #Check if the column is not full
    def check_valid_column(self, column):
        if column[0] == self.empty:
            return 1
        else:
            return 0
        
    #Draw the board on screen
    def draw_board(self, game_screen):
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(game_screen, self.color1, (i*120, j*120, 120, 120))
                if self.board[i][j] == 0:
                    pygame.draw.circle(game_screen, self.color2,(int(i*120+120/2), int(j*120+120/2)), 55)

                elif self.board[i][j] == 1:
                    pygame.draw.circle(game_screen, self.color3,(int(i*120+120/2), int(j*120+120/2)), 55)

                else:
                    pygame.draw.circle(game_screen, self.color4,(int(i*120+120/2), int(j*120+120/2)), 55)                  
        pygame.display.update()
                
               
    #Draw current players marker        
    def draw_current_marker(self, game_screen):
        font = pygame.font.SysFont(None, 40)
        if self.turn == 2:
            pygame.draw.circle(game_screen, self.color4,(960,400), 55)
            text = font.render("Player turn",True,self.color1)

        else:
            pygame.draw.circle(game_screen, self.color3,(960,400), 55)
            text = font.render("Player turn",True,self.color1)
        game_screen.blit(text, [880,300])
        pygame.display.update()
        
    #Display the winner     
    def draw_winner(self, game_screen, winner):
        font = pygame.font.SysFont(None, 50)      
        if winner == 1: 
            pygame.draw.rect(game_screen, self.color3,(300,240,480,245))
            text = font.render("Player Red is the winner!",True,self.color1)
            game_screen.blit(text, [340,340])

        else:
            pygame.draw.rect(game_screen, self.color4,(300,240,480,245))
            text = font.render("Player Yellow is the winner!",True,self.color1)
            game_screen.blit(text, [320,340])

        mixer.music.load('win.mp3')
        mixer.music.play()
        self.play_again(game_screen)
        pygame.display.update()
        
    #Display Draw 
    def draw_draw(self, game_screen):
        font = pygame.font.SysFont(None, 50) 
        pygame.draw.rect(game_screen, self.color2,(300,240,480,245))
        text = font.render("DRAW!",True,self.color1)
        game_screen.blit(text, [360,340])
        pygame.display.update()

    #Animate the dropped marker
    def animate_marker(self, row, column_index, game_screen):
        if self.turn == 1:  
            pygame.draw.circle(game_screen, self.color3, (int(column_index*120+120/2), int(row*120+120/2)), 55)   #animate red marker
        else:
            pygame.draw.circle(game_screen, self.color4,(int(column_index*120+120/2), int(row*120+120/2)), 55)    #animate yellow marker
        pygame.display.update()
        time.sleep(0.1)
        pygame.draw.circle(game_screen, self.color2,(int(column_index*120+120/2), int(row*120+120/2)), 55)       #draw empty slot

    #Display the play again 
    def play_again(self, game_screen):
         font = pygame.font.SysFont(None, 30)
         text = font.render("Press R to play again",True,self.color1)
         game_screen.blit(text, [440,420])
         pygame.display.update()
         
        
#Main game loop
def main():
    b = Board()
    #Initializing the graphics
    pygame.init()
    size = (1080, 840)
    game_screen = pygame.display.set_mode(size)

    #Game Menu
    choice = False
    mixer.music.load('menu.mp3')
    mixer.music.play()
    font = pygame.font.SysFont(None, 50)
    text = font.render("Press 2 to play against an AI",True,b.color2)
    game_screen.blit(text, [320,600])

    font1 = pygame.font.SysFont(None, 50)
    text1 = font.render("Press 1 to play against another player",True,b.color2)
    game_screen.blit(text1, [250,500])
    pygame.display.update()
 
    while choice is not True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    ai_playing_as = False
                    choice = True
                    
                if event.key == pygame.K_2:
                    ai_playing_as = b.p1
                    choice = True 
    game_screen.fill((0,0,0))
    b.draw_board(game_screen)
    b.draw_current_marker(game_screen)

    while not b.game_over_player(game_screen):
        
        if ai_playing_as == b.turn:
            b = ai.ai_make_play(b, ai_playing_as)
            
        else:
            b.drop_piece_player(game_screen)
            b.next_turn()

        
        b.draw_current_marker(game_screen)
        b.draw_board(game_screen)

    print("GAME OVER")

    #Check if the player wants to play again
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
      
main()

