import random
from algorithms.common import Node, is_goal, child_node, solution
from algorithms.informed.a_star import get_actions_astar

def objective(state):
    grid, x, y = state
    dirty_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "Dirty":
                dirty_cells.append((r, c))
    
    if not dirty_cells:
        return 0
        
    # SỬ DỤNG TỔNG BÌNH PHƯƠNG KHOẢNG CÁCH (Sum of Squared Distances)
    # Điều này tạo ra một "hố lõm" tại vị trí trung bình (trọng tâm) của các vết bẩn.
    # Nếu robot đi vào trọng tâm này, mọi bước đi ra xa đều làm tăng khoảng cách.
    # Nhờ đó, robot sẽ bị KẸT TẠI CỰC TRỊ CỤC BỘ (Local Optimum) nếu vết bẩn nằm tản mác.
    sum_sq_dist = sum((x - r)**2 + (y - c)**2 for r, c in dirty_cells)
    
    return len(dirty_cells) * 1000 + sum_sq_dist

def get_neighbors(node):
    neighbors = []
    for action in get_actions_astar(node.state):
        child = child_node(node, action)
        neighbors.append(child)
    return neighbors

def simple_hill_climbing(initial_state, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    current = Node(initial_state)
    iteration = 0

    while True:
        iteration += 1
        current_obj = objective(current.state)

        if is_goal(current.state):
            log(f"[Bước {iteration}] ✓ Đạt mục tiêu! Objective = 0")
            return solution(current)

        neighbors = get_neighbors(current)
        found_better = False

        for neighbor in neighbors:
            nb_obj = objective(neighbor.state)
            if nb_obj < current_obj:
                log(f"[Bước {iteration}] Objective: {current_obj} → {nb_obj} | Hành động: {neighbor.action}")
                current = neighbor
                found_better = True
                break

        if not found_better:
            log(f"[Bước {iteration}] ⛔ BỊ KẸT TẠI CỰC TRỊ CỤC BỘ (Local Optimum)!")
            log(f"   → Robot đang ở ({current.state[1]}, {current.state[2]}) nhưng mọi bước đi xung quanh đều có Objective lớn hơn {current_obj}.")
            log(f"   → Giải thuật thất bại trong việc tìm goal. Dừng tìm kiếm.")
            return solution(current) if current.parent else None

def steepest_ascent_hill_climbing(initial_state, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    current = Node(initial_state)
    iteration = 0

    while True:
        iteration += 1
        current_obj = objective(current.state)

        if is_goal(current.state):
            log(f"[Bước {iteration}] ✓ Đạt mục tiêu! Objective = 0")
            return solution(current)

        neighbors = get_neighbors(current)
        best_neighbor = None
        best_obj = current_obj

        for neighbor in neighbors:
            obj = objective(neighbor.state)
            if obj < best_obj:
                best_obj = obj
                best_neighbor = neighbor

        if best_neighbor is None:
            log(f"[Bước {iteration}] ⛔ BỊ KẸT TẠI CỰC TRỊ CỤC BỘ (Local Optimum)!")
            log(f"   → Robot đang ở ({current.state[1]}, {current.state[2]}). Đã xét {len(neighbors)} neighbors nhưng không có hướng nào tốt hơn {current_obj}.")
            log(f"   → Giải thuật thất bại trong việc tìm goal. Dừng tìm kiếm.")
            return solution(current) if current.parent else None

        log(f"[Bước {iteration}] Objective: {current_obj} → {best_obj} | Best action: {best_neighbor.action} | Xét {len(neighbors)} neighbors")
        current = best_neighbor

def stochastic_hill_climbing(initial_state, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    current = Node(initial_state)
    iteration = 0

    while True:
        iteration += 1
        current_obj = objective(current.state)

        if is_goal(current.state):
            log(f"[Bước {iteration}] ✓ Đạt mục tiêu! Objective = 0")
            return solution(current)

        neighbors = get_neighbors(current)
        better_neighbors = [n for n in neighbors if objective(n.state) < current_obj]

        if not better_neighbors:
            log(f"[Bước {iteration}] ⛔ BỊ KẸT TẠI CỰC TRỊ CỤC BỘ (Local Optimum)!")
            log(f"   → Robot đang ở ({current.state[1]}, {current.state[2]}). 0/{len(neighbors)} neighbors tốt hơn {current_obj}.")
            log(f"   → Giải thuật thất bại. Dừng tìm kiếm.")
            return solution(current) if current.parent else None

        chosen = random.choice(better_neighbors)
        chosen_obj = objective(chosen.state)
        log(f"[Bước {iteration}] Objective: {current_obj} → {chosen_obj} | {len(better_neighbors)}/{len(neighbors)} neighbors tốt hơn | Chọn ngẫu nhiên: {chosen.action}")
        current = chosen

def random_restart_hill_climbing(initial_state, max_restarts=10, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    best_solution = None
    best_obj = float('inf')
    best_restart = -1

    for restart_idx in range(max_restarts):
        log(f"=== Restart {restart_idx + 1}/{max_restarts} ===")

        current = Node(initial_state)
        # Random walk để tạo điểm xuất phát khác nhau
        walk_length = random.randint(0, 5)
        if walk_length > 0:
            for _ in range(walk_length):
                neighbors = get_neighbors(current)
                if not neighbors:
                    break
                current = random.choice(neighbors)
            log(f"  Đi ngẫu nhiên {walk_length} bước từ vị trí ban đầu | Objective khởi đầu: {objective(current.state)}")

        # Steepest ascent từ vị trí hiện tại
        step = 0
        while True:
            step += 1
            if is_goal(current.state):
                log(f"  [Bước {step}] ✓ Đạt mục tiêu! Restart {restart_idx + 1} thành công.")
                return solution(current)

            current_obj = objective(current.state)
            neighbors = get_neighbors(current)
            best_neighbor = None
            neighbor_best_obj = current_obj

            for neighbor in neighbors:
                obj = objective(neighbor.state)
                if obj < neighbor_best_obj:
                    neighbor_best_obj = obj
                    best_neighbor = neighbor

            if best_neighbor is None:
                log(f"  [Bước {step}] ⛔ KẸT TẠI CỰC TRỊ CỤC BỘ (Obj = {current_obj}) tại vị trí ({current.state[1]}, {current.state[2]}).")
                if current_obj < best_obj:
                    best_obj = current_obj
                    best_solution = solution(current) if current.parent else None
                    best_restart = restart_idx + 1
                    log(f"  → Ghi nhận đây là kết quả tốt nhất hiện tại: Obj = {best_obj}")
                break

            log(f"  [Bước {step}] Objective: {current_obj} → {neighbor_best_obj} | {best_neighbor.action}")
            current = best_neighbor

    log(f"=== Kết thúc Random Restart ===")
    log(f"  Kết quả tốt nhất: Objective = {best_obj} (từ Restart {best_restart})")
    return best_solution

def local_beam_search(initial_state, k=3, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    log(f"Khởi động Local Beam Search với k = {k} beams")
    current_nodes = [Node(initial_state) for _ in range(k)]
    iteration = 0

    while True:
        iteration += 1
        log(f"=== Iteration {iteration} ===")

        # Kiểm tra goal và log trạng thái từng beam
        for i, node in enumerate(current_nodes):
            obj = objective(node.state)
            _, bx, by = node.state
            log(f"  Beam {i+1}: Objective={obj} | Vị trí=({bx},{by})")
            if is_goal(node.state):
                log(f"  → Beam {i+1} đạt mục tiêu! ✓")
                return solution(node)

        # Mở rộng tất cả beams
        all_successors = []
        for node in current_nodes:
            all_successors.extend(get_neighbors(node))

        if not all_successors:
            best_node = min(current_nodes, key=lambda n: objective(n.state))
            log(f"  Không còn successor. Objective tốt nhất = {objective(best_node.state)}")
            return solution(best_node) if best_node.parent else None

        # Chọn k successors tốt nhất
        all_successors.sort(key=lambda n: objective(n.state))
        best_current_obj = min(objective(n.state) for n in current_nodes)
        best_successor_obj = objective(all_successors[0].state)

        log(f"  Tổng successor: {len(all_successors)} | Best successor Objective: {best_successor_obj} | Current best: {best_current_obj}")

        if best_successor_obj >= best_current_obj:
            best_node = min(current_nodes, key=lambda n: objective(n.state))
            log(f"  ⚠ Cục bộ tối ưu! Objective = {objective(best_node.state)} | Không có successor nào tốt hơn.")
            return solution(best_node) if best_node.parent else None

        current_nodes = all_successors[:k]
        log(f"  → Chọn {k} beams tốt nhất: Objectives = {[objective(n.state) for n in current_nodes]}")
