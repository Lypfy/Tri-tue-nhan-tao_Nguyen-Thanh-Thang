import json

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

# Grid sampling approach to find rough polygons
W = 100
H = 100
grid = [[None for _ in range(W)] for _ in range(H)]

for y in range(H):
    for x in range(W):
        nx = x / W
        ny = y / H
        # Find closest
        min_d = float('inf')
        closest = None
        for d, (px, py) in DISTRICT_POSITIONS.items():
            dist = (nx - px)**2 + (ny - py)**2
            if dist < min_d:
                min_d = dist
                closest = d
        grid[y][x] = closest

# For each district, find the boundary points
# We will just trace the boundary or take the convex hull of the points
polygons = {}

def get_convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1: return points
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

for d in DISTRICT_POSITIONS.keys():
    pts = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == d:
                # Is boundary?
                is_boundary = False
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if 0 <= y+dy < H and 0 <= x+dx < W:
                            if grid[y+dy][x+dx] != d:
                                is_boundary = True
                                break
                    if is_boundary: break
                if is_boundary or x==0 or y==0 or x==W-1 or y==H-1:
                    pts.append((x/W, y/H))
    
    if pts:
        hull = get_convex_hull(pts)
        polygons[d] = hull

with open("polygons.json", "w", encoding="utf-8") as f:
    json.dump(polygons, f, ensure_ascii=False, indent=2)

print("Generated polygons.json")
