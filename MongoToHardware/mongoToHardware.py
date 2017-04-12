from flask import Flask
from flask_pymongo import PyMongo
import pymongo, json
from bson import json_util
import sched, time
import bitly_api




app = Flask(__name__)
mongo = PyMongo(app)

uri = 'mongodb://heroku_6sbfpbmd:bok26mhnk5qipgihm3c78s5krf@ds131890.mlab.com:31890/heroku_6sbfpbmd'
connection = pymongo.MongoClient(uri)
db = connection['heroku_6sbfpbmd']
db.authenticate('heroku_6sbfpbmd','bok26mhnk5qipgihm3c78s5krf')


###### use for bitly thing #####
conn_btly = bitly_api.Connection(access_token='fe3a361216aa47a6a823a32613bba81ddf01cf29')

#get links
clicks = conn_btly.link_clicks('http://bit.ly/stc309test', rollup=False, unit='hour')

numberInAudience = clicks[0]["clicks"]
print numberInAudience
### use for bitly thing ###

starting_scores = {}

#checks if a reaction can go again
#this increases by one every 5 seconds. When haha is used at time 10 seconds
#haha's canReactDB value is 2. Haha must wait 30 seconds until it can go again
#aka repeatChecker value of 8
repeatChecker = 0
canReactDB = {}
waitUntil = repeatChecker
emojiDB = db.emoji.find()
for doc in emojiDB:
	starting_scores[doc["name"]] = doc["score"]
	canReactDB[doc["name"]] = -6


scores = {}
s = sched.scheduler(time.time, time.sleep)

def check_db(sc, repeatChecker, canReactDB, waitUntil):
	emojiDB = db.emoji.find()
	for doc in emojiDB:
		scores[doc["name"]] = doc["score"]
	print scores

	repeatChecker = repeatChecker + 1

	for score in scores:
		if (scores[score] >= starting_scores[score] + 5) and (repeatChecker - canReactDB[score] > 6) and (waitUntil <= repeatChecker):
			print "large change in " + score + " initiate the hardware!"
			canReactDB[score] = repeatChecker
			waitUntil = repeatChecker + 4
			#reset all scores
			for score in scores:
				starting_scores[score] = scores[score]
		elif (scores[score] >= starting_scores[score] + 5) and not (repeatChecker - canReactDB[score] > 6):
			starting_scores[score] = scores[score]
		elif (scores[score] >= starting_scores[score] + 5) and not (waitUntil <= repeatChecker):
			starting_scores[score] = scores[score]


			##poll - a percentage of audience, ##number of bitly access, bitly api?


	s.enter(5, 1, check_db, (sc,repeatChecker, canReactDB, waitUntil))

s.enter(5, 1, check_db, (s,repeatChecker, canReactDB, waitUntil))
s.run()

@app.route('/')
def home_page():
    online_users = db.users.find({'online': True})
    return render_template('index.html',
        online_users=online_users)



if __name__ == '__main__':
    app.run(debug = True)