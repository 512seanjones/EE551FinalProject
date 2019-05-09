import praw
import matplotlib.pyplot as plt
import pandas as pd

# Grab potentials from prediction run
prediction = pd.read_csv("prediction_list.csv")
past_potential = prediction["potential"]
past_id = prediction["id"]

reddit = praw.Reddit(client_id='xDcIT_gIctwdIw',
                     client_secret='-TUJPRH9eQhhO64Q29nJV_FTc74',
                     user_agent='pythonee551')

subreddit = reddit.subreddit('politics')

# To check if any predictions made it to hot
hot_subreddit = subreddit.hot(limit=25)
hot_dict = {"id":[], "score":[]}

# See what new scores are and analyze trends
new_subreddit = subreddit.new(limit=1000)
new_dict = {"id":[], "score":[]}


for submission in hot_subreddit:
	hot_dict["id"].append(submission.id)
	hot_dict["score"].append(submission.score)

hot_data = pd.DataFrame(hot_dict)

for submission in new_subreddit:
	new_dict["id"].append(submission.id)
	new_dict["score"].append(submission.score)

new_data = pd.DataFrame(new_dict)

# check if any of my top ten predictions made it to hot
count = 0
for i in range(10):
	if past_id[i] in hot_dict["id"]:
		print("Post made it to hot!")
		print("Prediction order: " + str(i + 1))
		print("Id: " + str(past_id[i]))
		print("Score: " + str(hot_data.loc[i, "score"]))
		print("Had potential of " + str(past_potential[i]))
		count += 1
print(str(count) + " of my top 10 predictions made it to the top 25 of hot\n")

x_val = []
y_val = []

for i in range(len(past_id)):
	row = new_data[new_data["id"] == past_id[i]]
	if row.empty == False:
		x_val.append(past_potential[i])
		y_val.append(row.iloc[0]['score'])

# used to track how the scores relate to the potential
plt.plot(x_val, y_val, 'bo')
plt.xlabel("potential")
plt.ylabel("score")
try:
	plt.show()
except(KeyboardInterrupt):
	print("Goodbye")