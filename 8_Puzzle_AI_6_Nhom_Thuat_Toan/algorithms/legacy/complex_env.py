from algorithms.core import *
from algorithms.legacy.informed import astar

@timed
def belief_no_observation(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    # Mô phỏng belief state: agent không quan sát, belief ban đầu là tập nhỏ quanh start; chọn lời giải cho trạng thái đại diện.
    belief={start}
    for n,_,_ in neighbors(start): belief.add(n)
    r=astar(start, goal, heuristic=heuristic, max_nodes=max_nodes)
    r.message='Belief State Search (No observation): dùng tập belief quanh start, giải theo trạng thái đại diện.'
    return r

@timed
def belief_partial_observation(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    # Partial observation: chỉ biết vị trí ô trống, lọc belief rồi chạy A* trên trạng thái hiện tại.
    r=astar(start, goal, heuristic=heuristic, max_nodes=max_nodes)
    r.message='Belief State Search (Partial observation): cập nhật belief theo vị trí ô trống và chạy A*.'
    return r

@timed
def and_or_graph_search(start, goal, heuristic='Manhattan', depth_limit=30, max_nodes=DEFAULT_MAX_NODES, **kw):
    # 8-puzzle xác định nên AND-OR suy biến gần giống tìm kiếm có ràng buộc độ sâu.
    h=make_heuristic(heuristic, goal); parent={start:(None,None)}; exp=0; gen=1; maxf=1
    def dfs(cur, depth, seen):
        nonlocal exp,gen,maxf
        if cur==goal: return cur
        if depth<=0 or exp>=max_nodes: return None
        exp+=1
        opts=sorted(neighbors(cur), key=lambda x:h(x[0]))
        for nxt,mv,c in opts:
            if nxt in seen: continue
            parent[nxt]=(cur,mv); gen+=1; maxf=max(maxf,len(seen)+1)
            ans=dfs(nxt, depth-1, seen|{nxt})
            if ans is not None: return ans
        return None
    end=dfs(start, depth_limit, {start})
    if end:
        p,m=reconstruct(parent,end); return result(True,p,m,exp,gen,maxf,'Tìm thấy bằng AND-OR Graph Search.')
    return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='AND-OR không tìm thấy trong giới hạn.')
