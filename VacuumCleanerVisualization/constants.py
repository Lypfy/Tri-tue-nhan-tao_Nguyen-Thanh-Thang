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
    ("Clean", "Clean", "Dirty", "Clean", "Clean"),
    ("Clean", "Dirty", "Clean", "Dirty", "Clean"),
    ("Clean", "Clean", "Clean", "Clean", "Clean"),
    ("Dirty", "Clean", "Clean", "Clean", "Dirty")
)
INITIAL_X, INITIAL_Y = 2, 2  # Máy hút bụi bắt đầu ở giữa

TERRAIN_MATRIX = [
    ["Normal", "Normal", "Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal", "Normal", "Normal"],
    ["Normal", "Normal", "Normal", "Normal", "Normal"]
]

ENVIRONMENTS = {
    "Phòng 5x5 (Cơ bản)": {
        "TYPE": "Grid",
        "GRID_SIZE": GRID_SIZE,
        "INITIAL_ENVIRONMENT": INITIAL_ENVIRONMENT,
        "INITIAL_X": INITIAL_X,
        "INITIAL_Y": INITIAL_Y,
        "TERRAIN_MATRIX": TERRAIN_MATRIX
    },
    "Phòng có thảm (Thử nghiệm Informed)": {
        "TYPE": "Grid",
        "GRID_SIZE": 5,
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Clean", "Clean", "Clean", "Dirty"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Clean", "Clean", "Dirty", "Clean", "Clean")
        ),
        "INITIAL_X": 4,
        "INITIAL_Y": 0,
        "TERRAIN_MATRIX": [
            ["Normal", "Rug", "Rug", "Rug", "Normal"],
            ["Normal", "Rug", "Rug", "Rug", "Normal"],
            ["Normal", "Rug", "Rug", "Rug", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"]
        ]
    },
    "Phòng trơn trượt (Slippery 3x3)": {
        "TYPE": "Grid",
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
    },
    "Bản đồ TPHCM (CSP)": {
        "TYPE": "CSP"
    },
    "TicTacToe": {
        "TYPE": "TicTacToe"
    },

    # ── Local Search Environments ──────────────────────────────────────────────
    # Môi trường thiết kế đặc biệt để làm nổi bật bản chất của các thuật toán
    # leo đồi: robot phải đi từ góc xuyên qua toàn bộ map để dọn sạch,
    # giúp thấy rõ cách objective function giảm dần theo từng bước di chuyển.
    "Phòng Local Search (5x5)": {
        "TYPE": "Grid",
        "GRID_SIZE": 5,
        # Vết bẩn ở 4 góc + giữa: thách thức leo đồi phải traverse toàn map
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Clean", "Clean", "Clean", "Dirty"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Clean", "Clean", "Dirty", "Clean", "Clean"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Dirty", "Clean", "Clean", "Clean", "Dirty"),
        ),
        # Robot bắt đầu ở góc (0,0): phải đi xa để dọn hết
        "INITIAL_X": 0,
        "INITIAL_Y": 0,
        # Không có Rug: local search không dùng cost-aware heuristic
        "TERRAIN_MATRIX": [
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
        ]
    },

    # Môi trường với nhiều vết bẩn phân tán đều, robot ở trung tâm.
    # Phù hợp với Local Beam Search: k beams có thể "tản ra" theo nhiều hướng
    # song song, thể hiện rõ lợi thế của việc duy trì k trạng thái cùng lúc.
    "Phòng Beam (5x5)": {
        "TYPE": "Grid",
        "GRID_SIZE": 5,
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Clean", "Dirty", "Clean", "Dirty"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Dirty", "Clean", "Clean", "Clean", "Dirty"),
            ("Clean", "Clean", "Clean", "Clean", "Clean"),
            ("Dirty", "Clean", "Dirty", "Clean", "Dirty"),
        ),
        "INITIAL_X": 2,
        "INITIAL_Y": 2,
        "TERRAIN_MATRIX": [
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal", "Normal", "Normal"],
        ]
    },
    
    # ── Complex Environments ──────────────────────────────────────────────
    "Môi trường nhìn thấy 1 phần (3x3)": {
        "TYPE": "Grid",
        "GRID_SIZE": 3,
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Clean", "Dirty"),
            ("Clean", "Dirty", "Clean"),
            ("Dirty", "Clean", "Dirty")
        ),
        "INITIAL_X": 1,
        "INITIAL_Y": 1,
        "TERRAIN_MATRIX": [
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"]
        ]
    },
    "Môi trường không cảm biến (3x3)": {
        "TYPE": "Grid",
        "GRID_SIZE": 3,
        "INITIAL_ENVIRONMENT": (
            ("Dirty", "Clean", "Dirty"),
            ("Clean", "Dirty", "Clean"),
            ("Dirty", "Clean", "Dirty")
        ),
        "INITIAL_X": 1,
        "INITIAL_Y": 1,
        "TERRAIN_MATRIX": [
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"],
            ["Normal", "Normal", "Normal"]
        ]
    },
}

# TicTacToe Colors
COLOR_X = "#E74C3C"  # Đỏ
COLOR_O = "#3498DB"  # Xanh dương
