from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os

# Récuperer le fichier contenant les sujets
path_event_description = "/projets/iris/CORPUS/DOCS/TWITTER_EVENTS_2012/Events2012/event_descriptions.tsv"
path_queries = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/queries_all_events.xml"
path_queries_terrier = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/Terrier/"
cmd_terrier = "/projets/iris/PROJETS/PRINCESS/TournAgg/Code/Soft/terrier-4.2/bin/trec_terrier.sh -r -Dterrier.var=/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Index/indexTerrier/2 -Dtrec.model=DFR_BM25 -Dtrec.topics=/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/Terrier/2.xml"


if os.path.isfile(path_queries):
	os.remove(path_queries)


if os.path.isfile(path_queries_terrier):
	os.remove(path_queries)

os.system("mkdir "+path_queries_terrier)

queries = {}


models = ["BB2","BM25","DFR_BM25","DLH", "DLH13", "DPH", "DFRee", "Hiemstra_LM", "IFB2","In_expB2", "In_expC2", "InL2", "LemurTF_IDF",
          "LGD", "PL2", "TF_IDF", "DFRWeightingModel"]


def word_feats(words):
	tokenizer = RegexpTokenizer(r'\w+')
	t = tokenizer.tokenize(words.lower())
	return [word for word in t if word not in stopset]


stopset = list(set(stopwords.words('english')))
morewords = 'tweet', 'tweets', 'discuss', 'discussing', 'many', 'u', 'discussa'
stopset.extend(morewords)

with open(path_queries, "a") as f:
	f.write("<parameters>\n")

# Lecture du fichier
with open(path_event_description, "r") as f:
	for line in f:
		tab = line.strip().split("\t")
		id_event = tab[0]
		raw_text = tab[1]

		res = word_feats(raw_text)
		print(res)

		with open(path_queries, "a") as fin:
			fin.write("<query>\n<number>" + id_event + "</number>\n"
			                                         "<text>" + ' '.join(res) + "</text>\n</query>\n")

		with open(path_queries_terrier+id_event+".xml", "w") as fTerrier :
			fTerrier.write("<top>\n"
			               "\n"
			               "<num>Number: "+id_event+"\n"
			               "<title> "+' '.join(res)+"\n"
			               "\n"
			               "</top>\n"
			)

		for model in models :
			cmd = cmd_terrier+" -Dterrier.var=/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Index/indexTerrier/"+id_event+" -Dtrec.model="+model+" -Dtrec.topics=/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/Terrier/"+id_event+".xml"
			os.system(cmd)


with open(path_queries, "a") as f:
	f.write("</parameters>\n")
