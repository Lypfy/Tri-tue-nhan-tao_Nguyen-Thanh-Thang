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
    return len(dirty_cells) * 1000 + min_dist

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

def random_restart_hill_climbing(initial_state, max_restarts=10):
    best_solution = None
    best_obj = float('inf')
    
    for _ in range(max_restarts):
        current = Node(initial_state)
        # Random walk to create a different starting point for this restart
        walk_length = random.randint(0, 5)
        for _ in range(walk_length):
            neighbors = get_neighbors(current)
            if not neighbors:
                break
            current = random.choice(neighbors)
            
        # Steepest ascent from current
        while True:
            if is_goal(current.state):
                return solution(current)
                
            current_obj = objective(current.state)
            neighbors = get_neighbors(current)
            
            best_neighbor = None
            neighbor_best_obj = current_obj
            
            for neighbor in neighbors:
                obj = objective(neighbor.state)
                if obj < neighbor_best_obj:
                    neighbor_best_obj = obj
                    best_neighbor = neighbor
                    
            if best_neighbor is None:
                if current_obj < best_obj:
                    best_obj = current_obj
                    best_solution = solution(current) if current.parent else None
                break
                
            current = best_neighbor
            
    return best_solution

def local_beam_search(initial_state, k=3):
    current_nodes = [Node(initial_state)]
    
    while True:
        for node in current_nodes:
            if is_goal(node.state):
                return solution(node)
                
        all_successors = []
        for node in current_nodes:
            all_successors.extend(get_neighbors(node))
            
        if not all_successors:
            return solution(current_nodes[0]) if current_nodes[0].parent else None
            
        # Select the best k successors
        all_successors.sort(key=lambda n: objective(n.state))
        
        best_current_obj = min(objective(n.state) for n in current_nodes)
        best_successor_obj = objective(all_successors[0].state)
        
        if best_successor_obj >= best_current_obj:
            # Reached local optimum
            best_node = min(current_nodes, key=lambda n: objective(n.state))
            return solution(best_node) if best_node.parent else None
            
        current_nodes = all_successors[:k]
