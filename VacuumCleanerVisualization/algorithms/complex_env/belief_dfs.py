from algorithms.common import Node, solution, is_goal, child_node

def belief_is_goal(belief_state):
    """
    Trạng thái đích của belief state: tất cả các trạng thái bên trong đều phải là đích.
    """
    return all(is_goal(state) for state in belief_state)

def get_actions_belief(belief_state):
    """
    Lấy các hành động hợp lệ.
    """
    actions = set(["SUCK", "UP", "DOWN", "LEFT", "RIGHT"])
    
    for state in belief_state:
        grid, x, y = state
        if "UP" in actions and x <= 0: actions.remove("UP")
        if "DOWN" in actions and x >= len(grid) - 1: actions.remove("DOWN")
        if "LEFT" in actions and y <= 0: actions.remove("LEFT")
        if "RIGHT" in actions and y >= len(grid[0]) - 1: actions.remove("RIGHT")
        
    return list(actions)

def belief_child_node(belief_node, action):
    """
    Tạo belief node con bằng cách áp dụng hành động lên TẤT CẢ trạng thái trong belief state hiện tại.
    """
    new_belief_state = set()
    for state in belief_node.state:
        dummy_node = Node(state)
        new_state = child_node(dummy_node, action).state
        new_belief_state.add(new_state)
        
    return Node(frozenset(new_belief_state), belief_node, action)

def belief_dfs(initial_state, log_callback=None):
    """
    DFS cho môi trường phức tạp (Belief State Search).
    """
    def log(msg):
        if log_callback: log_callback(msg)

    initial_belief = frozenset([initial_state])
    
    node = Node(initial_belief)
    if belief_is_goal(node.state): 
        log("Trạng thái ban đầu đã là đích!")
        return []
    
    frontier = [node]
    explored = set()
    frontier_states = {node.state}
    
    log(f"Bắt đầu Belief DFS với tập niềm tin có kích thước {len(initial_belief)}")
    
    step = 0
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        
        step += 1
        if step % 10 == 0:
            log(f"Đã duyệt {step} node, frontier size: {len(frontier)}")
            
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if belief_is_goal(node.state): 
            log(f"Tìm thấy đích sau khi duyệt {step} node!")
            return solution(node)
            
        actions = get_actions_belief(node.state)
        for action in reversed(actions):
            child = belief_child_node(node, action)
            
            if child.state not in explored and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
                
    log("Không tìm thấy đường đi!")
    return None

def sensorless_child_node(belief_node, action):
    """
    Tương tự child_node nhưng xử lý đụng tường (không đi xuyên tường, giữ nguyên vị trí).
    """
    new_belief_state = set()
    for state in belief_node.state:
        grid, x, y = state
        new_grid = [list(row) for row in grid]
        new_x, new_y = x, y
        
        if action == "SUCK":
            new_grid[new_x][new_y] = "Clean"
        elif action == "UP": new_x = max(0, new_x - 1)
        elif action == "DOWN": new_x = min(len(grid) - 1, new_x + 1)
        elif action == "RIGHT": new_y = min(len(grid[0]) - 1, new_y + 1)
        elif action == "LEFT": new_y = max(0, new_y - 1)
            
        new_state = (tuple(tuple(row) for row in new_grid), new_x, new_y)
        new_belief_state.add(new_state)
        
    return Node(frozenset(new_belief_state), belief_node, action)

def sensorless_belief_dfs(initial_state, log_callback=None):
    """
    DFS cho môi trường Sensorless (mù).
    Tạo initial_belief chứa MỌI vị trí (x,y) có thể trong phòng.
    """
    def log(msg):
        if log_callback: log_callback(msg)

    grid, _, _ = initial_state
    
    # Khởi tạo tập niềm tin: robot có thể ở bất kỳ ô nào trong phòng
    initial_belief_set = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            initial_belief_set.add((grid, r, c))
            
    initial_belief = frozenset(initial_belief_set)
    node = Node(initial_belief)
    
    if belief_is_goal(node.state): 
        log("Trạng thái ban đầu đã là đích!")
        return []
    
    frontier = [node]
    explored = set()
    frontier_states = {node.state}
    
    actions = ["UP", "DOWN", "LEFT", "RIGHT", "SUCK"]
    
    log(f"Bắt đầu Sensorless DFS với tập niềm tin có kích thước {len(initial_belief_set)} (mọi vị trí có thể)")
    step = 0
    
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        
        step += 1
        if step % 50 == 0:
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
