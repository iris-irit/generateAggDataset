def lookupTweet(id,json_raw) :
	for j in json_raw :
		if j["id"] == id :
			return j