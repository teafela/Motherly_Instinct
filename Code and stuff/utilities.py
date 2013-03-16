import pygame, math, sys, random, os

def bezier(A, B, C, t):
    """A,B, and C are 2-tuples (x,y), t is a float between 0 and 1"""
    x = (1 - t)**2 * A[0] + 2 * t * (1 - t) * B[0] + t**2 * C[0]
    y = (1 - t)**2 * A[1] + 2 * t * (1 - t) * B[1] + t**2 * C[1]
    return x, y

def cubicBezier(A, B, C, D, t):
    """A, B, C, and D are 2-tuples (x,y), t is a float between 0 and 1"""
    x = (1-t)**3 * A[0] + 3*t*(1-t)**2 * B[0] + 3*t**2*(1-t) * C[0] + t**3*D[0]
    y = (1-t)**3 * A[1] + 3*t*(1-t)**2 * B[1] + 3*t**2*(1-t) * C[1] + t**3*D[1]
    return x, y
    
def resource_path(file):
    
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    
    return os.path.join(basedir, 'resources', file)
    
def highscore_path():
    if getattr(sys, 'frozen', None):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'highscores.txt'))
    else:
        path = 'highscores.txt'
    return path

# ---------------------------------------------------------------------------------------    
# Vector2D class, represents a 2D vector and provides functions for manipulating it

class Vector2D(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def angle(self):
        return math.atan2(self.y, self.x) #range -pi to pi
        
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
        
    # adds other to self (modifies self)
    def add(self, other):
        self.x += other.x
        self.y += other.y
    
    # returns a new Vector2D object that represents self-other (does not modify self)
    def subtract(self, other):
        new_vector = Vector2D()
        new_vector.x = self.x - other.x
        new_vector.y = self.y - other.y
        return new_vector
    
    # multiplies self by a scalar
    def mult(self, scalar):
        new_mag = self.magnitude() * scalar
        angle = self.angle()
        self.x = math.cos(angle) * new_mag
        self.y = math.sin(angle) * new_mag
        
    def set_magnitude(self, scalar):
        angle = self.angle()
        self.x = math.cos(angle) * scalar
        self.y = math.sin(angle) * scalar
        
    def limit_x(self, x):
        if self.x < -x:
            self.x = -x
        if self.x > x:
            self.x = x
    
    def limit_x_range(self, x_min, x_max):
        if self.x < x_min:
            self.x = x_min
        if self.x > x_max:
            self.x = x_max
            
    def limit_y_range(self, y_min, y_max):
        if self.y < y_min:
            self.y = y_min
        if self.y > y_max:
            self.y = y_max
    
    def limit_y(self, y):
        if self.y < -y:
            self.y = -y
        if self.y > y:
            self.y = y
    
    def limit_magnitude(self, scalar):
        if self.magnitude > scalar:
            self.set_magnitude(scalar)
        
    def set_angle(self, angle):
        magnitude = self.magnitude()
        self.x = math.cos(angle) * magnitude
        self.y = math.sin(angle) * magnitude
        
    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x /= mag
            self.y /= mag
            
    def clear(self):
        self.x = 0
        self.y = 0
        
    # returns the opposite of self (does not modify self)
    def opposite(self):
        return Vector2D(-self.x, -self.y)
        
    def floor_x_y(self):
        self.x = math.floor(self.x)
        self.y = math.floor(self.y)
    
    def distance(self, second):
        dx = second.x - self.x
        dy = second.y - self.y
        
        return math.sqrt(dx**2 + dy**2)
        
        
        
        
        