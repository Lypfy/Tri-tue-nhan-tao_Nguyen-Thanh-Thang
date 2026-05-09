import random

environment = [
    ["Dirty", "Obstacle", "Obstacle"],
    ["Dirty", "Dirty", "Obstacle"],
    ["Obstacle", "Dirty", "Dirty"]
]

x, y = 0, 0

def interpret_input(percept):
    return percept

def rule_match(state, env):
    status, x, y = state

    if status == "Dirty":
        return "SUCK"
    
    possible_moves = []

    if x > 0 and env[x-1][y] != "Obstacle": 
        possible_moves.append("MOVE UP")
    if x < 2 and env[x+1][y] != "Obstacle":
        possible_moves.append("MOVE DOWN")
    if y > 0 and env[x][y-1] != "Obstacle":
        possible_moves.append("MOVE LEFT")
    if y < 2 and env[x][y+1] != "Obstacle":
        possible_moves.append("MOVE RIGHT")

    if not possible_moves:
        return "STAY"

    return random.choice(possible_moves)

def simple_reflex_agent(percept, env):
    state = interpret_input(percept)
    action = rule_match(state, env)
    return action

for i in range (25):
    
    percept = (environment[x][y], x, y)

    action = simple_reflex_agent(percept, environment)

    print(f"Step: {i+1}")
    print(f"Position: ({x}, {y}) | State: {percept[0]}")
    print(f"Action: {action}")
    
    

    if action == "SUCK":
        environment[x][y] = "Clean"

    elif action == "MOVE UP":
        x -= 1
    elif action == "MOVE DOWN":
        x += 1
    elif action == "MOVE RIGHT":
        y += 1
    elif action == "MOVE LEFT":
        y -= 1

    if "Dirty" not in (c for r in environment for c in r):
        print("Room clean!")
        break
    print("-" * 25)

print("After cleaning:")
for row in environment:
    print(row)