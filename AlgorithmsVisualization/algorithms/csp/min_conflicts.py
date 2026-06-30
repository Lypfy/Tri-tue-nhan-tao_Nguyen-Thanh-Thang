import random
from algorithms.csp.backtracking import HCMC_DISTRICTS, HCMC_NEIGHBORS, COLORS

def min_conflicts_search(max_steps=1000):
    """
    Thuật toán Min-Conflicts (Local Search) cho CSP.
    Bắt đầu với một cấu hình ngẫu nhiên đầy đủ, sau đó lặp lại việc chọn ngẫu nhiên
    một quận đang bị xung đột và đổi sang màu gây ra ít xung đột nhất.
    """
    steps = []
    
    # 1. Khởi tạo một trạng thái ban đầu ngẫu nhiên đầy đủ
    coloring = {d: random.choice(COLORS) for d in HCMC_DISTRICTS}
    
    steps.append({
        "coloring": dict(coloring),
        "current": None,
        "action": "init",
        "color": None,
        "message": "Khởi tạo bảng màu ngẫu nhiên cho tất cả các quận."
    })
    
    def get_conflicted_vars():
        conflicts = []
        for d in HCMC_DISTRICTS:
            c1 = coloring[d]
            for nb in HCMC_NEIGHBORS[d]:
                if coloring.get(nb) == c1:
                    conflicts.append(d)
                    break
        return conflicts

    def count_conflicts(var, color):
        count = 0
        for nb in HCMC_NEIGHBORS[var]:
            if coloring.get(nb) == color:
                count += 1
        return count

    for i in range(max_steps):
        conflicted_vars = get_conflicted_vars()
        
        if not conflicted_vars:
            steps.append({
                "coloring": dict(coloring),
                "current": None,
                "action": "done",
                "color": None,
                "message": f"✅ Giải quyết thành công sau {i} lần đổi màu!"
            })
            return steps
            
        # Chọn ngẫu nhiên một biến đang bị xung đột
        var = random.choice(conflicted_vars)
        
        steps.append({
            "coloring": dict(coloring),
            "current": var,
            "action": "select_conflict",
            "color": coloring[var],
            "message": f"Chọn {var} đang bị xung đột."
        })
        
        # Tìm màu thay thế gây ra ít xung đột nhất với hàng xóm
        min_c = float('inf')
        best_colors = []
        
        for color in COLORS:
            c_count = count_conflicts(var, color)
            if c_count < min_c:
                min_c = c_count
                best_colors = [color]
            elif c_count == min_c:
                best_colors.append(color)
                
        # Chọn màu ngẫu nhiên trong số những màu tốt nhất
        best_color = random.choice(best_colors)
        
        if coloring[var] != best_color:
            coloring[var] = best_color
            steps.append({
                "coloring": dict(coloring),
                "current": var,
                "action": "reassign",
                "color": best_color,
                "message": f"Đổi {var} → {best_color} (chỉ còn tạo {min_c} xung đột)."
            })
            
    steps.append({
        "coloring": dict(coloring),
        "current": None,
        "action": "fail",
        "color": None,
        "message": f"❌ Vượt quá giới hạn {max_steps} bước. Chạy lại để thử lại!"
    })
    return steps
