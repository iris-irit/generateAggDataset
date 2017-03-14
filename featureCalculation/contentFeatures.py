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
        max_urls = 0
        hashtags = 0
        max_hashtags = 0

        features[idDoc] = {}

        features[idDoc]["url_exist"] = 0
        features[idDoc]["url_count"] = 0
        features[idDoc]["hashtag_exist"] = 0
        features[idDoc]["hashtag_count"] = 0

        if mapping[idDoc]["type"] == "tweet":
            for tw in mapping[idDoc]["tweets"]:
                data = lookupTweet(int(tw))
             #   print(data)

                urls += len(data["entities"]["urls"])

                max_urls = max(urls,max_urls)

                hashtags += len(data["entities"]["hashtags"])

                max_hashtags = max(hashtags,max_hashtags)

            features[idDoc]["url_count"] = urls/max_urls

            if max_urls > 0 :
                features[idDoc]["url_exist"] = 1
                features[idDoc]["url_count"] = urls / max_urls

            if max_hashtags > 0:
                features[idDoc]["hashtag_exist"] = 1
                features[idDoc]["hashtag_count"] = hashtags / max_hashtags

    with open(path_features + repEvent + "/content.json", "w") as fout:
        json.dump(features, fout)
