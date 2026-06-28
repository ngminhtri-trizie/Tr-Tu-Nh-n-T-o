"""Belief State Search (Partial observation) cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.complex_env import belief_partial_observation as _impl

def belief_partial_observation(*args, **kwargs):
    return _impl(*args, **kwargs)
