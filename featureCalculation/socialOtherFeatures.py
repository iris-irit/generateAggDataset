import os, sys
import json


def lookupTweet(id) :
	for j in json_raw :
		if j["id"] == id :
			return j


path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/"


name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"

features = {}
mappingDocTweets = {}
mappingTweetUser = {}

for repEvent in os.listdir(path_events) :

	if not os.path.exists(path_features+repEvent) :
		os.mkdir(path_features+repEvent)

	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)

	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	with open(path_events+repEvent+name_dir_inverse, "r") as fjson :
		inverse = json.load(fjson)

	for idDoc in mapping :

		mappingDocTweets[idDoc] = mapping[idDoc]["tweets"]

		for tw in mapping[idDoc]["tweets"] :

			if tw not in mappingTweetUser :
				data = lookupTweet(int(tw))
				print(data)
				print(type(tw))
				sys.exit()



	with open(path_features+repEvent+"/social.json", "w") as fout :
		json.dump(features,fout)