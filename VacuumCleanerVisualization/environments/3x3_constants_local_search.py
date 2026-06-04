# File constant 3x3 thể hiện bản chất của thuật toán Tìm kiếm Cục bộ (Local Search)
# Đặc điểm: Leo đồi (Hill Climbing) chỉ nhìn vào các trạng thái lân cận để tìm bước đi giảm thiểu giá trị hàm mục tiêu (khoảng cách Manhattan đến vết bẩn).
# Môi trường: 3x3 với vết bẩn ở nhiều vị trí, thể hiện cách Local Search bị hút về vết bẩn gần nhất và có thể bị mắc kẹt (nếu hàm mục tiêu không hoàn hảo).

# Cấu hình grid
GRID_SIZE = 3

# Cấu hình môi trường đầu vào
INITIAL_ENVIRONMENT = (
    ("Dirty", "Clean", "Dirty"),
    ("Clean", "Clean", "Clean"),
    ("Dirty", "Clean", "Dirty")
)
INITIAL_X, INITIAL_Y = 1, 1  # Máy hút bụi bắt đầu ở giữa

TERRAIN_MATRIX = [
    ["Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal"]
]
