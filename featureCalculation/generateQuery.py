from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')



# Récuperer le fichier contenant les sujets
path_event_description = "/projets/iris/CORPUS/DOCS/TWITTER_EVENTS_2012/Events2012/event_descriptions.tsv"
path_queries = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Queries/queries_all_events.xml"


queries = {}

def word_feats(words):
	tokenizer = RegexpTokenizer(r'\w+')
	t = tokenizer.tokenize(words)
	return dict([(word, True) for word in t if word not in stopset])

stopset = list(set(stopwords.words('english')))
morewords = 'tweet', 'tweets'
stopset.append(morewords)

# Lecture du fichier
with open(path_event_description, "r") as f :
	for line in f :
		tab = line.strip().split("\t")
		id_event = tab[0]
		raw_text = tab[1]

		res = word_feats(raw_text)
		print(res)




