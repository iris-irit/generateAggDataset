#!/bin/bash
#
#SBATCH --job-name=getRawData
#SBATCH --output=/projets/iris/PROJETS/PRINCESS/TournAgg/Code/generateAggDataset/collectRawData/output.txt
#SBATCH --mail-user=pitarch@irit.fr
#SBATCH --mail-type=ALL
#SBATCH --ntasks=1

srun /logiciels/Python-3.5.2/bin/python3 /projets/iris/PROJETS/PRINCESS/TournAgg/Code/generateAggDataset/collectRawData/get_raw_data.py