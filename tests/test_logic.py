from logic import bingo_from_iterable, grouper


def test_grouper_pads_last_chunk():
    assert list(grouper('ABCDEFG', 3, 'x')) == [
        ('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]


def test_perfect_square_makes_square_grid():
    grid = list(bingo_from_iterable([str(i) for i in range(9)]))
    assert len(grid) == 3
    assert all(len(row) == 3 for row in grid)


def test_grid_contains_every_value_exactly_once():
    values = [str(i) for i in range(16)]
    grid = list(bingo_from_iterable(values))
    flat = [cell for row in grid for cell in row]
    assert sorted(flat) == sorted(values)


def test_missing_cells_are_none():
    grid = list(bingo_from_iterable(list('abcde')))
    flat = [cell for row in grid for cell in row]
    assert flat.count(None) == 1
    assert sorted(cell for cell in flat if cell is not None) == list('abcde')


def test_values_are_stripped_and_empty_ones_dropped():
    grid = list(bingo_from_iterable([' a\n', 'b\r', '', '   ', None, 'c', 'd']))
    flat = [cell for row in grid for cell in row]
    assert sorted(flat) == ['a', 'b', 'c', 'd']


def test_explicit_num_cols():
    grid = list(bingo_from_iterable(list('abcdef'), num_cols=3))
    assert [len(row) for row in grid] == [3, 3]


def test_empty_input_gives_empty_grid():
    assert list(bingo_from_iterable([])) == []
    assert list(bingo_from_iterable(['', '  ', None])) == []


def test_order_is_shuffled(monkeypatch):
    monkeypatch.setattr('logic.random.shuffle', lambda items: items.reverse())
    grid = list(bingo_from_iterable(list('abcd')))
    assert grid == [('d', 'c'), ('b', 'a')]
