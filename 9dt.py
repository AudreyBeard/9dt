'''
9dt.py
98point6 Drop Token
Joshua Beard
4/1/17
'''

class DropToken(object):
    '''
    Defines API for drop token game
    To process commands, use newCommands, passing in the full command string
    '''

    def __init__(self, startPlayer):
        ''' 
        Initialize:
            Board
            Scores
            Columns that have been successfully put to
            Winner
            If user wants to exit
            Player that goes first
        Display:
            First player
            Valid commands
            
        INPUT:
            Starting player (1 or 2)
        '''          
        try: # Make sure we start the game off right
            startPlayer = int(startPlayer) 
            assert(startPlayer == 1 or startPlayer == 2)
            self.player = startPlayer 
            self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
            self.scores = {'row':[0,0,0,0], 'col':[0,0,0,0], 'diag':[0,0]}
            self.putTo = []
            self.winner = 0
            self.exit = 0
            print('Player %i starts first.' % self.player)    
            print('Please enter one of the following commands: PUT <column>, GET, BOARD, or EXIT')
        
        except:
            print('ERROR: Starting player must be either 1 or 2. Exiting.')
            self.exit = 1        
        
    def newCommand(self, cmd):
        '''
        Parses all commands
        Verifies correctness
        Executes correctly-entered commands
        Prints informational error messages
        
        INPUT: Full command string (performs error checking)
        OUTPUT: 1, 0, or -1:
            Return 1: A-OK
            Return 0: Invalid choice, but format is OK
            Return -1: Invalid format.
        '''
        cmd = cmd.lower().split()   # Lower and split for easy processing
        if len(cmd) == 2:           # PUT is only 2-length command
        
            if cmd[0] == 'put':     
                try:                                # Cast second argument as integer
                    cmd[1] = int(cmd[1])
                except:                             # Only allow integers
                    print('ERROR')
                    return -1
                
                if cmd[1] < 1 or cmd[1] > 4:        # Second argument must be one of four columns
                    print('ERROR')
                    return -1
                    
                else:                               # Parsed OK, process validity next
                
                    if self.winner:                 # Game has been won
                        print('ERROR')
                        return 0                    # Invalid move, no error
                        
                    elif len(self.putTo) == 16:     # Game is already a draw
                        print('ERROR')
                        return 0                    # Invalid move, no error
                        
                    elif self._put(int(cmd[1])):     # This put command is valid
                    
                        if self.winner:             # Someone won
                            print('WIN')
                                                        
                        elif len(self.putTo) == 16: # If draw
                            print('DRAW')
                            
                        else:                       # Put to board OK
                            print('OK')
                        return 1                    # All three are valid moves
                    
                    else:                           # Full column
                        print('ERROR')
                    return 0                        # Invalid input, no error
                    
            else:                                   # Fudged input
                print('ERROR')
                return -1                           # Invalid input, not acceptable
                
        elif len(cmd) == 1:                         # GET, BOARD, or EXIT
        
            if cmd[0] == 'get':
                self.get()
                return 1
                
            elif cmd[0] == 'board':
                self.printBoard()
                return 1
                
            elif cmd[0] == 'exit':
                self.exit = 1
                return 1
                
            else:                                   # Invalid input
                print('ERROR')
                return -1
                
        else:                                       # INvalid input
            print('ERROR')
            return -1
            
        
    def _put(self, col):
        '''
        Uses helper functions to process player token dropping.
        Starts at bottom of defined column, finds first open row, and drops token there
        NOTE: Assumes newCommand processes all the commands from stdin, so we do minimal error processing
        
        INPUT:
            Column to put to
        OUTPUT:
            Column put to or 0 for full column
        '''
        if col != int(col):         # This should never happen under normal circumstances
            print('ERROR: PUT received noninteger value. Exiting now.')
            self.exit = 1;
                   
        for row in range(3,-1,-1):                      # Start at bottom of column
            if self.board[row][col-1] == 0:             # Check if row is empty
                self.board[row][col-1] = self.player    # Drop token there
                self._keepScore(row, col-1)             # Keep score and note if game is over
                self.putTo = self.putTo +[col]          # Add token to list of columns put to
                self.player = (self.player*2)%3         # Move to next player
                return col
        else:    # If we got this far, there are no empty rows in given column
            return 0
    
    def printBoard(self):
        '''
        Prints the board in a readable fashion
        NOTE: This follows print conventions for Python 2.7. Will not work with 3.X        
        '''
        for row in range(0,4):
            print('|'),      # Formatting
            for col in range(0,4):
                print(self.board[row][col]),
            print('')
        print('+--------\n  1 2 3 4') # Formatting
            
    def get(self):
        '''
        Simple function to print all columns successfully put to
        '''
        for col in self.putTo:
            print(col)
    
    
    def _keepScore(self, row, col):
        '''
        Helper function for keeping score and setting a winner
        Use of a player lookup list makes checking for win conditions easy and fast
        Updates winner of the game based on scores
        NOTE: It is assumed this has been called by newCommand via _put, and has thus been checked for errors numerous times, so we do minimal error checking here
        INPUT:
            Row and column that just received a token
        OUTPUT:
            Winner of the game (1 or 2) or 0 for no one (yet)
        '''
        # Error checking (these should never happen using API)
        if row < 0 or row > 3 or col < 0 or col > 3:
            print('ERROR: KEEPSCORE received invalid input. Exiting.')
            self.exit = 1
        row = int(row)
        col = int(col)
        
        pid = [0,1,-1]      # Lookup list for quick & easy win determination
        
        # Add +/- 1 to specific row and column scores.
        self.scores['row'][row] = self.scores['row'][row] + pid[self.player]
        self.scores['col'][col] = self.scores['col'][col] + pid[self.player]
        
        if row == col:      # Corresponds to top-left to bottom-right diagonal
            self.scores['diag'][0] = self.scores['diag'][0] + pid[self.player]
        elif row+col == 3:  # Corresponds to top-right to bottom-left diagonal
            self.scores['diag'][1] = self.scores['diag'][1] + pid[self.player]
            
        # If any scores in any of the directions is +/- 4, that means that row, column, or diagonal has a winner
        if 4 in self.scores['row'] or 4 in self.scores ['col'] or 4 in self.scores['diag']:
            self.winner = 1
            
        elif -4 in self.scores['row'] or -4 in self.scores['col'] or -4 in self.scores['diag']:
            self.winner = 2
            
        else:   # if we've made it this far, there is no winner
            self.winner = 0
            
        return self.winner
    
    
''' Things to do when called from the command line '''
if __name__ == '__main__':
    print('')
    print('[]=================================[]')
    print('|| Welcome to 98point6 Drop Token! ||')
    print('[]=================================[]')
    print('')
    
    thisGame = DropToken(1)
    
    while not thisGame.exit:
        thisGame.newCommand(raw_input('> '))
    
    
