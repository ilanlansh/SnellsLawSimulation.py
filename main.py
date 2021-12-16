from constants import *;
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
        command = lambda: draw(canvas, n1Entry, n2Entry, theta1Entry)
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

def drawIncidentRay(canv: tk.Canvas, theta1: float, n1: int):
    '''Draws the Incident ray and returns the Canvas Line object.'''

    source_y: int = RAYLENGTH * math.cos(math.radians(theta1));
    source_x: int = RAYLENGTH * math.cos(math.radians(90 - theta1));
    
    sourcePoint: Point = Point(CENTER.x - source_x, CENTER.y - source_y);

    # arrow line (source -> middle)
    canv.create_line(
        [
            sourcePoint.tuple,
            getMiddlePoint([CENTER, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    incidentRay: tk._CanvasItemId = canv.create_line(
        [
            sourcePoint.tuple,
            CENTER.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    velocity: float = SPEED_OF_LIGHT / n1;

    n1Label: tk.Label = tk.Label(
        text = f"n₁ = {n1}\nv = {velocity} [km / s]",
        font = "Helvetica 14 bold",
        relief = tk.SUNKEN,
        bg = Colors.DARK_GRAY.value,
        fg = Colors.WHITE.value
    );

    canv.create_window(WIDTH / 4.0, 50, window = n1Label);

    return incidentRay;

def drawReflectedRay(canv: tk.Canvas, theta1: float):
    '''Draws the Reflected ray and returns the Canvas Line object.'''

    source_y: int = RAYLENGTH * math.cos(math.radians(theta1));
    source_x: int = RAYLENGTH * math.cos(math.radians(90 - theta1));
    
    sourcePoint: Point = Point(CENTER.x + source_x, CENTER.y - source_y);

    # arrow line (center -> middle)
    canv.create_line(
        [
            CENTER.tuple,
            getMiddlePoint([CENTER, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    reflectedRay: tk._CanvasItemId = canv.create_line(
        [
            CENTER.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    return reflectedRay;

def drawRefractedRay(canv: tk.Canvas, theta1: float, n1: float, n2: float):
    '''Draws the Refracted ray and returns the Canvas Line object.'''

    theta2: float = math.degrees(math.asin(
        n1 * math.sin(math.radians(theta1)) / n2
    ));

    source_y: int = RAYLENGTH * math.cos(math.radians(theta2));
    source_x: int = RAYLENGTH * math.cos(math.radians(90 - theta2));
    
    sourcePoint: Point = Point(CENTER.x + source_x, CENTER.y + source_y);

    # arrow line (center -> middle)
    canv.create_line(
        [
            CENTER.tuple,
            getMiddlePoint([CENTER, sourcePoint]).tuple
        ],
        fill = Colors.ORANGE.value,
        width = 2,
        arrow = tk.LAST
    );

    refractedRay: tk._CanvasItemId = canv.create_line(
        [
            CENTER.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE.value,
        width = 2
    );

    return refractedRay;

def draw(c: tk.Canvas, n1Entry: tk.Entry, n2Entry: tk.Entry, theta1Entry: tk.Entry):
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

    drawIncidentRay(c, theta1, n1);
    
    if(n1 != n2):    
        drawReflectedRay(c, theta1);

    if(theta1 < thetac):
        drawRefractedRay(c, theta1, n1, n2);


if (__name__ == '__main__'):
    main();