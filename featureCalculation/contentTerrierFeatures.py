import os, sys
import json
import numpy as np


def findAppropriateFile(m,l):
	#print(m,l)
	for e in l :
		if e.startswith(m) and e.endswith(".res") :
			return e
	return None



def parseResultFile(fn):

	positive = True
	boundMin, boundMax = 0.0, 0.0
	res = {}

	# Get the first line to find if it is positive or not and init bound accordingly
	with open(fn,"r") as f :
		first_line = f.readline()
		t = first_line.split(" ")
		print(t)
		if len(t) > 1 :
			if float(t[4]) < 0 :
				positive = False
				boundMin = 0.0
				boundMax = -100000.0 # très sale

	with open(fn,"r") as f :
		for line in f :
			t = line.split(" ")
			if len(t) > 1 :
				idDoc = t[2]
				val = t[4]

				res[idDoc] = float(val)

				if float(val) > boundMax :
					boundMax = float(val)

				if not positive and float(val) < boundMin :
					boundMin = float(val)

		return (res,boundMin,boundMax,positive)



path_queries = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/queries_all_events.xml"
path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_index = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Index/indexTerrier/"
#path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/"


name_dir_mapping = "/mapping/mapping.json"
#name_dir_inverse = "/mapping/inverse.json"

features = {}

models = ["BB2","BM25","DFR_BM25","DLH", "DLH13", "DPH", "DFRee", "Hiemstra_LM", "IFB2","In_expB2", "In_expC2", "InL2", "LemurTF_IDF",
          "LGD", "PL2", "TF_IDF"]

events = os.listdir(path_events)

with open("pb.txt", 'w') as fpb:
	fpb.write("")


featPb = set()

for repEvent in os.listdir(path_events) :

	features = {}

	# initialisation de features avec tous les documents
	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	for idDoc in mapping:
		features.setdefault(idDoc,{x:0.0 for x in models})

	# On crée le répertoire pour stocker les features s'il n'xiste pas
	if not os.path.exists(path_features+repEvent) :
		os.mkdir(path_features+repEvent)

	# On cherche si les modèles ont été calculés (présence du répertoire results dans le répertoire d'index de l'évènement
	path_result_models = path_index+repEvent+"/results"
	if not os.path.exists(path_result_models) :
		continue


	fileModels = os.listdir(path_index+repEvent+"/results")

	for model in models :

		pb = False

		file = findAppropriateFile(model,fileModels)
		res,boundMin, boundMax, positive = parseResultFile(path_index+repEvent+"/results/"+file)
		if not positive :
			print(res,boundMin, boundMax, positive)

		for idDoc in res :
			val = 0.0
			if positive and boundMax > 0.0:
				val = res[idDoc] / boundMax
			elif not positive :
				 val = 1 - (res[idDoc] / boundMin) + (boundMax/boundMin)

			features[idDoc][model] = val

			if val < 0.0 :
				pb = True

		if pb :
			featPb.add(model)
			with open("pb.txt", 'a') as fpb :
				fpb.write(model+" in event "+repEvent+"\n")



	with open(path_features+repEvent+"/terrier.json", "w") as fout :
		json.dump(features,fout)

print(featPb)



