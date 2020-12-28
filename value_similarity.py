
import networkx as nx
import random
import numpy as np

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
    dist =  np.sqrt(2-2*VS(x,y))
    assert(dist>=0 and dist <= 2)
    return dist

def TriangleInequality(G1,G2,G3):
    if dist(G1,G3) <= (dist(G1,G2) + dist(G2,G3)):
        return True
    else: 
        return False


def TestInequality():

    for _ in range(10000):

        maxn = 100
        maxe = 100
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
    for kappa in rng:
        sim = {"xz":(1.0*kappa)/2,"xy":kappa,"yz":kappa}
        dist = {k:np.sqrt(2-2*v) for k,v in sim.items()}
        if dist["xz"] > dist["xy"] + dist["yz"]:
            print(kappa)
            return
            
if __name__ == "__main__":
    TestKappaCondition()

