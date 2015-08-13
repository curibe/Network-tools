#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "Allvars.h"
#include "Prototypes.h"


void makeCIJ_degreefixed(void){
	int i,j,row,column;
	int trash,Newindex;
	int warning;

	gsl_ran_shuffle(rand_generator,Netwk.edges[1],Netwk.Nedges,sizeof(int));

	for(i=0;i<Netwk.Nedges;i++){
		row = Netwk.edges[0][i];
	 	column = Netwk.edges[1][i];

	 	if(Netwk.CIJ[row*Nc+column]==1 or row==column){
	 		warning = 1;
// 	 		printf("row: %d   column: %d i:%d\n",row,column, i );
	 		while(1){
				
	 			Newindex = (int)ceil(Netwk.Nedges*gsl_rng_uniform(rand_generator));
	 			
	 			// Se verifica si el par de conexiones que resultan
	 			// en la permutacion no existe
	 			if ( !( Netwk.CIJ[ Netwk.edges[0][i]*Nc + Netwk.edges[1][Newindex] ] or 	
	 				Netwk.CIJ[ Netwk.edges[0][Newindex]*Nc + Netwk.edges[1][i] ] ) )
	 			{	
// 	 				printf("i: %d Ni:%d ,  %d %d %d %d\n",i,Newindex,Netwk.edges[0][i],Netwk.edges[1][Newindex],Netwk.edges[0][Newindex],Netwk.edges[1][i] );
	 				if( !( Netwk.edges[0][i] == Netwk.edges[1][Newindex] or 
					       Netwk.edges[0][Newindex] == Netwk.edges[1][i] ) )
					{
// 	 					printf("No Son iguales\n");
	 					//Se crea la nueva conexion
	 					Netwk.CIJ[ Netwk.edges[0][i]*Nc + Netwk.edges[1][Newindex] ] = 1;

	 					// Si la conexion resultante del indice permutado ya existia 
	 					// y se habia creado, se elimina dicha conexion.
	 					if(Newindex<i){
	 						//Se elimina la antigua conexion
	 						Netwk.CIJ[ Netwk.edges[0][Newindex]*Nc + Netwk.edges[1][Newindex] ] = 0; 
	 						// Se crea la otra conexion
	 						Netwk.CIJ[ Netwk.edges[0][Newindex]*Nc + Netwk.edges[1][i] ];
	 					}

	 					// Se reescribe el vector de conexiones
	 					trash = Netwk.edges[1][i];
	 					Netwk.edges[1][i] = Netwk.edges[1][Newindex];
	 					Netwk.edges[1][Newindex] = trash;
	 					break;
	 				}
	 			}
	 			warning = warning + 1;
	 			if(warning>2*Netwk.Nedges*Netwk.Nedges){
	 				printf(" ### Iteration limit was reached ###\n");
	 				gsl_ran_shuffle(rand_generator,Netwk.edges[1],Netwk.Nedges,sizeof(int));
	 				warning=1; 
	 				i=0;
					printf(" ===== The program has been terminated ====\n");
					exit(0);
	 			}	
	 		}
	 		
	 	}
	 	else{
	 		Netwk.CIJ[row*Nc+column]=1;
	 	}
	 }
	
	printf("***  Matrix was created with exit  ***\n");
	
	// Saving Matrix in an output file
	SaveMatrix("AdjacencyMatrix.txt");
	printf("***  Matrix was saved in file 'AdjacencyMatrix.txt' \n");
	
	//Saving Edges in an ouput file
	SaveEdges("Edges.txt");
	printf("***  Table of edges was saved in file 'Edges.txt' \n");
}

void MakeCIJ_Fast(void){
	int i,j,row,column;
		
	// Permuting out-edge vector
	gsl_ran_shuffle(rand_generator,Netwk.edges[1],Netwk.Nedges,sizeof(int));
	
	//Creating Adjacency Matrix
	for(i=0;i<Netwk.Nedges;i++){
	  
	  row = Netwk.edges[0][i];
	  column = Netwk.edges[1][i];
	  Netwk.CIJ[row*Nc+column]+=1;	  
	}
	
	//---------------------------------------------------
	//Eliminating autoloops and repeated edges
	//---------------------------------------------------
	for(i=0;i<Netwk.Nnodes;i++){
	  
	  // Autoloops
	  if(Netwk.CIJ[i*Nc+i]>0){
	    Nloops_deleted = Netwk.CIJ[i*Nc+i] + Nloops_deleted;
	    Netwk.CIJ[i*Nc+i]=0;
	  }
	    
	  for(j=0;j<Netwk.Nnodes;j++){
	    
	    // repeated edges
	    if(Netwk.CIJ[i*Nc+j]>1){
	      Nrepeated_deleted = Netwk.CIJ[i*Nc+j] + Nrepeated_deleted - 1;
	      Netwk.CIJ[i*Nc+j] = 1;
	      
	    }
	    
	  }
	}
	
	printf("***  Matrix was created with exit***\n");
	
	// Saving Matrix in an output file
	SaveMatrix("./data/AdjacencyMatrix0.txt");
	printf("*** Matrix was saved in file './data/AdjacencyMatrix0.txt' \n");
	
	//Saving Edges in an ouput file
	SaveEdges("./data/Edges.txt");
	printf("*** Table of edges was saved in file 'Edges.txt' \n");
}


void SaveMatrix(char filename[]){
      int i,j;
      FILE *Thefile;
  
      
      Thefile = fopen(filename,"w");
      for(i=0;i<Netwk.Nnodes;i++){
	for(j=0;j<Netwk.Nnodes;j++){
	  fprintf(Thefile,"%d ",Netwk.CIJ[i*Nc+j]);
	}
	fprintf(Thefile,"\n");
      }
      fclose(Thefile);
}

void SaveEdges(char filename[]){
  int i,j;
  FILE *Ofile;
  
  Ofile = fopen(filename,"w");
  for(i=0;i<Netwk.Nnodes;i++){
    for(j=0;j<Netwk.Nnodes;j++){
      if(Netwk.CIJ[i*Nc+j]==1){
	fprintf(Ofile,"%d %d\n",i,j);
      }
    }
  }
  fclose(Ofile);
}