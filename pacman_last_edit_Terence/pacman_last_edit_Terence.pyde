add_library("minim")

import os
import random as built_random
from ddf.minim import Minim
PATH = os.getcwd()

class PacmanGame:
    def __init__(self):
        self.stage = "menu"
        self.direction = ""
        self.vel = 5
        self.score = 0
        self.numOnScreen = 0
        self.numEaten = 0
        self.soundOn = True
        self.pause = False
        self.leaderboard = [0] * 5
        self.pacman = Pacman(self)
        self.ghosts = []
        self.maze = Maze(self)
        self.width = 750  # Adjusted to match the maze dimensions
        self.height = 500
        self.tamanho = self.width // len(self.maze.grid[0])  # Cell size based on window width and maze columns
        self.PATH = os.getcwd()
        self.crackmanFont = None
        self.lotFont = None
        self.minim = None
        self.intro = None
        self.chump = None
        self.hover_option = None
        self.grace_period = 120  # 2 seconds at 60 FPS
        self.game_over_option = None
        self.superpower = SuperPower(self)
        self.ghosts_vulnerable = False  # Tracks if ghosts can be removed
        self.ghost_pass_superpower = GhostPassSuperPower(self)  # New superpower
        self.ghost_pass_active = False  # Tracks if the ghost-pass superpower is active
        self.menu_image = loadImage(PATH + "/pacman/"+ "spiderman_vs_mysterio.jpg")

    def initialize(self):
        background(0)
        frameRate(60)

        # Load fonts
        self.crackmanFont = createFont(self.PATH + "/pacman/crackman.TTF", 18)
        self.lotFont = createFont(self.PATH + "/pacman/lot.otf", 18)

        # Load audio
        self.minim = Minim(this)
        self.intro = self.minim.loadFile(self.PATH + "/pacman/pacman_beginning.wav")
        self.chump = self.minim.loadFile(self.PATH + "/pacman/pacman_chomp.wav")

        # Set up ghosts
        self.ghosts = [
            Ghost(self, "red", color(255, 0, 0), 1, 1),
            Ghost(self, "blue", color(51, 204, 255), 13, 1),
            Ghost(self, "pink", color(255, 162, 122), 1, 8),
            Ghost(self, "orange", color(255, 204, 0), 13, 8),
        ]

        self.pacman.setup()
        for ghost in self.ghosts:
            ghost.setup()
        self.maze.setup_maze_dimensions()
        
        # Spawn both superpowers only if they haven't been spawned
        if not self.superpower.spawned:
            self.superpower.spawn()
        if not self.ghost_pass_superpower.spawned:
            self.ghost_pass_superpower.spawn()

    def draw(self):
        if self.stage == "menu":
            self.draw_menu()
        elif self.stage == "game":
            self.draw_game()
        elif self.stage == "leaderboard":
            self.draw_leaderboard()
        elif self.stage == "death":
            self.draw_death()
        elif self.stage == "ready":
            self.draw_ready()
        elif self.stage == "win":
            self.draw_win()
            
    def draw_game(self):
        background(0)
        self.maze.draw_maze()
        self.maze.draw_points()
        self.pacman.update()
        self.pacman.draw()
        self.check_dot_collision()
    
        # Update and draw each superpower
        self.superpower.update()
        self.superpower.draw()
    
        self.ghost_pass_superpower.update()
        self.ghost_pass_superpower.draw()
    
        # Check collisions with each superpower
        if not self.superpower.active and self.check_superpower_collision():
            self.superpower.activate()
            self.ghosts_vulnerable = True  # This superpower makes ghosts vulnerable
    
        if not self.ghost_pass_superpower.active and self.check_ghost_pass_collision():
            self.ghost_pass_superpower.activate()
            self.ghost_pass_active = True  # This superpower allows Pacman to pass through ghosts
    
        # Handle ghost vulnerability
        if self.superpower.active:
            self.ghosts_vulnerable = True
        else:
            self.ghosts_vulnerable = False
    
        # Handle ghost-pass logic independently
        if self.ghost_pass_superpower.active:
            self.ghost_pass_active = True
        else:
            self.ghost_pass_active = False
    
        # Update ghost logic
        for ghost in self.ghosts[:]:
            ghost.update()
            ghost.draw()
    
            # Apply appropriate logic for each superpower
            if self.grace_period <= 0:
                if self.ghost_pass_active:
                    # If ghost-pass superpower is active, Pacman can pass through ghosts
                    continue
                elif self.check_ghost_collision(ghost):
                    if self.ghosts_vulnerable:
                        # Remove the ghost if the vulnerability superpower is active
                        self.ghosts.remove(ghost)
                    else:
                        # End the game if no superpower is active
                        self.end_game()
    
        # Check if Pacman has eaten all dots
        if len(self.maze.dots) == 0:
            self.stage = "win"
    
        self.display_score()
    
        # Display "Get Ready!" during the grace period
        if self.grace_period > 0:
            self.grace_period -= 1
            fill(255, 255, 0)
            textFont(self.lotFont)
            textSize(30)
            textAlign(CENTER, CENTER)
            text("Get Ready!", self.width // 2, self.height // 2 - 100)

    def check_superpower_collision(self):
        """Check if Pacman collides with the superpower."""
        return dist(self.pacman.x, self.pacman.y, self.superpower.x, self.superpower.y) < (self.pacman.radius + self.superpower.radius)
    
    def check_ghost_pass_collision(self):
        """Check if Pacman collides with the ghost-pass superpower."""
        return dist(self.pacman.x, self.pacman.y, self.ghost_pass_superpower.x, self.ghost_pass_superpower.y) < (30 + self.ghost_pass_superpower.radius)
    
    
    def draw_menu(self):
        background(0)
        image(self.menu_image, 0, 0, self.width, self.height)
        textFont(self.crackmanFont)
        textAlign(CENTER, CENTER)

        # Play Button
        if self.hover_option == "play":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 0)
        text("Play", self.width // 2, self.height // 2 - 50)

        # Leaderboard Button
        if self.hover_option == "leaderboard":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 0)
        text("Leaderboard", self.width // 2, self.height // 2)

        # Exit Button
        if self.hover_option == "exit":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 0)
        text("Exit", self.width // 2, self.height // 2 + 50)

    def draw_ready(self):
        background(0)
        fill(255, 255, 0)
        textFont(self.lotFont)
        textSize(60)
        textAlign(CENTER, CENTER)
        text("READY!", self.width // 2, self.height // 2)
        if not self.intro.isPlaying():
            self.intro.play()
        if frameCount > 120:
            self.stage = "game"

    def draw_leaderboard(self):
        background(0)
        image(self.menu_image, 0, 0, self.width, self.height)
        fill(255, 255, 0)
        textFont(self.crackmanFont)
        textSize(60)
        textAlign(CENTER, CENTER)
        text("LEADERBOARD", self.width // 2, 50)

        textSize(40)
        for i, score in enumerate(self.leaderboard):
            text(str(i + 1) + ": " + str(score) + " points", self.width // 2, 150 + i * 50)

        # Add options to return or exit
        if self.hover_option == "play again":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Play Again", self.width // 2, self.height - 80)

        if self.hover_option == "exit":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Exit", self.width // 2, self.height - 40)

    def draw_death(self):
        background(0)
        image(self.menu_image, 0, 0, self.width, self.height)
        fill(255, 0, 0)
        textFont(self.lotFont)
        textSize(60)
        textAlign(CENTER, CENTER)
        text("GAME OVER", self.width // 2, self.height // 2 - 100)

        # Display the player's final score
        textSize(40)
        fill(255, 255, 0)
        text("Your Score: " + str(self.score), self.width // 2, self.height // 2)

        # Options for play again, leaderboard, or exit
        if self.hover_option == "play again":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Play Again", self.width // 2, self.height - 120)

        if self.hover_option == "leaderboard":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Leaderboard", self.width // 2, self.height - 80)

        if self.hover_option == "exit":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Exit", self.width // 2, self.height - 40)

    def draw_win(self):
        background(0)
        fill(0, 255, 0)
        textFont(self.lotFont)
        textSize(60)
        textAlign(CENTER, CENTER)
        text("YOU WIN!", self.width // 2, self.height // 2 - 100)

        # Display the player's final score
        textSize(40)
        fill(255, 255, 0)
        text("Your Score: " + str(self.score), self.width // 2, self.height // 2)

        # Options for play again or exit
        if self.hover_option == "play again":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Play Again", self.width // 2, self.height - 120)

        if self.hover_option == "exit":
            textSize(40)
            fill(0, 247, 255)
        else:
            textSize(32)
            fill(255, 255, 255)
        text("Exit", self.width // 2, self.height - 40)
        
        # Reset the superpower for the next game after a win
        self.superpower = SuperPower(self)

    def mouse_hover(self):
        x, y = mouseX, mouseY
        if self.stage in ["menu", "death", "leaderboard", "win"]:
            if self.width // 2 - 100 < x < self.width // 2 + 100:
                if self.stage == "menu":
                    if self.height // 2 - 70 < y < self.height // 2 - 30:
                        self.hover_option = "play"
                    elif self.height // 2 - 10 < y < self.height // 2 + 30:
                        self.hover_option = "leaderboard"
                    elif self.height // 2 + 40 < y < self.height // 2 + 70:
                        self.hover_option = "exit"
                elif self.stage in ["death", "leaderboard", "win"]:
                    if self.height - 140 < y < self.height - 100:
                        self.hover_option = "play again"
                    elif self.height - 100 < y < self.height - 60:
                        self.hover_option = "leaderboard"
                    elif self.height - 60 < y < self.height - 20:
                        self.hover_option = "exit"
            else:
                self.hover_option = None

    def menu_select(self):
        if self.hover_option == "play":
            self.start_game()
        elif self.hover_option == "leaderboard":
            self.stage = "leaderboard"
        elif self.hover_option == "exit":
            exit()

    def death_select(self):
        if self.hover_option == "play again":
            self.start_game()
        elif self.hover_option == "leaderboard":
            self.stage = "leaderboard"
            self.hover_option = None  # Reset hover option to allow re-selection
        elif self.hover_option == "exit":
            exit()

    def leaderboard_select(self):
        if self.hover_option == "play again":
            self.start_game()
        elif self.hover_option == "exit":
            exit()

    def win_select(self):
        if self.hover_option == "play again":
            self.start_game()
        elif self.hover_option == "exit":
            exit()

    def reset_ghosts(self):
        """Reset ghosts to their initial positions and states."""
        self.ghosts = [
            Ghost(self, "red", color(255, 0, 0), 1, 1),
            Ghost(self, "blue", color(51, 204, 255), 13, 1),
            Ghost(self, "pink", color(255, 162, 122), 1, 8),
            Ghost(self, "orange", color(255, 204, 0), 13, 8),
        ]
        for ghost in self.ghosts:
            ghost.setup()

    def start_game(self):
        """Reset the game state and start a new game."""
        self.score = 0
        self.pacman.setup()
        self.maze.setup_maze_dimensions()
        self.reset_ghosts()
        # Reset both superpowers for the next game
        self.superpower = SuperPower(self)
        self.ghost_pass_superpower = GhostPassSuperPower(self)
        self.superpower.spawn()
        self.ghost_pass_superpower.spawn()
        self.stage = "ready"
        self.grace_period = 120

    def display_score(self):
        fill(255)
        textSize(20)
        textAlign(RIGHT, TOP)
        text("Score: " + str(self.score), self.width - 10, 10)

    def end_game(self):
        self.stage = "death"
        self.update_leaderboard()
        # Reset both superpowers for the next game
        self.superpower = SuperPower(self)
        self.ghost_pass_superpower = GhostPassSuperPower(self)

    def update_leaderboard(self):
        self.leaderboard.append(self.score)
        self.leaderboard = sorted(self.leaderboard, reverse=True)[:5]

    def check_dot_collision(self):
        for dot in self.maze.dots[:]:
            if abs(self.pacman.x - dot[0]) < self.pacman.radius * 0.75 and abs(self.pacman.y - dot[1]) < self.pacman.radius * 0.75:
                self.maze.dots.remove(dot)
                self.score += 1
                if self.soundOn:
                    self.chump.rewind()
                    self.chump.play()

    def check_ghost_collision(self, ghost):
        return dist(self.pacman.x, self.pacman.y, ghost.x, ghost.y) < (self.pacman.radius + 15)
    
class SuperPower:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.radius = 15  # Radius of the superpower
        self.active = False  # Tracks if the superpower is active
        self.timer = 0  # Timer for how long the power lasts
        self.spawned = False  # Ensures it spawns only once per game
        self.jarvis_image = loadImage(PATH + "/pacman/"+ "jarvis_suit.png")  # Load the image

    def spawn(self):
        """Spawn the superpower at a random walkable location."""
        if not self.spawned:
            walkable_positions = []
            for row in range(len(self.game.maze.grid)):
                for col in range(len(self.game.maze.grid[row])):
                    if self.game.maze.grid[row][col] == 1:  # Check for walkable cell
                        x = col * self.game.tamanho + self.game.tamanho // 2
                        y = row * self.game.tamanho + self.game.tamanho // 2
                        walkable_positions.append((x, y))
            if walkable_positions:
                self.x, self.y = built_random.choice(walkable_positions)
                self.spawned = True  # Mark as spawned

    def activate(self):
        """Activate the superpower for 2 seconds."""
        self.active = True
        self.timer = 2 * 60  # 2 seconds at 60 FPS

    def update(self):
        """Update the timer if the superpower is active."""
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        
        """Draw the superpower as an image."""
        if not self.active and self.spawned:  # Only draw if spawned and not active
            image(self.jarvis_image, self.x -15, self.y -15, self.radius * 2, self.radius * 2)
            
class GhostPassSuperPower:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.radius = 15
        self.active = False
        self.timer = 0
        self.spawned = False
        self.invisible_suit_image = loadImage(PATH +"/pacman/"+"invisible_suit.png")

    def spawn(self):
        """Spawn the superpower at a random walkable location if it hasn't been spawned."""
        if not self.spawned:
            walkable_positions = []
            for row in range(len(self.game.maze.grid)):
                for col in range(len(self.game.maze.grid[row])):
                    if self.game.maze.grid[row][col] == 1:  # Check for walkable cell
                        x = col * self.game.tamanho + self.game.tamanho // 2
                        y = row * self.game.tamanho + self.game.tamanho // 2
                        walkable_positions.append((x, y))
            if walkable_positions:
                self.x, self.y = built_random.choice(walkable_positions)
                self.spawned = True

    def activate(self):
        """Activate the ghost-pass superpower for 2 seconds."""
        self.active = True
        self.timer = 5 * 60  # 5 seconds at 60 FPS

    def update(self):
        """Update the timer if the superpower is active."""
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        if not self.active and self.spawned:  # Only draw if spawned and not active
        # Center the image on (x, y)
            image(self.invisible_suit_image, self.x -15, self.y -15, self.radius * 2, self.radius * 2)

class Pacman:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.radius = 30
        self.sprite_index = 0
        self.sprite_images = [
            self.resize_sprite(loadImage(PATH +"/pacman/"+"spider_man_sprite_0.png")),
            self.resize_sprite(loadImage(PATH +"/pacman/"+"spider_man_sprite_1.png")),
            self.resize_sprite(loadImage(PATH +"/pacman/"+"spider_man_sprite_2.png")),
            self.resize_sprite(loadImage(PATH +"/pacman/"+"spider_man_sprite_3.png")),
        ]
        self.animation_speed = 10  # Frames to switch sprite
        self.frame_count = 0
        
    def resize_sprite(self, sprite):
        """Resize a sprite to 30x30 pixels."""
        sprite.resize(30, 30)
        return sprite
    
    def flip_sprite(self, sprite):
        """Flip the sprite horizontally."""
        flipped = createImage(sprite.width, sprite.height, ARGB)
        sprite.loadPixels()
        flipped.loadPixels()
        for x in range(sprite.width):
            for y in range(sprite.height):
                flipped.set(sprite.width - x - 1, y, sprite.get(x, y))
        flipped.updatePixels()
        return flipped

    def setup(self):
        self.x = self.game.maze.center_x(7)
        self.y = self.game.maze.center_y(5)
        self.vx = 0
        self.vy = 0
    def update(self):
        # Calculate the next position
        next_x = self.x + self.vx
        next_y = self.y + self.vy
    
        # Determine the current grid cell based on Pacman's position
        current_col = int(self.x // self.game.tamanho)
        current_row = int(self.y // self.game.tamanho)
    
        # Check direction of movement and calculate stopping distance
        if self.vx > 0:  # Moving right
            col = int((self.x + 25) // self.game.tamanho)
            row = current_row
        elif self.vx < 0:  # Moving left
            col = int((self.x - 25) // self.game.tamanho)
            row = current_row
        elif self.vy > 0:  # Moving down
            col = current_col
            row = int((self.y + 25) // self.game.tamanho)
        elif self.vy < 0:  # Moving up
            col = current_col
            row = int((self.y - 25) // self.game.tamanho)
        else:
            # Not moving
            col, row = current_col, current_row
    
        # Check if the next position is within bounds and not a wall
        if 0 <= row < len(self.game.maze.grid) and 0 <= col < len(self.game.maze.grid[0]):
            if self.game.maze.grid[row][col] != 0:
                # Update Pacman's position
                self.x = next_x
                self.y = next_y
            else:
                # Stop Pacman 50 pixels before the wall
                if self.vx > 0:  # Moving right
                    self.x = (col * self.game.tamanho) - 25
                elif self.vx < 0:  # Moving left
                    self.x = (col + 1) * self.game.tamanho + 25
                elif self.vy > 0:  # Moving down
                    self.y = (row * self.game.tamanho) - 25
                elif self.vy < 0:  # Moving up
                    self.y = (row + 1) * self.game.tamanho + 25
                self.vx = 0
                self.vy = 0
        else:
            # Out of bounds; stop movement
            self.vx = 0
            self.vy = 0
    
        # Update animation frame
        self.frame_count += 1
        if self.frame_count % self.animation_speed == 0:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_images)

    def draw(self):
        # Get the current sprite
        current_sprite = self.sprite_images[self.sprite_index]

        # Flip the sprite if moving left
        if self.vx < 0:  # Moving left
            current_sprite = self.flip_sprite(current_sprite)

        # Calculate the top-left corner for the sprite to center it on (self.x, self.y)
        sprite_width = current_sprite.width
        sprite_height = current_sprite.height
        top_left_x = self.x - sprite_width / 2
        top_left_y = self.y - sprite_height / 2

        # Draw the sprite at the calculated position
        image(current_sprite, top_left_x, top_left_y)

class Ghost:
    def __init__(self, game, name, color, grid_x, grid_y):
        self.game = game
        self.name = name
        self.color = color
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = self.game.maze.center_x(grid_x)
        self.y = self.game.maze.center_y(grid_y)
        self.vx = 0
        self.vy = 0
        self.speed = 2  # Speed of movement in pixels
        self.direction = (1, 0)  # Initial direction to start moving
        self.previous_direction = None  # Avoid reversing direction instantly
        self.facing_left = False  # Track the ghost's facing direction

        # Load and resize sprite frames
        self.sprite_frames = [
            self.resize_sprite(loadImage(PATH + "/pacman/mysterio_specific_adjustment_frame_1.png")),
            self.resize_sprite(loadImage(PATH + "/pacman/mysterio_specific_adjustment_frame_2.png")),
            self.resize_sprite(loadImage(PATH + "/pacman/mysterio_specific_adjustment_frame_3.png")),
        ]
        self.flipped_frames = [self.flip_sprite(frame) for frame in self.sprite_frames]  # Create flipped frames
        self.current_frame = 0
        self.frame_count = 0
        self.animation_speed = 10
        self.sprite_index = 0

    def resize_sprite(self, sprite):
        """Resize a sprite to 30x40 pixels."""
        sprite.resize(30, 40)
        return sprite

    def flip_sprite(self, sprite):
        """Create and return a horizontally flipped copy of the sprite."""
        flipped = sprite.get()  # Create a copy of the sprite
        flipped.loadPixels()
        width, height = flipped.width, flipped.height

        # Flip the pixels horizontally
        for y in range(height):
            for x in range(width // 2):
                left_index = x + y * width
                right_index = (width - 1 - x) + y * width
                flipped.pixels[left_index], flipped.pixels[right_index] = (
                    flipped.pixels[right_index],
                    flipped.pixels[left_index],
                )

        flipped.updatePixels()
        return flipped

    def setup(self):
        """Initialize ghost position and reset movement attributes."""
        self.x = self.game.maze.center_x(self.grid_x)
        self.y = self.game.maze.center_y(self.grid_y)
        self.direction = (1, 0)
        self.previous_direction = None
        
    def update(self):
        """Update ghost movement and handle pathfinding."""
        # Align with grid to prevent jittering
        if self.x % self.game.tamanho == 0 and self.y % self.game.tamanho == 0:
            grid_x, grid_y = self.game.maze.get_grid_position(self.x, self.y)
            self.direction = self.choose_random_direction(grid_x, grid_y)
    
        # Move in the current direction
        if self.direction:
            dx, dy = self.direction
            next_x = self.x + dx * self.speed
            next_y = self.y + dy * self.speed
    
            # Check the cell 25 pixels ahead in the direction of movement
            check_x = self.x + dx * (self.speed + 25)
            check_y = self.y + dy * (self.speed + 25)
            check_col = int(check_x // self.game.tamanho)
            check_row = int(check_y // self.game.tamanho)
    
            # Update facing direction
            if dx > 0:
                self.facing_left = True
            elif dx < 0:
                self.facing_left = False
    
            # Prevent ghost from moving into walls 25 pixels ahead
            if self.is_valid_cell(check_col, check_row):
                self.x = next_x
                self.y = next_y
            else:
                # Choose a new direction if the next cell is not valid
                grid_x, grid_y = self.game.maze.get_grid_position(self.x, self.y)
                self.direction = self.choose_random_direction(grid_x, grid_y)
    
        # Update animation frame
        self.frame_count += 1
        if self.frame_count % self.animation_speed == 0:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_frames)

    def is_valid_cell(self, grid_x, grid_y):
        """Check if the given grid cell is walkable."""
        maze = self.game.maze.grid
        if 0 <= grid_y < len(maze) and 0 <= grid_x < len(maze[0]):
            return maze[grid_y][grid_x] != 0
        return False

    def choose_random_direction(self, grid_x, grid_y):
        """Choose a random valid direction at a grid junction."""
        maze = self.game.maze.grid
        directions = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Up, Down, Left, Right
            nx, ny = grid_x + dx, grid_y + dy
            if self.is_valid_cell(nx, ny):
                directions.append((dx, dy))

        # Avoid reversing direction
        reverse_direction = None
        if self.previous_direction:
            reverse_direction = (-self.previous_direction[0], -self.previous_direction[1])
            directions = [d for d in directions if d != reverse_direction]

        # Ensure a valid direction is chosen when there are multiple possibilities
        if directions:
            new_direction = directions[int(random(len(directions)))]
        else:
            # If only reverse direction is available, allow reversing
            new_direction = reverse_direction

        self.previous_direction = new_direction
        return new_direction

    def draw(self):
        """Render the ghost."""
        # Get the appropriate sprite based on the facing direction
        if self.facing_left:
            current_sprite = self.flipped_frames[self.sprite_index]
        else:
            current_sprite = self.sprite_frames[self.sprite_index]

        image(current_sprite, self.x- 15, self.y -20)  # Adjust position to center the sprite


class Maze:
    def __init__(self, game):
        self.game = game
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.dots = []

    def setup_maze_dimensions(self):
        self.dots = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1:
                    x = col * self.game.tamanho + (self.game.tamanho) // 2
                    y = row * self.game.tamanho + (self.game.tamanho) // 2
                    self.dots.append((x, y))
                    

    def draw_maze(self):
        noStroke()
        fill(100, 100, 255)
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0:
                    x = col * self.game.tamanho
                    y = row * self.game.tamanho
                    rect(x, y, self.game.tamanho, self.game.tamanho)

    def draw_points(self):
        fill(255)
        noStroke()
        for dot in self.dots:
            ellipse(dot[0], dot[1], 10, 10)

    def center_x(self, col):
        return col * self.game.tamanho + self.game.tamanho // 2

    def center_y(self, row):
        return row * self.game.tamanho + self.game.tamanho // 2

    def get_grid_position(self, world_x, world_y):
        grid_x = int(world_x // self.game.tamanho)
        grid_y = int(world_y // self.game.tamanho)
        return grid_x, grid_y

game = PacmanGame()

def setup():
    size(game.width, game.height)
    game.initialize()

def draw():
    game.mouse_hover()
    game.draw()

def keyPressed():
    if game.stage == "menu" and key == ENTER:
        game.start_game()
    if game.stage == "game":
        if keyCode == LEFT:
            game.pacman.vx = -game.vel
            game.pacman.vy = 0
        elif keyCode == RIGHT:
            game.pacman.vx = game.vel
            game.pacman.vy = 0
        elif keyCode == UP:
            game.pacman.vy = -game.vel
            game.pacman.vx = 0
        elif keyCode == DOWN:
            game.pacman.vy = game.vel
            game.pacman.vx = 0

def mousePressed():
    if game.stage == "menu":
        game.menu_select()
    elif game.stage == "death":
        game.death_select()
    elif game.stage == "leaderboard":
        game.leaderboard_select()
    elif game.stage == "win":
        game.win_select()
