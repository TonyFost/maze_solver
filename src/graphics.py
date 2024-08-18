from tkinter import Tk, BOTH, Canvas

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x},{self.y})"


class Line():
    def __init__(self, pt_1:Point, pt_2:Point):
        self.point1 = pt_1
        self.point2 = pt_2

    def draw(self, canvas:Canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y,
                           self.point2.x, self.point2.y,
                           fill=fill_color, width=2)
        
class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=self.height, width=self.width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.is_window_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw(self, line:Line, fill_color):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.is_window_running = True
        while self.is_window_running:
            self.redraw()

    def close(self):
        self.is_window_running = False
        print("Closing window...")
        
class Cell():
    def __init__(self, x1, y1, x2, y2, win:Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def center(self):
        return ((self._x2 + self._x1)//2, (self._y2 + self._y1)//2)

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw(Line(Point(x1, y1), Point(x1, y2)), "red")
        if self.has_right_wall:
            self._win.draw(Line(Point(x2, y1), Point(x2, y2)), "yellow")
        if self.has_top_wall:
            self._win.draw(Line(Point(x1, y1), Point(x2, y1)), "blue")
        if self.has_bottom_wall:
            self._win.draw(Line(Point(x1, y2), Point(x2, y2)), "black")

    def draw_move(self, to_cell, undo=False):
        color = "red" if not undo else "gray"

        center = Point(*self.center())
        print(center)
        other_center = Point(*to_cell.center())
        print(other_center)

        self._win.draw(Line(center, other_center), color)
