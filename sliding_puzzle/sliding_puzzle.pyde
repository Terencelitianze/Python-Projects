import os
import random

PATH = os.getcwd() # get the current working directory of the folder this file is stored in
NUM_ROWS = 4
NUM_COLS = 4
RESOLUTION = 800
TILE_WIDTH = RESOLUTION/NUM_COLS
TILE_HEIGHT = RESOLUTION/NUM_ROWS

# your classes come here
class Tile:
    def __init__(self, r, c):
        self.row = r
        self.column = c
        self.value = self.row * NUM_COLS + self.column
        self.img = loadImage(PATH + "/images/" + str(self.value) + ".png")
        
    def swap(self, other):
        temp_v = self.value
        self.value = other.value
        other.value = temp_v
        
        temp_img = self.img
        self.img = other.img
        other.img = temp_img
    
    def display(self):
        if self.value != 15:
            image(self.img, 200 * self.column , 200 * self.row, TILE_WIDTH, TILE_HEIGHT)
            noFill()
            strokeWeight(5)
            rect(200 * self.column , 200 * self.row, TILE_WIDTH, TILE_HEIGHT)
        
class Puzzle:
    def __init__(self):
        self.tiles = []
        for r in range(0,NUM_ROWS):
            for c in range(0,NUM_COLS):
                self.tiles.append(Tile(r,c))
                
    def get_missing_tile(self):
        for tile in self.tiles:
            if tile.value == 15:
                return tile
            
    def get_tile(self, r, c):
        for tile in self.tiles:
            if tile.row == r and tile.column == c:
                return tile
        return None
    
    def slide(self, dir):
        missing_tile = self.get_missing_tile()
        neighbor_tile = None
        if dir == RIGHT:
            neighbor_tile = self.get_tile(missing_tile.row, missing_tile.column -1)
        if dir == LEFT:
            neighbor_tile = self.get_tile(missing_tile.row, missing_tile.column +1)
        if dir == UP:
            neighbor_tile = self.get_tile(missing_tile.row +1, missing_tile.column)
        if dir == DOWN:
            neighbor_tile = self.get_tile(missing_tile.row -1, missing_tile.column)
            
        if neighbor_tile != None:
            missing_tile.swap(neighbor_tile)
        
    def check_win(self):
        for tile in self.tiles:
            if tile.row * NUM_COLS + tile.column != tile.value:
                return False
        return True
    
    def shuffle(self):
        for i in range(10):
            dir = random.choice([LEFT,RIGHT,UP,DOWN])
            self.slide(dir)

    def display_tiles(self):
        for tile in self.tiles:
            tile.display()

def setup():
    size(RESOLUTION, RESOLUTION)
    background(0,0,0)
    puzzle.shuffle()

def draw():
    background(0,0,0)
    puzzle.display_tiles()
    
def keyPressed():
   puzzle.slide(keyCode)
   
   if puzzle.check_win() == True:
       print("Puzzle is solved")
    
puzzle = Puzzle()




    
    
