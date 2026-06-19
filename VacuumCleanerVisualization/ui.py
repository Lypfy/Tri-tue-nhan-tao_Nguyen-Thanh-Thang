import tkinter as tk
from tkinter import ttk
from constants import *
from algorithms import bfs1, bfs2, dfs1, dfs2, ucs_standard, iddfs, gbfs, a_star, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, random_restart_hill_climbing, local_beam_search, simulated_annealing, belief_dfs, sensorless_belief_dfs, partially_observable_belief_dfs, and_or_graph_search
from algorithms import backtracking_search, HCMC_DISTRICTS, HCMC_NEIGHBORS, DISTRICT_POSITIONS, COLOR_HEX, DISTRICT_POLYGONS
import time
import threading
import random

class AccordionMenu(tk.Frame):
    def __init__(self, master, title, options, var, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDEBAR, **kwargs)
        self.var = var
        self.options = options
        self.is_expanded = False
        
        # Nút tiêu đề của nhóm
        self.btn_header = tk.Button(self, text=f"▶ {title}", anchor="w", 
                                    bg="#444444", fg="white", activebackground="#555555", activeforeground="white",
                                    relief="flat", font=("Arial", 9, "bold"),
                                    command=self.toggle)
        self.btn_header.pack(fill="x", pady=(5,0))
        
        # Khu vực chứa nội dung sổ xuống
        self.content_frame = tk.Frame(self, bg=COLOR_BG_SIDEBAR)
        
        self.radio_buttons = []
        for opt in options:
            rb = tk.Radiobutton(self.content_frame, text=opt, variable=self.var, value=opt,
                                bg=COLOR_BG_SIDEBAR, fg="white", selectcolor="#444444",
                                activebackground=COLOR_BG_SIDEBAR, activeforeground="white",
                                font=("Arial", 9))
            self.radio_buttons.append(rb)

    def toggle(self):
        if self.is_expanded:
            self.content_frame.pack_forget()
            self.btn_header.configure(text=self.btn_header.cget("text").replace("▼", "▶"))
        else:
            self.content_frame.pack(fill="x", padx=(20, 0), pady=5)
            for rb in self.radio_buttons:
                rb.pack(anchor="w", pady=2)
            self.btn_header.configure(text=self.btn_header.cget("text").replace("▶", "▼"))
        self.is_expanded = not self.is_expanded


class VacuumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vacuum Cleaner AI Visualization")
        self.geometry("1100x650")
        self.configure(bg=COLOR_BG_MAIN)
        
        # Cấu hình grid chính
        self.grid_columnconfigure(0, weight=1, uniform="equal_cols") # Sidebar
        self.grid_columnconfigure(1, weight=3, uniform="equal_cols") # Main
        self.grid_columnconfigure(2, weight=2, uniform="equal_cols") # Right log
        self.grid_rowconfigure(0, weight=1)
        
        self.is_running = False
        self.csp_mode = False          # True khi đang ở chế độ CSP
        self.csp_coloring = {}         # Kết quả tô màu hiện tại

        # Zoom & Pan state cho CSP
        self.csp_zoom = 1.0
        self.csp_pan_x = 0.0
        self.csp_pan_y = 0.0
        self._drag_start = None
        # Room setup
        self.room_var = tk.StringVar(value="Phòng 3x3 (Cơ bản)")
        self.load_environment()
        
        self.setup_sidebar()
        self.setup_main_area()
        self.setup_action_log()
        
        self.draw_grid()

    def load_environment(self):
        env_key = self.room_var.get()
        config = ROOM_ENVIRONMENTS.get(env_key, ROOM_ENVIRONMENTS["Phòng 3x3 (Cơ bản)"])
        self.grid_size = config["GRID_SIZE"]
        self.initial_environment = config["INITIAL_ENVIRONMENT"]
        self.initial_x, self.initial_y = config["INITIAL_X"], config["INITIAL_Y"]
        self.terrain_matrix = config["TERRAIN_MATRIX"]
        self.env_list = [list(row) for row in self.initial_environment]
        self.vac_x, self.vac_y = self.initial_x, self.initial_y
        self.current_belief_state = None

    def on_room_change(self, event):
        if self.is_running: return
        self.load_environment()
        self.reset_simulation()

    def setup_sidebar(self):
        self.sidebar_container = tk.Frame(self, bg=COLOR_BG_SIDEBAR)
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_canvas = tk.Canvas(self.sidebar_container, bg=COLOR_BG_SIDEBAR, highlightthickness=0)
        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_container, orient="vertical", command=self.sidebar_canvas.yview)
        
        self.sidebar = tk.Frame(self.sidebar_canvas, bg=COLOR_BG_SIDEBAR)
        self.sidebar.bind(
            "<Configure>",
            lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))
        )
        
        self.sidebar_window = self.sidebar_canvas.create_window((0, 0), window=self.sidebar, anchor="nw")
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)
        
        self.sidebar_canvas.pack(side="left", fill="both", expand=True)
        self.sidebar_scrollbar.pack(side="right", fill="y")
        
        # Đảm bảo sidebar chiếm toàn bộ chiều rộng của canvas
        self.sidebar_canvas.bind("<Configure>", lambda e: self.sidebar_canvas.itemconfig(self.sidebar_window, width=e.width))
        
        # Bind cuộn chuột
        def _on_mousewheel(event):
            self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        lbl_title = tk.Label(self.sidebar, text="Algorithm Selection", font=("Arial", 14, "bold"), bg=COLOR_BG_SIDEBAR, fg="white")
        lbl_title.pack(pady=(10, 10), padx=10)
        
        lbl_room = tk.Label(self.sidebar, text="Room Environment", bg=COLOR_BG_SIDEBAR, fg="white", font=("Arial", 9))
        lbl_room.pack(pady=(5, 0))
        self.cb_room = ttk.Combobox(self.sidebar, textvariable=self.room_var, values=list(ROOM_ENVIRONMENTS.keys()), state="readonly")
        self.cb_room.pack(pady=5, padx=10, fill="x")
        self.cb_room.bind("<<ComboboxSelected>>", self.on_room_change)
        
        self.algo_var = tk.StringVar(value="BFS 1 (Cơ bản)")
        
        self.acc_uninformed = AccordionMenu(self.sidebar, "Tìm kiếm không có thông tin", 
                                            ["BFS 1 (Cơ bản)", "BFS 2 (Tối ưu)", "DFS 1 (Cơ bản)", "DFS 2 (Tối ưu)", "UCS", "IDDFS"], self.algo_var)
        self.acc_uninformed.pack(fill="x", padx=10, pady=5)
        self.acc_uninformed.toggle() # Mở sẵn
        
        self.acc_informed = AccordionMenu(self.sidebar, "Tìm kiếm có thông tin", 
                                          ["Greedy BFS", "A*", "IDA*"], self.algo_var)
        self.acc_informed.pack(fill="x", padx=10, pady=5)
        
        self.acc_local_search = AccordionMenu(self.sidebar, "Tìm kiếm cục bộ", 
                                              ["Leo đồi đơn giản", "Leo đồi dốc nhất", "Leo đồi ngẫu nhiên", "Leo đồi khởi động lại", "Local Beam Search", "Mô phỏng luyện kim"], self.algo_var)
        self.acc_local_search.pack(fill="x", padx=10, pady=5)
        
        self.acc_complex_env = AccordionMenu(self.sidebar, "Môi trường phức tạp", 
                                              ["Nhìn thấy một phần (DFS)", "Không nhìn thấy (DFS)", "HĐ Không xác định"], self.algo_var)
        self.acc_complex_env.pack(fill="x", padx=10, pady=5)
        
        self.acc_csp = AccordionMenu(self.sidebar, "Constraint Satisfaction",
                                     ["Backtracking Search", "Backtracking + AC-3", "Min-Conflicts"], self.algo_var)
        self.acc_csp.pack(fill="x", padx=10, pady=5)
        
        self.btn_start = tk.Button(self.sidebar, text="Start Visualization", bg=COLOR_BTN_START, fg="white", 
                                   activebackground="#388E3C", activeforeground="white", font=("Arial", 11, "bold"),
                                   relief="flat", command=self.start_simulation)
        self.btn_start.pack(pady=(20, 10), padx=10, fill="x", ipady=5)
        
        self.btn_reset = tk.Button(self.sidebar, text="Reset", bg=COLOR_BTN_RESET, fg="white", 
                                   activebackground="#D32F2F", activeforeground="white", font=("Arial", 11, "bold"),
                                   relief="flat", command=self.reset_simulation)
        self.btn_reset.pack(pady=5, padx=10, fill="x", ipady=5)
        
        lbl_speed = tk.Label(self.sidebar, text="Animation Speed", bg=COLOR_BG_SIDEBAR, fg="white", font=("Arial", 9))
        lbl_speed.pack(pady=(20, 0))
        self.slider_speed = ttk.Scale(self.sidebar, from_=0.1, to=4.0, orient="horizontal")
        self.slider_speed.set(1.0)
        self.slider_speed.pack(pady=10, padx=20, fill="x")

    def setup_main_area(self):
        self.main_area = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main_area.grid_rowconfigure(0, weight=4)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)
        
        # Khu vực vẽ lưới
        self.canvas_frame = tk.Frame(self.main_area, bg=COLOR_BG_MAIN)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.canvas = tk.Canvas(self.canvas_frame, bg=COLOR_BG_MAIN, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Bắt sự kiện resize để vẽ lại grid cho vừa
        self.canvas.bind("<Configure>", lambda e: self.draw_grid())

        # ── Zoom & Pan cho CSP map ──────────────────────────────
        self.canvas.bind("<MouseWheel>",       self._on_csp_scroll)    # Windows
        self.canvas.bind("<Button-4>",         self._on_csp_scroll)    # Linux scroll up
        self.canvas.bind("<Button-5>",         self._on_csp_scroll)    # Linux scroll down
        self.canvas.bind("<ButtonPress-1>",    self._on_pan_start)
        self.canvas.bind("<B1-Motion>",        self._on_pan_move)
        self.canvas.bind("<ButtonRelease-1>",  self._on_pan_end)
        self.canvas.bind("<Double-Button-1>",  self._on_zoom_reset)
        
        # Khu vực Final Solution
        self.solution_frame = tk.Frame(self.main_area, bg=COLOR_BG_MAIN)
        self.solution_frame.grid(row=1, column=0, sticky="nsew")
        
        lbl_sol = tk.Label(self.solution_frame, text="Final Solution", font=("Arial", 12, "bold"), bg=COLOR_BG_MAIN)
        lbl_sol.pack(pady=5)
        
        self.txt_solution = tk.Text(self.solution_frame, width=1, height=1, font=("Consolas", 10), bg="white", fg="black", relief="solid", bd=1)
        self.txt_solution.pack(fill="both", expand=True)
        self.txt_solution.configure(state="disabled")

    def setup_action_log(self):
        self.log_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.log_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        lbl_log = tk.Label(self.log_frame, text="ACTION LOG", font=("Arial", 12, "bold"), bg=COLOR_BG_MAIN)
        lbl_log.pack(pady=10)
        
        self.txt_log = tk.Text(self.log_frame, width=1, height=1, font=("Consolas", 9), bg="white", fg="black", relief="solid", bd=1)
        self.txt_log.pack(fill="both", expand=True)
        self.txt_log.configure(state="disabled")

    def log(self, message):
        def _log():
            self.txt_log.configure(state="normal")
            self.txt_log.insert("end", message + "\n")
            self.txt_log.see("end")
            self.txt_log.configure(state="disabled")
        self.after(0, _log)
        
    def set_solution_text(self, text):
        def _set():
            self.txt_solution.configure(state="normal")
            self.txt_solution.delete("1.0", "end")
            self.txt_solution.insert("end", text)
            self.txt_solution.configure(state="disabled")
        self.after(0, _set)

    def draw_grid(self):
        self.canvas.delete("all")
        self.update_idletasks()
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        cell_w = width / self.grid_size
        cell_h = height / self.grid_size
        
        # Calculate belief state probabilities if active
        dirt_probs = {}
        vac_positions = set()
        is_belief = self.current_belief_state is not None
        
        if is_belief:
            num_states = len(self.current_belief_state)
            for state in self.current_belief_state:
                grid, vx, vy = state
                vac_positions.add((vx, vy))
                for r in range(self.grid_size):
                    for c in range(self.grid_size):
                        if grid[r][c] == "Dirty":
                            dirt_probs[(r, c)] = dirt_probs.get((r, c), 0) + 1
            for k in dirt_probs:
                dirt_probs[k] /= num_states
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x0 = c * cell_w
                y0 = r * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                
                # Determine cell appearance
                if is_belief:
                    prob = dirt_probs.get((r, c), 0)
                    if prob > 0:
                        bg_color = COLOR_DIRTY_CELL
                        status_text = f"Bẩn ({int(prob*100)}%)"
                    else:
                        bg_color = COLOR_CLEAN_CELL
                        status_text = "Sạch"
                else:
                    bg_color = COLOR_DIRTY_CELL if self.env_list[r][c] == "Dirty" else COLOR_CLEAN_CELL
                    status_text = "Bẩn" if self.env_list[r][c] == "Dirty" else "Sạch"
                
                if self.terrain_matrix[r][c] == "Rug":
                    cost_text = f"\n(Phí: {COST_RUG})"
                else:
                    cost_text = f"\n(Phí: {COST_NORMAL})"
                    
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="white", width=2)
                
                text = status_text + cost_text
                font_size = max(8, int(min(cell_w, cell_h) / 8))
                self.canvas.create_text((x0+x1)/2, (y0+y1)/2 - font_size, text=text, font=("Arial", font_size, "bold"), fill="#222222", justify="center")
                
                # Vẽ robot
                cx, cy = (x0+x1)/2, (y0+y1)/2 + font_size
                radius = min(cell_w, cell_h) / 5
                robot_font = max(6, int(font_size * 0.7))
                
                if is_belief:
                    if (r, c) in vac_positions:
                        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill=COLOR_VACUUM, outline="#C4A000", width=3)
                        self.canvas.create_text(cx, cy, text=f"AI", font=("Arial", robot_font, "bold"), fill="black")
                else:
                    if r == self.vac_x and c == self.vac_y:
                        is_slip = getattr(self, "is_slipping", False)
                        color = "#FF4500" if is_slip else COLOR_VACUUM
                        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill=color, outline="#C4A000", width=3)
                        self.canvas.create_text(cx, cy, text="AI", font=("Arial", robot_font, "bold"), fill="black")
                        if is_slip:
                            self.canvas.create_text(cx, cy - radius - 15, text="Oops! Trượt", font=("Arial", max(8, int(font_size*0.8)), "bold"), fill="red")

    # ──────────────────────────────────────────────────────────────
    # ZOOM & PAN HANDLERS
    # ──────────────────────────────────────────────────────────────
    def _on_csp_scroll(self, event):
        """Zoom bản đồ CSP vào/ra tại vị trí con trỏ chuột."""
        if not self.csp_mode:
            return
        # Xác định hướng scroll
        if event.num == 4:      # Linux scroll up
            delta = 1
        elif event.num == 5:    # Linux scroll down
            delta = -1
        else:                   # Windows
            delta = 1 if event.delta > 0 else -1

        factor = 1.15 if delta > 0 else (1 / 1.15)
        old_zoom = self.csp_zoom
        self.csp_zoom = max(0.5, min(10.0, self.csp_zoom * factor))
        actual_factor = self.csp_zoom / old_zoom

        # Zoom hướng vào vị trí con trỏ
        mx, my = event.x, event.y
        self.csp_pan_x = mx - actual_factor * (mx - self.csp_pan_x)
        self.csp_pan_y = my - actual_factor * (my - self.csp_pan_y)

        if self.csp_mode:
            self.after(0, lambda col=dict(self.csp_coloring), st=getattr(self, '_last_step_info', None):
                       self.draw_csp_map(col, st))

    def _on_pan_start(self, event):
        if not self.csp_mode:
            return
        self._drag_start = (event.x, event.y)

    def _on_pan_move(self, event):
        if not self.csp_mode or self._drag_start is None:
            return
        dx = event.x - self._drag_start[0]
        dy = event.y - self._drag_start[1]
        self.csp_pan_x += dx
        self.csp_pan_y += dy
        self._drag_start = (event.x, event.y)
        self.after(0, lambda col=dict(self.csp_coloring), st=getattr(self, '_last_step_info', None):
                   self.draw_csp_map(col, st))

    def _on_pan_end(self, event):
        self._drag_start = None

    def _on_zoom_reset(self, event):
        """Double-click: reset zoom và pan về trạng thái ban đầu."""
        if not self.csp_mode:
            return
        self.csp_zoom = 1.0
        self.csp_pan_x = 0.0
        self.csp_pan_y = 0.0
        self.after(0, lambda col=dict(self.csp_coloring), st=getattr(self, '_last_step_info', None):
                   self.draw_csp_map(col, st))

    def reset_simulation(self):
        self.is_running = False
        self.env_list = [list(row) for row in self.initial_environment]
        self.vac_x, self.vac_y = self.initial_x, self.initial_y
        self.current_belief_state = None
        self.csp_coloring = {}
        self._last_step_info = None

        # Reset zoom & pan khi bắt đầu lại
        self.csp_zoom = 1.0
        self.csp_pan_x = 0.0
        self.csp_pan_y = 0.0
        
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")
        
        self.set_solution_text("")
        
        # Chọn kiểu vẽ tuỳ theo chế độ
        if self.csp_mode:
            self.draw_csp_map({}, None)
        else:
            self.draw_grid()
        self.btn_start.configure(state="normal")

    def start_simulation(self):
        if self.is_running: return
        # Xác định chế độ trước khi reset
        algo = self.algo_var.get()
        self.csp_mode = algo in ("Backtracking Search", "Backtracking + AC-3", "Min-Conflicts")
        self.reset_simulation()
        self.is_running = True
        self.btn_start.configure(state="disabled")
        
        # Chạy thuật toán trong luồng riêng để UI không bị đơ
        threading.Thread(target=self.run_algorithm, daemon=True).start()
        
    # ──────────────────────────────────────────────────────────────
    # CSP VISUALIZATION
    # ──────────────────────────────────────────────────────────────
    def draw_csp_map(self, coloring, step_info):
        """Vẽ bản đồ đồ thị quận TPHCM với tô màu hiện tại."""
        # Lưu step_info mới nhất để pan/zoom có thể vẽ lại
        self._last_step_info = step_info

        self.canvas.delete("all")
        self.update_idletasks()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return

        margin_x, margin_y = 40, 40
        usable_w = w - 2 * margin_x
        usable_h = h - 2 * margin_y

        # Áp dụng zoom & pan: hàm chuyển đổi tọa độ normalized -> pixel
        z = self.csp_zoom
        px0 = self.csp_pan_x  # pan offset
        py0 = self.csp_pan_y

        def to_screen(nx, ny):
            sx = margin_x + nx * usable_w
            sy = margin_y + ny * usable_h
            # Áp dụng zoom quanh tâm canvas
            cx = w / 2
            cy = (h - 55) / 2  # Trừ overlay phía dưới
            sx = cx + (sx - cx) * z + px0
            sy = cy + (sy - cy) * z + py0
            return sx, sy

        def pos(district):
            nx, ny = DISTRICT_POSITIONS[district]
            return to_screen(nx, ny)

        current = step_info["current"] if step_info else None

        def get_center(district):
            if district in DISTRICT_POLYGONS:
                all_pts = []
                for poly_pts in DISTRICT_POLYGONS[district]:
                    all_pts.extend(poly_pts)
                if all_pts:
                    cx = sum(x for x, y in all_pts) / len(all_pts)
                    cy = sum(y for x, y in all_pts) / len(all_pts)
                    return to_screen(cx, cy)
            return pos(district)

        # Vẽ polygon
        for d in HCMC_DISTRICTS:
            if d in DISTRICT_POLYGONS:
                color_name = coloring.get(d)
                fill = COLOR_HEX.get(color_name, "#AAAAAA")

                # Hiệu ứng: node đang xét thì viền đậm hơn
                if step_info and d == current:
                    outline = "#FFFFFF"
                    outline_w = 3
                else:
                    outline = "#444444"
                    outline_w = 1

                for poly_pts in DISTRICT_POLYGONS[d]:
                    screen_pts = []
                    for (nx, ny) in poly_pts:
                        sx, sy = to_screen(nx, ny)
                        screen_pts.extend([sx, sy])

                    if screen_pts:
                        self.canvas.create_polygon(screen_pts, fill=fill, outline=outline, width=outline_w)

        # Highlight cạnh đang vi phạm ràng buộc (nếu có)
        if current and coloring.get(current):
            cx, cy = get_center(current)
            for nb in HCMC_NEIGHBORS[current]:
                if coloring.get(nb) == coloring.get(current):
                    nx2, ny2 = get_center(nb)
                    self.canvas.create_line(cx, cy, nx2, ny2,
                                            fill="#FF0000", width=4, dash=(8, 4))
        
        # Draw arc consistency check line
        if step_info and step_info.get("action") == "revise":
            target = step_info.get("target")
            if target and target in DISTRICT_POSITIONS and current in DISTRICT_POSITIONS:
                cx, cy = get_center(current)
                tx, ty = get_center(target)
                self.canvas.create_line(tx, ty, cx, cy, fill="#FF69B4", width=3, arrow=tk.LAST, dash=(4, 4))


        # Highlight viền quận đang xét (vẽ lại polygon với viền sáng)
        if current and current in DISTRICT_POLYGONS:
            for poly_pts in DISTRICT_POLYGONS[current]:
                screen_pts = []
                for (nx, ny) in poly_pts:
                    sx, sy = to_screen(nx, ny)
                    screen_pts.extend([sx, sy])
                if screen_pts:
                    self.canvas.create_polygon(screen_pts, fill="", outline="#FFD700", width=3)

        # Vẽ Tên quận
        for d in HCMC_DISTRICTS:
            px, py = get_center(d)
            color_name = coloring.get(d)

            # Tên quận rút gọn
            short = d.replace("Quận ", "Q").replace("Bình Thạnh", "B.Thạnh")\
                      .replace("Bình Tân", "B.Tân").replace("Bình Chánh", "B.Chánh")\
                      .replace("Cần Giờ", "C.Giờ").replace("Hóc Môn", "H.Môn")\
                      .replace("Củ Chi", "C.Chi").replace("Nhà Bè", "N.Bè")\
                      .replace("Tân Bình", "T.Bình").replace("Tân Phú", "T.Phú")\
                      .replace("Thủ Đức", "T.Đức").replace("Gò Vấp", "G.Vấp")\
                      .replace("Phú Nhuận", "P.Nhuận")
            fsize = max(7, int(min(usable_w, usable_h) // 40 * z))
            fsize = max(7, min(fsize, 18))  # giới hạn font

            # Màu chữ tuỳ màu nền
            text_fill = "#111111" if color_name in ("Vàng", "Xanh lá") else "#FFFFFF"
            if color_name is None:
                text_fill = "#DDDDDD"

            fw = "bold"
            if d == current:
                self.canvas.create_text(px+1, py+1, text=short,
                                        font=("Arial", fsize, fw), fill="#000000")
            self.canvas.create_text(px, py, text=short,
                                    font=("Arial", fsize, fw), fill=text_fill)

        # Overlay hướng dẫn zoom (góc trên phải)
        self.canvas.create_text(w - 10, 10, text="🖱 Scroll: Zoom | Kéo: Di chuyển | Double-click: Reset",
                                font=("Arial", 8), fill="#888888", anchor="ne")

        # Overlay thông tin zoom
        zoom_pct = int(self.csp_zoom * 100)
        self.canvas.create_text(10, 10, text=f"Zoom: {zoom_pct}%",
                                font=("Arial", 9, "bold"), fill="#AAAAAA", anchor="nw")

        # Overlay thông tin bước
        if step_info:
            action = step_info.get("action", "")
            msg = step_info.get("message", "")
            assigned = sum(1 for v in coloring.values() if v is not None)
            total = len(HCMC_DISTRICTS)

            bg_color = {"assign": "#1A472A", "backtrack": "#7B1818", "done": "#1A3A6A"}.get(action, "#333333")
            self.canvas.create_rectangle(10, h - 55, w - 10, h - 10,
                                         fill=bg_color, outline="", stipple="")
            self.canvas.create_text(w // 2, h - 38, text=msg,
                                    font=("Arial", 10, "bold"), fill="white")
            self.canvas.create_text(w // 2, h - 20,
                                    text=f"Đã tô: {assigned}/{total} quận",
                                    font=("Arial", 9), fill="#DDDDDD")

    def run_algorithm(self):
        initial_state = (self.initial_environment, self.initial_x, self.initial_y)
        algo = self.algo_var.get()
        
        self.log(f"--- Bắt đầu mô phỏng: {algo} ---")

        # ── CSP MODE ──────────────────────────────────────────────
        if algo in ("Backtracking Search", "Backtracking + AC-3", "Min-Conflicts"):
            self.log(f"Đang chạy {algo}...")
            
            if algo == "Backtracking Search":
                steps = backtracking_search()
            elif algo == "Backtracking + AC-3":
                from algorithms import mac_search
                steps = mac_search()
            else:
                from algorithms import min_conflicts_search
                steps = min_conflicts_search()
                
            self.log(f"Tổng số bước (kể cả backtrack/reassign): {len(steps)}")

            for i, step in enumerate(steps):
                if not self.is_running:
                    break
                speed = self.slider_speed.get()
                delay = max(0.03, 0.5 / (speed * 2))
                time.sleep(delay)

                self.csp_coloring = step["coloring"]
                self.log(f"Bước {i+1}: {step['message']}")

                # Capture cho lambda
                s = step
                c = dict(self.csp_coloring)
                self.after(0, lambda col=c, st=s: self.draw_csp_map(col, st))

            if self.is_running:
                final_coloring = self.csp_coloring
                colors_used = set(v for v in final_coloring.values() if v)
                summary = "\n".join(f"  {d}: {c}" for d, c in sorted(final_coloring.items()))
                self.set_solution_text(
                    f"Số màu sử dụng: {len(colors_used)} ({', '.join(colors_used)})\n\n" + summary
                )
                self.log(f"--- HOÀN THÀNH: dùng {len(colors_used)} màu ---")
                self.is_running = False

            self.after(0, lambda: self.btn_start.configure(state="normal"))
            return

        # ── VACUUM MODE ───────────────────────────────────────────
        path = []
        if algo == "BFS 1 (Cơ bản)":
            path = bfs1(initial_state)
        elif algo == "BFS 2 (Tối ưu)":
            path = bfs2(initial_state)
        elif algo == "DFS 1 (Cơ bản)":
            path = dfs1(initial_state)
        elif algo == "DFS 2 (Tối ưu)":
            path = dfs2(initial_state)
        elif algo == "UCS":
            path = ucs_standard(initial_state)
        elif algo == "IDDFS":
            path = iddfs(initial_state)
        elif algo == "Greedy BFS":
            path = gbfs(initial_state)
        elif algo == "A*":
            path = a_star(initial_state)
        elif algo == "IDA*":
            path = ida_star(initial_state)
        elif algo == "Leo đồi đơn giản":
            path = simple_hill_climbing(initial_state)
        elif algo == "Leo đồi dốc nhất":
            path = steepest_ascent_hill_climbing(initial_state)
        elif algo == "Leo đồi ngẫu nhiên":
            path = stochastic_hill_climbing(initial_state)
        elif algo == "Leo đồi khởi động lại":
            path = random_restart_hill_climbing(initial_state)
        elif algo == "Local Beam Search":
            path = local_beam_search(initial_state)
        elif algo == "Mô phỏng luyện kim":
            path = simulated_annealing(initial_state)
        elif algo == "Nhìn thấy một phần (DFS)":
            path = partially_observable_belief_dfs(initial_state)
        elif algo == "Không nhìn thấy (DFS)":
            path = sensorless_belief_dfs(initial_state)
        elif algo == "HĐ Không xác định":
            path = and_or_graph_search(initial_state)
            
            if path == 'failure' or path is None:
                self.log("Không tìm thấy đường đi (Failure).")
                self.is_running = False
                self.after(0, lambda: self.btn_start.configure(state="normal"))
                return
                
            self.set_solution_text("Conditional Plan (xem Log)")
            self.log("Đã tìm thấy Conditional Plan!")
            
            # Now simulate it
            from algorithms.complex_env.and_or_search import slippery_results
            
            current_state = initial_state
            current_plan = path
            
            while self.is_running and current_plan != []:
                action, subplans = current_plan[0], current_plan[1]
                
                speed = self.slider_speed.get()
                delay = max(0.05, 1.0 / (speed * 2))
                time.sleep(delay)
                
                self.log(f"-> Thực hiện: {action}")
                
                outcomes = slippery_results(current_state, action)
                next_state = random.choice(outcomes)
                
                if len(outcomes) > 1:
                    if next_state == current_state:
                        self.log("   (Kết quả: Trượt! Robot bị đứng yên tại chỗ)")
                        self.is_slipping = True
                    else:
                        self.log("   (Kết quả: Bình thường - Di chuyển thành công)")
                        self.is_slipping = False
                else:
                    self.is_slipping = False
                        
                grid, nx, ny = next_state
                self.env_list = [list(row) for row in grid]
                self.vac_x, self.vac_y = nx, ny
                
                self.after(0, self.draw_grid)
                
                current_state = next_state
                from algorithms.common import is_goal
                if is_goal(current_state):
                    current_plan = []
                elif current_state in subplans:
                    subplan = subplans[current_state]
                    if subplan == "RETRY":
                        self.log("   -> [Nhánh lặp] Thử lại hành động trước đó do bị trượt.")
                        # Giữ nguyên current_plan để thử lại
                    else:
                        current_plan = subplan
                else:
                    self.log("Lỗi: Trạng thái không có trong kế hoạch!")
                    break
            
            if self.is_running:
                self.log("--- HOÀN THÀNH DỌN DẸP ---")
                self.is_running = False
            self.after(0, lambda: self.btn_start.configure(state="normal"))
            return
        else:
            self.log("Thuật toán đang được phát triển...")
            self.is_running = False
            self.after(0, lambda: self.btn_start.configure(state="normal"))
            return
            
        if path is None:
            self.log("Không tìm thấy đường đi.")
            self.is_running = False
            self.after(0, lambda: self.btn_start.configure(state="normal"))
            return
            
        self.set_solution_text(" -> ".join(path))
        
        # Tính toán chi phí
        total_cost = 0
        curr_x, curr_y = self.initial_x, self.initial_y
        for action in path:
            if action == "SUCK":
                total_cost += 1
            else:
                if action == "UP": curr_x -= 1
                elif action == "DOWN": curr_x += 1
                elif action == "LEFT": curr_y -= 1
                elif action == "RIGHT": curr_y += 1
                total_cost += COST_RUG if self.terrain_matrix[curr_x][curr_y] == "Rug" else COST_NORMAL
                
        self.log(f"Đã tìm thấy giải pháp gồm {len(path)} bước.")
        self.log(f"Tổng chi phí đường đi: {total_cost}")
        self.log("Bắt đầu di chuyển...")
        
        # Mô phỏng từng bước
        is_belief_algo = algo in ["Nhìn thấy một phần (DFS)", "Không nhìn thấy (DFS)"]
        
        if is_belief_algo:
            from algorithms.common import Node
            
            if algo == "Không nhìn thấy (DFS)":
                from algorithms.complex_env.belief_dfs import sensorless_child_node as belief_child_node
                
                # Khởi tạo initial belief set cho sensorless (tất cả các ô)
                grid = initial_state[0]
                initial_belief_set = set()
                for r in range(len(grid)):
                    for c in range(len(grid[0])):
                        initial_belief_set.add((grid, r, c))
                self.current_belief_state = frozenset(initial_belief_set)
                
            elif algo == "Nhìn thấy một phần (DFS)":
                from algorithms.complex_env.belief_dfs import sensorless_child_node as belief_child_node
                grid, x, _ = initial_state
                initial_belief_set = set()
                for c in range(len(grid[0])):
                    initial_belief_set.add((grid, x, c))
                self.current_belief_state = frozenset(initial_belief_set)
                
            current_belief_node = Node(self.current_belief_state)
            self.after(0, self.draw_grid)
            
            for i, action in enumerate(path):
                if not self.is_running: break
                
                speed = self.slider_speed.get()
                delay = max(0.05, 1.0 / (speed * 2))
                time.sleep(delay)
                
                self.log(f"Bước {i+1}: {action}")
                
                current_belief_node = belief_child_node(current_belief_node, action)
                self.current_belief_state = current_belief_node.state
                
                self.after(0, self.draw_grid)
        else:
            for i, action in enumerate(path):
                if not self.is_running: break
                
                # Slider speed logic
                speed = self.slider_speed.get()
                delay = max(0.05, 1.0 / (speed * 2))
                time.sleep(delay)
                
                self.log(f"Bước {i+1}: {action}")
                if action == "SUCK":
                    self.env_list[self.vac_x][self.vac_y] = "Clean"
                elif action == "UP": self.vac_x -= 1
                elif action == "DOWN": self.vac_x += 1
                elif action == "RIGHT": self.vac_y += 1
                elif action == "LEFT": self.vac_y -= 1
                
                self.log(f"  -> Máy ở vị trí ({self.vac_x}, {self.vac_y})")
                
                self.after(0, self.draw_grid)
            
        if self.is_running:
            self.log("--- HOÀN THÀNH DỌN DẸP ---")
            self.is_running = False
        
        self.after(0, lambda: self.btn_start.configure(state="normal"))
