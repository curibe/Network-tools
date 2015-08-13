import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def Print_parameters(prm):

  Ofile = open("./data/InitialParam.param","w")
  Ofile.write('''\
%%****************************************
%% PARAMETERS FILE
%%****************************************

%%Number of Nodes 
Nn      =      %d

%%Number od conections
NC      =      %d
'''%(int(prm[0]), int(prm[1])))
  Ofile.close()



def assortativity(A,flag,opt=False):
    
    #Calculating degree nodes
    indeg = np.sum(A,axis=0) # Sum over columns
    outdeg = np.sum(A,axis=1) #Sum over rows
    
    #Calculating number of conections
    M =np.sum(indeg)
    
    #Determining edges conections
    i,j = np.where(A>0)
    
    # In-Out 
    if flag == 0: jd = indeg[i]; kd = outdeg[j]
    # Out-In
    elif flag == 1: jd = outdeg[i]; kd = indeg[j]
    # In-In
    elif flag == 2: jd = indeg[i]; kd = indeg[j]
    # Out-Out
    elif flag == 3: jd = outdeg[i]; kd = outdeg[j]
    else:
        print "You need choose some configuration"
        
  
    # Calculating some terms of assortativity
    if opt:
      Term0 = np.sum(jd*kd)/M
      Term1 = np.square(0.5*np.sum(jd+kd)/M)
      Term2 = 0.5*np.sum(jd*jd+kd*kd)/M
      
      r = (Term0 - Term1)/(Term2 - Term1)
      
      return r,Term0,Term1,Term2
    else:
      
      r = ( np.sum(jd*kd)/M - np.square(0.5*np.sum(jd+kd)/M) )/( 0.5*np.sum(jd*jd+kd*kd)/M - np.square(0.5*np.sum(jd+kd)/M) )
        
      return r
   


def Assortativity_rewired(Terms):
  
  r =  (Terms[0] - Terms[1])/(Terms[2] - Terms[1])
  return r
  

#=========================================================================================================================
# PLOT FUNCTIONS
#=========================================================================================================================

#******************************
# GENERAL PARAMETERS OF PLOT
#******************************
#mpl.rcParams['xtick.labelsize'] = 17
#mpl.rcParams['ytick.labelsize'] = 17
#mpl.rcParams['font.family'] = 'cmr10'
#mpl.rcParams['xtick.minor.size'] = 3
#mpl.rcParams['font.size'] = 17.0

def Plot_AssortativityProfile(Aij,namefig):
  AS = np.zeros(4)
  x = range(4)
  for mode in range(4):
    AS[mode] = assortativity(Aij,mode)
  label = ["(in,out)","(out,in)","(in,in)","(out,out)"]
  plt.figure()
  plt.plot(x,AS,'g*--',markersize=14,linewidth=2)
  plt.xticks(x,label,fontsize=18)
  plt.yticks(fontsize=18)
  plt.ylabel("Assortativity")
  plt.xlim(xmin=0.8,xmax=4.2)
  plt.ylim(ymin=-1,ymax=1)
  plt.savefig('./Plots/'+namefig)


def Plot_AssortativityProfile_rewired(Aij,Bij,namefig):
  AS_ini = np.zeros(4)
  AS_end = np.zeros(4)
  x = range(4)
  
  for mode in range(4):
    AS_ini[mode] = assortativity(Aij,mode)
    AS_end[mode] = assortativity(Bij,mode)
    
  label = ["(in,out)","(out,in)","(in,in)","(out,out)"]
  plt.figure()
  plt.plot(x,AS_ini,'g^--',label='Initial',markersize=8,linewidth=2)
  plt.plot(x,AS_end,'ro--',label='Rewired',markersize=8,linewidth=2)
  plt.xticks(x,label,fontsize=18)
  plt.yticks(fontsize=18)
  plt.ylabel("Assortativity")
  plt.xlim(xmin=-1,xmax=4)
  plt.ylim(ymin=-1,ymax=1)
  plt.legend(fontsize=12)
  plt.grid()
  plt.savefig('./Plots/'+namefig)
  
  

def Rewiring_eff(Cij):
  
  # Obtaining edges table
  C = Cij.copy()
  i,j = np.where(C)
  k = len(i)
  #M = np.sum(i)
  edgesR = np.array([],dtype='int')
  maxiter = 0.5*k*(k+1)
  rw = 0
  
  
  n1 = np.random.randint(k)
  n2 = np.random.randint(k)
  #print n1,n2
  #print i[n1],j[n1],i[n2],j[n2]
  
  
  mi = 0
  it = 0
  while 1 and mi<maxiter:
    #print "mi : ",mi
    n2 = np.random.randint(k)
    # Verifying if there is autoloops
    succes = 1
   
    while succes and it<maxiter:
      if(i[n1]==j[n2] or i[n2]==j[n1]):
	n2 = np.random.randint(k)
	#print "dentro: ", i[n1],j[n1],i[n2],j[n2]
	it+=1
      else:
	succes = 0
	
      
    a = i[n1]; b = j[n1]
    c = i[n2]; d = j[n2]
  
    # Verifying existent conections
    if not (C[a,d] or C[c,b]):
      #print "Without repeated conections"
      #print "succes: ", i[n1],j[n1],i[n2],j[n2]
      C[a,d] = C[a,b];  C[a,b]=0
      C[c,b] = C[c,d];  C[c,d]=0
      # Saving nodes rewired
      edgesR = np.append(edgesR,[a,b,c,d],axis=0)
      rw = 1
      break
    else:
       #n2 = np.random.randint(k)
       mi+=1
  
  return C,edgesR,rw
 
 
def Rewiring(Cij):
  # Obtaining edges table
  C = Cij.copy()
  i,j = np.where(C)
  k = len(i) #Number of conections
  edgesR = np.array([],dtype='int')
  maxiter = 0.5*k*(k+1)
  flag = 0
  
  n1 = np.random.randint(k)
  n2 = np.random.randint(k)
  #print n1,n2
  #print i[n1],j[n1],i[n2],j[n2]
  
  if(i[n1]==j[n2] or i[n2]==j[n1]):
    return C,edgesR,flag
  else:
    a = i[n1]; b = j[n1]
    c = i[n2]; d = j[n2]
    
    # Verifying existent conections
    if not (C[a,d] or C[c,b]):
      #print "Without repeated conections"
      #print "succes: ", i[n1],j[n1],i[n2],j[n2]
      C[a,d] = C[a,b];  C[a,b]=0
      C[c,b] = C[c,d];  C[c,d]=0
      # Saving nodes rewired
      edgesR = np.append(edgesR,[a,b,c,d],axis=0)
      flag = 1
      return C,edgesR,flag
    else:
      return C,edgesR,flag
      


  
  

def GetDegree(CIJ):
  indeg = np.sum(CIJ,axis=0) # columns
  outdeg = np.sum(CIJ,axis=1) # rows
  return indeg,outdeg
    

def DeltaR(indeg,outdeg,edgesR,flag):
  # In-Out 
  if flag == 0: 
    Jdo = indeg[edgesR[[0,2]]];  Kdo = outdeg[edgesR[[1,3]]]
    Jdn = indeg[edgesR[[0,2]]];  Kdn = outdeg[edgesR[[3,1]]]
  # Out-In
  elif flag == 1: 
    Jdo = outdeg[edgesR[[0,2]]];  Kdo = indeg[edgesR[[1,3]]]
    Jdn = outdeg[edgesR[[0,2]]];  Kdn = indeg[edgesR[[3,1]]]
  # In-In
  elif flag == 2: 
    Jdo = indeg[edgesR[[0,2]]];  Kdo = indeg[edgesR[[1,3]]]
    Jdn = indeg[edgesR[[0,2]]];  Kdn = indeg[edgesR[[3,1]]]
  # Out-Out
  elif flag == 3: 
    Jdo = outdeg[edgesR[[0,2]]];  Kdo = outdeg[edgesR[[1,3]]]
    Jdn = outdeg[edgesR[[0,2]]];  Kdn = outdeg[edgesR[[3,1]]]
  else:
   print "You need choose some configuration"
    
  #print "Edges: ",edgesR
  #print Jdo,Kdo,Jdn,Kdn
  Oldterm = np.sum(Jdo*Kdo)
  Newterm = np.sum(Jdn*Kdn) 
  delta = Newterm - Oldterm
  #print "delta: ",delta
  return delta
   
    



def randmio_dir(R,iter):
	'''
This function randomizes a directed network, while preserving the in-
and out-degree distributions. In weighted networks, the function
preserves the out-strength but not the in-strength distributions.

Input:      W,      directed (binary/weighted) connection matrix
		    ITER,   rewiring parameter
				    (each edge is rewired approximately ITER times)

Output:     R,      randomized network
		    eff,    number of actual rewirings carried out
	'''
	R=R.copy()
	n=len(R)
	i,j=np.where(R)
	k=len(i)
	iter*=k
	
	# Degress and edges
	edges = np.array([],dtype="int").reshape(0,4)
	indeg = np.sum(R,axis=0) # Sum over columns
        outdeg = np.sum(R,axis=1) #Sum over row
        #Calculating number of conections
        M =np.sum(indeg)
        
        
        
	max_attempts=np.round(n*k/(n*(n-1)))
	eff=0

	for it in xrange(iter):
		att=0
		while att<=max_attempts:			#while not rewired
			while True:
				e1=np.random.randint(k)
				e2=np.random.randint(k)
				while e1==e2:
					e2=np.random.randint(k)
				a=i[e1]; b=j[e1]
				c=i[e2]; d=j[e2]

				if a!=c and a!=d and b!=c and b!=d:
					break					#all 4 vertices must be different

			#rewiring condition
			if not (R[a,d] or R[c,b]):
				print "R[%d][%d] = %d    R[%d][%d] = %d   iter: %d"%(c,d,R[c,d],a,b,R[a,b],it)
				R[c,b]=R[c,d]; R[c,d]=0
				R[a,d]=R[a,b]; R[a,b]=0
				#R[c,b]=1; R[c,d]=0
                                #R[a,d]=1; R[a,b]=0
                                
				edges=np.append(edges,[[a,c,b,d]],axis=0) # nodes rewired
				#DeltaR(indeg,outdeg,edges[-1],1)
				i.setflags(write=True); j.setflags(write=True)
				j[e1]=d; j[e2]=b			#reassign edge indices
				eff+=1
				break
			att+=1
				
	return R,eff,edges,np.array([i,j])



