import random
import os
PATH = os.getcwd()

# Constants
CELL_SIZE = 30
GRID_SIZE = 20
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
TEXTSIZE = 32

# Colors for snake and food
SNAKE_COLOR = color(80, 152, 32)
APPLE_COLOR = color(172, 48, 32)
BANANA_COLOR = color(252, 226, 76)

# Game state variables
score = 0
game_over = False

class SnakeElement:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = CELL_SIZE / 2
        self.color = color

    def display(self):
            # Draw the body as circles
            fill(self.color)
            noStroke()
            ellipse(self.x * CELL_SIZE + self.radius, self.y * CELL_SIZE + self.radius, self.radius * 2, self.radius * 2)

class Snake:
    def __init__(self):
        # Initialize snake with one head and two body segments
        start_x = GRID_SIZE // 2
        start_y = GRID_SIZE // 2
        # Head at (start_x, start_y), body behind it to the left
        self.body = [SnakeElement(start_x, start_y,SNAKE_COLOR),          # Head
                     SnakeElement(start_x - 1, start_y,SNAKE_COLOR),      # First body segment to the left of head
                     SnakeElement(start_x - 2, start_y,SNAKE_COLOR)]       # Second body segment to the left of first body segment
        self.grow_next_move = False
        self.direction_x = 1  # Initially moving right (positive x direction)
        self.direction_y = 0   # No movement in y direction initially
        self.img_up_down = loadImage(PATH + "/images/" + "head_up.png")
        self.img_left_right = loadImage(PATH + "/images/" + "head_left.png")

    def move(self):
        if not game_over:
            head_x = self.body[0].x + self.direction_x
            head_y = self.body[0].y + self.direction_y

            # Check for collisions with boundaries or itself
            if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE or self.collides_with_self(head_x, head_y):
                end_game()
                return
            
            # Shift all body segments forward (each takes the position of the one in front)
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Update the head's position to the new calculated position
        self.body[0].x = head_x
        self.body[0].y = head_y

        # If grow_next_move is True, add a new segment at the end of the snake
        if self.grow_next_move:
            last_segment = self.body[-1]
            new_segment = SnakeElement(last_segment.x, last_segment.y, last_segment.color)
            self.body.append(new_segment)
            self.grow_next_move = False

    def change_direction(self, new_direction_x, new_direction_y):
        # Prevent moving in the opposite direction directly (e.g., left to right)
        if (self.direction_x + new_direction_x != 0) or (self.direction_y + new_direction_y != 0):
            self.direction_x = new_direction_x
            self.direction_y = new_direction_y

    def grow(self):
        # Mark that we need to grow on next move and use next_segment_color for new segment.
        last_segment = self.body[-1]
        new_segment_color = game.food_item.color  # Use food's color for new segment
        # Add a new segment at the position of the last one with appropriate color.
        new_segment = SnakeElement(last_segment.x, last_segment.y, new_segment_color)
        # Add this segment to grow on next move.
        self.body.append(new_segment)
    
    def collides_with_self(self, x, y):
        return any(segment.x == x and segment.y == y for segment in self.body)

    def display(self):
        # Display snake body as circles except for the head
        for i in range(1, len(self.body)):
            segment = self.body[i]
            segment.display()

        # Display the head based on direction
        head_segment = self.body[0]
        
        if self.direction_x == 1:   # Moving right
            image(self.img_left_right, head_segment.x * CELL_SIZE, head_segment.y * CELL_SIZE, 30, 30, 30, 30, 0, 0)
        
        elif self.direction_x == -1:   # Moving left
            image(self.img_left_right, head_segment.x * CELL_SIZE, head_segment.y * CELL_SIZE, 30, 30)
        
        elif self.direction_y == -1:   # Moving up
            image(self.img_up_down, head_segment.x * CELL_SIZE, head_segment.y * CELL_SIZE, 30, 30)
        
        elif self.direction_y == 1:   # Moving down
            image(self.img_up_down, head_segment.x * CELL_SIZE, head_segment.y * CELL_SIZE, 30, 30, 30, 30, 0, 0)


class Food:
    def __init__(self, snake):
        # Pass snake as an argument to check for overlap during repositioning.
        self.snake = snake  
        self.reposition()
        
    def reposition(self):
        # Reposition food to a random location that does not overlap with the snake.
        while True:
            new_x = random.randint(0, GRID_SIZE - 1)
            new_y = random.randint(0, GRID_SIZE - 1)
            
            # Ensure the new food position does not overlap with any part of the snake
            if not any(segment.x == new_x and segment.y == new_y for segment in self.snake.body):
                break
        
        # Set new position for the food
        self.x = new_x
        self.y = new_y
        
        # Randomly choose between apple and banana images each time food is repositioned
        self.fruit_type = random.randint(0, 1)  # Randomly choose between apple (0) and banana (1)
        if self.fruit_type == 0:
            self.img = loadImage(PATH + "/images/" + "apple.png")
            self.color = APPLE_COLOR  # Apple (red)
        elif self.fruit_type == 1:
            self.img = loadImage(PATH + "/images/" + "banana.png")
            self.color = BANANA_COLOR  # Banana (yellow)

    def display(self):
        # Display food on screen at the correct position (assuming Processing.py)
        image(self.img, self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

class Game:
    def __init__(self):
        global score
        score = 0
        global game_over 
        game_over = False
        
        # Initialize snake and food objects
        self.snake = Snake()
        # Pass snake object to Food class so it can avoid overlapping with it.
        self.food_item = Food(self.snake)

    def update(self):
        if not game_over:
            # Move the snake and check for collisions with food
            self.snake.move()
            
            if self.snake.body[0].x == self.food_item.x and self.snake.body[0].y == self.food_item.y:
                global score 
                score += 1
                
                # Grow the snake and reposition food item after eating it.
                self.snake.grow()
                self.food_item.reposition()

    def display(self):
        
        # Display score in top-right corner.
        textSize(TEXTSIZE)
        fill(255,0,0)  
        text(("Score: "+str(score)), WIDTH - TEXTSIZE * 4.5 , TEXTSIZE)

        # Display snake and food.
        self.snake.display()
        self.food_item.display()
        
def end_game():
    global game_over 
    game_over= True 
    if score == GRID_SIZE*GRID_SIZE - 3:  #check if the snake takes up the whole game, if yes then player wins
        fill(255,255,255)
        noStroke()
        rect(0,0, 600, 600)
        
        textSize(TEXTSIZE * 2)   # Make text larger for Game Over message
        fill(255, 0, 0)          # Set color to red for Game Over message
        text("YOU WIN",125,250)   # Display Game Over message
        
        textSize(TEXTSIZE)       # Reset text size for score display
        fill(255,0,0)                # Set color to white for score display
        text(("Final Score: "+str(score)), 200,300)   # Display final score below Game Over message
    else:
        fill(255,255,255)
        noStroke()
        rect(0,0, 600, 600)
        
        textSize(TEXTSIZE * 2)   # Make text larger for Game Over message
        fill(255, 0, 0)          # Set color to red for Game Over message
        text("GAME OVER",125,250)   # Display Game Over message
        
        textSize(TEXTSIZE)       # Reset text size for score display
        fill(255,0,0)                # Set color to white for score display
        text(("Final Score: "+str(score)), 200,300)   # Display final score below Game Over message


# Processing functions
def setup():
    size(WIDTH, HEIGHT)
    background(255)
    global game 

game= Game()

def draw():
    if frameCount %12 ==0 and game_over == False:
        background(255)
        game.update()
        game.display()
    elif game_over == True:
        end_game()

def keyPressed():
    if keyCode == UP:
         game.snake.change_direction(0, -1)  # Move up (negative y direction)
    elif keyCode == DOWN:
         game.snake.change_direction(0, 1)   # Move down (positive y direction)
    elif keyCode == LEFT:
         game.snake.change_direction(-1, 0)   # Move left (negative x direction)
    elif keyCode == RIGHT:
         game.snake.change_direction(1, 0)   # Move right (positive x direction)

'''def mousePressed():
    global game_over 
    if game_over:
      setup()# Restart the game when mouse is pressed after Game Over.'''
def mousePressed():
    global game_over, game, score
    if game_over:
        # Reset game state variables
        game_over = False
        score = 0
        # Create a new Game instance to restart the game
        game = Game()
