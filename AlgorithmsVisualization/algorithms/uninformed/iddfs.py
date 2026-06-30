from algorithms.common import Node, is_goal, child_node, solution
from algorithms.uninformed.dfs import get_actions_dfs2

def get_actions_iddfs(state):
    return get_actions_dfs2(state)

def dls(node, limit):
    frontier = [(node, 0)]
    explored = {node.state: 0}
    
    while frontier:
        import algorithms.common as common
        common.max_frontier_size = max(common.max_frontier_size, len(frontier))
        
        current_node, depth = frontier.pop()
        
        if is_goal(current_node.state):
            return solution(current_node)
            
        if depth < limit:
            for action in get_actions_iddfs(current_node.state):
                child = child_node(current_node, action)
                child_depth = depth + 1
                
                if child.state not in explored or explored[child.state] > child_depth:
                    explored[child.state] = child_depth
                    frontier.append((child, child_depth))
    return None

def iddfs(initial_state):
    node = Node(initial_state)
    max_depth = 50 
    for limit in range(max_depth):
        result = dls(node, limit)
        if result is not None:
            return result
    return None
