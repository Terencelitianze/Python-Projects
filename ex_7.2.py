import random


random_value = random.randint(1,6)

num_col = 1
num_row = 1

board = []
for row in range(num_row):
    row_list = []
    for col in range(num_col):
        row_list.append(random_value)
    board.append(row_list)

for row in range(num_row):
    print("*---*")
    print('|',end=' ')
    for col in range(num_col):
        print(board[row][col], end=' ')
        print('|')
    print("*---*")

print('\n'*100)

flag = True
while flag == True:
    guess = (input("Please guess the number of the dice: "))
    if guess.isdigit() != True:
        print('please enter a digit value')
    elif int(guess) > 6 or int(guess) < 1:
        print('please enter a number between 1 and 6')
    elif int(guess) == random_value:
        print("correct guess")
        flag = False
    else:
        print("wrong guess")