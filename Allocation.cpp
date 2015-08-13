#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>

#include "Allvars.h"
#include "Prototypes.h"

void allocate_variables(void){
	
	int i;
	
	// Nodes parameters
	//-------------------------
	//Nod.Nconections = exec("wc -l NodesDegree.txt | awk -F\" \" \'{print $1}\'");
#ifdef PROBE
	Netwk.Ndegree = exec("awk 'END {print NR}' ./data/NodesDegree.txt");
#else
	Netwk.Ndegree = exec("awk 'END {print NR}' ./data/NodesDegree2.txt");
#endif
	Netwk.Nnodes = prm[NODES];
	Netwk.Nedges = prm[NEDGES];
	Netwk.indegree = (int *)malloc(Netwk.Ndegree * sizeof(int));
	Netwk.outdegree = (int *)malloc(Netwk.Ndegree * sizeof(int));


	//Network parameters
	//-------------------------
	Netwk.pos = (int *)malloc(Netwk.Ndegree * sizeof(int));
	// Number of rows and columns
	Nr = Netwk.Ndegree;
	Nc = Netwk.Ndegree;
	for(i=0;i<NROWS;i++){
		Netwk.edges[i] = (int *)malloc(Netwk.Nedges * sizeof(Netwk.edges[0])); // 2 rows
	}
	Netwk.CIJ = (int *)malloc(Nr*Nc * sizeof(int));

	


	// Alocation and  Initialitation of rng in gsl
	//gsl_rng_env_setup();
	type = gsl_rng_mt19937;
	rand_generator = gsl_rng_alloc(type);
	gsl_rng_set(rand_generator,time(NULL)*getpid());
	printf("***  Variables was succesfully allocated  ***\n");
}

void free_memory(void){
	int i;
	free(Netwk.indegree);
	free(Netwk.outdegree);
	free(Netwk.pos);
	for(i=0;i<NROWS;i++){
	  free(Netwk.edges[i]);
	}
	//free(Netwk.edges);
	free(Netwk.CIJ);
	gsl_rng_free (rand_generator);
	printf("***  Memory was succesfully liberated  ***\n");
}