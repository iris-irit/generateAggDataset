import os, sys
import json
from lxml import etree
import pyndri
import numpy as np


#def lookupTweet(id) :
#	for j in json_raw :
#		if j["id"] == id :
#			return j


path_queries = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/queries_all_events.xml"
path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_index = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Index/index/"
#path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/"


#name_dir_mapping = "/mapping/mapping.json"
#name_dir_inverse = "/mapping/inverse.json"

features = {}

events = os.listdir(path_events)

tree = etree.parse(path_queries)
for q in tree.xpath("/parameters/query"):
	tobedone = "false"
	for element in q.iter():
		#print("%s - %s" % (element.tag, element.text))
		# si la requete fait partie des requetes à tester, on doit lancer Indri
		if (element.tag=="number") and (element.text in events):
			tobedone="true"
			query = element.text
		if (element.tag=="text") and tobedone=="true":
			print("----------------"+element.text )
			with pyndri.open(path_index+query) as index:
				features = {}
				num_documents=0
				for document_id in range(index.document_base(), index.maximum_document()):
					num_documents += 1
					ext_document_id, _ = index.document(document_id)
					features[ext_document_id] = {}
					features[ext_document_id]["lm"] = 0
					features[ext_document_id]["tfidf"] = 0
					features[ext_document_id]["bm25"] = 0


				# Constructs a QueryEnvironment that uses a
				# language model with Dirichlet smoothing.
				lm_query_env = pyndri.QueryEnvironment(index, rules=('method:dirichlet,mu:5000',))
				#results = lm_query_env.query(element.text, results_requested=num_documents, include_snippets=True)
				results = lm_query_env.query(element.text, results_requested=num_documents)
				minscore=0
				maxscore = - np.inf
				for int_document_id, score in results:
					ext_document_id, _ = index.document(int_document_id)
					if score< minscore:
						minscore=score
					if score > maxscore:
						maxscore = score
					#print('Document {ext_document_id} retrieved with score {score}, snippet : {snippet}.'.format(ext_document_id=ext_document_id, score=score, snippet=snippet))
					print('Document {ext_document_id} retrieved with score {score}.'.format(ext_document_id=ext_document_id, score=score))
					features[ext_document_id]["lm"] = score
					#print()
				print(str(len(results))+" / "+str(num_documents))

				# Constructs a QueryEnvironment that uses the TF-IDF retrieval model.
				#
				# See "Baseline (non-LM) retrieval"
				# (https://lemurproject.org/doxygen/lemur/html/IndriRunQuery.html)
				tfidf_query_env = pyndri.TFIDFQueryEnvironment(index)
				resultstfidf = tfidf_query_env.query(element.text, results_requested=num_documents)
				maxscoretf = 0
				for int_document_id, score in resultstfidf:
					ext_document_id, _ = index.document(int_document_id)
					if score > maxscoretf:
						maxscoretf = score
					#print('Document {ext_document_id} retrieved with score {score}, snippet : {snippet}.'.format(ext_document_id=ext_document_id, score=score, snippet=snippet))
					print('Document {ext_document_id} retrieved with score {score}.'.format(ext_document_id=ext_document_id, score=score))
					features[ext_document_id]["tfidf"] = score
					#print()
				print(str(len(results))+" / "+str(num_documents))

				# Constructs a QueryEnvironment that uses the Okapi BM25 retrieval model.
				#See "Baseline (non-LM) retrieval"
				#(https://lemurproject.org/doxygen/lemur/html/IndriRunQuery.html)
				bm25_query_env = pyndri.OkapiQueryEnvironment(index)
				resultsbm = bm25_query_env.query(element.text, results_requested=num_documents)
				maxscorebm25 = 0
				for int_document_id, score in resultsbm:
					ext_document_id, _ = index.document(int_document_id)
					if score > maxscorebm25:
						maxscorebm25 = score
					#print('Document {ext_document_id} retrieved with score {score}, snippet : {snippet}.'.format(ext_document_id=ext_document_id, score=score, snippet=snippet))
					print('Document {ext_document_id} retrieved with score {score}.'.format(ext_document_id=ext_document_id, score=score))
					features[ext_document_id]["bm25"] = score
					#print()
				print(str(len(results))+" / "+str(num_documents))



				for doc in features:
					#print (doc + " - " +str(features[doc]["lm"]))
					if (features[doc]["lm"]!=0):
						features[doc]["lm"] = 1 - (features[doc]["lm"]/minscore) + maxscore/minscore
					if (features[doc]["tfidf"]>0):
						features[doc]["tfidf"] = features[doc]["tfidf"]/maxscoretf
					if (features[doc]["bm25"]>0):
						features[doc]["bm25"] = features[doc]["bm25"]/maxscorebm25

				with open(path_features+query+"/indri.json", "w") as fout :
					json.dump(features,fout)

		# Constructs a QueryEnvironment that uses the TF-IDF retrieval model.
		#
		# See "Baseline (non-LM) retrieval"
		# (https://lemurproject.org/doxygen/lemur/html/IndriRunQuery.html)
		# tfidf_query_env = pyndri.TFIDFQueryEnvironment(index)
		# print(tfidf_query_env.query('hello world'))

		# # Constructs a QueryEnvironment that uses the Okapi BM25 retrieval model.
		# #
		# # See "Baseline (non-LM) retrieval"
		# # (https://lemurproject.org/doxygen/lemur/html/IndriRunQuery.html)
		# bm25_query_env = pyndri.OkapiQueryEnvironment(index)
		# print(bm25_query_env.query('hello world'))





# for repEvent in os.listdir(path_events) :
# 	json_raw = {}
# 	mapping = {}
# 	inverse = {}

# 	if not os.path.exists(path_features+repEvent) :
# 		os.mkdir(path_features+repEvent)

# 	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
# 		json_raw = json.load(fjson)

# 	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
# 		mapping = json.load(fjson)

# 	with open(path_events+repEvent+name_dir_inverse, "r") as fjson :
# 		inverse = json.load(fjson)

# 	for idDoc in mapping :

# 		favourites = 0
# 		retweets = 0
# 		followers = 0

# 		features[idDoc] = {}

# 		for tw in mapping[idDoc]["tweets"] :
# 			data = lookupTweet(int(tw))
# 			print(data)

# 			favourites += data["favorite_count"]
# 			retweets += data["retweet_count"]
# 			followers += data["user"]["followers_count"]

# 		features[idDoc]["favorite_count"] = favourites
# 		features[idDoc]["retweet_count"] = retweets
# 		features[idDoc]["followers_count"] = followers

# 	with open(path_features+repEvent+"/social.json", "w") as fout :
# 		json.dump(features,fout)