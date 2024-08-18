from tkinter import Tk, BOTH, Canvas
from time import sleep

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
    def __init__(self, x1, y1, x2, y2, win=None):
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
        color = "black"
        if not self._win:
            return
        
        if self.has_left_wall:
            color = "black"
        else:
            color = "white"
        self._win.draw(Line(Point(x1, y1), Point(x1, y2)), color)

        if self.has_right_wall:
            color = "black"
        else:
            color = "white"
        self._win.draw(Line(Point(x2, y1), Point(x2, y2)), color)

        if self.has_top_wall:
            color = "black"
        else:
            color = "white"
        self._win.draw(Line(Point(x1, y1), Point(x2, y1)), color)

        if self.has_bottom_wall:
            color = "black"
        else:
            color = "white"
        self._win.draw(Line(Point(x1, y2), Point(x2, y2)), color)

    def draw_move(self, to_cell, undo=False):
        color = "red" if not undo else "gray"

        center = Point(*self.center())
        other_center = Point(*to_cell.center())

        if self._win:
            self._win.draw(Line(center, other_center), color)

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cel_size_x, cel_size_y, win=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cel_size_x = cel_size_x
        self._cel_size_y = cel_size_y
        self._win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = [
                        [Cell(self._x1 + (self._cel_size_x * col),
                            self._y1 + (self._cel_size_y * row),
                            self._cel_size_x + (self._cel_size_x * col),
                            self._cel_size_y + (self._cel_size_y * row),
                            self._win)
                            for row in range(self._num_rows)]
                        for col in range(self._num_cols)
        ]

        for c in range(self._num_cols):
            for r in range(self._num_rows):
                self._draw_cell(c, r)

        self._break_entrance_and_exit()

    def _draw_cell(self, i, j):
        x1 = self._x1 + (i * self._cel_size_x)
        y1 = self._y1 + (j * self._cel_size_y)
        x2 = x1 + self._cel_size_x
        y2 = y1 + self._cel_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            sleep(.01)

    def _break_entrance_and_exit(self):
        if self._num_rows < 1 or self._num_cols < 1:
            return
        
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        
        last_col = self._num_cols - 1
        last_row = self._num_rows - 1
        self._cells[last_col][last_row].has_bottom_wall = False
        self._draw_cell(last_col,last_row)

    