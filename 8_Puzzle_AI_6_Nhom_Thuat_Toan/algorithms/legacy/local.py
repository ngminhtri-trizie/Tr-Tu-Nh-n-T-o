from algorithms.core import *

def _hc(start, goal, heuristic, stochastic=False, max_nodes=DEFAULT_MAX_NODES):
    h=make_heuristic(heuristic, goal); cur=start; path=[cur]; moves=[]; exp=0; gen=1
    while exp<max_nodes:
        if cur==goal: return result(True,path,moves,exp,gen,1,'Tìm thấy lời giải bằng Hill Climbing.')
        exp+=1; opts=[(h(n),n,mv) for n,mv,c in neighbors(cur)]; gen+=len(opts); best=min(x[0] for x in opts)
        if best>=h(cur): return result(False,path,moves,exp,gen,1,'Bị kẹt tại cực trị cục bộ/vùng bằng phẳng.')
        cand=[x for x in opts if x[0]==best]
        _,nxt,mv=random.choice(cand) if stochastic else cand[0]
        cur=nxt; path.append(cur); moves.append(mv)
    return result(False,path,moves,exp,gen,1,'Vượt giới hạn node.')

@timed
def simple_hill_climbing(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    return _hc(start, goal, heuristic, False, max_nodes)

@timed
def stochastic_hill_climbing(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    return _hc(start, goal, heuristic, True, max_nodes)

@timed
def random_restart_hill_climbing(start, goal, heuristic='Manhattan', restarts=20, max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); total_exp=0; total_gen=0; best_path=[]; best_moves=[]; best_h=10**9
    seeds=[start]+[random_solvable_state(start, random.randint(10,60)) for _ in range(max(0,restarts-1))]
    for seed in seeds:
        r=_hc(seed, goal, heuristic, True, max(1,(max_nodes-total_exp)//max(1,len(seeds))))
        total_exp+=r.expanded; total_gen+=r.generated
        if r.path and h(r.path[-1])<best_h:
            best_h=h(r.path[-1]); best_path=r.path; best_moves=r.moves
        if r.found:
            return result(True,r.path,r.moves,total_exp,total_gen,1,'Tìm thấy bằng Random Restart Hill Climbing.')
        if total_exp>=max_nodes: break
    return result(False,best_path,best_moves,total_exp,total_gen,1,'Không tìm thấy sau các lần restart; trả về đường đi tốt nhất.')

@timed
def local_beam_search(start, goal, heuristic='Manhattan', beam_width=5, max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); beams=[(start,[start],[])]+[(random_solvable_state(start, random.randint(5,40)), [], []) for _ in range(max(0,beam_width-1))]
    exp=0; gen=len(beams); maxf=len(beams); seen={start}
    while exp<max_nodes:
        candidates=[]
        for state,path,moves in beams:
            if state==goal: return result(True,path or [state],moves,exp,gen,maxf,'Tìm thấy bằng Local Beam Search.')
            exp+=1
            for nxt,mv,c in neighbors(state):
                if nxt in seen: continue
                seen.add(nxt); gen+=1; candidates.append((h(nxt),nxt,(path or [state])+[nxt],moves+[mv]))
        if not candidates: break
        candidates.sort(key=lambda x:x[0]); beams=[(s,p,m) for _,s,p,m in candidates[:beam_width]]; maxf=max(maxf,len(candidates))
    if beams:
        best=min(beams,key=lambda x:h(x[0])); return result(False,best[1],best[2],exp,gen,maxf,'Không tìm thấy; trả về beam tốt nhất.')
    return result(False,expanded=exp,generated=gen,max_frontier=maxf,message='Không tìm thấy.')

@timed
def simulated_annealing(start, goal, heuristic='Manhattan', max_nodes=DEFAULT_MAX_NODES, **kw):
    h=make_heuristic(heuristic, goal); cur=start; path=[cur]; moves=[]; exp=0; gen=1; temp=25.0; cooling=0.995
    while exp<max_nodes and temp>0.001:
        if cur==goal: return result(True,path,moves,exp,gen,1,'Tìm thấy bằng Simulated Annealing.')
        exp+=1; opts=neighbors(cur); gen+=len(opts); nxt,mv,c=random.choice(opts); delta=h(nxt)-h(cur)
        if delta<0 or random.random()<math.exp(-delta/temp):
            cur=nxt; path.append(cur); moves.append(mv)
        temp*=cooling
    return result(cur==goal,path,moves,exp,gen,1,'Dừng SA; có thể chưa đạt goal.' if cur!=goal else 'Tìm thấy.')
