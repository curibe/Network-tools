#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include "Allvars.h"

struct network Netwk;
char temp[256];
int Nr,Nc;
int Nedges_deleted=0;
int Nloops_deleted=0;
int Nrepeated_deleted=0;
FILE *file;
FILE *in;
int prm[MAXSIZE];

const gsl_rng_type *type;
gsl_rng *rand_generator;