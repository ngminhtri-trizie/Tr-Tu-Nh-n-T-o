# 🧩 8 Puzzle
# 🎯 Mục tiêu
- Minh họa cách hoạt động của các thuật toán tìm kiếm trong AI.
- So sánh hiệu quả giữa các nhóm thuật toán.
- Hỗ trợ học tập và trực quan hóa quá trình giải bài toán 8 Puzzle.

# 🧠 Các nhóm thuật toán
## 1. Uninformed Search
- Breadth First Search (BFS)
- Depth First Search (DFS)
- Uniform Cost Search (UCS)
- Iterative Deepening Search (IDS)

## 2. Informed Search
- Greedy Best First Search (GBFS)
- A*
- IDA*

## 3. Local Search
- Simple Hill Climbing
- Stochastic Hill Climbing
- Random Restart Hill Climbing
- Local Beam Search
- Simulated Annealing

## 4. Searching in Complex Environments
- Belief State Search
  - No Observation
  - Partial Observation
- AND-OR Graph Search

## 5. Constraint Satisfaction Problems (CSP)
- Backtracking Search
- Forward Checking
- AC-3 Search
- Min-Conflicts
  
## 6. Adversarial Search
- Minimax
- Alpha-Beta Pruning
- Expectimax

> **Lưu ý:** Nhóm Adversarial Search được cài đặt nhằm minh họa các thuật toán AI. Do bài toán 8 Puzzle là bài toán một tác tử (Single-Agent Search), nhóm thuật toán này chỉ mang tính học thuật và mô phỏng.

# ✨ Chức năng
- Sinh bàn cờ ngẫu nhiên
- Chạy từng thuật toán
- Hiển thị từng bước giải
- Điều chỉnh tốc độ mô phỏng
- Hiển thị:
  - Cost
  - Depth
  - Expanded Nodes
  - Running Time
- Lưu lịch sử chạy
- Xem lại lịch sử
- So sánh kết quả giữa các thuật toán

# 🖥️ Giao diện
Giao diện gồm:
- Danh sách thuật toán
- Bàn cờ 8 Puzzle
- Khu vực điều khiển
- Thông tin thống kê
- Lịch sử chạy

# 📊 Thông tin hiển thị
Sau mỗi lần chạy chương trình sẽ hiển thị:
- Thuật toán
- Nhóm thuật toán
- Số bước
- Độ sâu
- Số node mở rộng
- Cost
- Thời gian chạy
- Bộ nhớ sử dụng (nếu có)
