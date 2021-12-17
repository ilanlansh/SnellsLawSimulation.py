
class Point:
    '''
    Class for creating a point object that has values of x and y
    >>> Point(x, y)
    '''

    def __init__(self, x: int, y: int) -> None:
       '''Point class constructor.'''

       self.x: int = x;
       self.y: int = y;

       self.tuple: tuple[int, int] = (self.x, self.y);

    def __repr__(self) -> str:
        '''Printable representation of a Point object'''

        return f"Point({self.x}, {self.y})";

def getMiddlePoint(*points: Point) -> Point:
    '''Function to get the middle point of all points given as arguments'''

    x_sum: int = sum(map(lambda point: point.x, points));
    y_sum: int = sum(map(lambda point: point.y, points));
    length: float = float(len(points));

    middlePoint: Point = Point(x_sum / length, y_sum / length);

    return middlePoint;