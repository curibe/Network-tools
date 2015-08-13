import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from modules import *

# Reading adjacency matrix
A = np.loadtxt("AdjacencyMatrix.txt")
EdgesIni = np.loadtxt("Edges.txt")
B = np.copy(A) # creating a copy

#===============================================================
# VARIABLES
#===============================================================
r = np.zeros((4,4)) # Initializing vector of assortativities and terms
rr = np.zeros(4)    # Initializing vector of assortativities
rr2 = np.zeros(4)
Delta = np.zeros(4) # Initializing vector of delta's
R = []              # List of assortativity per effective rewiring
RR = np.array([]).reshape(0,4)   # Assortativity for effective rewiring
Rr = np.array([]).reshape(0,4)   # Assortativity for each successful/failed rewiring
DD = np.array([]).reshape(0,4) 
RR2 = np.array([]).reshape(0,4) 
rewire = [0]        # rewirings
NR = 2000             # Number of rewirings
EffRewiring=0       # Counter for effective rewirings
SuccessRewiring=0   # Counter for success rewirings

Indeg , Outdeg = GetDegree(A)      # Degree of nodes
M = np.sum(Indeg)                  #number of conections

#=======================================
# TYPE:
#     1  In-Out    2  Out-In
#     3  In-In     4  Out-Out
#=======================================
TYPE = 2




# Calculating initial assortativity
for mode in range(4):
 r[mode] = np.array(assortativity(A,mode,True))   

# Save initial assortativity 
R.append(r[:,0])
RR =np.append(RR,[r[:,0]],axis=0)
RR2 = np.append(RR2,[r[:,0]],axis=0)
Rr =np.append(Rr,[r[:,0]],axis=0)
rr = r[:,0]
rr2 = r[:,0]
rcopy = r.copy()
#Terms = Assortativity_rewired(A,1)

for i in range(1,NR+1):
  
  # Doing de rewiring
  Result  = Rewiring(B)
  
  # Verifiying if rewiring was successful
  if Result[2]:
    
                  # Updating adjacency matrix
    Edges = Result[1]          # keeping edges of pair nodes rewired
    
    # Calculating DeltaR
    for mode in range(4):
      Delta[mode] = DeltaR(Indeg,Outdeg,Edges,mode)/M   
    
    # Verifiying if rewiring increment assortativity of mode TYPE
    if Delta[TYPE]>0:
      B = Result[0]
      for mode in range(4):
	r[mode,1] = r[mode,1] + Delta[mode]              # update term0
      # Calculating new assortativity
      for mode in range(4):
	rr[mode] = Assortativity_rewired(r[mode,1:])
	rr2[mode] = np.array(assortativity(B,mode,False))

      RR = np.append(RR,[rr],axis=0)        # Saving four assortativities
      RR2 = np.append(RR2,[rr2],axis=0)        
      DD = np.append(DD,[Delta],axis=0)     # Saving four delta's
      Rr = np.append(Rr,[rr],axis=0)
      rewire.append(i)         # Saving number of rewirings
      EffRewiring+=1
      #print "Rewiring accepted (i,delta,rr): (%d,%.3f,%.3f)"%(i,Delta[0],rr)
    else:
      for mode in range(4):
	rcopy[mode,1] = rcopy[mode,1] + Delta[mode]              # update term0
      # Calculating new assortativity
      for mode in range(4):
	rr[mode] = Assortativity_rewired(rcopy[mode,1:])
      Rr = np.append(Rr,[rr],axis=0)
      
    SuccessRewiring+=1
  else:
    Rr = np.append(Rr,[rr],axis=0)
    
    if np.trace(B)>0:
      break
    
    


  
CIJ  = A-B
ed1 = np.where(A)
ed2 = np.where(B)
print "="*60
print "elementos cambiados: ",np.sum(CIJ<0)
print "Nro antiguas conexiones encontradas: ",2*NR-np.sum(CIJ<0)
print "Rewirings existosos: ",SuccessRewiring
print "Rewiring efecivos: ",EffRewiring
#print "Asortatividad inicial (in-out): ",r
#print "Delta: ",Delta
#print "Degrees A(in): \n",GetDegree(A)[0]
#print "Degrees A(out): \n",GetDegree(A)[1]
#print "Degrees B(in): \n",GetDegree(B)[0]
#print "Degrees B(out): \n",GetDegree(B)[1]
print "="*60
#print "Tabla de conexiones antiguas: "
#print ed1[0],'\n',ed1[1]
#print "Tabla de conexiones nuevas: "
#print ed2[0],'\n',ed2[1]


#===================================================
# PLOTS
#===================================================

#=====================================
# GENERAL PARAMETERS OF PLOT
#=====================================
mpl.rcParams['xtick.labelsize'] = 17
mpl.rcParams['ytick.labelsize'] = 17
mpl.rcParams['font.family'] = 'Freeserif' #cmr10
mpl.rcParams['xtick.minor.size'] = 3
mpl.rcParams['font.size'] = 17.0
#mpl.rcParams['xtick.minor.width'] = 1
#majorFormatter = FormatStrFormatter('%.2lf')
#majorLocator   = MultipleLocator(1)
#minorLocator = MultipleLocator(0.5)


label = ["In-out","Out-In","In-In","Out-Out"]
for i in range(4):
  plt.plot(rewire,RR[:,i],'-',label=label[i],lw=2)
  plt.grid()
  plt.xlabel("Effective Rewiring")
  plt.ylabel("Assortativity")
  plt.legend(loc=9, bbox_to_anchor=(0.5, 1.1), ncol=3,fontsize=15)
  plt.ylim([2*RR.min(),2*RR.max()])
plt.savefig("EffectiveRewiring.pdf")

plt.figure()
plt.plot(rewire[1:],DD[:,TYPE],'go-',lw=1.5,ms=3,mfc='b')
plt.ylim(ymax=1.2*DD[:,TYPE].max())
plt.grid()
plt.xlabel("Effective Rewiring")
plt.ylabel("Delta")
plt.savefig("EffRewiring_Delta.pdf")

plt.figure()
for i in range(4):
  plt.plot(range(NR+1),Rr[:,i],'-',label=label[i], lw=1.5)
plt.ylim(ymax=1.2*Rr.max())
plt.grid()
plt.legend(loc="lower left", ncol=2,fontsize=15)
plt.xlabel("Total Rewiring")
plt.ylabel("Assortativity")
plt.savefig("TotalRewiring.pdf")
plt.show()


for i in range(4):
  plt.plot(rewire,RR2[:,i],'-',label=label[i],lw=2)
  plt.grid()
  plt.xlabel("Effective Rewiring")
  plt.ylabel("Assortativity")
  plt.title("Assortativity")
  #plt.legend(loc=9, bbox_to_anchor=(0.5, 1.1), ncol=3,fontsize=15)
  plt.ylim([2*RR2.min(),2*RR2.max()])
plt.savefig("Assortativity.pdf")
