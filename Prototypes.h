#ifndef ALLVARS_H
#include "Allvars.h"
#endif

int exec(char *cmd);
int Sum(int *vec, int dim);
void ordinal_assign(void);
void allocate_variables(void);
void free_memory(void);
void InitMatrixCij(void);
void makeCIJ_degreefixed(void);
void MakeCIJ_Fast(void);
void SaveMatrix(char filename[]);
void SaveEdges(char filename[]);
void Todump(char filename[]);
int ReadParameters(char filename[]);
void PrintResults(char mode[]);
