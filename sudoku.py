"""
Copyright (C) 2013 Stacey Ell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import itertools


def _locations_for_row(size, location):
    assert 0 <= location[0] < size[0]
    assert 0 <= location[1] < size[1]
    return [(location[0], i) for i in xrange(size[0])]


def _locations_for_col(size, location):
    assert 0 <= location[0] < size[0]
    assert 0 <= location[1] < size[1]
    return [(i, location[1]) for i in xrange(size[1])]


def _locations_for_box(size, box_size, location):
    quant = lambda qq, x: x / qq * qq
    xoff = quant(box_size[0], location[0])
    yoff = quant(box_size[1], location[1])
    return [(xoff + x, yoff + y) for x in xrange(3) for y in xrange(3)]


class SudokuGrid(object):
    size = (9, 9)
    box_size = (3, 3)
    valid_symbols = set(xrange(1, 10))

    def __init__(self, parent=None, mut=None):
        self.cells = [None] * self.size[0] * self.size[1]
        if parent is not None:
            self.cells = list(parent.cells)
        if mut:
            for location, val in mut:
                self[location] = val

    def _loc_to_idx(self, location):
        assert location is not None
        assert 0 <= location[0] < self.size[0]
        assert 0 <= location[1] < self.size[1]
        return location[0] * self.size[0] + location[1]

    def __getitem__(self, location):
        assert location is not None
        return self.cells[self._loc_to_idx(location)]

    def __setitem__(self, location, value):
        assert location is not None
        self.cells[self._loc_to_idx(location)] = value

    def empty_locations(self):
        for i in xrange(self.size[0]):
            for j in xrange(self.size[1]):
                if self[i, j] is None:
                    yield (i, j)

    def empty_location(self):
        try:
            return next(self.empty_locations())
        except StopIteration:
            return False

    def allowed_values(self, location):
        assert location is not None
        locations = set(itertools.chain(
            _locations_for_row(self.size, location),
            _locations_for_col(self.size, location),
            _locations_for_box(self.size, self.box_size, location)
        ))
        found_values = set()
        for location in locations:
            cell_value = self[location]
            if cell_value is not None:
                found_values.add(cell_value)
        return self.valid_symbols - found_values

    def to_string(self):
        cell_to_string = lambda cell: " " if cell is None else str(cell)
        s = ""
        for i in xrange(self.size[0]):
            for j in xrange(self.size[1]):
                s += cell_to_string(self[i, j])
            s += "\n"
        return s

    def _solved_for_location_list(self, location_list):
        found_values = set(map(self.__getitem__, location_list))
        return self.valid_symbols == found_values

    def is_solved(self):
        for x in xrange(self.size[0]):
            if not self._solved_for_location_list(_locations_for_row(self.size, (x, 0))):
                return False
        for y in xrange(self.size[1]):
            if not self._solved_for_location_list(_locations_for_col(self.size, (0, y))):
                return False
        for x in xrange(3):
            for y in xrange(3):
                if not self._solved_for_location_list(_locations_for_box(self.size, self.box_size, (x, y))):
                    return False
        return True


def _solve_helper(sudoku_grid, location, value):
    for grid in solve(SudokuGrid(sudoku_grid, [(location, value)])):
        yield grid


def solve(sudoku_grid):
    try:
        empty_location = next(sudoku_grid.empty_locations())
    except StopIteration:
        assert sudoku_grid.is_solved()
        yield sudoku_grid
    else:
        for val in sudoku_grid.allowed_values(empty_location):
            for grid in _solve_helper(sudoku_grid, empty_location, val):
                yield grid


"""
#  Source problem:
#
#  75 |9 3|  6
#     |   |
#     |45 |  3
#  ---+---+---
#  62 | 9 |8
#   15|   |23
#    9| 1 | 75
#  ---+---+---
#  3  | 84|
#     |   |
#  9  |6 1| 57
#
#  Output:
#
#  758|923|146
#  243|167|598
#  196|458|723
#  ---+---+---
#  627|395|814
#  815|746|239
#  439|812|675
#  ---+---+---
#  371|584|962
#  564|279|381
#  982|631|457

import sudoku
sg2 = sudoku.SudokuGrid(mut=[
    ((0, 0), 7), ((0, 1), 5), ((0, 3), 9), ((0, 5), 3),
    ((0, 8), 6), ((2, 3), 4), ((2, 4), 5), ((2, 8), 3),
    ((3, 0), 6), ((3, 1), 2), ((3, 4), 9), ((3, 6), 8),
    ((4, 1), 1), ((4, 2), 5), ((4, 6), 2), ((4, 7), 3),
    ((5, 2), 9), ((5, 4), 1), ((5, 7), 7), ((5, 8), 5),
    ((6, 0), 3), ((6, 4), 8), ((6, 5), 4), ((8, 0), 9),
    ((8, 3), 6), ((8, 5), 1), ((8, 7), 5), ((8, 8), 7)
])
print sg2.to_string()

print next(sudoku.solve(sg2)).to_string()
"""
