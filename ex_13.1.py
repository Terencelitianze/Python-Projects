class System:
    def __init__(self,x=0,y=0):
        self.x_coordinate = x
        self.y_coordinate = y

    def __str__(self):
        return f"({self.x_coordinate},{self.y_coordinate})"
    
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

    def __str__(self):
        return f"(({self.x},{self.y}),{self.width},{self.height})"
    
    def resize(self,width,height):
        self.width = self.width + width
        self.height = self.height + height
    
    def move(self,x,y):
        self.x = self.x + x
        self.y = self.y + y

point1 = System(4,3)
point2 = System(5.8)
point1.distance_from_origin()
print(point1)
midpoint = point1.midpoint(point2)
distance_of_two_point = point1.distance(point2)
print(midpoint)
print(distance_of_two_point)

r1 = Rectangle(point1,100,50)
print(r1)
r1.resize(25,-10)
print(r1)
r1.move(10,-10)
print(r1)