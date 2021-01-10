import csv

def lottery(id, user_prediction):
	def checklottery(id):
		with open('../OnlineNewsPopularity.csv', newline='') as csvfile:
			articles = csv.reader(csvfile, delimiter=' ', quotechar='|')
			i=0
			for currentArticle in articles:
				if i == id:
					article = currentArticle
					break
				else:
					i+=1
			shares = int(article[-1])
			print(shares)
			return shares > 1400


	return checklottery(id) == user_prediction

print(lottery(3, True))