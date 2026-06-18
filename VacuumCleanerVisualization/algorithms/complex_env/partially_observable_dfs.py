from algorithms.common import Node, solution
from algorithms.complex_env.belief_dfs import belief_is_goal, sensorless_child_node

def partially_observable_belief_dfs(initial_state):
    """
    DFS cho môi trường nhìn thấy một phần (Partially Observable).
    Giả định: Robot biết được bản đồ và hàng (x) hiện tại, 
    nhưng không biết chính xác cột (y) do hỏng cảm biến.
    Do đó, tập niềm tin ban đầu chứa tất cả các vị trí trên hàng x.
    """
    grid, x, _ = initial_state
    
    # Khởi tạo tập niềm tin: robot có thể ở bất kỳ cột nào trên hàng x
    initial_belief_set = set()
    for c in range(len(grid[0])):
        initial_belief_set.add((grid, x, c))
            
    initial_belief = frozenset(initial_belief_set)
    node = Node(initial_belief)
    
    if belief_is_goal(node.state): return []
    
    frontier = [node]
    explored = set()
    frontier_states = {node.state}
    
    actions = ["UP", "DOWN", "LEFT", "RIGHT", "SUCK"]
    
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if belief_is_goal(node.state): 
            return solution(node)
            
        for action in reversed(actions):
            child = sensorless_child_node(node, action)
            
            if child.state not in explored and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
                
    return None
