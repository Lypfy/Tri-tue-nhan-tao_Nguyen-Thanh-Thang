import random

environment = [
    ["Dirty", "Dirty", "Obstacle"],
    ["Dirty", "Dirty", "Dirty"],
    ["Obstacle", "Dirty", "Dirty"]
]

rows = len(environment)
cols = len(environment[0]) if rows > 0 else 0

model = [["Unknown" for _ in range(cols)] for _ in range(rows)]
x, y = 0, 0

def update_model(x, y, status):
    """Cập nhật bộ nhớ dựa trên những gì Robot vừa thấy"""
    model[x][y] = status

def rule_match(state, rows, cols):
    status, x, y = state

    if status == "Dirty":
        return "SUCK"

    possible_moves = []
    
    directions = {
        "MOVE UP": (x-1, y),
        "MOVE DOWN": (x+1, y),
        "MOVE LEFT": (x, y-1),
        "MOVE RIGHT": (x, y+1)
    }

    # Lọc ra các bước đi hợp lệ
    valid_moves = {}
    for move, (nx, ny) in directions.items():
        if 0 <= nx < rows and 0 <= ny < cols:
            if model[nx][ny] != "Obstacle": 
                valid_moves[move] = (nx, ny)

    # Đi vào những ô trong bộ nhớ vẫn còn Dirty
    priority_moves = [m for m, (nx, ny) in valid_moves.items() if model[nx][ny] == "Dirty"]
    
    # Đi vào những ô chưa biết để khám phá
    if not priority_moves:
        priority_moves = [m for m, (nx, ny) in valid_moves.items() if model[nx][ny] == "Unknown"]

    # Nếu xung quanh toàn ô đã được clean, đi ngẫu nhiên để tìm đường khác
    if not priority_moves:
        priority_moves = list(valid_moves.keys())

    if not priority_moves:
        return "STAY"

    return random.choice(priority_moves)

def model_based_agent(percept, rows, cols):
    # Cập nhật model trước khi ra quyết định
    status, cur_x, cur_y, surroundings = percept
    update_model(cur_x, cur_y, status)
    
    # Cập nhật thông tin các ô xung quanh (cảm biến tiệm cận)
    for (nx, ny), n_status in surroundings.items():
        update_model(nx, ny, n_status)
    
    # Ra quyết định dựa trên model đã cập nhật
    action = rule_match((status, cur_x, cur_y), rows, cols)
    return action

for i in range(15):
    # Môi trường thu thập thông tin xung quanh
    surroundings = {}
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            surroundings[(nx, ny)] = environment[nx][ny]

    percept = (environment[x][y], x, y, surroundings)

    action = model_based_agent(percept, rows, cols)

    print(f"Step: {i+1}")
    print(f"Position: ({x}, {y}) | State: {percept[0]}")
    print(f"Action: {action}")
    
    # update model và environment
    if action == "SUCK":
        environment[x][y] = "Clean"
        update_model(x, y, "Clean")

    elif action == "MOVE UP": x -= 1
    elif action == "MOVE DOWN": x += 1
    elif action == "MOVE RIGHT": y += 1
    elif action == "MOVE LEFT": y -= 1

    # Kiểm tra xem toàn bộ các ô Dirty mà robot biết đã sạch chưa
    dirty_exists = any("Dirty" in row for row in environment)
    if not dirty_exists:
        print("Room clean!")
        break
    print("-" * 25)

print("\nFinal Environment (Thực tế):")
for row in environment: print(row)

print("\nFinal Model (Bộ nhớ Robot):")
for row in model: print(row)