import random
import math
from algorithms.common import Node, is_goal, solution
from algorithms.local_search.hill_climbing import objective, get_neighbors

def simulated_annealing(initial_state, initial_temp=1000.0, cooling_rate=0.995, min_temp=0.01, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    current = Node(initial_state)
    current_obj = objective(current.state)
    temp = initial_temp

    # Track the best solution found so far just in case
    best_node = current
    best_obj = current_obj

    log(f"Khởi động Simulated Annealing")
    log(f"  Nhiệt độ ban đầu: {initial_temp:.1f} | Cooling rate: {cooling_rate} | Min temp: {min_temp}")
    log(f"  Objective ban đầu: {current_obj}")

    step = 0
    accepted_count = 0
    rejected_count = 0
    uphill_accepted = 0

    while temp > min_temp:
        if is_goal(current.state):
            log(f"[Bước {step}] ✓ Đạt mục tiêu! Objective = 0")
            log(f"Thống kê: Chấp nhận {accepted_count} bước (trong đó {uphill_accepted} leo đồi ngược), từ chối {rejected_count} bước")
            return solution(current)

        neighbors = get_neighbors(current)
        if not neighbors:
            break

        next_node = random.choice(neighbors)
        next_obj = objective(next_node.state)

        # Minimize objective: nếu next_obj < current_obj thì delta_e > 0 (cải thiện)
        delta_e = current_obj - next_obj
        step += 1

        if delta_e > 0:
            # Cải thiện → luôn chấp nhận
            log(f"[Bước {step}] Temp={temp:7.2f} | Obj: {current_obj} → {next_obj} | ΔE=+{delta_e} | ✓ CHẤP NHẬN (cải thiện) | Action: {next_node.action}")
            current = next_node
            current_obj = next_obj
            accepted_count += 1
            if current_obj < best_obj:
                best_node = current
                best_obj = current_obj
        else:
            # Tệ hơn → chấp nhận theo xác suất Boltzmann
            probability = math.exp(delta_e / temp)
            if random.random() < probability:
                log(f"[Bước {step}] Temp={temp:7.2f} | Obj: {current_obj} → {next_obj} | ΔE={delta_e} | P={probability:.3f} → ↑ CHẤP NHẬN (leo đồi ngược) | Action: {next_node.action}")
                current = next_node
                current_obj = next_obj
                accepted_count += 1
                uphill_accepted += 1
            else:
                log(f"[Bước {step}] Temp={temp:7.2f} | Obj: {current_obj} → {next_obj} | ΔE={delta_e} | P={probability:.3f} → ✗ TỪ CHỐI | Action: {next_node.action}")
                rejected_count += 1

        temp *= cooling_rate

    log(f"=== Kết thúc (nhiệt độ = {temp:.4f} < {min_temp}) ===")
    log(f"Thống kê: {step} bước | Chấp nhận {accepted_count} ({uphill_accepted} leo ngược) | Từ chối {rejected_count}")
    log(f"Objective tốt nhất tìm được: {best_obj}")
    return solution(best_node) if best_node.parent else None
