import random

# Constants
Num_row = 10
Num_col = 10
players = ['X','O','V','H','M']  # Two players can be expanded to ['X', 'O', 'V', 'H', 'M']
Board_letters = []
board = []

# Check if the column input is valid
def is_valid_column(board, col):
    return col >= 0 and col < Num_col and board[0][col] == " "

# Drop checker into the board
def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            break

# Check for a win (horizontal, vertical, diagonal)
def check_win(board, player):
    # Check horizontal locations
    for r in range(Num_row):
        for c in range(Num_col - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical locations
    for r in range(Num_row - 3):
        for c in range(Num_col):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(Num_row - 3):
        for c in range(Num_col - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, Num_row):
        for c in range(Num_col - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full (draw)
def check_draw(board):
    return all(board[0][col] != " " for col in range(Num_col))

# Main game 
for n in range(65,Num_col+65): # determining the Capitial letters for the top of the visible board
    character = chr(n)
    Board_letters.append(character)

for row in range(Num_row): # dynamically appending the " " into the "Board" 2D list
    row_list=[]
    for col in range(Num_col):
        row_list.append(" ")
    board.append(row_list)

#dynamically printing the game table
i = 0
for col in range(Num_col):
    print("   "+Board_letters[i], end = '')
    i = i + 1
print("\n +"+"---+"*Num_col)
for row in range(Num_row): 
    print(" |", end = " ")
    for col in range(Num_col):
        print(board[row][col]+" | ", end = "")
    print("\n +"+"---+"*Num_col)
game_over = False
turn = random.randint(0, len(players) - 1)

while not game_over:
    # Get user input
    while True:
        player = players[turn]
        print(f"\nPlayer {player}'s turn.")
        col_input = input("Choose a column (A-G): ")
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + Num_col - 1):
            col = ord(col_input) - 65
            if is_valid_column(board, col):
                break
            else:
                print("Column is full. Turn lost.")
                turn = (turn + 1) % len(players)
                continue
        else:
            print("Invalid input. Please enter a valid column letter.")

    # Place the checker
    drop_checker(board, col, player)
    #dynamically printing the game table
    i = 0
    for col in range(Num_col):
        print("   "+Board_letters[i], end = '')
        i = i + 1
    print("\n +"+"---+"*Num_col)
    for row in range(Num_row): 
        print(" |", end = " ")
        for col in range(Num_col):
            print(board[row][col]+" | ", end = "")
        print("\n +"+"---+"*Num_col)

    # Check for win or draw
    if check_win(board, player):
        print(f"Player {player} wins!")
        game_over = True
    elif check_draw(board):
        print("The game is a draw!")
        game_over = True
    else:
        turn = (turn + 1) % len(players)

