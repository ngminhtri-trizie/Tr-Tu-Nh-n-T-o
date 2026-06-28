"""Belief State Search (No observation) cho bài toán 8-Puzzle.

File này được tách riêng theo đúng nhóm thuật toán để giảng viên dễ kiểm tra.
Phần cài đặt lõi được dùng lại từ module legacy nhằm tránh lặp code.
"""
from algorithms.legacy.complex_env import belief_no_observation as _impl

def belief_no_observation(*args, **kwargs):
    return _impl(*args, **kwargs)
