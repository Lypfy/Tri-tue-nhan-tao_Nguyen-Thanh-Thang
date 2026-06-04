# Màu sắc cho lưới Visualization
COLOR_DIRTY_CELL = "#D2B48C"  # Nâu nhạt
COLOR_CLEAN_CELL = "#ADD8E6"  # Xanh dương nhạt
COLOR_VACUUM = "#FFD700"      # Vàng
COLOR_RUG_CELL = "#A9A9A9"    # Xám (thảm dày)

COST_NORMAL = 1
COST_RUG = 10

# Màu sắc giao diện chung
COLOR_BG_MAIN = "#F0F0F0"
COLOR_BG_SIDEBAR = "#2B2B2B"

# Nút bấm
COLOR_BTN_START = "#4CAF50"   # Xanh lá mạ
COLOR_BTN_RESET = "#F44336"   # Đỏ

# Cấu hình grid
GRID_SIZE = 5

# Cấu hình môi trường đầu vào
INITIAL_ENVIRONMENT = (
    ("Dirty", "Clean", "Clean", "Clean", "Dirty"),
    ("Clean", "Clean", "Clean", "Clean", "Clean"),
    ("Clean", "Clean", "Dirty", "Clean", "Clean"),
    ("Clean", "Clean", "Clean", "Clean", "Clean"),
    ("Dirty", "Clean", "Clean", "Clean", "Dirty")
)
INITIAL_X, INITIAL_Y = 2, 2

TERRAIN_MATRIX = [
    ["Normal", "Normal", "Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Rug", "Normal", "Normal"],
    ["Normal", "Rug", "Normal", "Rug", "Normal"],
    ["Normal", "Normal", "Rug", "Normal", "Normal"],
    ["Normal", "Normal", "Normal", "Normal", "Normal"]
]
