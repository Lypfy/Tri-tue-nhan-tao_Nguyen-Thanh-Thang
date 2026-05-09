import random

environmnent = [
    ["Dirty", "Clean", "Dirty"],
    ["Clean", "Dirty", "Dirty"],
    ["Dirty", "Dirty", "Dirty"]
]

x, y = 1, 1

def interpret_input(percept):
    return percept

def rule_match(state):
    status, x, y = state

    if status == "Dirty":
        return "SUCK"
    
    possible_moves = []

    if x > 0: possible_moves.append("UP")
    if x < 2: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < 2: possible_moves.append("RIGHT")

    return random.choice(possible_moves)

def simple_reflex_agent(percept):
    state = interpret_input(percept)
    action = rule_match(state)
    return action

for i in range (100):
    
    percept = (environmnent[x][y], x, y)

    action = simple_reflex_agent(percept)

    print(f"Step: {i+1}")
    print(f"Position: {percept[1]}, {percept[2]}")
    print(f"State: {percept[0]}")
    print(f"Action: {action}")
    print("---------------------")
    if "Dirty" not in (c for r in environmnent for c in r):
        print("Room clean!")
        break

    if action == "SUCK":
        environmnent[x][y] = "Clean"

    elif action == "UP":
        x -= 1
    elif action == "DOWN":
        x += 1
    elif action == "RIGHT":
        y += 1
    elif action == "LEFT":
        y -= 1


for row in environmnent:
    print(row)