
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

sims = []
outcomes = []
def VR(w1,w2):
    return (1.0*min(w1,w2))/max(w1,w2)

def VS(G1,G2):
    _sum = 0
    for edge in G1.edges():
        if edge in G2.edges():
            w1 = G1.get_edge_data(edge[0],edge[1])["weight"]
            w2 = G2.get_edge_data(edge[0],edge[1])["weight"]
            _sum+= VR(w1,w2)
    assert(len(list(G1.edges())) != 0)
    res = (_sum*1.0)/(max(len(list(G1.edges())),len(list(G2.edges()))))
    assert(res >= 0 and res <= 1)
    return res 


def dist(x,y):
    global sims
    sim = VS(x,y)
    sims.append(sim)
    dist =  np.sqrt(2-2*sim)
    assert(dist>=0 and dist <= 2)
    return dist

def TriangleInequality(G1,G2,G3):
    global outcomes
    if dist(G1,G3) <= (dist(G1,G2) + dist(G2,G3)):
        outcomes.append(1)
        return True
    else: 
        outcomes.append(0)
        return False

def DecomposeXYZ(arr):

    xarr = []
    yarr = []
    zarr = []
    for x in range(len(arr)):
        case = x % 3
        if case == 1:
            xarr.append(arr[x])
        elif case == 2:
            yarr.append(arr[x])
        else:
            zarr.append(arr[x])

    assert(3*len(xarr)==len(arr))
    assert(len(yarr)==len(xarr))
    assert(len(zarr)==len(yarr))
    return xarr,yarr,zarr

def ScatterVis3D():
    global outcomes
    global sims
    assert(3*len(outcomes) ==len(sims))
    xarr,yarr,zarr = DecomposeXYZ(sims)
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111,projection='3d')
    ax.set_title("Triangle Inequality Satisfaction",fontsize=14)

    ax.set_xlabel("sim(x,z)",fontsize=12)
    ax.set_ylabel("sim(x,y)",fontsize=12)
    ax.set_zlabel("sim(y,z)",fontsize=12)
    ax.grid(True,linestyle='-',color='0.75')
    ax.scatter(xarr,yarr,zarr,s=20,c=outcomes, marker = 'o', cmap = cm.jet );
    plt.savefig('simscatter.png',bbox_inches='tight')


def TestInequality():

    maxn = 100
    maxe = 100

    for _ in range(10**4):
        n = [random.randint(2,maxn),random.randint(2,maxn),random.randint(2,maxn)]
        m = [random.randint(2,maxe),random.randint(2,maxe),random.randint(2,maxe)]
        print(n,m)
    
        G = [nx.gnm_random_graph(n[i],m[i]) for i in range(3)] 
        for g in G:        
            for (u,v,w) in g.edges(data=True):
                w['weight'] = random.randint(1,10)
            
        assert(TriangleInequality(G[0],G[1],G[2]))


def TestKappaCondition():
    rng = np.linspace(0,1,1000)
    succ = []
    for kappa in rng:
        sim = {"xz":(1.0*kappa)/2,"xy":kappa,"yz":kappa}
        dist = {k:np.sqrt(2-2*v) for k,v in sim.items()}
        ineq = (dist["xz"] > dist["xy"] + dist["yz"])      
        if succ:
            assert(ineq)
        elif ineq:
            succ.append(kappa)
    print(min(succ))
    return kappa

if __name__ == "__main__":
  
    TestKappaCondition()
    TestInequality()
    ScatterVis3D()

