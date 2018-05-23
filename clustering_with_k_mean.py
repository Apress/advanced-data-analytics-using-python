import numpy as np
import random
 
def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return (set([tuple(b) for b in mu]) == set([tuple(b) for b in oldmu]))
 
def find_centers(X, K):
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        
        clusters = cluster_points(X, mu)
        
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)
	
X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(10)])

print(find_centers(X,2))
    