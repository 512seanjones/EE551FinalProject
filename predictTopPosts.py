import praw
import pandas as pd
import datetime as dt
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist

def get_date(created):
	return dt.datetime.fromtimestamp(created)

stop_words = ["to", "s", "of", "a", "for", "on", "is", "in", "and", "the", "t", "he", "his", "i", "be" ,"if", "that", "r"]

reddit = praw.Reddit(client_id='********', #hidden on github
                     client_secret='*********', #hidden on github
                     user_agent='pythonee551')

subreddit = reddit.subreddit('politics')

hot_subreddit = subreddit.hot() # grabs top 100
new_subreddit = subreddit.new(limit=1000)

hot_dict = { "title":[], \
             "score":[], \
             "id":[], \
             "comms_num":[], \
             "created": []}

new_dict = { "title":[], \
             "score":[], \
             "id":[], \
             "comms_num":[], \
             "created": []}

# trying to use most recent posts, less than 1 day old
for submission in hot_subreddit:
	if dt.datetime.now() - get_date(submission.created) < dt.timedelta(days=1):
	    hot_dict["title"].append(submission.title)
	    hot_dict["score"].append(submission.score)
	    hot_dict["id"].append(submission.id)
	    hot_dict["comms_num"].append(submission.num_comments)
	    hot_dict["created"].append(get_date(submission.created))

hot_data = pd.DataFrame(hot_dict)

tokenizer = RegexpTokenizer(r'\w+')
hot_tokens = []

# find most popular words
for title in hot_dict["title"]:
	hot_toks = tokenizer.tokenize(title)
	hot_toks = [t.lower() for t in hot_toks if t.lower() not in stop_words]
	hot_tokens.extend(hot_toks)

# find frequency of these words
hot_freq = FreqDist(hot_tokens)

# only look at posts that have not become popular yet, < 1000 upvotes
for submission in new_subreddit:
	if submission.score < 1000:
	    new_dict["title"].append(submission.title)
	    new_dict["score"].append(submission.score)
	    new_dict["id"].append(submission.id)
	    new_dict["comms_num"].append(submission.num_comments)
	    new_dict["created"].append(get_date(submission.created))

new_data = pd.DataFrame(new_dict)
new_dict["potential"] = []

# compare words from hot posts to new posts
for row in new_data.index:
	pot_score = 0
	for tok in hot_tokens:
		if tok in new_data.loc[row, "title"]:
			# rn just add the frequency of the words to find potential
			# most popular words have highest weight
			pot_score += hot_freq[tok]
	new_dict["potential"].append(pot_score)

# sort by highest potential and put in readable format
new_data = pd.DataFrame(new_dict)
sorted_data = new_data.sort_values(by=["potential"], ascending=False)
sorted_data.to_csv('prediction_list.csv', index=False, encoding='utf-8')
