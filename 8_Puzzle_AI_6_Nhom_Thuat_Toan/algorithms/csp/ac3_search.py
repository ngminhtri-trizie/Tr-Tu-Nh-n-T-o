"""AC-3 Search cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.csp import ac3_search as _impl

def ac3_search(*args, **kwargs):
    return _impl(*args, **kwargs)
