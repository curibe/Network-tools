#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <time.h>
#include "Allvars.h"
#include "Prototypes.h"


int main(void){

	int i,j,l,Newindex,flag=0;
	int row,column,m,n;
	int trash;
	int ncon;
		
	
	ReadParameters("./data/InitialParam.param");
	allocate_variables();
#ifdef PROBE
	file = fopen("./data/NodesDegree.txt","r");
#else
	file = fopen("./data/NodesDegree2.txt","r");
#endif
	for(i=0;i<Netwk.Nnodes;i++)
	{
		fscanf(file,"%d %d",&Netwk.indegree[i],&Netwk.outdegree[i]);
		Netwk.id = i;
	}


	ordinal_assign();
	InitMatrixCij();
// 	makeCIJ_degreefixed();
	MakeCIJ_Fast();
#ifdef PROBE
	// Showing Edge vector
	printf("\nEdge Matrix:\n");
	for(i=0;i<Netwk.Nedges;i++){
	  printf("%d ",Netwk.edges[0][i] );
	}
	printf("\n");
	for(i=0;i<Netwk.Nedges;i++){
	  printf("%d ",Netwk.edges[1][i] );
	}
	printf("\n");
#endif
	PrintResults("basic");
	free_memory();
	fclose(file);






}
