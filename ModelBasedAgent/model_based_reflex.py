import copy
import random

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

state = None
action = None
visited_states = []

model = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

def find_blank(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col

def update_state(state, action, percept, model):
    new_state = copy.deepcopy(percept)
    
    if new_state not in visited_states:
        visited_states.append(new_state)
        
    return new_state

def apply_action(state, action):
    new_state = copy.deepcopy(state)
    row, col = find_blank(new_state)
    dr, dc = model[action]
    
    new_row = row + dr
    new_col = col + dc

    # hoán đổi vị trí
    new_state[row][col], new_state[new_row][new_col] = \
    new_state[new_row][new_col], new_state[row][col]

    return new_state

def rule_match(state):
    row, col = find_blank(state)
    if state == GOAL_STATE:
        return "HOÀN THÀNH"

    all_valid_moves = []
    possible_moves = []

    directions = [
        ("UP", -1, 0), ("DOWN", 1, 0),
        ("LEFT", 0, -1), ("RIGHT", 0, 1)
    ]

    for move_name, dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        
        # kiểm tra giới hạn 3x3
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            all_valid_moves.append(move_name)
            
            # kiểm tra xem hướng đi mới có nằm trong những hướng đã đi rồi không
            test_state = apply_action(state, move_name)
            if test_state not in visited_states:
                possible_moves.append(move_name)

    # Ưu tiên 1: Chọn ngẫu nhiên 1 trong các hướng đi chưa đi qua
    if possible_moves:
        return rules[random.choice(possible_moves)]

    # Ưu tiên 2: Nếu tất cả các hướng đều dẫn đến trạng thái đã đi qua, 
    # chọn ngẫu nhiên 1 trong các hướng hợp lệ để thoát kẹt
    return rules[random.choice(all_valid_moves)]

def model_based_reflex_agent(percept):
    global state, action

    state = update_state(state, action, percept, model)
    rule = rule_match(state)
    action = rule

    return action

current_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

print("Bắt đầu giải:")

for step in range(1, 1000):

    print(f"\nBước {step}:")

    for row in current_state:
        print(row)

    result = model_based_reflex_agent(current_state)

    print("Agent quyết định:", result)

    if result == "HOÀN THÀNH":
        print("--- THÀNH CÔNG! ---")
        break

    current_state = apply_action(current_state, result)

else:
    print("\nĐã hết số bước mô phỏng.")