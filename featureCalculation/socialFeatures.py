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

for repEvent in os.listdir(path_events) :
	json_raw = {}
	mapping = {}
	inverse = {}

	if not os.path.isfile(path_features+repEvent) :
		os.mkdir(path_features+repEvent)

	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)

	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	with open(path_events+repEvent+name_dir_inverse, "r") as fjson :
		inverse = json.load(fjson)

	for idDoc in mapping :

		favourites = 0
		retweets = 0
		followers = 0

		features[idDoc] = {}

		for tw in mapping[idDoc]["tweets"] :
			data = lookupTweet(int(tw))
			print(data)

			favourites += data["favourite_count"]
			retweets += data["retweet_count"]
			followers += data["user"]["followers_count"]

		features[idDoc]["favourite_count"] = favourites
		features[idDoc]["retweet_count"] = retweets
		features[idDoc]["followers_count"] = followers

	json.dump(features,path_features+repEvent+"/social.json")