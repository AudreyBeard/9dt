'''
9dt.py
98point6 Drop Token
Joshua Beard
4/1/17
'''

#b2p = [0,2,0,1]
#p2b = [0,1,-1]
BOARD = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] # Version for human reading
# Consider replacing the next few lines with a dictionary i.e.
#scores = ['row':[0,0,0,0], 'col':[0,0,0,0]. 'diag':[0,0]]
rowScores = [0,0,0,0]   # Scores for each row, determines win
colScores = [0,0,0,0]   # Scores for each column, determines win
diagScores = [0,0]      # Scores for each diagonal, determines win
playerID = [0,1,-1]     # lookup list for quick win determination

# Cumulatively collects scores to determine if someone has won
def isGameOver(player, row, col, rs = rowScores, cs = colScores, ds = diagScores, pid = playerID):
#def isGameOver(player, row, col, S, pid=playerID)

    rs[row] = rs[row]+pid[player]
    cs[col] = cs[col]+pid[player]
    if row == col: ds[0] = ds[0] + pid[player]
    if row+col == 3: ds[1] = ds[1] + pid[player]
    
    # Check rows and columns for win conditions
    for i in range(0,4):
        if rs[i] == 4 or rs[i] == 4:
            return 1
        elif rs[i] == -4 or cs[i] == -4:
            return 2
    # Check diagonals for win conditions
    if ds[0] == 4 or ds[1] == 4:
        return 1
    elif ds[0] == -4 or ds[1] == -4:
        return 2

    # if we've made it this far, there is no winner
    return 0
                 
# Goes through every row (bottom to top) of designated row then checks if someone has won, it then prints the board
def put(player, col, board=BOARD):#, player2board=p2b):
    for row in range(3,-1,-1):
        if board[row][col] == 0:
            #board[row][col] = player2board[player]
            board[row][col] = player
            winner = isGameOver(player, row, col)
            printBoard(board)
            if winner > 0:
                print('Player %i wins!\n' % winner) 
            return player
    return -1
        
# Function for printing the board
def printBoard(board=BOARD):#, board2player=b2p):
    for row in range(0,4):
        print '|',      # Formatting
        for col in range(0,4):
            #print board2player[board[row][col]+2],
            print board[row][col],
        print
    print '+--------\n' # Formatting
    
# Things to do when called from the command line
if __name__ == '__main__':
    winner = 0
    while not winner:
        # Testing raw_input
        cmd = int(raw_input())
        print cmd
        print cmd
         
