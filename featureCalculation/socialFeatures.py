import os
import json


def lookupTweet(id) :
	for j in json_raw :
		if j["id"] == id :
			return j


path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"

name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"


for repEvent in os.listdir(path_events) :
	json_raw = {}
	mapping = {}
	inverse = {}
	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)

	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	with open(path_events+repEvent+name_dir_inverse, "r") as fjson :
		inverse = json.load(fjson)

	for idDoc in mapping :

		for tw in mapping[idDoc]["tweets"] :
			data = lookupTweet(int(tw))
			print(data)