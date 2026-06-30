# File constant 3x3 thể hiện bản chất của thuật toán Tìm kiếm Mù (Uninformed Search)
# Đặc điểm: Các thuật toán tìm kiếm mù như BFS, DFS, UCS sẽ duyệt không gian trạng thái một cách hệ thống (mù quáng).
# Môi trường: 3x3 với vết bẩn ở các góc xa để thấy rõ sự khác biệt trong cách lan truyền (BFS loang đều, DFS đi sâu).

# Cấu hình grid
GRID_SIZE = 3

# Cấu hình môi trường đầu vào
INITIAL_ENVIRONMENT = (
    ("Dirty", "Clean", "Clean"),
    ("Clean", "Clean", "Clean"),
    ("Clean", "Clean", "Dirty")
)
INITIAL_X, INITIAL_Y = 1, 1  # Máy hút bụi bắt đầu ở giữa

TERRAIN_MATRIX = [
    ["Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal"]
]
