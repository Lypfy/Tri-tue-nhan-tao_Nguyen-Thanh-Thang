import collections
from algorithms.common import Node, is_goal, child_node, solution

def get_actions_bfs1(state):
    grid, x, y = state
    possible_moves = []
    if grid[x][y] == "Dirty":
        possible_moves.append("SUCK")
    if x > 0: possible_moves.append("UP")
    if x < len(grid) - 1: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < len(grid[0]) - 1: possible_moves.append("RIGHT")
    return possible_moves

def bfs1(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): return []
    frontier = collections.deque([node])
    frontier_states = {node.state} 
    reached = set()
    
    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        reached.add(node.state)
        
        if is_goal(node.state): return solution(node)
            
        for action in get_actions_bfs1(node.state):
            child = child_node(node, action)
            if child.state not in reached and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
    return None

def get_actions_bfs2(state):
    grid, x, y = state
    if grid[x][y] == "Dirty":
        return ["SUCK"]
    
    possible_moves = []
    if x > 0: possible_moves.append("UP")
    if x < len(grid) - 1: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < len(grid[0]) - 1: possible_moves.append("RIGHT")
    return possible_moves

def bfs2(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): return []
    frontier = collections.deque([node])
    frontier_states = {node.state} 
    explored = set()
    
    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        explored.add(node.state)
        
        for action in get_actions_bfs2(node.state):
            child = child_node(node, action)
            if child.state not in explored and child.state not in frontier_states:
                if is_goal(child.state): return solution(child)
                frontier.append(child)
                frontier_states.add(child.state)
    return None
