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

### 2. Tìm kiếm có thông tin (Informed Search)
*Các thuật toán sử dụng hàm heuristic để hướng dẫn quá trình tìm kiếm.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm A* (A‑Star)** | ![A Star](docs/astar.gif) | Kết hợp chi phí đã đi (g) và ước lượng chi phí còn lại (h) để luôn mở rộng nút có khả năng tốt nhất. |

### 3. Tìm kiếm không cảm biến / Trạng thái niềm tin (Belief State Search)
*Trong môi trường không có cảm biến, tác tử phải suy đoán dựa trên tập các trạng thái có thể xảy ra.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Belief State Search** | ![Belief State](docs/belief_state.gif) | Tìm kiếm trong không gian các trạng thái niềm tin, đảm bảo đạt được mục tiêu dù không biết chính xác trạng thái thực. |

---

## 🗺️ Bài toán Thỏa mãn Ràng buộc (CSP)

### Tô màu bản đồ (các quận/huyện TP.HCM)
*Giải quyết việc gán màu cho các khu vực sao cho không có hai khu vực liền kề cùng màu.*

| Thuật toán | Minh họa | Mô tả |
| :---: | :---: | :--- |
| **Tìm kiếm quay lui (Backtracking Search)** | ![Backtracking](docs/backtracking.gif) | Thuật toán duyệt sâu, gán giá trị cho từng biến một và quay lui khi không còn giá trị hợp lệ cho biến hiện tại. |

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
