
class Point:
    '''
    Class for creating a point object that has values of x and y
    >>> Point(x, y)
    '''
    
    def __init__(self, x: int, y: int) -> None:
       '''Point class constructor.'''

       self.x = x;
       self.y = y;

       self.tuple = (self.x, self.y);