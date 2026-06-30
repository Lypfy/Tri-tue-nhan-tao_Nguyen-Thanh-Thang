import sys
from algorithms.common import Node, is_goal, child_node, solution
from algorithms.informed.heuristic import heuristic
from algorithms.informed.a_star import get_actions_astar
from constants import COST_RUG, COST_NORMAL
import algorithms.common as common

def ida_star(initial_state):
    root = Node(initial_state, path_cost=0)
    bound = heuristic(root.state)
    
    while True:
        t, path_node = search(root, 0, bound, 1)
        if t == "FOUND":
            return solution(path_node)
        if t == float('inf'):
            return None
        bound = t

def search(node, g, bound, depth):
    common.max_frontier_size = max(common.max_frontier_size, depth)
    
    f = g + heuristic(node.state)
    if f > bound:
        return f, None
    if is_goal(node.state):
        return "FOUND", node
        
    min_cost = float('inf')
    
    for action in get_actions_astar(node.state):
        child = child_node(node, action)
        new_x, new_y = child.state[1], child.state[2]
        
        if action == "SUCK":
            move_cost = 1
        else:
            cell_type = common.current_terrain_matrix[new_x][new_y]
            move_cost = COST_RUG if cell_type == "Rug" else COST_NORMAL
            
        child.path_cost = g + move_cost
        
        # Avoid cyclic paths in current branch
        is_cycle = False
        curr = node
        while curr:
            if curr.state == child.state:
                is_cycle = True
                break
            curr = curr.parent
            
        if not is_cycle:
            t, path_node = search(child, child.path_cost, bound, depth + 1)
            if t == "FOUND":
                return "FOUND", path_node
            if t < min_cost:
                min_cost = t
                
    return min_cost, None
