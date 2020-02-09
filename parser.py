import os 
import pandas as pd 
import json
from pandas.io.json import json_normalize 
import numpy as np
import nltk
#from stopwordsnltk.corpus import 
from nltk.corpus import stopwords
set(stopwords.words('english'))
from nltk.tokenize import word_tokenize 
from collections import Counter 
from nltk.tokenize import RegexpTokenizer
from datetime import datetime
from random import seed 
from random import randint
seed(1)

facebook_dir = "/Users/marissadalonzo/Downloads/facebook-marissadalonzo/"
folders = os.listdir(facebook_dir)
fp = open("listfile.txt", "w")

data = []
for folder in folders: 
	if folder == "comments":
		with open(facebook_dir + folder + "/comments.json") as data_file:    
			temp = json.load(data_file)
		df = json_normalize(temp, u"comments", [u'timestamp',  u'title', u"data", u"comment", u"group"],  record_prefix='data_', errors='ignore')
		df2 = df["data_data"].dropna().values
		comments = []
		for x in range(0, len(df2)):
			comments.extend([df2[x][0]["comment"]["comment"]])

		fp.write("You have commented on " + str(len(df2)) + " posts.\n")
	
		stop_words = set(stopwords.words('english'))
		filtered = []
		tokenizer = RegexpTokenizer(r'\w+')
		#comment = comment.encode('ascii','ignore')
		temp = [x for x in comments if x.lower() != "u"]
		temp = [x for x in temp if not x.lower() in stop_words]
		for x in temp:
			x = word_tokenize(x)
			x = tokenizer.tokenize(str(x))
			x = [a for a in x if a.lower() != "u"]
			x = [a for a in x if not a.lower() in stop_words]
			filtered.extend(x)

		occurence_count = Counter(filtered) 
		fp.write("You tagged " + str(occurence_count.most_common(1)[0][0]) + " in the most posts.\n")

		titles = df["data_title"].values
		new_stopwords = ["commented", "post", "video", "timeline", "comment", "photo", "replied", "own"]

		filtered = []

		seperator =","
		for title in titles:
			x = word_tokenize(title)
			x = tokenizer.tokenize(str(title.encode('ascii', 'ignore')))

			x= [a for a in x[2:] if not a.lower() in stop_words]

			x = [a for a in x[2:] if not a.lower() in new_stopwords]
			x = seperator.join(x) 
			if x != '':
				filtered.append(x)

		occurence_count = Counter(filtered) 
		most = occurence_count.most_common(1)[0][0]
		test_string = most.replace(",", ' ') 
		fp.write("You commented on " + test_string + "'s page the most.\n")

		first = filtered[-1]
		first= first.replace(",", ' ') 
		fp.write("The first person's page you commented on was: " + str(first) + ".\n")

		last = filtered[0]
		fp.write(str(last) + " was the most recent page you commented on. \n")

	if folder == "likes_and_reactions": 
		with open(facebook_dir + folder + "/posts_and_comments.json") as data_file:    
			temp = json.load(data_file)

		df = json_normalize(temp, u"reactions", [u'timestamp', u"data"],  record_prefix='data_', errors='ignore')
		reactions = df["data_title"].dropna().values
		fp.write("You have reacted to " + str(len(reactions)) + " posts.\n")

		new_stopwords = ["commented", "post", "video", "timeline", "likes", "photo", "replied", "own"]

		filtered = []

		seperator =","
		for reaction in reactions:
			x = word_tokenize(reaction)
			x = tokenizer.tokenize(str(reaction.encode('ascii', 'ignore')))
			x= [a for a in x[2:] if not a.lower() in stop_words]
			x = [a for a in x[2:] if not a.lower() in new_stopwords]
			x = seperator.join(x) 
			if x != '':
				filtered.append(x)

		occurence_count = Counter(filtered) 
		most = occurence_count.most_common(1)[0][0]
		test_string = most.replace(",", ' ') 
		fp.write("You reacted to  " + test_string + " the most.\n")
		

		first = filtered[-1]
		first= first.replace(",", ' ') 
		fp.write("The first person's post you liked was " + str(first) + ".\n")

		last = filtered[0]
		last= last.replace(",", ' ') 
		fp.write(str(last) + " was the most recent post you reacted to.\n")

	if folder == "messages": 
		people = os.listdir(facebook_dir + folder + "/inbox/")
		num_messages = []
		count = 0 
		for person in people: 
			if person != ".DS_Store" :
				with open(facebook_dir + folder +  "/inbox/"+ person + "/message_1.json") as data_file:    
					temp = json.load(data_file)
				num_messages.append(len(temp["messages"]))
			else: 
				num_messages.append(0)
		df = pd.DataFrame({'person' : people, "num_messages" : num_messages})
		x = df.loc[df['num_messages'].idxmax()]
		most = x["person"].split("_")
		fp.write("You messaged " + str(most[0]) + " the most over Facebook Messenger.\n")
	
	if folder == "events":
		with open(facebook_dir + folder + "/your_event_responses.json") as data_file:    
			temp = json.load(data_file)
			declines = temp[u'event_responses'][u'events_declined']
			event = declines[randint(0, len(declines)-1)]

			fp.write("You declined to attend " + event[u'name']  +" on "  + str(datetime.fromtimestamp(event[u'start_timestamp'])) + ".\n")
	
	if folder == "location":
		df = pd.read_json(facebook_dir + folder  + "/location_history.json")
		temp = df.values
		locations = []
		for x in range(0, len(temp)):
			locations.extend([temp[x][0][u'name']])

		occurence_count = Counter(locations) 
		most = occurence_count.most_common(1)[0][0]
		test_string = most.replace("u'", '') 
		fp.write("You spent the most time in " + test_string + ".\n")
		

		random = temp[randint(0, len(temp)-1)]
		fp.write("You visited " + str(random[0][u"name"]) + " on "  + str(datetime.fromtimestamp(random[0][u'creation_timestamp'])) + ".\n")

		first = temp[-1]
		fp.write("The first place you visited with your Facebook location on was " + first[0][u'name'] + " on "  + str(datetime.fromtimestamp(first[0][u'creation_timestamp'])) + ".\n")
		
		last = temp[0]
		fp.write("The most recent place you visited before your data was downloaded was " + last[0][u'name'] + " on "  + str(datetime.fromtimestamp(last[0][u'creation_timestamp'])) + ".\n")


	if folder == "payment_history": 
		with open(facebook_dir + folder + "/payment_history.json") as data_file:    
			temp = json.load(data_file)
		fp.write("You sent " + str(temp[u'payments'][ u'payments'][0][u'amount']) + " to " + temp[u'payments'][ u'payments'][0][ u'receiver'] + " on " + str(datetime.fromtimestamp(temp[u'payments'][ u'payments'][0][u'created_timestamp'])) + ".\n")


