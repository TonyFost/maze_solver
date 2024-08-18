from window import Window
from drawing import Point, Line

def main():
    win = Window(800, 600)
    new_point = Point(10, 100)
    next_point = Point(10, 200)
    line = Line(new_point, next_point)
    win.draw(line, "black")

    win.wait_for_close()



if __name__ == "__main__":
    main()