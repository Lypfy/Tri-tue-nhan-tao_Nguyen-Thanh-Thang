from algorithms.common import is_goal

def slippery_results(state, action):
    grid, x, y = state
    
    if action == "SUCK":
        # SUCK is deterministic
        new_grid = [list(row) for row in grid]
        if new_grid[x][y] == "Dirty":
            new_grid[x][y] = "Clean"
        return [(tuple(tuple(row) for row in new_grid), x, y)]
        
    outcomes = []
    # Slippery behavior: The robot might fail to move and stay in the same place
    outcomes.append(state)
    
    if action == "UP":
        if x > 0: outcomes.append((grid, x - 1, y))
    elif action == "DOWN":
        if x < len(grid) - 1: outcomes.append((grid, x + 1, y))
    elif action == "LEFT":
        if y > 0: outcomes.append((grid, x, y - 1))
    elif action == "RIGHT":
        if y < len(grid[0]) - 1: outcomes.append((grid, x, y + 1))
        
    # Remove duplicates if it hit a wall (state is added twice)
    return list(set(outcomes))

def and_or_graph_search(initial_state, log_callback=None):
    def log(msg):
        if log_callback: log_callback(msg)

    log("Bắt đầu AND-OR Graph Search cho môi trường không xác định (nhiều kết quả)")

    def or_search(state, path):
        if is_goal(state):
            log(f"  [OR] Trạng thái {state[1:]} là đích.")
            return []
        if state in path:
            log(f"  [OR] Phát hiện chu trình tại {state[1:]}. Yêu cầu thử lại (RETRY).")
            return "RETRY" # Detect cycle and return a retry instruction
            
        grid, x, y = state
        valid_actions = ["SUCK"]
        if x > 0: valid_actions.append("UP")
        if x < len(grid) - 1: valid_actions.append("DOWN")
        if y > 0: valid_actions.append("LEFT")
        if y < len(grid[0]) - 1: valid_actions.append("RIGHT")
        
        for action in valid_actions:
            results = slippery_results(state, action)
            log(f"  [OR] Khám phá hành động {action} từ {state[1:]} (có {len(results)} kết quả có thể xảy ra)")
            plan = and_search(results, path + [state])
            if plan != 'failure':
                return [action, plan]
                
        return 'failure'

    def and_search(states, path):
        plan = {}
        has_progress = False
        for s in states:
            log(f"    [AND] Xem xét kết quả {s[1:]}...")
            plan_s = or_search(s, path)
            if plan_s == 'failure':
                log(f"    [AND] Thất bại tại nhánh {s[1:]}!")
                return 'failure'
            if plan_s != "RETRY":
                has_progress = True
            plan[s] = plan_s
            
        # A valid cyclic plan must have at least one branch that makes progress
        if not has_progress:
            log(f"    [AND] Tất cả các nhánh đều lặp chu trình. Kế hoạch thất bại.")
            return 'failure'
            
        return plan

    result = or_search(initial_state, [])
    if result == 'failure':
        log("Không tìm thấy conditional plan!")
    else:
        log("Đã tìm thấy conditional plan thành công!")
    return result
