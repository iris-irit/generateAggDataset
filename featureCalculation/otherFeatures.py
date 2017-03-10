import os, sys
import json
from otherFunctions import *

# #############################################
#
# Calcule des features de type other
#
# #############################################


path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" # Pas utile pour l'instant
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/" # Pas utile pour l'instant


name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"

features = {}

for repEvent in os.listdir(path_events) :
	json_raw = {}
	mapping = {} # Pas  utile pour l'instant
	inverse = {} # Pas  utile pour l'instant


	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)


	print(getBurstiness(json_raw))
	sys.exit()