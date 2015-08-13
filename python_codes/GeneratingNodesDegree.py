"""
NAME: GeneratingNodesDegree
DESCRIPTION: This program generate Indegree and Outdegree vector of a Network following
	     some distribution (gaussian,poisson,power law...) and create a initial
	     parameter's file that is read by a another code in C++

INPUT: NONE
OUTPUT: 
	  file of degree nodes         ---->    NodesDegree2.txt
	  file of initial parameters   ---->    InitialParam.param

"""
import numpy as np
import matplotlib.pyplot as plt
from modules import *


print "%"*50
print "Generating vectors with degree of nodes..."

# Number of nodes
NP = 50

# Mean of conections
# OBS: The conection's mean is about 5% of number of nodes
mu= 0.05*NP

# Sigma of normal distribution
sigma = 2


R = np.random.normal(mu,sigma,NP)
R[R<1]=1



# Converting in integers each values
decimal = np.fabs(R-np.floor(R))
R[decimal>0.5]=np.ceil(R[decimal>0.5])
R[decimal<0.5]=np.floor(R[decimal<0.5])

# In-degree and Out-degree
Indegree = np.copy(R)
Outdegree = Indegree[np.random.permutation(NP)]
Vector = np.array([Indegree,Outdegree])

# Saving vector of IN-OUT degree in a file
np.savetxt("./data/NodesDegree2.txt",Vector.T,fmt="%d")


print "Number of Nodes: ",NP
print "Number of edges: %d"%np.sum(Indegree)
print "%"*60
Param = [NP,int(np.sum(Indegree))] 
Print_parameters(Param)





#=====================================================================
# PLOTING
#=====================================================================
Bins = np.arange(R.min(),R.max()+1,1)
plt.hist(R,Bins,align='right')
plt.xlabel("Nodes Degree")
plt.ylabel("Frecuency")
#plt.ylim(ymax=100)
plt.show()
