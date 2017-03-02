import pandas as pd
import json
import sys,os
import requests
import socket
import urllib.request



SEUIL = 100
csv_file = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/event_statistics.csv"

df = pd.read_csv(csv_file)
gb = pd.DataFrame(df.groupby("IdEvent").sum().reset_index())

listEventOk = []

for index, row in gb.iterrows() :
    if row["Tweets"] >= SEUIL :
        listEventOk.append(row["IdEvent"])

try :
    urllib.request.urlretrieve('http://www.toto.fr/test.png', 'test.png')
except urllib.error.HTTPError :
    print("404")
sys.exit()

"""
url404 = "https://twitter.com/WheresKernan/status/256925517494763520"
req = requests.get(url404,verify=False, timeout=5)
print(req.status_code)
print(req.history)
with open("test.html","w") as f : 
    f.write(req.content.decode('utf-8'))

sys.exit()
"""



#for eventId in listEventOk :
for eventId in [3] :
    mappingUrl = {}

    # Création du répertoire pour chaque évènement
    dir_data = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)
    dir_urls = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/urls/"
    dir_img = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/images/"
    dir_videos = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/videos/"
    os.system("rm -r "+dir_data)
    os.system("mkdir "+dir_data)
    os.system("mkdir " + dir_data+"/urls")
    os.system("mkdir " + dir_data+"/images")

    print("*********",eventId,"*********")
    # Lecture des fichiers json
    path_json = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/data_"+str(eventId)+".txt"
    f = open(path_json,"r")
    js = json.load(f)
    f.close()

    # Parcours des tweets pour chaque évènement
    for tw in js :
        if "entities" in tw :

            id_tweet = str(tw["id"])


            # On s'occupe du champ media (les images uploadees)
            if "media" in tw["entities"] :
                for m in tw["entities"]["media"] :
                    try:
                        urllib.request.urlretrieve(m["media_url"], dir_img+id_tweet+"_"+m["media_url"].split("/")[-1])
                    except urllib.error.HTTPError:
                        print("404")

                    sys.exit()

            # On s'occupe des entités (urls + images)
            if "urls" in tw["entities"] :
                for u in tw["entities"]["urls"] :
                    url = u["expanded_url"]
                    print("************************************")
                    print(url)
                    try :
                        req = requests.get(url,verify=False, timeout=5)

                        if req.status_code == 404 :
                            print("404")
                        print(req.status_code)
                        print(req.url)

                        mappingUrl.setdefault(req.url, [])
                        mappingUrl[req.url].append(id_tweet)
                        #print(req.content)
                    except requests.exceptions.Timeout :
                        print("socket.timeout")
                    except requests.exceptions.ConnectionError :
                        print("socket.gaierror")

    print(mappingUrl)
    sys.exit()