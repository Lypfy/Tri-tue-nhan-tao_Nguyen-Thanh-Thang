from algorithms.csp.backtracking import HCMC_DISTRICTS, HCMC_NEIGHBORS, COLORS

def mac_search():
    """
    Chạy Backtracking Search kết hợp Maintaining Arc Consistency (AC-3).
    Trả về list steps (mỗi step là dict mô tả trạng thái hiện tại).
    """
    domains = {d: list(COLORS) for d in HCMC_DISTRICTS}
    coloring = {}
    steps = []

    def select_unassigned_variable():
        # Lựa chọn MRV (Minimum Remaining Values)
        unassigned = [d for d in HCMC_DISTRICTS if d not in coloring]
        if not unassigned: return None
        return min(unassigned, key=lambda d: len(domains[d]))

    def is_consistent(district, color):
        for neighbor in HCMC_NEIGHBORS[district]:
            if coloring.get(neighbor) == color:
                return False
        return True

    def ac3(queue, local_domains):
        """
        Thuật toán AC-3 để duy trì tính nhất quán cung (Arc Consistency).
        queue: danh sách các cung (xi, xj) cần kiểm tra.
        local_domains: dict chứa miền giá trị của mỗi biến.
        """
        while queue:
            xi, xj = queue.pop(0)
            if revise(xi, xj, local_domains):
                if not local_domains[xi]:
                    return False # Miền giá trị rỗng -> Thất bại
                for xk in HCMC_NEIGHBORS[xi]:
                    if xk != xj and xk not in coloring:
                        queue.append((xk, xi))
        return True

    def revise(xi, xj, local_domains):
        """
        Xóa giá trị x khỏi domains[xi] nếu không tồn tại
        giá trị y nào trong domains[xj] thỏa ràng buộc khác màu (y != x).
        Với map coloring: ràng buộc là xi != xj,
        vì vậy loại x khi mọi y trong domain[xj] đều bằng x.
        """
        revised = False
        for x in list(local_domains[xi]):
            # Giữ x nếu tồn tại ít nhất 1 giá trị y trong xj mà y != x
            if all(y == x for y in local_domains[xj]):
                local_domains[xi].remove(x)
                revised = True
                steps.append({
                    "coloring": dict(coloring),
                    "current": xi,
                    "target": xj,
                    "action": "revise",
                    "color": None,
                    "message": f"✂️ AC-3: Cắt màu {x} của {xi} (bị ràng buộc bởi {xj})"
                })
        return revised

    def backtrack():
        if len(coloring) == len(HCMC_DISTRICTS):
            steps.append({
                "coloring": dict(coloring),
                "current": None,
                "action": "done",
                "color": None,
                "message": "✅ Tô màu hoàn thành (MAC/AC-3)!"
            })
            return True

        var = select_unassigned_variable()
        if var is None:
            return False

        for color in list(domains[var]):
            if is_consistent(var, color):
                domains_backup = {d: list(v) for d, v in domains.items()}

                coloring[var] = color
                domains[var] = [color] # Biến đã gán chỉ còn 1 màu

                steps.append({
                    "coloring": dict(coloring),
                    "current": var,
                    "action": "assign",
                    "color": color,
                    "message": f"Gán: {var} → {color} (Bắt đầu AC-3)"
                })

                # Khởi tạo queue cho AC-3: tất cả cung (X_k, var) với X_k là hàng xóm chưa gán của var
                queue = [(neighbor, var) for neighbor in HCMC_NEIGHBORS[var] if neighbor not in coloring]

                if ac3(queue, domains):
                    if backtrack():
                        return True

                # Backtrack
                del coloring[var]
                for d in domains:
                    domains[d] = domains_backup[d]

                steps.append({
                    "coloring": dict(coloring),
                    "current": var,
                    "action": "backtrack",
                    "color": None,
                    "message": f"↩ Backtrack: {var} (AC-3 phát hiện xung đột)"
                })

        return False

    backtrack()
    return steps
