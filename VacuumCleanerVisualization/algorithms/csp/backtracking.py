"""
Backtracking Search for CSP – Bài toán tô màu bản đồ các quận TPHCM.

Sử dụng:
  - Static Variable Ordering để chọn biến tiếp theo.
  - Forward Checking để cắt tỉa domain.
  - 4 màu: Đỏ, Xanh lá, Xanh dương, Vàng.

Trả về danh sách steps để animation, mỗi step là:
  {
    "coloring": {quận: màu hoặc None},
    "current": quận đang xét,
    "action": "assign" | "backtrack" | "done",
    "color": màu vừa gán (nếu assign),
    "message": chuỗi log
  }
"""

# ──────────────────────────────────────────────
# Danh sách quận/huyện TPHCM (22 đơn vị gộp Thủ Đức)
# ──────────────────────────────────────────────
HCMC_DISTRICTS = [
    "Quận 1",  "Quận 3",  "Quận 4",  "Quận 5",
    "Quận 6",  "Quận 7",  "Quận 8",  "Quận 10",
    "Quận 11", "Quận 12", "Bình Thạnh", "Gò Vấp",
    "Phú Nhuận", "Tân Bình", "Tân Phú", "Bình Tân",
    "Thủ Đức", "Nhà Bè",  "Hóc Môn", "Củ Chi",
    "Bình Chánh", "Cần Giờ"
]

# ──────────────────────────────────────────────
# Đồ thị kề (adjacency list) – dựa trên địa lý thực tế TPHCM
# ──────────────────────────────────────────────
HCMC_NEIGHBORS = {
    "Quận 1":     ["Quận 3", "Quận 5", "Quận 10", "Bình Thạnh", "Quận 4", "Phú Nhuận"],
    "Quận 3":     ["Quận 1", "Quận 5", "Phú Nhuận", "Quận 10", "Tân Bình"],
    "Quận 4":     ["Quận 1", "Quận 7"],
    "Quận 5":     ["Quận 1", "Quận 3", "Quận 6", "Quận 8", "Quận 10", "Quận 11"],
    "Quận 6":     ["Quận 5", "Quận 8", "Quận 11", "Tân Phú", "Bình Tân"],
    "Quận 7":     ["Quận 4", "Nhà Bè", "Bình Chánh", "Quận 8"],
    "Quận 8":     ["Quận 5", "Quận 6", "Quận 7", "Bình Chánh", "Bình Tân"],
    "Quận 10":    ["Quận 1", "Quận 3", "Quận 5", "Quận 11", "Tân Bình"],
    "Quận 11":    ["Quận 5", "Quận 6", "Quận 10", "Tân Bình", "Tân Phú"],
    "Quận 12":    ["Gò Vấp", "Tân Bình", "Tân Phú", "Bình Tân", "Bình Thạnh", "Hóc Môn", "Thủ Đức"],
    "Bình Thạnh": ["Quận 1", "Phú Nhuận", "Gò Vấp", "Quận 12", "Thủ Đức"],
    "Gò Vấp":    ["Bình Thạnh", "Phú Nhuận", "Tân Bình", "Quận 12"],
    "Phú Nhuận": ["Quận 1", "Quận 3", "Bình Thạnh", "Gò Vấp", "Tân Bình"],
    "Tân Bình":  ["Quận 3", "Quận 10", "Quận 11", "Phú Nhuận", "Gò Vấp", "Quận 12", "Tân Phú"],
    "Tân Phú":   ["Quận 11", "Quận 6", "Quận 12", "Tân Bình", "Bình Tân"],
    "Bình Tân":  ["Quận 6", "Quận 8", "Quận 12", "Tân Phú", "Bình Chánh", "Hóc Môn"],
    "Thủ Đức":   ["Bình Thạnh", "Quận 12"],
    "Nhà Bè":    ["Quận 7", "Bình Chánh", "Cần Giờ"],
    "Hóc Môn":   ["Quận 12", "Bình Tân", "Bình Chánh", "Củ Chi"],
    "Củ Chi":    ["Hóc Môn"],
    "Bình Chánh": ["Quận 7", "Quận 8", "Bình Tân", "Nhà Bè", "Hóc Môn"],
    "Cần Giờ":   ["Nhà Bè"]
}

# ──────────────────────────────────────────────
# Tọa độ hiển thị (normalized 0.0–1.0) – mô phỏng vị trí địa lý
# (x=cột từ trái, y=hàng từ trên)
# ──────────────────────────────────────────────
DISTRICT_POSITIONS = {
    "Củ Chi":     (0.18, 0.08),
    "Hóc Môn":   (0.30, 0.20),
    "Thủ Đức":   (0.70, 0.18),
    "Quận 12":   (0.45, 0.22),
    "Gò Vấp":    (0.42, 0.32),
    "Bình Thạnh":(0.60, 0.36),
    "Tân Bình":  (0.35, 0.40),
    "Phú Nhuận": (0.54, 0.42),
    "Quận 3":    (0.52, 0.50),
    "Quận 10":   (0.40, 0.50),
    "Quận 1":    (0.60, 0.52),
    "Tân Phú":   (0.26, 0.50),
    "Quận 11":   (0.34, 0.56),
    "Quận 5":    (0.42, 0.58),
    "Bình Tân":  (0.22, 0.60),
    "Quận 6":    (0.30, 0.62),
    "Quận 4":    (0.60, 0.62),
    "Quận 8":    (0.40, 0.68),
    "Quận 7":    (0.64, 0.72),
    "Bình Chánh":(0.30, 0.78),
    "Nhà Bè":    (0.62, 0.82),
    "Cần Giờ":   (0.70, 0.93),
}

# ──────────────────────────────────────────────
# 4 màu dùng để tô
# ──────────────────────────────────────────────
COLORS = ["Đỏ", "Xanh lá", "Xanh dương", "Vàng"]

COLOR_HEX = {
    "Đỏ":        "#E74C3C",
    "Xanh lá":   "#2ECC71",
    "Xanh dương":"#3498DB",
    "Vàng":      "#F1C40F",
    None:         "#AAAAAA"  # chưa tô
}


def backtracking_search():
    """
    Chạy Backtracking Search với MRV + Forward Checking.
    Trả về list steps (mỗi step là dict mô tả trạng thái hiện tại).
    """
    # domains[district] = tập màu còn hợp lệ
    domains = {d: list(COLORS) for d in HCMC_DISTRICTS}
    coloring = {}  # district -> color (None nếu chưa gán)
    steps = []

    def select_unassigned_variable():
        """Chọn quận chưa gán đầu tiên theo thứ tự danh sách (bỏ MRV)."""
        for d in HCMC_DISTRICTS:
            if d not in coloring:
                return d
        return None

    def is_consistent(district, color):
        for neighbor in HCMC_NEIGHBORS[district]:
            if coloring.get(neighbor) == color:
                return False
        return True

    def forward_check(district, color, domains_copy):
        """
        Sau khi gán color cho district, loại màu đó khỏi domain
        của các hàng xóm chưa gán. Trả về False nếu có domain rỗng.
        """
        for neighbor in HCMC_NEIGHBORS[district]:
            if neighbor not in coloring:
                if color in domains_copy[neighbor]:
                    domains_copy[neighbor] = [c for c in domains_copy[neighbor] if c != color]
                if not domains_copy[neighbor]:
                    return False
        return True

    def backtrack():
        if len(coloring) == len(HCMC_DISTRICTS):
            steps.append({
                "coloring": dict(coloring),
                "current": None,
                "action": "done",
                "color": None,
                "message": "✅ Tô màu hoàn thành! Không có quận liền kề cùng màu."
            })
            return True

        var = select_unassigned_variable()
        if var is None:
            return False

        for color in domains[var]:
            if is_consistent(var, color):
                # Snapshot domains trước khi gán
                domains_backup = {d: list(v) for d, v in domains.items()}

                coloring[var] = color
                steps.append({
                    "coloring": dict(coloring),
                    "current": var,
                    "action": "assign",
                    "color": color,
                    "message": f"Gán: {var} → {color}"
                })

                # Forward checking
                if forward_check(var, color, domains):
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
                    "message": f"↩ Backtrack: {var} (màu {color} xung đột)"
                })

        return False

    backtrack()
    return steps
