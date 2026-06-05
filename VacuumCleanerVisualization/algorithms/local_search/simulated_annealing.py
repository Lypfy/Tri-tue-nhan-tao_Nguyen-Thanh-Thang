import random
import math
from algorithms.common import Node, is_goal, solution
from algorithms.local_search.hill_climbing import objective, get_neighbors

def simulated_annealing(initial_state, initial_temp=1000.0, cooling_rate=0.995, min_temp=0.01):
    current = Node(initial_state)
    current_obj = objective(current.state)
    temp = initial_temp
    
    # Track the best solution found so far just in case
    best_node = current
    best_obj = current_obj
    
    while temp > min_temp:
        if is_goal(current.state):
            return solution(current)
            
        neighbors = get_neighbors(current)
        if not neighbors:
            break
            
        next_node = random.choice(neighbors)
        next_obj = objective(next_node.state)
        
        # We want to minimize objective, so if next_obj < current_obj, delta_e > 0
        delta_e = current_obj - next_obj
        
        if delta_e > 0:
            current = next_node
            current_obj = next_obj
            if current_obj < best_obj:
                best_node = current
                best_obj = current_obj
        else:
            probability = math.exp(delta_e / temp)
            if random.random() < probability:
                current = next_node
                current_obj = next_obj
                
        temp *= cooling_rate
        
    return solution(best_node) if best_node.parent else None
