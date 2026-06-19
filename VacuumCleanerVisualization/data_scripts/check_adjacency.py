"""
Tự động tính đồ thị kề (adjacency) chính xác từ dữ liệu polygon GADM.
Hai quận được coi là kề nhau nếu biên giới của chúng cách nhau <= EPS.
"""
import sys
import ast
import json

sys.stdout.reconfigure(encoding='utf-8')

# Đọc dữ liệu polygon
with open("algorithms/csp/map_data.py", "r", encoding="utf-8") as f:
    content = f.read()
data = ast.literal_eval(content.split("=", 1)[1].strip())

HCMC_DISTRICTS = [
    "Quận 1", "Quận 3", "Quận 4", "Quận 5",
    "Quận 6", "Quận 7", "Quận 8", "Quận 10",
    "Quận 11", "Quận 12", "Bình Thạnh", "Gò Vấp",
    "Phú Nhuận", "Tân Bình", "Tân Phú", "Bình Tân",
    "Thủ Đức", "Nhà Bè", "Hóc Môn", "Củ Chi",
    "Bình Chánh", "Cần Giờ"
]

# Hàm: lấy tất cả các điểm biên của một quận
def get_boundary_points(district):
    pts = set()
    for poly in data.get(district, []):
        for x, y in poly:
            # Làm tròn để tránh lỗi floating point
            pts.add((round(x, 4), round(y, 4)))
    return pts

# Hàm: kiểm tra hai tập điểm có điểm chung không
def share_boundary(pts_a, pts_b, eps=0.0005):
    """Trả về True nếu hai polygon có điểm biên trong khoảng eps của nhau."""
    # Chuyển sang list để so sánh khoảng cách
    list_b = list(pts_b)
    for ax, ay in pts_a:
        for bx, by in list_b:
            if abs(ax - bx) <= eps and abs(ay - by) <= eps:
                return True
    return False

print("Đang tính toán adjacency từ polygon data...")

# Xây dựng adjacency mới
new_neighbors = {d: set() for d in HCMC_DISTRICTS}

for i, d1 in enumerate(HCMC_DISTRICTS):
    pts1 = get_boundary_points(d1)
    for j, d2 in enumerate(HCMC_DISTRICTS):
        if j <= i:
            continue
        pts2 = get_boundary_points(d2)
        if share_boundary(pts1, pts2):
            new_neighbors[d1].add(d2)
            new_neighbors[d2].add(d1)

print("\nĐồ thị kề MỚI (từ polygon GADM):")
for d in HCMC_DISTRICTS:
    nb_list = sorted(new_neighbors[d])
    print(f'    "{d}": {nb_list},')

# So sánh với đồ thị cũ
OLD_NEIGHBORS = {
    "Quận 1":     ["Quận 3", "Bình Thạnh", "Quận 4", "Phú Nhuận"],
    "Quận 3":     ["Quận 1", "Phú Nhuận", "Quận 10", "Tân Bình"],
    "Quận 4":     ["Quận 1", "Quận 7", "Quận 8", "Nhà Bè"],
    "Quận 5":     ["Quận 6", "Quận 8", "Quận 10", "Quận 11"],
    "Quận 6":     ["Quận 5", "Quận 8", "Quận 11", "Tân Phú", "Bình Tân"],
    "Quận 7":     ["Quận 4", "Nhà Bè", "Bình Chánh", "Quận 8"],
    "Quận 8":     ["Quận 4", "Quận 5", "Quận 6", "Quận 7", "Bình Chánh", "Bình Tân"],
    "Quận 10":    ["Quận 3", "Quận 5", "Quận 11", "Tân Bình"],
    "Quận 11":    ["Quận 5", "Quận 6", "Quận 10", "Tân Phú"],
    "Quận 12":    ["Gò Vấp", "Tân Bình", "Hóc Môn", "Thủ Đức"],
    "Bình Thạnh": ["Quận 1", "Phú Nhuận", "Gò Vấp", "Thủ Đức"],
    "Gò Vấp":    ["Bình Thạnh", "Phú Nhuận", "Tân Bình", "Quận 12", "Hóc Môn"],
    "Phú Nhuận": ["Quận 1", "Quận 3", "Bình Thạnh", "Gò Vấp", "Tân Bình"],
    "Tân Bình":  ["Quận 3", "Quận 10", "Phú Nhuận", "Gò Vấp", "Quận 12", "Tân Phú"],
    "Tân Phú":   ["Quận 11", "Quận 6", "Tân Bình", "Bình Tân"],
    "Bình Tân":  ["Quận 6", "Quận 8", "Tân Phú", "Bình Chánh", "Hóc Môn"],
    "Thủ Đức":   ["Bình Thạnh", "Quận 12", "Hóc Môn"],
    "Nhà Bè":    ["Quận 4", "Quận 7", "Bình Chánh", "Cần Giờ"],
    "Hóc Môn":   ["Quận 12", "Gò Vấp", "Bình Tân", "Thủ Đức", "Củ Chi"],
    "Củ Chi":    ["Hóc Môn", "Bình Chánh"],
    "Bình Chánh": ["Quận 7", "Quận 8", "Bình Tân", "Nhà Bè", "Củ Chi", "Cần Giờ"],
    "Cần Giờ":   ["Nhà Bè", "Bình Chánh"]
}

print("\n--- CÁC CẶP BỊ THIẾU (có trong GADM nhưng không có trong OLD_NEIGHBORS) ---")
missing = []
for d in HCMC_DISTRICTS:
    old_nb = set(OLD_NEIGHBORS.get(d, []))
    new_nb = new_neighbors[d]
    for nb in new_nb:
        if nb not in old_nb:
            pair = tuple(sorted([d, nb]))
            if pair not in missing:
                missing.append(pair)
                print(f"  THIẾU: {d} <-> {nb}")

print("\n--- CÁC CẶP DƯ THỪA (có trong OLD nhưng không có trong GADM) ---")
for d in HCMC_DISTRICTS:
    old_nb = set(OLD_NEIGHBORS.get(d, []))
    new_nb = new_neighbors[d]
    for nb in old_nb:
        if nb not in new_nb and nb in HCMC_DISTRICTS:
            pair = tuple(sorted([d, nb]))
            print(f"  THỪA: {d} <-> {nb}")
