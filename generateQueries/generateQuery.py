from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os

tokenizer = RegexpTokenizer(r'\w+')



# Récuperer le fichier contenant les sujets
path_event_description = "/projets/iris/CORPUS/DOCS/TWITTER_EVENTS_2012/Events2012/event_descriptions.tsv"
path_queries = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/queries_all_events.xml"


if os.path.isfile(path_queries) :
	os.remove(path_queries)

queries = {}

def word_feats(words):
	tokenizer = RegexpTokenizer(r'\w+')
	t = tokenizer.tokenize(words.lower())
	return [word for word in t if word not in stopset]

stopset = list(set(stopwords.words('english')))
morewords = 'tweet', 'tweets', 'discuss', 'discussing', 'many', 'u', 'discussa'
stopset.extend(morewords)




# Lecture du fichier
with open(path_event_description, "r") as f :
	for line in f :
		tab = line.strip().split("\t")
		id_event = tab[0]
		raw_text = tab[1]

		res = word_feats(raw_text)
		print(res)

		with open(path_queries, "a") as f:
			f.write("<top>\n<num>"+id_event+"</num>\n"
			                                "<title>"+' '.join(res)+"</title>\n"
			                                "<desc>"+raw_text+"</desc>\n"
			                                "<narr></narr>\n</top>\n")




