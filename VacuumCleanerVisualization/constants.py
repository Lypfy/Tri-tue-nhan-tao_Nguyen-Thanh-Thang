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

ROOM_ENVIRONMENTS = {
    "Phòng 3x3 (Cơ bản)": {
        "GRID_SIZE": GRID_SIZE,
        "INITIAL_ENVIRONMENT": INITIAL_ENVIRONMENT,
        "INITIAL_X": INITIAL_X,
        "INITIAL_Y": INITIAL_Y,
        "TERRAIN_MATRIX": TERRAIN_MATRIX
    },
    "Phòng trơn trượt (Slippery 3x3)": {
        "GRID_SIZE": 3,
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Dirty", "Dirty"),
            ("Dirty", "Dirty", "Dirty"),
            ("Dirty", "Dirty", "Dirty")
        ),
        "INITIAL_X": 1,
        "INITIAL_Y": 1,
        "TERRAIN_MATRIX": [
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"]
        ]
    }
}
