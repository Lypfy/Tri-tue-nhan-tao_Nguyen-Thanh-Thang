from collections import deque
import copy

GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Các hướng di chuyển
MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Chuyển state thành tuple để lưu visited
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# Sinh các trạng thái kế tiếp
def generate_next_states(state):
    next_states = []

    x, y = find_zero(state)

    for move, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy

        # Kiểm tra hợp lệ
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)

            # Hoán đổi ô trống
            new_state[x][y], new_state[nx][ny] = \
                new_state[nx][ny], new_state[x][y]

            next_states.append((new_state, move))

    return next_states

# BFS
def bfs(initial_state):
    queue = deque()
    visited = set()

    queue.append((initial_state, []))
    visited.add(state_to_tuple(initial_state))

    while queue:
        current_state, path = queue.popleft()

        # Kiểm tra goal
        if current_state == GOAL_STATE:
            return path, current_state

        # Sinh trạng thái mới
        for next_state, move in generate_next_states(current_state):

            state_tuple = state_to_tuple(next_state)

            if state_tuple not in visited:
                visited.add(state_tuple)

                queue.append((
                    next_state,
                    path + [move]
                ))

    return None, None


initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

solution, final_state = bfs(initial_state)

if solution:
    print("Các bước di chuyển:")
    print(solution)

    print("\nTrạng thái đích:")
    for row in final_state:
        print(row)

else:
    print("Không tìm thấy lời giải.")