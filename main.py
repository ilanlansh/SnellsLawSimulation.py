from constants import Colors;
from point import Point, getMiddlePoint;

import tkinter as tk;
import math;

def main() -> None:
    '''Main function.'''

    root: tk.Tk = tk.Tk();
    root.title("Snell's Law Simulation");
    root.attributes("-fullscreen", True);
    root["background"] = Colors.GRAY.value;

    tk.Label(
        root,
        text = "n₁sin(θ₁) = n₂sin(θ₂)",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY.value,
        fg = Colors.WHITE.value
    ).pack();

    canvasFrame: tk.Frame = tk.Frame(root, bg = Colors.GRAY.value);
    canvasFrame.pack();

    HEIGHT: int = 600;
    WIDTH:  int = 600;
    CENTER: Point = Point(WIDTH * 0.5, HEIGHT * 0.5);
    RAYLENGTH: int = 250;

    canvas: tk.Canvas = tk.Canvas(
        canvasFrame,
        width = WIDTH,
        height = HEIGHT,
        background = Colors.DARK_GRAY.value
    );
    canvas.pack();

    clearBoard(canvas);

    entriesContainer: tk.Frame = tk.Frame(root, bg = Colors.GRAY.value);
    entriesContainer.pack(pady = 5);

    tk.Label(
        entriesContainer,
        text = "n₁: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY.value,
        fg = Colors.WHITE.value
    ).pack(side = tk.LEFT);

    n1Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY.value,
        fg = Colors.DARK_GRAY.value,
        width = 5
    );
    n1Entry.pack(side = tk.LEFT);

    tk.Label(
        entriesContainer,
        text = "  n₂: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY.value,
        fg = Colors.WHITE.value
    ).pack(side = tk.LEFT);

    n2Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY.value,
        fg = Colors.DARK_GRAY.value,
        width = 5
    );
    n2Entry.pack(side = tk.LEFT);

    tk.Label(
        entriesContainer,
        text = "  θ₁: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY.value,
        fg = Colors.WHITE.value
    ).pack(side = tk.LEFT);

    theta1Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY.value,
        fg = Colors.DARK_GRAY.value,
        width = 5
    );
    theta1Entry.pack(side = tk.LEFT);

    drawButton: tk.Button = tk.Button(
        root,
        text = "DRAW",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY.value,
        fg = Colors.WHITE.value,
        command = lambda: draw(canvas, n1Entry, n2Entry, theta1Entry, RAYLENGTH, CENTER)
    );
    drawButton.pack();

    tk.Button(
        root,
        text = "Exit",
        font = "Helvetica 16 bold",
        bg = Colors.DARK_RED.value,
        fg = Colors.WHITE.value,
        command = root.destroy
    ).pack(pady = 5);

    root.mainloop();

def clearBoard(canvas: tk.Canvas):
    '''Clears canvas and draws center lines.'''

    canvas.delete(tk.ALL);

    HEIGHT: int = 600;
    WIDTH:  int = 600;

    TOPMOST:    Point = Point(WIDTH * 0.5, 0);
    BOTTOMMOST: Point = Point(WIDTH * 0.5, HEIGHT);
    LEFTMOST:   Point = Point(0, HEIGHT * 0.5);
    RIGHTMOST:  Point = Point(WIDTH, HEIGHT * 0.5);

    canvas.create_line(
        [
            LEFTMOST.tuple, 
            RIGHTMOST.tuple
        ],
        width = 2,
        fill = Colors.LIGHT_SEA_GREEN.value
    );
    canvas.create_line(
        [
            TOPMOST.tuple,
            BOTTOMMOST.tuple
        ],
        width = 2,
        dash = 255,
        fill = Colors.GREEN_YELLOW.value
    );

def drawIncidentRay(canv: tk.Canvas, theta1: float, center: Point, length: int):
    '''Draws the Incident ray and returns the Canvas Line object.'''

    source_y: int = length * math.cos(math.radians(theta1));
    source_x: int = length * math.cos(math.radians(90 - theta1));
    
    sourcePoint: Point = Point(center.x - source_x, center.y - source_y);

    # arrow line (source -> middle)
    canv.create_line(
        [
            sourcePoint.tuple,
            getMiddlePoint([center, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    incidentRay: tk._CanvasItemId = canv.create_line(
        [
            sourcePoint.tuple,
            center.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    return incidentRay;

def drawReflectedRay(canv: tk.Canvas, theta1: float, center: Point, length: int):
    '''Draws the Reflected ray and returns the Canvas Line object.'''

    source_y: int = length * math.cos(math.radians(theta1));
    source_x: int = length * math.cos(math.radians(90 - theta1));
    
    sourcePoint: Point = Point(center.x + source_x, center.y - source_y);

    # arrow line (center -> middle)
    canv.create_line(
        [
            center.tuple,
            getMiddlePoint([center, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    reflectedRay: tk._CanvasItemId = canv.create_line(
        [
            center.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    return reflectedRay;

def drawRefractedRay(canv: tk.Canvas, theta1: float, center: Point, length: int, n1: float, n2: float):
    '''Draws the Refracted ray and returns the Canvas Line object.'''

    theta2: float = math.degrees(math.asin(
        n1 * math.sin(math.radians(theta1)) / n2
    ));

    source_y: int = length * math.cos(math.radians(theta2));
    source_x: int = length * math.cos(math.radians(90 - theta2));
    
    sourcePoint: Point = Point(center.x + source_x, center.y + source_y);

    # arrow line (center -> middle)
    canv.create_line(
        [
            center.tuple,
            getMiddlePoint([center, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    refractedRay: tk._CanvasItemId = canv.create_line(
        [
            center.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    return refractedRay;

def draw(c: tk.Canvas, n1Entry: tk.Entry, n2Entry: tk.Entry, theta1Entry: tk.Entry, length: int, center: Point):
    '''Draw button callback. Draws the rays on the canvas.'''

    n1: float = float(n1Entry.get());
    n2: float = float(n2Entry.get());
    theta1: float = float(theta1Entry.get());
    thetac: float = 90.0;

    if(n1 > n2):
        thetac: float = math.degrees(math.asin(
        n2 * math.sin(math.radians(90)) / n1
    ));

    clearBoard(c);

    drawIncidentRay(c, theta1, center, length);

    if(n1 != n2):    
        drawReflectedRay(c, theta1, center, length);

    if(theta1 < thetac):
        drawRefractedRay(c, theta1, center, length, n1, n2);


if (__name__ == '__main__'):
    main();