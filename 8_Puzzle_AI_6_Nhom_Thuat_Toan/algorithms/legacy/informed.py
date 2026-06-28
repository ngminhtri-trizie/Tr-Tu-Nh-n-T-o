from algorithms.core import *

@timed
def gbfs(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); pq=[(h(start),0,start)]; parent={start:(None,None)}; seen=set(); gen=1; exp=0; maxf=1; tick=0
    while pq:
        if exp>=max_nodes: return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Vượt giới hạn node.')
        _,_,cur=heapq.heappop(pq)
        if cur in seen: continue
        seen.add(cur); exp+=1
        if cur==goal:
            p,m=reconstruct(parent,cur); return result(True,p,m,exp,gen,maxf,'Tìm thấy lời giải bằng GBFS.')
        for nxt,mv,c in neighbors(cur):
            if nxt not in seen and nxt not in parent:
                parent[nxt]=(cur,mv); tick+=1; gen+=1; heapq.heappush(pq,(h(nxt),tick,nxt))
        maxf=max(maxf,len(pq))
    return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Không tìm thấy lời giải.')

@timed
def astar(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); pq=[(h(start),0,0,start)]; parent={start:(None,None)}; gbest={start:0}; seen=set(); gen=1; exp=0; maxf=1; tick=0
    while pq:
        if exp>=max_nodes: return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Vượt giới hạn node.')
        f,g,_,cur=heapq.heappop(pq)
        if cur in seen: continue
        seen.add(cur); exp+=1
        if cur==goal:
            p,m=reconstruct(parent,cur); return result(True,p,m,exp,gen,maxf,'Tìm thấy lời giải tối ưu bằng A*.')
        for nxt,mv,c in neighbors(cur):
            ng=g+c
            if nxt not in gbest or ng<gbest[nxt]:
                gbest[nxt]=ng; parent[nxt]=(cur,mv); tick+=1; gen+=1; heapq.heappush(pq,(ng+h(nxt),ng,tick,nxt))
        maxf=max(maxf,len(pq))
    return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Không tìm thấy lời giải.')

@timed
def idastar(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); bound=h(start); path=[start]; moves=[]; exp=0; gen=1; maxf=1
    def search(g,bound,visited):
        nonlocal exp,gen,maxf
        cur=path[-1]; f=g+h(cur)
        if f>bound: return f
        if cur==goal: return 'FOUND'
        exp+=1
        if exp>=max_nodes: return math.inf
        minb=math.inf
        for nxt,mv,c in neighbors(cur):
            if nxt in visited: continue
            path.append(nxt); moves.append(mv); visited.add(nxt); gen+=1; maxf=max(maxf,len(path))
            t=search(g+c,bound,visited)
            if t=='FOUND': return 'FOUND'
            minb=min(minb,t)
            visited.remove(nxt); path.pop(); moves.pop()
        return minb
    while True:
        t=search(0,bound,{start})
        if t=='FOUND': return result(True,path.copy(),moves.copy(),exp,gen,maxf,'Tìm thấy lời giải bằng IDA*.')
        if t==math.inf or exp>=max_nodes: return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Không tìm thấy hoặc vượt giới hạn node.')
        bound=t
