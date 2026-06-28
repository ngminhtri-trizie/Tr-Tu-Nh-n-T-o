"""Forward Checking cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.csp import forward_checking as _impl

def forward_checking(*args, **kwargs):
    return _impl(*args, **kwargs)
