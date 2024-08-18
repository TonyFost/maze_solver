from tkinter import Tk, BOTH, Canvas
from drawing import Line
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

        
