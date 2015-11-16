from textblob import TextBlob
import math
from samr.data import Datapoint

def sentiment_reviews(reviews, gram_n=5, predictor=None):
	datalist = []

	tag = []
	counttag = [0] * len(reviews)
	for (i, review) in enumerate(reviews):
		blob = TextBlob(review)
		ngrams=blob.ngrams(n=min(gram_n, len(blob.words)))
		
		for gram in ngrams:
			str_gram=" ".join(gram)
			data = (0, 0, str_gram, None)
			datalist.append(Datapoint(*data))
			tag.append(i)
			counttag[i] += 1

	print "start prediction"

	prediction = predictor.predict(datalist)

	cstm = [[0] * 5 for x in reviews]
	for (i, sentiment) in enumerate(prediction):
		sentiment = int(sentiment)
		cstm[tag[i]][sentiment] += 1.0 / counttag[tag[i]]

	trating = 0.0
	tcount = 0.0

	for i in range(len(reviews)):
		if counttag[i] == 0:
			continue
			
		cstm[i][2] = cstm[i][2] / math.pow(counttag[i], 0.44)
		cstm[i][0] = cstm[i][0] * math.pow(counttag[i], 0.22)
		cstm[i][3] = cstm[i][3] * math.pow(counttag[i], 0.22)
		rating = 0.0
		count = 0.0
		for j in range(5):
			rating += (j + 1) * cstm[i][j]
			count += cstm[i][j]

		print cstm[i], " ", counttag[i]

		t = 1 / (1 + math.exp(-(cstm[i][2] / count - 0.45) * 15))
		print cstm[i][2] / count
		trating += rating / count * (1 - t)
		tcount += 1 - t

	trating = trating / tcount
	if trating > 3:
		x = trating - 3
		x = math.pow(x, 0.4647) * 1.4492
		return x + 3
	else:
		x = 3 - trating
		x = math.pow(x, 0.4647) * 1.4492
		return 3 - x
