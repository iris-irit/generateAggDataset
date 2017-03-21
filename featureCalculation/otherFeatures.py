import os, sys
import json
from otherFunctions import *

# #############################################
#
# Calcule des features de type other
#
# #############################################


path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/" # Pas utile pour l'instant


name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"

features = {}

for repEvent in os.listdir(path_events) :

	features = {}

	print("["+repEvent+"]")

	if not os.path.exists(path_features+repEvent) :
		os.mkdir(path_features+repEvent)


	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)

	burst = getBurstiness(json_raw)
	fresh = getFreshness(json_raw)


	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	for docId in mapping :
		lTweets = mapping[docId]["tweets"]

		listBurst = [burst[x] for x in lTweets]
		listFresh = [fresh[x] for x in lTweets]

		features[docId] = {
			"freshness": sum(listFresh) / len(listFresh),
			"burstiness": sum(listBurst) / len(listBurst)
		}

	print(features)

	with open(path_features+repEvent+"/other.json", "w") as fout :
		json.dump(features,fout)
