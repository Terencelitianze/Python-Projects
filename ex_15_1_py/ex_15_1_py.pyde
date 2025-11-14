class System:
    def __init__(self,x=0,y=0):
        self.x_coordinate = x
        self.y_coordinate = y
    
    def distance_from_origin(self):
        distance = (self.x_coordinate**2 + self.y_coordinate**2)**0.5
        print(distance)

    def midpoint(self,other):
        mx = (self.x_coordinate + other.x_coordinate)/2
        my = (self.y_coordinate + other.y_coordinate)/2
        return System(mx,my)
    
    def distance(self,other):
        distance_away = ((self.x_coordinate-other.x_coordinate)**2+(self.y_coordinate-other.y_coordinate)**2)
        return distance_away
    

class Rectangle:
    def __init__(self,point1,width=0,height=0):
        self.x = point1.x_coordinate
        self.y = point1.y_coordinate
        self.width = width
        self.height = height
    
    def resize(self,width,height):
        self.width = self.width + width
        self.height = self.height + height
    
    def move(self,x,y):
        self.x = x
        self.y = y
        
    def display(self):
        fill(255,0,0)
        noStrock()
        rect(self.x, self.y, self,width, self.height)
        
def setup():
    size(800, 800)
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    r1.move(mouseX, mouseY)
    r1.display()
    
def keyPressed():
    if keyCode == UP:
        r1.resize(10, 10)
    elif keyCode == DOWN:
        r1.resize(-10, -10)
    
r1 = Rectangle(100, 100, 100, 100)
