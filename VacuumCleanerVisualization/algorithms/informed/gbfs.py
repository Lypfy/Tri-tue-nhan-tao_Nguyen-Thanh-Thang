import heapq
from algorithms.common import Node, is_goal, child_node, solution
from algorithms.informed.heuristic import heuristic

def get_actions_gbfs(state):
    grid, x, y = state
    possible_moves = []
    
    if grid[x][y] == "Dirty":
        return ["SUCK"] 
        
    if x > 0: possible_moves.append("UP")
    if x < len(grid) - 1: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < len(grid[0]) - 1: possible_moves.append("RIGHT")
    return possible_moves

def gbfs(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): return []
    
    frontier = []
    heapq.heappush(frontier, (heuristic(node.state), id(node), node))
    frontier_states = {node.state}
    explored = set()
    
    while frontier:
        h, _, node = heapq.heappop(frontier)
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if is_goal(node.state): 
            return solution(node)
            
        for action in get_actions_gbfs(node.state):
            child = child_node(node, action)
            
            if child.state not in explored and child.state not in frontier_states:
                heapq.heappush(frontier, (heuristic(child.state), id(child), child))
                frontier_states.add(child.state)
                
    return None
