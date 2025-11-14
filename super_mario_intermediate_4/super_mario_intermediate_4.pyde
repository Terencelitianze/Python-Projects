import random, os
PATH = os.getcwd()

WIDTH = 1280
HEIGHT = 720
GROUND = 585

class Creature:
    def __init__(self, x, y, r, g, img, w, h, num_slices):
        self.x = x
        self.y = y
        self.r = r #radius of creature
        self.g = g #ground for creature # GROUND
        self.vy = 0 #velocity y axis
        self.vx = 0 #velocity x axis
        self.img_w = w
        self.img_h = h
        self.num_slices = num_slices #number of frames/slices for the image (sprite) to display the creature. we will over them by applying cropping to enable animation
        self.img = loadImage(PATH + "/images/" + img)
        self.slice = 0 #current slice/frame of the image that is being displayed 
        self.dir = RIGHT #current moving direction of the creature 
        
    def gravity(self):
        #if creture is on or below ground, stop gravity
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            #simulate gravity by incrementing vy with ever call of the the display method
            self.vy += 0.3
            #prevent the creature to overshoot the ground (see lecture slides)
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
                
        # make the creature land on a platform 
        for p in game.platforms:
            if self.y + self.r <= p.y and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w:
                self.g = p.y
                break
            else:
                self.g = game.g

       
    def update(self):
        #simulate gravity and update the coordinates accordingly
        self.gravity()
        self.x += self.vx
        self.y += self.vy
    
    def display(self):
        self.update()
        #change the image depending on the direction the creture moves. game.x_shift is controlled by mario when he moves to right and updated when crossing half of the screen width  
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)        
        
        
class Mario(Creature):
    def __init__(self, x, y, r, g, img, w, h, num_slices):
        Creature.__init__(self, x, y, r, g, img, w, h, num_slices)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False} #dictionary to store the current movement of mario
        self.alive = True

        
    def update(self):
        self.gravity()
        
        #update velocity depending on the walking direction
        if self.key_handler[LEFT] == True:
            self.vx = -5
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 5
            self.dir = RIGHT
        else:
            self.vx = 0
        
        #make mario jump (only if he is on the ground)
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -10
        
        self.x += self.vx
        self.y += self.vy
        
        #update frame counter to simulate animation of mario
        if frameCount%5 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.num_slices
        elif self.vx == 0:
            #no animation if mario stands still
            self.slice = 0
        
        #prevent mario from leaving the screen on the left side
        if self.x - self.r <= 0:
            self.x = self.r
                    

        #check for collision with gombas and kill them if mario jumps on them (vy > 0)
        for g in game.gombas:
            if self.distance(g) <= self.r + g.r:
                if self.vy > 0:
                    game.gombas.remove(g)
                    self.vy = -8
                else:
                    self.alive = False
        
    def distance(self, target):
        return ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5
    
        
class Gomba(Creature):
    def __init__(self, x, y, r, g, img, w, h, num_slices, xl, xr):
        Creature.__init__(self, x, y, r, g, img, w, h, num_slices)
        self.vx = random.randint(1,10) #random velocity
        self.xl = xl #left boundary for movement
        self.xr = xr #right bounday for movement
            
    def update(self):
        self.gravity()
        #make the gomba move between the boundaries
        if self.x < self.xl:
            self.dir = RIGHT
            self.vx *= -1
        elif self.x > self.xr:
            self.dir = LEFT
            self.vx *= -1
        
        #apply image cropping every 10th frame on the sprites; 
        #that makes it look like they move slower as they have lesser frames as compared to mario
        if frameCount%10 == 0:
            self.slice = (self.slice + 1) % self.num_slices
            
        self.x += self.vx
        self.y += self.vy
        

        
class Platform:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(PATH + "/images/" + img)
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
        
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.x_shift = 0
        self.mario = Mario(100, 100, 35, self.g, "mario.png", 100, 70, 11)
        
        self.platforms = []
        # 200, 500
        # 500, 400
        # 800, 300
        for i in range(3):
            self.platforms.append(Platform(200 + i *300, 500-i*100, 200, 50, "platform.png"))


        self.gombas = []
        for g in range(5):
            self.gombas.append(Gomba(random.randint(200, 800), 100, 35, self.g, "gomba.png", 70, 70, 5, 200, 800))

                                                                
    def display(self):
        if self.mario.alive == False:
            textSize(15)
            text("Game over", 600, 350)
            return
        

        strokeWeight(0)
        fill(0, 125, 0)
        rect(0, self.g, self.w, self.h)
        
                
        for p in self.platforms:
            p.display()


        for g in self.gombas:
            g.display()


        self.mario.display()
        
        
        
game = Game(WIDTH, HEIGHT, GROUND)

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()
    
def keyPressed():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.mario.key_handler[UP] = True
        
def keyReleased():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.mario.key_handler[UP] = False
        

def mouseClicked():
    global game
    if game.mario.alive == False:
        game = Game(WIDTH, HEIGHT, GROUND)
        
        
