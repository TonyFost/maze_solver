from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

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
        self._visited = False

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
    _left = -1
    _right = 1
    _top = -2
    _bottom = 2

    def __init__(self, x1, y1, num_rows, num_cols, cel_size_x, cel_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cel_size_x = cel_size_x
        self._cel_size_y = cel_size_y
        self._win = win
        self._create_cells()
        if seed:
            random.seed(seed)

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
                self._draw_cell(c, r, .01)

        self._break_entrance_and_exit()
        if self._num_rows > 0 and self._num_cols > 0:
            self._break_walls_r(0,0)

    def _draw_cell(self, i, j, wait=.05):
        x1 = self._x1 + (i * self._cel_size_x)
        y1 = self._y1 + (j * self._cel_size_y)
        x2 = x1 + self._cel_size_x
        y2 = y1 + self._cel_size_y

        if wait == 0:
            input("Press enter to continue")
            print("Drawing Cell ", i, j, "at coordinates", x1, y1, " and ", x2, y2)
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate(wait)

    def _animate(self, wait):
        if self._win:
            self._win.redraw()
            sleep(wait)

    def _break_wall(self, cell, direction):
        match (direction):
            case -2:
                cell.has_top_wall = False
            case -1:
                cell.has_left_wall = False
            case 1:
                cell.has_right_wall = False
            case 2:
                cell.has_bottom_wall = False

    def _break_entrance_and_exit(self):
        if self._num_rows < 1 or self._num_cols < 1:
            return
        entrance = self._cells[0][0]
        self._break_wall(entrance, Maze._top)
        self._draw_cell(0,0)
        
        last_col = self._num_cols - 1
        last_row = self._num_rows - 1
        exit = self._cells[last_col][last_row]
        self._break_wall(exit, Maze._bottom)
        self._draw_cell(last_col,last_row)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        to_visit = []
        check_left = i-1
        check_right = i+1
        check_up = j-1
        check_down = j+1

        if check_left >= 0 and not self._cells[check_left][j]._visited:
            to_visit.append( ((check_left, j), Maze._left) )
        if check_right < self._num_cols and not self._cells[check_right][j]._visited:
            to_visit.append( ((check_right, j), Maze._right) )
        if check_up >= 0 and not self._cells[i][check_up]._visited:
            to_visit.append( ((i, check_up), Maze._top) )
        if check_down < self._num_rows and not self._cells[i][check_down]._visited:
            to_visit.append( ((i, check_down), Maze._bottom) )

        random.shuffle(to_visit)

        for cell in to_visit:
            cell_i = cell[0][0]
            cell_j = cell[0][1]
            self._break_wall(self._cells[i][j], cell[1])
            self._break_wall(self._cells[cell_i][cell_j], cell[1]*-1)
            self._draw_cell(i,j)
            self._break_walls_r(*cell[0])

        # self._draw_cell(i,j)
        

        
