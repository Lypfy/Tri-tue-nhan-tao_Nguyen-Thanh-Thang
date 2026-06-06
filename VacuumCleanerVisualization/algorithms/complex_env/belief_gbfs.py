import heapq
from algorithms.common import Node, is_goal, child_node, solution

def belief_heuristic(belief_state):
    """
    Heuristic cho belief state: h là số ô sai (số ô bẩn lớn nhất trong các trạng thái có thể).
    """
    max_h = 0
    for state in belief_state:
        grid, x, y = state
        dirty_count = sum(row.count("Dirty") for row in grid)
        max_h = max(max_h, dirty_count)
    return max_h

def belief_is_goal(belief_state):
    """
    Trạng thái đích của belief state: tất cả các trạng thái bên trong đều phải là đích.
    """
    return all(is_goal(state) for state in belief_state)

def get_actions_belief(belief_state):
    """
    Lấy các hành động hợp lệ. Trong mô hình đơn giản này, ta giả sử chỉ lấy 
    các hành động hợp lệ cho tất cả các trạng thái trong niềm tin, 
    hoặc đơn giản là lấy từ trạng thái đầu tiên nếu ta chỉ mô phỏng.
    """
    # Nếu chỉ có 1 trạng thái (mô phỏng UI), lấy các hành động của trạng thái đó.
    # Trong môi trường phức tạp thực sự, ta sẽ thử SUCK, UP, DOWN, LEFT, RIGHT
    # và áp dụng bộ lọc (ví dụ: không cho đi xuyên tường).
    # Ở đây để tương thích với child_node, ta sẽ giới hạn các hành động 
    # sao cho không làm x, y của bất kỳ trạng thái nào bị ra ngoài lưới.
    actions = set(["SUCK", "UP", "DOWN", "LEFT", "RIGHT"])
    
    for state in belief_state:
        grid, x, y = state
        if "UP" in actions and x <= 0: actions.remove("UP")
        if "DOWN" in actions and x >= len(grid) - 1: actions.remove("DOWN")
        if "LEFT" in actions and y <= 0: actions.remove("LEFT")
        if "RIGHT" in actions and y >= len(grid[0]) - 1: actions.remove("RIGHT")
        
        # Tối ưu: nếu có ô bẩn, ưu tiên SUCK. Tuy nhiên, SUCK có thể không hợp lệ 
        # với trạng thái khác (mặc dù SUCK trên ô sạch không gây lỗi trong child_node).
    
    # Để thuật toán hướng tới SUCK khi có ô bẩn, ta có thể giữ SUCK luôn hợp lệ.
    return list(actions)

def belief_child_node(belief_node, action):
    """
    Tạo belief node con bằng cách áp dụng hành động lên TẤT CẢ trạng thái trong belief state hiện tại.
    """
    new_belief_state = set()
    for state in belief_node.state:
        # child_node(Node, action) trả về Node, ta chỉ cần state của nó
        dummy_node = Node(state)
        new_state = child_node(dummy_node, action).state
        new_belief_state.add(new_state)
        
    return Node(frozenset(new_belief_state), belief_node, action)

def belief_gbfs(initial_state):
    """
    Greedy BFS cho môi trường phức tạp (Belief State Search).
    """
    # Khởi tạo belief state ban đầu. 
    # Trong môi trường không cảm biến (sensorless), nó có thể là tất cả các trạng thái có thể.
    # Nhưng để liên kết với UI trực quan hóa (có 1 trạng thái khởi đầu cụ thể),
    # ta giả lập belief state chứa trạng thái đó. 
    # Người dùng muốn thuật toán hoạt động theo cơ chế niềm tin.
    initial_belief = frozenset([initial_state])
    
    node = Node(initial_belief)
    if belief_is_goal(node.state): return []
    
    frontier = []
    heapq.heappush(frontier, (belief_heuristic(node.state), id(node), node))
    frontier_states = {node.state}
    explored = set()
    
    while frontier:
        h, _, node = heapq.heappop(frontier)
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if belief_is_goal(node.state): 
            return solution(node)
            
        for action in get_actions_belief(node.state):
            child = belief_child_node(node, action)
            
            if child.state not in explored and child.state not in frontier_states:
                heapq.heappush(frontier, (belief_heuristic(child.state), id(child), child))
                frontier_states.add(child.state)
                
    return None
