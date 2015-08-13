#ifndef ALLVARS_H
#define ALLVARS_H

#include <stdio.h>
#include <math.h>
#include <malloc.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

//=================
// GSL libraries
//=================
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
// #include <gsl/gsl_permutation.h> 

//===================
// MACROS
//===================
#define MAXCOL  1000
#define MAXROW  1000
#define MAXSIZE 100
#define NROWS   2

//=======================
// SOME TAGS
//=======================
#define NODES   0
#define NEDGES  1

extern struct network
{
	int id;
	int *indegree;
	int *outdegree;
	int Nnodes;
	int Ndegree;
	int *edges[NROWS];
	int Nedges;
	float assortativity;
	int degree;
	int *pos;
	int *CIJ;
}Netwk;

extern char temp[256];
extern int Nr,Nc;
extern int Nedges_deleted;
extern int Nrepeated_deleted;
extern int Nloops_deleted;
extern FILE *file;
extern FILE *in;
extern int prm[MAXSIZE];

extern const gsl_rng_type *type;
extern gsl_rng *rand_generator;


#endif