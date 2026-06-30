def heuristic(state):
    """
    Hàm heuristic: Tính tổng số ô bẩn.
    """
    grid, x, y = state
    dirty_count = sum(row.count("Dirty") for row in grid)
    return dirty_count
