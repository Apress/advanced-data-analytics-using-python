import numpy as np
import random

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])
    return res
	
def find_centre(x, X, mu):
	min = 100
	cent = 0
	for c in mu:
		dist = LD(x, X[c])
		if dist < min:
			min = dist
			cent = c
	return cent
		
	 
def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = find_centre(x, X, mu)
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(k)
    return newmu
 
def has_converged(mu, oldmu):
    return sorted(mu) == sorted(oldmu)
 
def find_centers(X, K):
    oldmu = random.sample(range(0,5), K)
    mu = random.sample(range(0,5), K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)
	
X = ['Delhi','Dehli', 'Delli','Kolkata','Kalkata','Kalkota']

print(find_centers(X,2))
    