# Trí Tuệ Nhân Tạo – Mô Phỏng các Thuật Toán

## Thông tin dự án
- **Họ và tên:** [Tên sinh viên]
- **MSSV:** [Mã số sinh viên]
- **Ngày:** [Ngày tháng năm]

Kho lưu trữ này tập hợp các mô phỏng trực quan cho nhiều thuật toán Trí tuệ nhân tạo, chủ yếu bao gồm **bài toán Máy Hút Bụi (Vacuum Cleaner)** và **Bài toán Thỏa mãn Ràng buộc (CSP)**.

Trong dự án, mỗi thuật toán đều được minh họa dưới dạng ảnh GIF động, giúp bạn nhanh chóng hiểu cách chúng hoạt động.

## 🧹 Bài toán Máy Hút Bụi

### 1. Tìm kiếm mù (Uninformed Search)
*Các thuật toán tìm kiếm không dựa trên bất kỳ thông tin bổ sung nào ngoài mô tả bài toán.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm theo chiều rộng (BFS)** | ![BFS](docs/bfs.gif) | Mở rộng các nút ở mức sâu nhất nhỏ trước, đảm bảo tìm được đường ngắn nhất theo số bước. |
| **Tìm kiếm theo chiều sâu (DFS)** | ![DFS](docs/dfs.gif) | Đi sâu vào các nhánh càng sâu càng tốt trước khi quay lui, thích hợp cho không gian trạng thái lớn. |
| **Tìm kiếm chi phí đồng nhất (UCS)** | ![UCS](docs/ucs.gif) | Mở rộng nút có chi phí đường đi nhỏ nhất, đảm bảo tìm được đường đi tối ưu khi các bước có chi phí khác nhau. |
| **Tìm kiếm sâu dần (IDDFS)** | ![IDDFS](docs/iddfs.gif) | Kết hợp ưu điểm bộ nhớ của DFS và tính tối ưu của BFS bằng cách tăng dần giới hạn độ sâu. |

### 2. Tìm kiếm có thông tin (Informed Search)
*Các thuật toán sử dụng hàm heuristic để hướng dẫn quá trình tìm kiếm.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm Greedy Best-First (GBFS)** | ![GBFS](docs/gbfs.gif) | Luôn mở rộng nút có vẻ gần mục tiêu nhất dựa trên hàm heuristic (h). |
| **Tìm kiếm A* (A‑Star)** | ![A Star](docs/astar.gif) | Kết hợp chi phí đã đi (g) và ước lượng chi phí còn lại (h) để luôn mở rộng nút có khả năng tốt nhất. |
| **Tìm kiếm A* sâu dần (IDA*)** | ![IDA Star](docs/ida_star.gif) | Tương tự IDDFS nhưng sử dụng giới hạn dựa trên chi phí f(n) = g(n) + h(n) thay vì độ sâu. |

### 3. Tìm kiếm không cảm biến / Trạng thái niềm tin (Belief State Search)
*Trong môi trường không có cảm biến, tác tử phải suy đoán dựa trên tập các trạng thái có thể xảy ra.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm trạng thái niềm tin (Belief State Search)** | ![Belief State](docs/belief_state.gif) | Tìm kiếm trong không gian các trạng thái niềm tin (môi trường không cảm biến). |
| **Tìm kiếm với quan sát một phần (Partially Observable)** | ![Partially Observable](docs/partially_observable.gif) | Cập nhật trạng thái niềm tin dựa trên thông tin cảm biến hạn chế (nhận biết phòng sạch/dơ). |
| **Tìm kiếm đồ thị AND-OR** | ![AND-OR Graph](docs/and_or.gif) | Giải quyết tính không xác định của môi trường (ví dụ: máy hút bụi có thể hút trượt). |

### 4. Tìm kiếm cục bộ (Local Search)
*Các thuật toán không quan tâm đến đường đi mà chỉ tập trung tìm trạng thái mục tiêu tối ưu hoặc thỏa mãn điều kiện.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Leo đồi (Hill Climbing)** | ![Hill Climbing](docs/hill_climbing.gif) | Liên tục di chuyển theo hướng tăng dần giá trị (hoặc giảm chi phí), dễ mắc kẹt ở cực đại cục bộ. |
| **Tôi luyện mô phỏng (Simulated Annealing)** | ![Simulated Annealing](docs/simulated_annealing.gif) | Cho phép các bước đi "xấu" ở giai đoạn đầu để thoát khỏi cực đại cục bộ, xác suất này giảm dần theo "nhiệt độ". |
| **Tìm kiếm chùm cục bộ (Local Beam Search)** | ![Local Beam](docs/local_beam.gif) | Duy trì k trạng thái tốt nhất thay vì chỉ 1, cho phép khám phá không gian tìm kiếm rộng hơn. |

---

## 🗺️ Bài toán Thỏa mãn Ràng buộc (CSP)

### Tô màu bản đồ (các quận/huyện TP.HCM)
*Giải quyết việc gán màu cho các khu vực sao cho không có hai khu vực liền kề cùng màu.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm quay lui (Backtracking)** | ![Backtracking](docs/backtracking.gif) | Thuật toán duyệt sâu, gán giá trị cho từng biến một và quay lui khi không còn giá trị hợp lệ. |
| **MAC (Maintaining Arc Consistency)** | ![MAC Search](docs/mac_search.gif) | Kết hợp quay lui với việc duy trì tính nhất quán cung (AC-3) để phát hiện sớm nhánh bế tắc. |
| **Tìm kiếm Min-Conflicts** | ![Min Conflicts](docs/min_conflicts.gif) | Thuật toán tìm kiếm cục bộ, sửa lỗi bằng cách chọn giá trị làm giảm thiểu số lượng ràng buộc bị vi phạm. |

---

## ⚔️ Tìm kiếm đối kháng (Adversarial Search)

### Trò chơi Tic-Tac-Toe
*Các thuật toán ra quyết định trong môi trường có đối thủ cạnh tranh.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Minimax** | ![Minimax](docs/minimax.gif) | Giả định đối thủ luôn chơi tối ưu, chọn nước đi tối đa hóa điểm số của mình (và tối thiểu hóa điểm của đối thủ). |

---

## 🚀 Cách thêm GIF của bạn

1. Tạo một thư mục có tên `docs/` trong dự án (nếu chưa có).
2. Đặt các file `.gif` vào thư mục này.
3. Sửa lại đường dẫn trong các thẻ `![Alt text](docs/your_image.gif)` cho phù hợp với tên file thực tế.
4. Bạn có thể mở rộng bảng hoặc tạo các mục mới nếu muốn bổ sung thuật toán khác.

## 🛠️ Cách chạy dự án

```bash
# Chạy giao diện mô phỏng chính
python main.py
```
