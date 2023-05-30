#!/bin/bash -x
#SBATCH --time 6:00:00
#SBATCH --cpus-per-task 10

 ./fixdata.py -w 10 /scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL16v9_nano_v10/Met
 ./fixdata.py -w 10 /scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL16APVv9_nano_v10/Met
 ./fixdata.py -w 10 /scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL17v9_nano_v10/Met
 ./fixdata.py -w 10 /scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL18v9_nano_v10/Met
