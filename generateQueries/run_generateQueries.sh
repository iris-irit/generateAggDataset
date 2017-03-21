#!/bin/bash
#
#SBATCH --job-name=getRawData
#SBATCH --error=/projets/iris/PROJETS/PRINCESS/TournAgg/Code/generateAggDataset/generateQueries/error.txt
#SBATCH --mail-user=pitarch@irit.fr
#SBATCH --mail-type=ALL
#SBATCH --ntasks=1

srun /logiciels/Python-3.5.2/bin/python3 /projets/iris/PROJETS/PRINCESS/TournAgg/Code/generateAggDataset/generateQueries/generateQuery.py