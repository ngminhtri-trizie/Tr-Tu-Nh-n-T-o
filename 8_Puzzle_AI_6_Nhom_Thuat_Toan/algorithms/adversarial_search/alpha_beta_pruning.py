"""Alpha-Beta Pruning cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.adversarial import alpha_beta_pruning as _impl

def alpha_beta_pruning(*args, **kwargs):
    return _impl(*args, **kwargs)
