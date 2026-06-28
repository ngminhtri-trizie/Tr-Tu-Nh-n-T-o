"""Stochastic Hill Climbing cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.local import stochastic_hill_climbing as _impl

def stochastic_hill_climbing(*args, **kwargs):
    return _impl(*args, **kwargs)
