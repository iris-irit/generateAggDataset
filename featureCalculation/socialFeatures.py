import os
import json

path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"

name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"


for repEvent in os.listdir(path_events) :
	print(repEvent)
