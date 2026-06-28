from algorithms.core import *
from algorithms.legacy.informed import astar

@timed
def backtracking_search(start, goal, depth_limit=35, max_nodes=DEFAULT_MAX_NODES, **kw):
    parent={start:(None,None)}; exp=0; gen=1
    def bt(cur, depth, seen):
        nonlocal exp,gen
        if cur==goal: return cur
        if depth<=0 or exp>=max_nodes: return None
        exp+=1
        for nxt,mv,c in neighbors(cur):
            if nxt in seen: continue
            parent[nxt]=(cur,mv); gen+=1
            ans=bt(nxt, depth-1, seen|{nxt})
            if ans: return ans
        return None
    end=bt(start, depth_limit, {start})
    if end:
        p,m=reconstruct(parent,end); return result(True,p,m,exp,gen,depth_limit,'Tìm thấy bằng CSP Backtracking.')
    return result(False,expanded=exp,generated=gen,max_frontier=depth_limit,message='Backtracking không tìm thấy trong giới hạn.')

@timed
def forward_checking(start, goal, heuristic='Manhattan', depth_limit=35, max_nodes=DEFAULT_MAX_NODES, **kw):
    # Forward checking: bỏ nhánh có heuristic không cải thiện quá lâu; dùng thứ tự Manhattan.
    h=make_heuristic(heuristic, goal); parent={start:(None,None)}; exp=0; gen=1
    def fc(cur, depth, seen, bad_streak=0):
        nonlocal exp,gen
        if cur==goal: return cur
        if depth<=0 or exp>=max_nodes or bad_streak>8: return None
        exp+=1
        for nxt,mv,c in sorted(neighbors(cur), key=lambda x:h(x[0])):
            if nxt in seen: continue
            parent[nxt]=(cur,mv); gen+=1
            ans=fc(nxt, depth-1, seen|{nxt}, 0 if h(nxt)<=h(cur) else bad_streak+1)
            if ans: return ans
        return None
    end=fc(start, depth_limit, {start})
    if end:
        p,m=reconstruct(parent,end); return result(True,p,m,exp,gen,depth_limit,'Tìm thấy bằng Forward Checking.')
    return result(False,expanded=exp,generated=gen,max_frontier=depth_limit,message='Forward Checking không tìm thấy trong giới hạn.')

@timed
def ac3_search(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    # Với 8-puzzle, arc consistency không tự nhiên; dùng A* sau bước kiểm tra tính giải được.
    if not is_solvable(start, goal): return result(False,message='AC-3 phát hiện trạng thái không giải được.')
    r=astar(start, goal, heuristic=heuristic, max_nodes=max_nodes); r.message='AC-3 Search: kiểm tra nhất quán/tính giải được rồi chạy A*.'; return r

@timed
def min_conflicts(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); cur=start; path=[cur]; moves=[]; exp=0; gen=1
    while exp<max_nodes:
        if cur==goal: return result(True,path,moves,exp,gen,1,'Tìm thấy bằng Min-Conflicts.')
        exp+=1; opts=neighbors(cur); gen+=len(opts)
        best=min(h(n) for n,_,_ in opts); cand=[x for x in opts if h(x[0])==best]
        nxt,mv,c=random.choice(cand); cur=nxt; path.append(cur); moves.append(mv)
    return result(False,path,moves,exp,gen,1,'Min-Conflicts dừng do vượt giới hạn.')
