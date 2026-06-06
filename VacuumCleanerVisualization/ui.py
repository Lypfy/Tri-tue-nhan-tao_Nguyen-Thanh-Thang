import tkinter as tk
from tkinter import ttk
from constants import *
from algorithms import bfs1, bfs2, dfs1, dfs2, ucs_standard, iddfs, gbfs, a_star, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, random_restart_hill_climbing, local_beam_search, simulated_annealing, belief_gbfs
import time
import threading

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
        
        self.initial_environment = INITIAL_ENVIRONMENT
        self.initial_x, self.initial_y = INITIAL_X, INITIAL_Y
        
        self.terrain_matrix = TERRAIN_MATRIX
        
        # State để vẽ
        self.env_list = [list(row) for row in self.initial_environment]
        self.vac_x, self.vac_y = self.initial_x, self.initial_y
        
        self.setup_sidebar()
        self.setup_main_area()
        self.setup_action_log()
        
        self.draw_grid()

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
                                              ["Niềm tin (Greedy BFS)"], self.algo_var)
        self.acc_complex_env.pack(fill="x", padx=10, pady=5)
        
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
            
        cell_w = width / GRID_SIZE
        cell_h = height / GRID_SIZE
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x0 = c * cell_w
                y0 = r * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                
                bg_color = COLOR_DIRTY_CELL if self.env_list[r][c] == "Dirty" else COLOR_CLEAN_CELL
                if self.terrain_matrix[r][c] == "Rug":
                    cost_text = f"\n(Phí: {COST_RUG})"
                else:
                    cost_text = f"\n(Phí: {COST_NORMAL})"
                    
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="white", width=2)
                
                status_text = "Bẩn" if self.env_list[r][c] == "Dirty" else "Sạch"
                text = status_text + cost_text
                font_size = max(8, int(min(cell_w, cell_h) / 8))
                self.canvas.create_text((x0+x1)/2, (y0+y1)/2 - font_size, text=text, font=("Arial", font_size, "bold"), fill="#222222", justify="center")
                
                # Vẽ robot
                if r == self.vac_x and c == self.vac_y:
                    radius = min(cell_w, cell_h) / 5
                    cx, cy = (x0+x1)/2, (y0+y1)/2 + font_size
                    robot_font = max(6, int(font_size * 0.7))
                    self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill=COLOR_VACUUM, outline="#C4A000", width=3)
                    self.canvas.create_text(cx, cy, text="AI", font=("Arial", robot_font, "bold"), fill="black")

    def reset_simulation(self):
        self.is_running = False
        self.env_list = [list(row) for row in self.initial_environment]
        self.vac_x, self.vac_y = self.initial_x, self.initial_y
        
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")
        
        self.set_solution_text("")
        self.draw_grid()
        self.btn_start.configure(state="normal")

    def start_simulation(self):
        if self.is_running: return
        self.reset_simulation()
        self.is_running = True
        self.btn_start.configure(state="disabled")
        
        # Chạy thuật toán trong luồng riêng để UI không bị đơ
        threading.Thread(target=self.run_algorithm, daemon=True).start()
        
    def run_algorithm(self):
        initial_state = (self.initial_environment, self.initial_x, self.initial_y)
        algo = self.algo_var.get()
        
        self.log(f"--- Bắt đầu mô phỏng: {algo} ---")
        
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
        elif algo == "Niềm tin (Greedy BFS)":
            path = belief_gbfs(initial_state)
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
