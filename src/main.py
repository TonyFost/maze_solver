from graphics import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    new_point = Point(10, 100)
    next_point = Point(10, 200)
    line = Line(new_point, next_point)
    win.draw(line, "black")

    cell = Cell(150, 200, 170, 220, win)
    cell.draw(150, 200, 170, 220)
    cell.draw(200, 250, 250, 300)
    cell.has_right_wall = False
    cell.draw(250, 300, 300, 350)
    win.wait_for_close()



if __name__ == "__main__":
    main()