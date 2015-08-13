#==================================================================================================
# IMPORTING LIBRARIES
#==================================================================================================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from modules import *

#Library to define macros
from pypreprocessor import pypreprocessor

#==================================================================================================
# MACROS
#==================================================================================================
# Init macros
pypreprocessor.parse()
#define PLOT



#==================================================================================================
# PARAMETERS
#==================================================================================================
NR = 8000                                         # Number of rewirings
NA = 4						  # Number of assortativites to calculate
Allterms = True
Training = False				  # Training the network

#********************************
# Establishing TYPE:
#     0  In-Out    1  Out-In
#     2  In-In     3  Out-Out
#********************************
TYPE = [2,0]
NTraining = len(TYPE)

for Training in range(NTraining):
  #==================================================================================================
  # INITIALITING VARIABLES
  #==================================================================================================
  r_ini = np.zeros((NA,4))                         # Initializing vector of assortativities and terms
  R = np.zeros(NA) 				 # Initializing vector of assortativities
  r_t = np.zeros(NA)
  Delta = np.zeros(4)                              #
  Delta_plot = np.array([]).reshape(0,NA)          #
  AllDeltas = np.array([]).reshape(0,NA)           #
  R_plot = np.array([]).reshape(0,NA)
  Rtheoric = np.array([]).reshape(0,NA)
  AllR = np.array([]).reshape(0,NA)
  Eff_rewire = np.array([0],dtype="int")

  # Initializing counters
  EffRewiring = 0
  SuccessRewiring = 0



  #==================================================================================================
  # GET PRELIMINAR VALUES
  #==================================================================================================

  # Reading adjacency matrix
  A = np.loadtxt("./data/AdjacencyMatrix%d.txt"%Training)
  B = np.copy(A)
  C = np.copy(A)

  # Calculating degree of nodes and Number of total connections
  Indeg , Outdeg = GetDegree(A)                     # Degree of nodes
  M = np.sum(Indeg)                                #number of conections

  # Calculating initial assortativity
  for mode in range(NA):
    r_ini[mode] = np.array(assortativity(A,mode,True))


  # Save initial assortativity
  R_plot = np.append(R_plot, [r_ini[:,0]], axis=0)
  Rtheoric = np.append(Rtheoric, [r_ini[:,0]], axis=0)
  AllR = np.append(AllR, [r_ini[:,0]], axis=0)

  # Making a copy of r_ini
  rcopy = r_ini.copy()

  #==================================================================================================
  # CALCULATION OF REWIRING
  #==================================================================================================
  for i in range(1,NR+1):
    # Doing de rewiring
    Matrix,edgeR,flag = Rewiring(B)
    
    # Verifiying if rewiring was successful
    if flag:
      # saving edges of pair nodes rewired
      Edges = edgeR
      
      # Calculating DeltaR
      for mode in range(NA):
	Delta[mode] = DeltaR(Indeg,Outdeg,Edges,mode)/M
      
      if Allterms:
	#****************************************************************
	# Calculating all terms independently of delta criterion
	#****************************************************************
	# Updating adjacency matrix
	B = Matrix
	# Updating first term of assortativity formula
	for mode in range(NA):
	  rcopy[mode,1] = rcopy[mode,1] + Delta[mode]
	  # Calculating new assortativity
	  rcopy[mode,0] = Assortativity_rewired(rcopy[mode,1:])
	
	# Saving the value of delta
	AllR = np.append(AllR,[rcopy[:,0]], axis = 0)
	AllDeltas = np.append( AllDeltas, [Delta], axis=0)
	
      else:
      
	#****************************************************************
	# Verifiying if rewiring increment assortativity of mode TYPE
	#****************************************************************

	if Delta[TYPE[Training]]>0:
	
	  # Updating adjacency matrix
	  B = Matrix
	  
	  # Updating first term of assortativity formula
	  # This avoid the calculation of all terms in order to get performance
	  for mode in range(NA):
	    r_ini[mode,1] = r_ini[mode,1] + Delta[mode]
	    
	  # Calculating new assortativity
	  for mode in range(NA):
	    r_ini[mode,0] = Assortativity_rewired(r_ini[mode,1:])
	    r_t[mode] = np.array(assortativity(B,mode,False)) 
	    
	  # Saving the assortativities for each mode or type
	  # and all deltas > 0
	  R_plot = np.append( R_plot, [r_ini[:,0]], axis=0)
	  Rtheoric = np.append( Rtheoric, [r_t], axis=0)
	  Delta_plot = np.append( Delta_plot, [Delta], axis=0)
	  Eff_rewire = np.append( Eff_rewire,i)
	  
	  EffRewiring+=1
      SuccessRewiring+=1
      
    # For cases in which rewire is not successful
    else:
      if Allterms:
	AllR = np.append(AllR,[rcopy[:,0]],axis=0)
	AllDeltas = np.append( AllDeltas, [Delta], axis=0)
    
  np.savetxt("./data/AdjacencyMatrix%d.txt"%(Training+1),B,fmt="%d")  
#ifdef PLOT    
  #==================================================================================================
  #  PLOTS
  #==================================================================================================

  #******************************
  # GENERAL PARAMETERS OF PLOT
  #******************************
  mpl.rcParams['xtick.labelsize'] = 17
  mpl.rcParams['ytick.labelsize'] = 17
  mpl.rcParams['font.family'] = 'FreeSans' #'Norasi'
  mpl.rcParams['xtick.minor.size'] = 3
  mpl.rcParams['font.size'] = 17.0
  Label = ["In-out","Out-In","In-In","Out-Out"]

  if not Allterms:
    #***********************************************
    # Plot of assortativity vs effective rewirings
    #***********************************************
    plt.figure()
    for i in range(NA):
      plt.plot(Eff_rewire,R_plot[:,i],'-', label=Label[i], lw=2, ms=7)
    plt.grid()
    plt.xlabel("Rewiring")
    plt.ylabel("Assortativity")
    plt.legend(loc="upper left",fontsize=15)
    plt.savefig("Plots/EffectiveRewiring_t%d.pdf"%Training)

    #***********************************************
    # Plot of assortativity vs real rewirings
    #***********************************************
    plt.figure()
    for i in range(NA):
      plt.plot(R_plot[:,i],'-', label=Label[i], lw=2, ms=7)
    plt.grid()
    plt.xlabel("Rewiring")
    plt.ylabel("Assortativity")
    plt.legend(loc="upper left",fontsize=15)
    plt.savefig("Plots/RealRewiring_t%d.pdf"%Training)

    #***********************************************
    # Plot of assortativity vs effective rewirings
    # using assortativity routine
    #***********************************************
    plt.figure()
    for i in range(NA):
      plt.plot(Eff_rewire,Rtheoric[:,i],'-', label=Label[i], lw=2, ms=7)
    plt.grid()
    plt.xlabel("Rewiring")
    plt.ylabel("Assortativity")
    plt.title("Assortativity calculated with routine")
    plt.legend(loc="upper left",fontsize=15)
    plt.savefig("Plots/TheoricRewiring_t%d.pdf"%Training)
    
    #***********************************************
    # Plot of assortativity profile after rewiring
    #***********************************************
    Plot_AssortativityProfile_rewired(A,B,'Profile_afterRewired_t%d.pdf'%Training)
    

  if Allterms:
    #***********************************************
    # Plot of all deltas vs total rewirings
    #***********************************************
    plt.figure()
    plt.plot(range(NR),AllDeltas[:,TYPE[Training]],'r-', lw=0.5, ms=7)
    plt.grid()
    plt.xlabel("Rewiring")
    plt.ylabel("All Deltas")
    #plt.legend(loc="upper left",fontsize=15)
    plt.savefig("Plots/AllDeltas_Rewiring_t%d.pdf"%Training)
    
    #***********************************************
    # Plot of assortativity vs total rewirings
    #***********************************************
    plt.figure()
    #for i in range(NA):
      #plt.plot(range(NR+1),AllR[:,i],'-', label=Label[i], lw=0.5)
    plt.plot(range(NR+1),AllR[:,TYPE[Training]],'-', label=Label[TYPE[Training]], lw=0.5,color='green')
    plt.grid() 
    plt.xlabel("Total Rewiring")
    plt.ylabel("Assortativity")
    plt.legend(loc="upper left",fontsize=15)
    plt.savefig("Plots/AllR_Rewiring_t%d.pdf"%Training)
#endif