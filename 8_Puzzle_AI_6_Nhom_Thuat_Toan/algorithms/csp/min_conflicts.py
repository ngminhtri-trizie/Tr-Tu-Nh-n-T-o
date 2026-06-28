"""Min-Conflicts cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.csp import min_conflicts as _impl

def min_conflicts(*args, **kwargs):
    return _impl(*args, **kwargs)
