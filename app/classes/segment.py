from app.classes.point import Point

class Segment:
    def __init__(self, x, y):
        self.Position = Point(x,y)
        self.IsHit = False