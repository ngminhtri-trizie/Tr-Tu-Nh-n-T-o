from algorithms.core import *
from algorithms.legacy.informed import astar

# Ghi chú: 8-puzzle gốc không phải bài toán đối kháng. Các hàm dưới đây mô phỏng biến thể
# MAX muốn giảm heuristic, MIN / chance làm trạng thái xấu hơn để có thể minh họa nhóm thuật toán.

def _score(s, goal, heuristic):
    return -make_heuristic(heuristic, goal)(s)

def _choose_by_game_tree(start, goal, heuristic, depth_limit, mode='minimax'):
    h=make_heuristic(heuristic, goal); exp=0
    def value(s, depth, max_turn, alpha=-10**9, beta=10**9):
        nonlocal exp
        exp+=1
        if s==goal or depth==0: return -h(s)
        ns=neighbors(s)
        if mode=='expectimax' and not max_turn:
            return sum(value(n, depth-1, True, alpha, beta) for n,_,_ in ns)/len(ns)
        if max_turn:
            v=-10**9
            for n,_,_ in ns:
                v=max(v,value(n,depth-1,False,alpha,beta)); alpha=max(alpha,v)
                if mode=='alphabeta' and alpha>=beta: break
            return v
        v=10**9
        for n,_,_ in ns:
            v=min(v,value(n,depth-1,True,alpha,beta)); beta=min(beta,v)
            if mode=='alphabeta' and alpha>=beta: break
        return v
    best=None; bestv=-10**9
    for n,mv,c in neighbors(start):
        v=value(n, max(0,depth_limit-1), False)
        if v>bestv: bestv=v; best=(n,mv)
    return best, exp

@timed
def minimax(start, goal, heuristic='Manhattan', depth_limit=8, max_nodes=DEFAULT_MAX_NODES, **kw):
    # Sau khi chọn nước đầu bằng Minimax, dùng A* để hiển thị được full path đến goal.
    choice, exp=_choose_by_game_tree(start, goal, heuristic, min(depth_limit,10), 'minimax')
    if not choice: return result(False,expanded=exp,message='Không có nước đi.')
    r=astar(choice[0], goal, heuristic=heuristic, max_nodes=max_nodes)
    if r.path:
        r.path=[start]+r.path; r.moves=[choice[1]]+r.moves; r.cost=len(r.moves)
    r.expanded+=exp; r.message='Minimax chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.'
    return r

@timed
def alpha_beta_pruning(start, goal, heuristic='Manhattan', depth_limit=8, max_nodes=DEFAULT_MAX_NODES, **kw):
    choice, exp=_choose_by_game_tree(start, goal, heuristic, min(depth_limit,10), 'alphabeta')
    if not choice: return result(False,expanded=exp,message='Không có nước đi.')
    r=astar(choice[0], goal, heuristic=heuristic, max_nodes=max_nodes)
    if r.path:
        r.path=[start]+r.path; r.moves=[choice[1]]+r.moves; r.cost=len(r.moves)
    r.expanded+=exp; r.message='Alpha-Beta Pruning chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.'
    return r

@timed
def expectimax(start, goal, heuristic='Manhattan', depth_limit=8, max_nodes=DEFAULT_MAX_NODES, **kw):
    choice, exp=_choose_by_game_tree(start, goal, heuristic, min(depth_limit,10), 'expectimax')
    if not choice: return result(False,expanded=exp,message='Không có nước đi.')
    r=astar(choice[0], goal, heuristic=heuristic, max_nodes=max_nodes)
    if r.path:
        r.path=[start]+r.path; r.moves=[choice[1]]+r.moves; r.cost=len(r.moves)
    r.expanded+=exp; r.message='Expectimax chọn nước đầu với chance node, sau đó A* hoàn tất đường đi.'
    return r
