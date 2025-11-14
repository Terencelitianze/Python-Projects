import os, time

board = [
            [1," "," "," "," ",7," ",9," "],
            [" ",3," "," ",2," "," "," ",8],
            [" "," ",9,6," "," ",5," "," "],
            [" "," ",5,3," "," ",9," "," "],
            [" ",1," "," ",8," "," "," ",2],
            [6," "," "," "," ",4," "," "," "],
            [3," "," "," "," "," "," ",1," "],
            [" ",4," "," "," "," "," "," ",7],
            [" "," ",7," "," "," ",3," "," "]
        ]

def print_board():
    os.system('clear')
    print ('-'*25, sep='')
    for row in range(len(board)):
        print ('|', end=' ')
        for col in range(len(board[0])):
            print (board[row][col], end=' ')
            if (col+1)%3 == 0:
                print ('|', end=' ')
        if (row+1)%3 == 0:
            print ('\n','-'*25, sep='')
        else:
            print()
    time.sleep(1)

def valid_play(num,r,c):
    # horizontal
    if num in board[r]:
        return False

    # vertical
    for i in range(9):
        if board[i][c] == num:
            return False

    # sector
    for row in range(3*int(r/3), 3*int(r/3) + 3):
        for col in range(3*int(c/3), 3*int(c/3) + 3):
            if board[row][col] == num:
                return False

    return True

def get_next(r, c):
    if c < 8:
        return r, c+1
    return r+1, 0

def solver(r=0, c=0):

    # Base case: If we've reached past the last row, the board is solved
    if r == 9:
        return True

    # Skip pre-filled cells
    if board[r][c] != " ":
        next_r, next_c = get_next(r, c)
        return solver(next_r, next_c)

    # Try all numbers from 1 to 9
    for num in range(1, 10):
        if valid_play(num, r, c):
            board[r][c] = num
            next_r, next_c = get_next(r, c)
            
            # Recursively attempt to solve the rest of the board
            if solver(next_r, next_c):
                return True

            # Backtrack if placing num doesn't lead to a solution
            board[r][c] = " "

    # If no number works in this cell, backtrack
    return False
    # 1. Define base case, e.g. when r becomes larger than the board dimensions -> return True
    # 2. Skip pre-filled cells. Use get_next() function to get next cell
    # 3. Use brute force method (for loop) to fill the the current cells with a number (1-9)
    # 4. Verify if it is a valid play
    #   a) if yes, move on to next cell and call solver() recursively
    #   b) if not, try next number
    # 5. reset cell and return False if none of the above worked
    #return False

print_board()
solver()
print_board()
