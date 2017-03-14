def lookupTweet(id) :
	for j in json_raw :
		if j["id"] == id :
			return j