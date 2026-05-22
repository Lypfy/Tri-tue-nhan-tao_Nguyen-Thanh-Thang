import collections

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def is_goal(state):
    grid, _, _ = state
    for row in grid:
        if "Dirty" in row:
            return False
    return True

def child_node(parent_node, action):
    grid, x, y = parent_node.state
    new_grid = [list(row) for row in grid]
    new_x, new_y = x, y
    
    if action == "SUCK":
        new_grid[new_x][new_y] = "Clean"
    elif action == "UP": new_x -= 1
    elif action == "DOWN": new_x += 1
    elif action == "RIGHT": new_y += 1
    elif action == "LEFT": new_y -= 1
        
    new_state = (tuple(tuple(row) for row in new_grid), new_x, new_y)
    return Node(new_state, parent_node, action)

def solution(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    return path[::-1] 

# --- BFS 1: CƠ BẢN ---
def get_actions_bfs1(state):
    grid, x, y = state
    possible_moves = []
    if grid[x][y] == "Dirty":
        possible_moves.append("SUCK")
    if x > 0: possible_moves.append("UP")
    if x < 2: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < 2: possible_moves.append("RIGHT")
    return possible_moves

def bfs1(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): return []
    frontier = collections.deque([node])
    frontier_states = {node.state} 
    reached = set()
    
    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        reached.add(node.state)
        
        if is_goal(node.state): return solution(node)
            
        for action in get_actions_bfs1(node.state):
            child = child_node(node, action)
            if child.state not in reached and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
    return None


# --- BFS 2: TỐI ƯU ---
def get_actions_bfs2(state):
    grid, x, y = state
    if grid[x][y] == "Dirty":
        return ["SUCK"]
    
    possible_moves = []
    if x > 0: possible_moves.append("UP")
    if x < 2: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < 2: possible_moves.append("RIGHT")
    return possible_moves

def bfs2(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): return []
    frontier = collections.deque([node])
    frontier_states = {node.state} 
    explored = set()
    
    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        explored.add(node.state)
        
        for action in get_actions_bfs2(node.state):
            child = child_node(node, action)
            if child.state not in explored and child.state not in frontier_states:
                if is_goal(child.state): return solution(child)
                frontier.append(child)
                frontier_states.add(child.state)
    return None

# --- DFS 1: CƠ BẢN ---
def get_actions_dfs1(state):
    grid, x, y = state
    possible_moves = []
    
    if y < 2: possible_moves.append("RIGHT")
    if y > 0: possible_moves.append("LEFT")
    if x < 2: possible_moves.append("DOWN")
    if x > 0: possible_moves.append("UP")
    if grid[x][y] == "Dirty":
        possible_moves.append("SUCK")
        
    return possible_moves

def dfs1(initial_state):
    node = Node(initial_state)
    if is_goal(node.state): 
        return []
        
    frontier = [node] 
    frontier_states = {node.state} 
    reached = set()
    
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        reached.add(node.state)
        
        if is_goal(node.state): 
            return solution(node)
            
        for action in get_actions_dfs1(node.state):
            child = child_node(node, action)
            
            if child.state not in reached and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
                
    return None

# --- DFS 2: TỐI ƯU ---
def get_actions_dfs2(state):
    grid, x, y = state

    if grid[x][y] == "Dirty":
        return ["SUCK"] 
    
    possible_moves = []

    if y < 2: possible_moves.append("RIGHT")
    if y > 0: possible_moves.append("LEFT")
    if x < 2: possible_moves.append("DOWN")
    if x > 0: possible_moves.append("UP")
    
    return possible_moves

def dfs2(initial_state):
    node = Node(initial_state)
    
    frontier = [node]
    frontier_states = {node.state}
    explored = set()
    
    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        
        if is_goal(node.state):
            return solution(node)
            
        if node.state not in explored:
            explored.add(node.state)
            
            for action in get_actions_dfs2(node.state): # Dùng hàm get_actions_dfs2
                child = child_node(node, action)
                
                if child.state not in explored and child.state not in frontier_states:
                    frontier.append(child) # Đẩy vào đỉnh STACK
                    frontier_states.add(child.state)
                    
    return None

# --- UCS: CƠ BẢN ---
import heapq

TERRAIN_COST = [
    [1, 5, 1],
    [1, 1, 1],
    [5, 5, 5]
]

def get_actions_ucs(state):
    grid, x, y = state
    possible_moves = []
    
    if grid[x][y] == "Dirty":
        return ["SUCK"] 
        
    if x > 0: possible_moves.append("UP")
    if x < 2: possible_moves.append("DOWN")
    if y > 0: possible_moves.append("LEFT")
    if y < 2: possible_moves.append("RIGHT")
    return possible_moves

def ucs_standard(initial_state):
    node = Node(initial_state, path_cost=0)
    if is_goal(node.state): return []
    
    frontier = []
    heapq.heappush(frontier, (node.path_cost, id(node), node))
    frontier_states = {node.state: node}
    explored = set()
    
    while frontier:
        cost, _, node = heapq.heappop(frontier)
        
        if node.state in explored:
            continue
            
        explored.add(node.state)
        
        if is_goal(node.state): 
            return solution(node)
            
        for action in get_actions_ucs(node.state):
            child = child_node(node, action)
            new_x, new_y = child.state[1], child.state[2]
            
            if action == "SUCK":
                move_cost = 1
            else:
                move_cost = TERRAIN_COST[new_x][new_y]
                
            child.path_cost = node.path_cost + move_cost
            
            if child.state not in explored and child.state not in frontier_states:
                heapq.heappush(frontier, (child.path_cost, id(child), child))
                frontier_states[child.state] = child
            elif child.state in frontier_states:
                existing_node = frontier_states[child.state]
                if child.path_cost < existing_node.path_cost:
                    heapq.heappush(frontier, (child.path_cost, id(child), child))
                    frontier_states[child.state] = child
                    
    return None