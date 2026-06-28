from collections import deque
from algorithms.core import *

@timed
def bfs(start, goal, max_nodes=DEFAULT_MAX_NODES, **kw):
    q=deque([start]); parent={start:(None,None)}; expanded=0; gen=1; maxf=1
    if start==goal: return result(True,[start],[],0,1,1,'Start đã là goal.')
    while q:
        if expanded>=max_nodes: return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='Vượt giới hạn node.')
        cur=q.popleft(); expanded+=1
        for nxt,mv,c in neighbors(cur):
            if nxt in parent: continue
            parent[nxt]=(cur,mv); gen+=1
            if nxt==goal:
                p,m=reconstruct(parent,nxt); return result(True,p,m,expanded,gen,maxf,'Tìm thấy lời giải bằng BFS.')
            q.append(nxt)
        maxf=max(maxf,len(q))
    return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='Không tìm thấy lời giải.')

@timed
def dfs(start, goal, depth_limit=35, max_nodes=DEFAULT_MAX_NODES, **kw):
    st=[(start,0)]; parent={start:(None,None)}; best={start:0}; expanded=0; gen=1; maxf=1
    while st:
        if expanded>=max_nodes: return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='Vượt giới hạn node.')
        cur,d=st.pop(); expanded+=1
        if cur==goal:
            p,m=reconstruct(parent,cur); return result(True,p,m,expanded,gen,maxf,'Tìm thấy lời giải bằng DFS.')
        if d>=depth_limit: continue
        for nxt,mv,c in reversed(neighbors(cur)):
            if nxt not in best or d+1<best[nxt]:
                best[nxt]=d+1; parent[nxt]=(cur,mv); gen+=1; st.append((nxt,d+1))
        maxf=max(maxf,len(st))
    return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='DFS không tìm thấy trong giới hạn độ sâu.')

@timed
def ucs(start, goal, max_nodes=DEFAULT_MAX_NODES, **kw):
    pq=[(0,0,start)]; parent={start:(None,None)}; cost={start:0}; seen=set(); gen=1; expanded=0; maxf=1; tick=0
    while pq:
        if expanded>=max_nodes: return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='Vượt giới hạn node.')
        g,_,cur=heapq.heappop(pq)
        if cur in seen: continue
        seen.add(cur); expanded+=1
        if cur==goal:
            p,m=reconstruct(parent,cur); return result(True,p,m,expanded,gen,maxf,'Tìm thấy lời giải bằng UCS.')
        for nxt,mv,c in neighbors(cur):
            ng=g+c
            if nxt not in cost or ng<cost[nxt]:
                cost[nxt]=ng; parent[nxt]=(cur,mv); tick+=1; gen+=1; heapq.heappush(pq,(ng,tick,nxt))
        maxf=max(maxf,len(pq))
    return result(False,expanded=expanded,generated=gen,max_frontier=maxf,message='Không tìm thấy lời giải.')

@timed
def ids(start, goal, depth_limit=35, max_nodes=DEFAULT_MAX_NODES, **kw):
    total_exp=0; total_gen=0; maxf=0
    for limit in range(depth_limit+1):
        st=[(start,0)]; parent={start:(None,None)}; pathset={start}; expanded=0; gen=1
        while st:
            if total_exp+expanded>=max_nodes: return result(False,expanded=total_exp+expanded,generated=total_gen+gen,max_frontier=maxf,message='Vượt giới hạn node.')
            cur,d=st.pop(); expanded+=1
            if cur==goal:
                p,m=reconstruct(parent,cur); return result(True,p,m,total_exp+expanded,total_gen+gen,maxf,f'Tìm thấy ở depth limit = {limit}.')
            if d>=limit: continue
            for nxt,mv,c in reversed(neighbors(cur)):
                if nxt in pathset: continue
                pathset.add(nxt); parent[nxt]=(cur,mv); gen+=1; st.append((nxt,d+1))
            maxf=max(maxf,len(st))
        total_exp+=expanded; total_gen+=gen
    return result(False,expanded=total_exp,generated=total_gen,max_frontier=maxf,message='IDS không tìm thấy trong giới hạn.')
