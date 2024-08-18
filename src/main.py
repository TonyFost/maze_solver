from graphics import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    # new_point = Point(10, 100)
    # next_point = Point(10, 200)
    # line = Line(new_point, next_point)
    # win.draw(line, "black")

    # cell = Cell(150, 200, 170, 220, win)
    # cell.draw(150, 200, 170, 220)
    # cell.draw(200, 250, 250, 300)
    # cell.has_right_wall = False
    # cell.draw(250, 300, 300, 350)
    # other_cell = Cell(300, 350, 350, 400, win)
    # other_cell.draw(300, 350, 350, 400)
    # cell.draw_move(other_cell)

    cell_size_x = 20
    cell_size_y = 20
    num_cols = 30
    num_rows = 20
    maze = Maze(50, 50, num_rows, num_cols, cell_size_x, cell_size_y, win)
    win.wait_for_close()



if __name__ == "__main__":
    main()