# File constant 3x3 thể hiện bản chất của thuật toán Tìm kiếm Có Thông tin (Informed Search)
# Đặc điểm: A* tính toán cả chi phí (g(n)) và khoảng cách ước lượng (h(n)). GBFS chỉ dùng h(n).
# Môi trường: 3x3 với một tấm thảm (Rug - chi phí cao) nằm chắn đường đi ngắn nhất đến vết bẩn.
# GBFS có thể đi thẳng qua thảm vì khoảng cách ngắn hơn, nhưng A* sẽ đi vòng qua thảm để tiết kiệm chi phí.

# Cấu hình grid
GRID_SIZE = 3

# Cấu hình môi trường đầu vào
INITIAL_ENVIRONMENT = (
    ("Clean", "Clean", "Dirty"),
    ("Clean", "Clean", "Clean"),
    ("Clean", "Clean", "Clean")
)
INITIAL_X, INITIAL_Y = 2, 0  # Máy hút bụi bắt đầu ở góc dưới bên trái

TERRAIN_MATRIX = [
    ["Normal", "Normal", "Normal"],
    ["Rug",    "Rug",    "Normal"],
    ["Normal", "Normal", "Normal"]
]
