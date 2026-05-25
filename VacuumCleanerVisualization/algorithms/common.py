class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def is_goal(state):
    grid, _, _ = state
    for row in grid:
        if "Dirty" in row:
            return False
    return True

def child_node(parent_node, action):
    grid, x, y = parent_node.state
    new_grid = [list(row) for row in grid]
    new_x, new_y = x, y
    
    if action == "SUCK":
        new_grid[new_x][new_y] = "Clean"
    elif action == "UP": new_x -= 1
    elif action == "DOWN": new_x += 1
    elif action == "RIGHT": new_y += 1
    elif action == "LEFT": new_y -= 1
        
    new_state = (tuple(tuple(row) for row in new_grid), new_x, new_y)
    return Node(new_state, parent_node, action)

def solution(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    return path[::-1] 
