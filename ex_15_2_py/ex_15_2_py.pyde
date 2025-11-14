Class Paticle:
    def __init__(self,x,y,d,center_x,center_y.radius,):
        self.x = x
        self.y = y
        self.d = diameter
        self.cx = center_x
        self.cy = center_y
        self.r = radius
        self.t = 0
    
    def update(self):
        self.t = (self.t + 0.1)% 6.28
        self.x = self.cx + self.r*cos(self.t)
        self.y = self.cy + self.r*cos(self.t)
