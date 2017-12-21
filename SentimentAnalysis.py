import re 
import string
import json
import random
import nltk
from positive import positive
from negative import negative
from intensifier import intensifier

def main():
	#dictionary for all the venues that are read
	venues = {}
	#how many totals user reviews to read
	toRead = 0
	#dictionary for all the restaurants
	restaurants = []
	#check to see if the business was a restaurant itself
	checkRestaurant(restaurants)

	#open the dataset, parse through reviews and only add reviews of venue to the dictionary if the text is not in german and the venue is a restaurant
	with open("dataset/review.json" , "r", encoding = "utf8") as json_file:
		for json_data in json_file:
			if (toRead < 1000):
				json_content = json.loads(json_data)

				if (not checkGerman(json_content["text"]) and json_content["business_id"] in restaurants):
					if (venues.get(json_content["business_id"]) == None):
						venues[json_content["business_id"]] = []

					# print(json_content["business_id"])
					# print(json_content["text"])
					# print(getEssence(json_content["text"]))
					# print("user: " + str(json_content["stars"]))
					# print("sentiment: " + str(sentimentAnalysis(getEssence(json_content["text"]))))
					# print("------------------------------------------------------------")
					venues[json_content["business_id"]].append([json_content["text"], json_content["stars"]])
					toRead+=1
			else:
				break

	totalYelpScore = 0
	totalUserScore = 0
	totalSentimentScore = 0
	for values in venues:
		yelpScore = 0
		userScore = 0
		sentimentScore = 0

		with open("dataset/business.json", "r", encoding = "utf8") as json_file:
			for json_data in json_file:
				json_content = json.loads(json_data)

				if (json_content["business_id"] == values):
					yelpScore = json_content["stars"]

		for ii in range(0, len(venues.get(values))):
			userScore+=venues.get(values)[ii][1]
			sentimentScore+=sentimentAnalysis(getEssence(venues.get(values)[ii][0]))
		userScore/=len(venues.get(values))
		sentimentScore/=len(venues.get(values))

		totalYelpScore+=yelpScore
		totalUserScore+=userScore
		totalSentimentScore+=sentimentScore
		print(yelpScore, userScore, sentimentScore)

	totalYelpScore/=len(venues)
	totalUserScore/=len(venues)
	totalSentimentScore/=len(venues)

	print("total:")
	print(totalYelpScore, totalUserScore, totalSentimentScore)
		

#takes the text of the review and only returns the nouns and adjectives in the text
def getEssence(text):
	text = nltk.word_tokenize(text)
	text = nltk.pos_tag(text)

	essence = []
	for line in text:
		if (line[1] == 'RB' or line[1] == 'RBR' or line[1] == 'RBS' or line[1] == 'JJ' or line[1] == 'JJR' or line[1] == 'JJS'): #line[1] == 'NNP' or line[1] == 'NNPS' or
			essence.append(line[0].lower())

	return essence

#checks to see if the review is in German by checking the most frequent words used in German
def checkGerman(text):
	text = nltk.word_tokenize(text)

	for line in text:
		if (line == "ist" or line == "es"):
			return 1

	return 0

#used to find all the restaurants in the dataset
def checkRestaurant(restaurants):
	with open("dataset/business.json", "r", encoding = "utf8") as json_file:
		for json_data in json_file:
			json_content = json.loads(json_data)

			# print(json_content["name"].encode("utf-8"))
			# print(json_content["categories"])

			for line in json_content["categories"]:
				if (line == "Restaurants"):
					restaurants.append(json_content["business_id"])

def sentimentAnalysis(text):
	if (len(text) == 0):
		return 0

	score = 0
	numberLines = 0
	toAdd = 1
	for line in text:
		if (line in positive):
			score+=toAdd
			toAdd = 1
		elif (line in negative):
			score-=toAdd
			toAdd = 1
		elif (line in intensifier):
			toAdd*=2
		elif (line == "not" or line == "n't"):
			toAdd*=-1
		else:
			toAdd += 0
			#print(line)

		numberLines+=1

	score/=numberLines
	score*=100
	if (score >= -100 and score < -60):
		return 1
	elif (score >= -60 and score < -20):
		return 2
	elif (score >= -20 and score < 20):
		return 3
	elif (score >= 20 and score < 60):
		return 4
	elif (score >= 60):
		return 5
	else:
		return 0

if __name__ == "__main__":
  main()