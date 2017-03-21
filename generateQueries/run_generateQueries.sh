#!/bin/bash
#
#SBATCH --job-name=getRawData
#SBATCH --mail-user=pitarch@irit.fr
#SBATCH --mail-type=ALL
#SBATCH --ntasks=1

srun /logiciels/Python-3.5.2/bin/python3 /projets/iris/PROJETS/PRINCESS/TournAgg/Code/generateQueries/generateQuery.py