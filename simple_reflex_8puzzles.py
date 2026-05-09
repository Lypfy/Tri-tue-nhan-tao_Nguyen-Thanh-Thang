GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

rules = {
    "UP": "UP",
    "DOWN": "DOWN",
    "LEFT": "LEFT",
    "RIGHT": "RIGHT"
}

def find_blank(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col

def rule_match(state):
    row, col = find_blank(state)
    target_value = GOAL_STATE[row][col]
    
    if target_value == 0:
        if state == GOAL_STATE:
            return "HOÀN THÀNH"
        else:
            if row > 0:
                return rules["UP"]
            if col > 0:
                return rules["LEFT"]
    
    if row > 0:
        value_above = state[row - 1][col]
        if value_above == target_value:
            return rules["UP"]
            
    if row < 2:
        value_below = state[row + 1][col]
        if value_below == target_value:
            return rules["DOWN"]
            
    if col > 0:
        value_left = state[row][col - 1]
        if value_left == target_value:
            return rules["LEFT"]
            
    if col < 2:
        value_right = state[row][col + 1]
        if value_right == target_value:
            return rules["RIGHT"]

    if row > 0: return rules["UP"]
    if col > 0: return rules["LEFT"]
    if row < 2: return rules["DOWN"]
    if col < 2: return rules["RIGHT"]

def simple_reflex_agent(percept):
    action = rule_match(percept)
    return action

initial_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]

action = simple_reflex_agent(initial_state)
print(action)