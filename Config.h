#include<stdio.h>
#include<math.h>
#include<malloc.h>
#include<time.h>

//=================
// GSL libraries
//=================
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
// #include <gsl/gsl_permutation.h> 

struct Nodes
{
	int id;
	int *indegree;
	int *outdegree;
	int Nnodes;
};

int Nconections;


int vector_sumelm(int *vec){
	int sum,length;

	length = sizeof(vec)/sizeof(vec[0]);
	printf("Len: %d\n",length);
	return length;
}
