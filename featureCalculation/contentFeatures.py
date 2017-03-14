import os, sys
import json


def lookupTweet(id):
    for j in json_raw:
        if j["id"] == id:
            return j


path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/"

name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"

features = {}

for repEvent in os.listdir(path_events):
    json_raw = {}
    mapping = {}
    inverse = {}

    if not os.path.exists(path_features + repEvent):
        os.mkdir(path_features + repEvent)

    with open(path_json + "data_" + repEvent + ".txt", "r") as fjson:
        json_raw = json.load(fjson)

    with open(path_events + repEvent + name_dir_mapping, "r") as fjson:
        mapping = json.load(fjson)

    with open(path_events + repEvent + name_dir_inverse, "r") as fjson:
        inverse = json.load(fjson)

    for idDoc in mapping:

        urls = 0
        hashtags = 0

        features[idDoc] = {}

        for tw in mapping[idDoc]["tweets"]:
            data = lookupTweet(int(tw))
            print(data)

            urls += len(data["entities"]["urls"])
            hashtags += len(data["entities"]["hashtags"])

        features[idDoc]["url_count"] = urls
        #		features[idDoc]["url_exist"] = urls
        features[idDoc]["hashtag_count"] = hashtags
    #		features[idDoc]["hashtag_exist"] = hashtags

    with open(path_features + repEvent + "/content.json", "w") as fout:
        json.dump(features, fout)
