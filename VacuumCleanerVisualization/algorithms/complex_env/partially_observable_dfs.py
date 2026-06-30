from algorithms.common import Node, solution
from algorithms.complex_env.belief_dfs import belief_is_goal, sensorless_child_node

def partially_observable_belief_dfs(initial_state, log_callback=None):
    """
    DFS cho môi trường nhìn thấy một phần (Partially Observable).
    Giả định: Robot biết được bản đồ và hàng (x) hiện tại, 
    nhưng không biết chính xác cột (y) do hỏng cảm biến.
    Do đó, tập niềm tin ban đầu chứa tất cả các vị trí trên hàng x.
    """
    def log(msg):
        if log_callback: log_callback(msg)

    grid, x, _ = initial_state
    
    # Khởi tạo tập niềm tin: robot có thể ở bất kỳ cột nào trên hàng x
    initial_belief_set = set()
    for c in range(len(grid[0])):
        initial_belief_set.add((grid, x, c))
            
    initial_belief = frozenset(initial_belief_set)
    node = Node(initial_belief)
    
    if belief_is_goal(node.state): 
        log("Trạng thái ban đầu đã là đích!")
        return []
    
    frontier = [node]
    explored = set()
    frontier_states = {node.state}
    
    actions = ["UP", "DOWN", "LEFT", "RIGHT", "SUCK"]
    
    log(f"Bắt đầu Partially Observable DFS với tập niềm tin có kích thước {len(initial_belief_set)} (các ô trên hàng {x})")
    step = 0
    
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        
        step += 1
        if step % 20 == 0:
            log(f"Đã duyệt {step} node, frontier size: {len(frontier)}")
            
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if belief_is_goal(node.state): 
            log(f"Tìm thấy đích sau khi duyệt {step} node!")
            return solution(node)
            
        for action in reversed(actions):
            child = sensorless_child_node(node, action)
            
            if child.state not in explored and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
                
    log("Không tìm thấy đường đi!")
    return None
