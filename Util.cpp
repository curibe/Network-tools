#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "Allvars.h"
#include "Prototypes.h"


int exec(char *cmd){
	
	FILE *In;
	
	In = popen(cmd,"r");
	
	if (!In) return (1);
	fgets(temp,256,In);
	
	pclose(In);
	return atoi(temp);
}

int Sum(int *vec, int dim){
	int i;
	int sum = 0.0;
	for(i=0;i<dim;i++){
		sum = sum + vec[i];
	}
	return sum;
}

void ordinal_assign(void){
	int i,j,uplimit[2],lowlimit[2];
	int k=0,kpos=0;
	lowlimit[0] = lowlimit[1] = 0;	
	for(i=0;i<Netwk.Ndegree;i++){

		// Out - Edges
		uplimit[0] = lowlimit[0] + Netwk.outdegree[i];
		Netwk.pos[i] = kpos;
		for(j=lowlimit[0];j<uplimit[0];j++){
			//printf("j: %d   i: %d\n",j,i);

			Netwk.edges[0][j] = i;
			kpos++;
		}
		lowlimit[0] = uplimit[0];

		// In - Edges
		uplimit[1] = lowlimit[1] + Netwk.indegree[i];
		for(j=lowlimit[1];j<uplimit[1];j++){
			Netwk.edges[1][j] = i;	
		}
		lowlimit[1] = uplimit[1];
	}
	printf("***  Edges vector created with exit  ***\n");
// 	printf("Edges:\n");
// 	for(i=0;i<Netwk.Nedges;i++){
// 	  printf("%d %d\n",Netwk.edges[0][i],Netwk.edges[1][i]);
// 	}
}

void InitMatrixCij(void){
	int i,j;
	for(i=0;i<Netwk.Nnodes;i++){
		for(j=0;j<Netwk.Nnodes;j++){
			Netwk.CIJ[i*Nc + j] = 0;
			// printf("Asigning i:%d j:%d C[%d,%d]=%d\n",i,j,i,j,Net.CIJ[i*Nc+j] );
		}
	}
	printf("***  Matrix was successfully initialized  ***\n");
}

void Todump(char filename[]){
	char cmd[100];
	sprintf(cmd,"grep -v \"\%\" %s | grep -v \"^$\" | awk -F\"=\" '{print $2}' > %s.dump",filename,&filename[7]);
	printf("cmd: %s\n",cmd);
	system(cmd);
}

int ReadParameters(char filename[]){
	char cmd[100],filedump[100];
	int i=0;
	FILE *file;
	printf("Reading files...\n");
	file=fopen(filename,"r");
	printf("Reading files...\n");
	if(file==NULL){
		printf("File %s not exist\n",filename);
		return(1);
	}
	fclose(file);

	printf("Exec Todump...\n");
	Todump(filename);
	printf("Todump executed...\n");
	sprintf(filedump,"%s.dump",&filename[7]);
	file = fopen(filedump,"r");

	while(getc(file) != EOF){
		fscanf(file,"%d",&prm[i]);
		i++;
	}
	
	fclose(file);
	
	printf("***  The file '%s' has been loaded  ***\n",filename);
	
	sprintf(cmd,"rm -rf %s.dump",&filename[7]);
	system(cmd);
	return(0);
}

void PrintResults(char mode[]){
  int Ndeleted;
  if(strcmp(mode,"basic")==0){
    Ndeleted = Nloops_deleted+Nrepeated_deleted;
    printf("\n===========================================================\n");
    printf("Basic information:\n\n"); 
    printf("Number of nodes:                       %d\n",Netwk.Nnodes);
    printf("Number of initial edges:               %d\n",Netwk.Nedges);
    printf("Number of loops deleted:               %d\n",Nloops_deleted);
    printf("Number of repeated edges deleted:      %d\n",Nrepeated_deleted);
    printf("Number of edges deleted:               %d\n",Ndeleted);
    printf("Percent of edges deleted:              %.2f\%\n",Ndeleted*100.0/Netwk.Nedges);
    printf("===========================================================\n");
  }
  
}