import unittest
from graphics import Maze, Cell

class Tests(unittest.TestCase):
    def test_graphics_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_graphics_cell_center(self):
        cell = Cell(10,10,20,20)
        self.assertEqual(
            cell.center(), (15, 15)
        )
        
        cell = Cell(0,0,5,5)
        self.assertEqual(
            cell.center(), (2, 2)
        )
    def test_graphics_maze_create_cells_zero(self):
        num_cols = 1
        num_rows = 0
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


if __name__ == "__main__":
    unittest.main()