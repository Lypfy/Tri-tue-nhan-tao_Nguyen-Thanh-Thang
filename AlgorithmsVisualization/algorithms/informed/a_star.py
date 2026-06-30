import heapq
from algorithms.common import Node, is_goal, child_node, solution
from algorithms.informed.heuristic import heuristic
from constants import COST_RUG, COST_NORMAL
import algorithms.common as common

def get_actions_astar(state):
    grid, x, y = state
    possible_moves = []
    
    if grid[x][y] == "Dirty":
        return ["SUCK"] 
        
    if x > 0: possible_moves.append("UP")
    if x < len(grid) - 1: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < len(grid[0]) - 1: possible_moves.append("RIGHT")
    return possible_moves

def a_star(initial_state):
    node = Node(initial_state, path_cost=0)
    if is_goal(node.state): return []
    
    frontier = []
    h = heuristic(node.state)
    heapq.heappush(frontier, (node.path_cost + h, node.id, node))
    frontier_states = {node.state: node}
    explored = set()
    
    while frontier:
        common.max_frontier_size = max(common.max_frontier_size, len(frontier))
        f, _, node = heapq.heappop(frontier)
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if is_goal(node.state): 
            return solution(node)
            
        for action in get_actions_astar(node.state):
            child = child_node(node, action)
            new_x, new_y = child.state[1], child.state[2]
            
            if action == "SUCK":
                move_cost = 1
            else:
                cell_type = common.current_terrain_matrix[new_x][new_y]
                move_cost = COST_RUG if cell_type == "Rug" else COST_NORMAL
                
            child.path_cost = node.path_cost + move_cost
            h_child = heuristic(child.state)
            f_child = child.path_cost + h_child
            
            if child.state not in explored and child.state not in frontier_states:
                heapq.heappush(frontier, (f_child, child.id, child))
                frontier_states[child.state] = child
            elif child.state in frontier_states:
                existing_node = frontier_states[child.state]
                if child.path_cost < existing_node.path_cost:
                    heapq.heappush(frontier, (f_child, child.id, child))
                    frontier_states[child.state] = child
                    
    return None
