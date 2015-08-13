#===========================================================================
#  NEURAL NETWORK
#  Code to study complex networks
#
#  By: Cesar Alfredo Uribe Leon
#      alfredo.uribe@udea.edu.co
#      2015
#===========================================================================


#####################
# OPTIONS
#####################

# For testing the code
# OPT += -DPROBE


#-------------------------------------------------------
CC = g++

OPTIONS = $(OPT)

GSLPATH = /usr/local/include/

LFLAGS = -lm -L$(GSLPATH) -lgsl -lgslcblas

CPPFLAGS =  -c  ${OPTIONS} -I$(GSLPATH) -I.

OBJ = main.o Allvars.o Util.o Allocation.o Network.o

INCL = Allvars.h Prototypes.h makefile

EXEC = main.out


###################
# BASIC RULES
###################

compile:${EXEC}
	@echo "\nCOMPILING..." $^
	@echo "options" ${OPT}

${EXEC}:${OBJ}
	@echo "\n ---- Compiling ---- \n" $@
	$(CC) ${OBJ} ${LFLAGS} -o ${EXEC}

${OBJ}:$(INCL)


# %.o:%.cpp
# 	@echo "\n ---- Creating .o files ----"
# 	$(CC) $< $(CFLAGS) -o $@


###################
# RUN RULES
###################
run:
	./${EXEC}

init:
	python python_codes/GeneratingNodesDegree.py

rewire:
	#python Rewiring.py
	python python_codes/MakeRewiring.py
	
viewplots:
	qpdfview ./Plots/*.pdf &

###########################
# CLEAN RULES
###########################

clean:
	@echo "Cleaning..."
	rm -rf *.out *~ *.o ./data/*~
	rm -rf $(PROGS:.out=)
	rm python_codes/*.pyc python_codes/*~
	#rm -rf *.dat
