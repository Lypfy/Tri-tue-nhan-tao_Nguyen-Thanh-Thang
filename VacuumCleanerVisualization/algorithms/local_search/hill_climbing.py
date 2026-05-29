import random
from algorithms.common import Node, is_goal, child_node, solution
from algorithms.informed.a_star import get_actions_astar

def objective(state):
    grid, x, y = state
    dirty_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "Dirty":
                dirty_cells.append((r, c))
    
    if not dirty_cells:
        return 0
        
    min_dist = min(abs(x - r) + abs(y - c) for r, c in dirty_cells)
    return len(dirty_cells) * 10 + min_dist

def get_neighbors(node):
    neighbors = []
    for action in get_actions_astar(node.state):
        child = child_node(node, action)
        neighbors.append(child)
    return neighbors

def simple_hill_climbing(initial_state):
    current = Node(initial_state)
    while True:
        if is_goal(current.state):
            return solution(current)
            
        current_obj = objective(current.state)
        neighbors = get_neighbors(current)
        
        found_better = False
        for neighbor in neighbors:
            if objective(neighbor.state) < current_obj:
                current = neighbor
                found_better = True
                break
                
        if not found_better:
            return solution(current) if current.parent else None

def steepest_ascent_hill_climbing(initial_state):
    current = Node(initial_state)
    while True:
        if is_goal(current.state):
            return solution(current)
            
        current_obj = objective(current.state)
        neighbors = get_neighbors(current)
        
        best_neighbor = None
        best_obj = current_obj
        
        for neighbor in neighbors:
            obj = objective(neighbor.state)
            if obj < best_obj:
                best_obj = obj
                best_neighbor = neighbor
                
        if best_neighbor is None:
            return solution(current) if current.parent else None
            
        current = best_neighbor

def stochastic_hill_climbing(initial_state):
    current = Node(initial_state)
    while True:
        if is_goal(current.state):
            return solution(current)
            
        current_obj = objective(current.state)
        neighbors = get_neighbors(current)
        
        better_neighbors = []
        for neighbor in neighbors:
            if objective(neighbor.state) < current_obj:
                better_neighbors.append(neighbor)
                
        if not better_neighbors:
            return solution(current) if current.parent else None
            
        current = random.choice(better_neighbors)
