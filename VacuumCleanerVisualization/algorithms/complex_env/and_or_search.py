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

def and_or_graph_search(initial_state):
    def or_search(state, path):
        if is_goal(state):
            return []
        if state in path:
            return "RETRY" # Detect cycle and return a retry instruction
            
        grid, x, y = state
        valid_actions = ["SUCK"]
        if x > 0: valid_actions.append("UP")
        if x < len(grid) - 1: valid_actions.append("DOWN")
        if y > 0: valid_actions.append("LEFT")
        if y < len(grid[0]) - 1: valid_actions.append("RIGHT")
        
        for action in valid_actions:
            results = slippery_results(state, action)
            plan = and_search(results, path + [state])
            if plan != 'failure':
                return [action, plan]
                
        return 'failure'

    def and_search(states, path):
        plan = {}
        has_progress = False
        for s in states:
            plan_s = or_search(s, path)
            if plan_s == 'failure':
                return 'failure'
            if plan_s != "RETRY":
                has_progress = True
            plan[s] = plan_s
            
        # A valid cyclic plan must have at least one branch that makes progress
        if not has_progress:
            return 'failure'
            
        return plan

    return or_search(initial_state, [])
