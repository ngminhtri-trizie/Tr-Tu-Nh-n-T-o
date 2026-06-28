from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import deque
import time, random, math, heapq

State = tuple[int, ...]
GOAL_DEFAULT: State = (1,2,3,4,5,6,7,8,0)
START_DEFAULT: State = (1,2,3,4,0,6,7,5,8)
DEFAULT_MAX_NODES = 250000
MOVES = [(-1,0,'Lên'),(1,0,'Xuống'),(0,-1,'Trái'),(0,1,'Phải')]

@dataclass
class SearchResult:
    found: bool
    path: list[State]
    moves: list[str]
    cost: int
    expanded: int
    generated: int
    max_frontier: int
    elapsed: float
    message: str
    algorithm: str = ''
    group: str = ''


def parse_state(text: str) -> State:
    cleaned = text.replace(',', ' ').replace(';', ' ').strip()
    parts = cleaned.split() if ' ' in cleaned else list(cleaned)
    if len(parts) != 9:
        raise ValueError('Trạng thái phải có đúng 9 số từ 0 đến 8.')
    nums = tuple(int(x) for x in parts)
    if set(nums) != set(range(9)):
        raise ValueError('Trạng thái phải chứa đủ các số 0..8, mỗi số đúng một lần.')
    return nums

def state_to_text(s: State) -> str:
    return ''.join(map(str, s))

def inversion_count(s: State) -> int:
    arr=[x for x in s if x!=0]; inv=0
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            inv += arr[i] > arr[j]
    return inv

def is_solvable(start: State, goal: State) -> bool:
    return inversion_count(start) % 2 == inversion_count(goal) % 2

def neighbors(state: State) -> list[tuple[State,str,int]]:
    blank=state.index(0); r,c=divmod(blank,3); out=[]
    for dr,dc,mv in MOVES:
        nr,nc=r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            ni=nr*3+nc; a=list(state); a[blank],a[ni]=a[ni],a[blank]
            out.append((tuple(a),mv,1))
    return out

def goal_positions(goal: State) -> dict[int, tuple[int,int]]:
    return {v: divmod(i,3) for i,v in enumerate(goal)}

def misplaced(s: State, goal: State) -> int:
    return sum(1 for i,v in enumerate(s) if v and v != goal[i])

def manhattan(s: State, goal: State) -> int:
    pos=goal_positions(goal); total=0
    for i,v in enumerate(s):
        if v:
            r,c=divmod(i,3); gr,gc=pos[v]; total += abs(r-gr)+abs(c-gc)
    return total

def make_heuristic(name: str, goal: State):
    if name == 'Số ô sai': return lambda s: misplaced(s, goal)
    return lambda s: manhattan(s, goal)

def reconstruct(parent: dict[State, tuple[State|None,str|None]], end: State):
    path=[]; moves=[]; cur=end
    while cur is not None:
        path.append(cur); prev,mv=parent[cur]
        if mv is not None: moves.append(mv)
        cur=prev
    return list(reversed(path)), list(reversed(moves))

def result(found, path=None, moves=None, expanded=0, generated=0, max_frontier=0, message=''):
    path=path or []; moves=moves or []
    return SearchResult(found,path,moves,len(moves),expanded,generated,max_frontier,0.0,message)

def timed(fn):
    def wrap(*args, **kwargs):
        t=time.perf_counter(); r=fn(*args, **kwargs); r.elapsed=time.perf_counter()-t; return r
    return wrap

def random_solvable_state(goal: State=GOAL_DEFAULT, steps: int=60) -> State:
    cur=goal; last=None
    for _ in range(steps):
        opts=neighbors(cur)
        if last is not None and len(opts)>1:
            opts=[o for o in opts if o[0]!=last]
        last=cur; cur=random.choice(opts)[0]
    return cur
