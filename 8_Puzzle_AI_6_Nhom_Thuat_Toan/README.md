# 🧩 8 Puzzle AI Solver - 6 Nhóm Thuật Toán

Đây là đồ án môn **Trí tuệ nhân tạo** mô phỏng bài toán **8 Puzzle** với giao diện trực quan và đầy đủ 6 nhóm thuật toán AI.

## 1. Mục tiêu

- Trực quan hóa quá trình giải bài toán 8 Puzzle.
- Chạy và so sánh nhiều thuật toán AI khác nhau.
- Lưu lại lịch sử chạy để xem lại kết quả.
- Tổ chức code rõ ràng theo từng nhóm thuật toán để giảng viên dễ kiểm tra.

## 2. Các nhóm thuật toán đã triển khai

### Uninformed Search
- BFS
- DFS
- UCS
- IDS

### Informed Search
- GBFS
- A*
- IDA*

### Local Search
- Simple Hill Climbing
- Stochastic Hill Climbing
- Random Restart Hill Climbing
- Local Beam Search
- Simulated Annealing

### Searching in Complex Environments
- Belief State Search (No observation)
- Belief State Search (Partial observation)
- AND-OR Graph Search

### Constraint Satisfaction Problems - CSP
- Backtracking Search
- Forward Checking
- AC-3 Search
- Min-Conflicts

### Adversarial Search
- Minimax
- Alpha-Beta Pruning
- Expectimax

> Lưu ý: 8 Puzzle gốc là bài toán một tác tử. Nhóm CSP và Adversarial Search được triển khai theo hướng mô phỏng/minh họa để phục vụ yêu cầu học thuật của môn học.

## 3. Cấu trúc thư mục

```text
8_Puzzle_AI_6_Nhom_Thuat_Toan/
├── algorithms/
│   ├── uninformed_search/
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── ucs.py
│   │   └── ids.py
│   ├── informed_search/
│   │   ├── gbfs.py
│   │   ├── astar.py
│   │   └── idastar.py
│   ├── local_search/
│   │   ├── simple_hill_climbing.py
│   │   ├── stochastic_hill_climbing.py
│   │   ├── random_restart_hill_climbing.py
│   │   ├── local_beam_search.py
│   │   └── simulated_annealing.py
│   ├── complex_environment/
│   │   ├── belief_no_observation.py
│   │   ├── belief_partial_observation.py
│   │   └── and_or_graph_search.py
│   ├── csp/
│   │   ├── backtracking_search.py
│   │   ├── forward_checking.py
│   │   ├── ac3_search.py
│   │   └── min_conflicts.py
│   ├── adversarial_search/
│   │   ├── minimax.py
│   │   ├── alpha_beta_pruning.py
│   │   └── expectimax.py
│   ├── core.py
│   └── registry.py
├── gui/
│   └── main_window.py
├── history/
│   └── history.json
├── main.py
├── gui.py
├── requirements.txt
└── README.md
```

## 4. Chức năng chính

- Nhập trạng thái đầu và trạng thái đích.
- Random trạng thái hợp lệ.
- Chọn nhóm thuật toán và thuật toán.
- Chọn heuristic Manhattan hoặc số ô sai.
- Chạy thuật toán và mô phỏng từng bước.
- Play/Pause, xem bước trước/sau, về đầu/cuối.
- Hiển thị cost, expanded nodes, generated nodes, max frontier, thời gian chạy.
- Lưu và xem lại lịch sử chạy.
- Khung lịch sử có thanh cuộn ngang/dọc để xem rõ đầy đủ thông tin.

## 5. Cách chạy chương trình

Yêu cầu Python từ phiên bản 3.10 trở lên.

```bash
python main.py
```

Hoặc:

```bash
python gui.py
```

## 6. Cách commit lên GitHub

```bash
git init
git add .
git commit -m "Thêm project 8 Puzzle AI với 6 nhóm thuật toán"
git branch -M main
git remote add origin https://github.com/ngminhtri-trizie/Tr-Tu-Nh-n-T-o.git
git push -u origin main --force
```

## 7. Sinh viên thực hiện

- Nguyễn Minh Trí

## 8. Mục đích

Project được xây dựng phục vụ học tập, báo cáo và thực hành môn Trí tuệ nhân tạo.
