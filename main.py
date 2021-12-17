from constants import *;
from point import Point, getMiddlePoint;

import tkinter as tk;
import math;

def main() -> None:
    '''Main function.'''

    root: tk.Tk = tk.Tk();
    root.title("Snell's Law Simulation");
    root.attributes("-fullscreen", True);
    root["background"] = Colors.GRAY;

    tk.Label(
        root,
        text = "n₁sin(θ₁) = n₂sin(θ₂)",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE
    ).pack();

    canvasFrame: tk.Frame = tk.Frame(root, bg = Colors.GRAY);
    canvasFrame.pack();

    canvas: tk.Canvas = tk.Canvas(
        canvasFrame,
        width = WIDTH,
        height = HEIGHT,
        background = Colors.DARK_GRAY
    );
    canvas.pack();

    clearBoard(canvas);

    entriesContainer: tk.Frame = tk.Frame(root, bg = Colors.GRAY);
    entriesContainer.pack(pady = 5);

    tk.Label(
        entriesContainer,
        text = "n₁: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE
    ).pack(side = tk.LEFT);

    n1Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY,
        fg = Colors.DARK_GRAY,
        width = 5
    );
    n1Entry.pack(side = tk.LEFT);

    tk.Label(
        entriesContainer,
        text = "  n₂: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE
    ).pack(side = tk.LEFT);

    n2Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY,
        fg = Colors.DARK_GRAY,
        width = 5
    );
    n2Entry.pack(side = tk.LEFT);

    tk.Label(
        entriesContainer,
        text = "  θ₁: ",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE
    ).pack(side = tk.LEFT);

    theta1Entry: tk.Entry = tk.Entry(
        entriesContainer,
        font = "Helvetica 24",
        bg = Colors.LIGHT_GRAY,
        fg = Colors.DARK_GRAY,
        width = 5
    );
    theta1Entry.pack(side = tk.LEFT);

    drawButton: tk.Button = tk.Button(
        root,
        text = "DRAW",
        font = "Helvetica 24 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE,
        command = lambda: draw(canvas, n1Entry, n2Entry, theta1Entry)
    );
    drawButton.pack();

    tk.Button(
        root,
        text = "Exit",
        font = "Helvetica 16 bold",
        bg = Colors.DARK_RED,
        fg = Colors.WHITE,
        command = root.destroy
    ).pack(pady = 5);

    tk.Label(
        text = "Created by: Ilan Shrir & Gilbar Goncharov",
        font = "Helvetica 12 bold",
        bg = Colors.GRAY,
        fg = Colors.WHITE
    ).pack();

    n1Entry.insert(0, "1");
    n2Entry.insert(0, "1.5");
    theta1Entry.insert(0, "60");

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
        fill = Colors.LIGHT_SEA_GREEN
    );
    canvas.create_line(
        [
            TOPMOST.tuple,
            BOTTOMMOST.tuple
        ],
        width = 2,
        dash = 255,
        fill = Colors.GREEN_YELLOW
    );

def drawIncidentRay(canv: tk.Canvas, theta1: float):
    '''Draws the Incident ray and returns the Canvas Line object.'''

    source_y: int = RAYLENGTH * math.cos(math.radians(theta1));
    source_x: int = RAYLENGTH * math.cos(math.radians(90 - theta1));
    
    sourcePoint: Point = Point(CENTER.x - source_x, CENTER.y - source_y);

    # arrow line (source -> middle)
    canv.create_line(
        [
            sourcePoint.tuple,
            getMiddlePoint(CENTER, sourcePoint).tuple
        ],
        fill = Colors.ORANGE,
        width = 2,
        arrow = tk.LAST
    );

    incidentRay: tk._CanvasItemId = canv.create_line(
        [
            sourcePoint.tuple,
            CENTER.tuple
        ],
        fill = Colors.WHITE,
        width = 2
    );

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
            getMiddlePoint(CENTER, sourcePoint).tuple
        ],
        fill = Colors.ORANGE,
        width = 2,
        arrow = tk.LAST
    );

    reflectedRay: tk._CanvasItemId = canv.create_line(
        [
            CENTER.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE,
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
            getMiddlePoint(CENTER, sourcePoint).tuple
        ],
        fill = Colors.ORANGE,
        width = 2,
        arrow = tk.LAST
    );

    refractedRay: tk._CanvasItemId = canv.create_line(
        [
            CENTER.tuple,
            sourcePoint.tuple
        ],
        fill = Colors.WHITE,
        width = 2
    );

    return refractedRay;

def drawCanvasLabels(c: tk.Canvas, n1: float, n2: float) -> None:
    '''Draws data labels on the canvas that contain n1 and n2 values, and the speed of light in those materials'''

    v1: float = SPEED_OF_LIGHT / n1;
    c.create_window(
        WIDTH / 4.0,
        50,
        window = tk.Label(
            text = "n₁ = %s\nv = %.2f [km / s]" % (str(n1), v1),
            font = "Helvetica 14 bold",
            relief = tk.SUNKEN,
            bg = Colors.DARK_GRAY,
            fg = Colors.WHITE
        )
    );

    v2: float = SPEED_OF_LIGHT / n2;
    c.create_window(
        WIDTH / 4.0,
        HEIGHT - 50,
        window = tk.Label(
            text = "n₂ = %s\nv = %.2f [km / s]" % (str(n2), v2),
            font = "Helvetica 14 bold",
            relief = tk.SUNKEN,
            bg = Colors.DARK_GRAY,
            fg = Colors.WHITE
        )
    );

def draw(c: tk.Canvas, n1Entry: tk.Entry, n2Entry: tk.Entry, theta1Entry: tk.Entry) -> None:
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

    drawIncidentRay(c, theta1);
    
    if(n1 != n2):    
        drawReflectedRay(c, theta1);

    if(theta1 < thetac):
        drawRefractedRay(c, theta1, n1, n2);

    drawCanvasLabels(c, n1, n2);

if (__name__ == '__main__'):
    main();