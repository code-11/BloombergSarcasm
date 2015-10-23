from textblob import TextBlob
from itertools import imap

import pprint

"""
Install Instructions
pip install textblob
python -m nltk.downloader
sudo pip install -U nltk

"""

"""
Sentiment pattern
Will extract a sentiment pattern from a string of words.
The pattern can look like many things as dictated by the options.
The default options result in a pattern simmilar to (-1,1,1,1,0 )
"""
def sentiment_pattern(text, gram_n=1):
	blob= TextBlob(text)
	ngrams=blob.ngrams(n=gram_n)
	sentiment_list=[]
	for gram in ngrams:
		str_gram=" ".join(gram)
		gram_blob=TextBlob(str_gram)
		sentiment=gram_blob.sentiment[0]
		if sentiment>0:
			sentiment=1
		elif sentiment<0:
			sentiment=-1
		sentiment_list.append(sentiment)

	return sentiment_list

def crush(pattern):
	if pattern==[]:
		return []
	else:
		last=pattern[0]
		crushed=[last]
		i=1
		while i<len(pattern):
			if pattern[i]!=last:
				crushed.append(pattern[i])
				last=pattern[i]
			i+=1
		return crushed

def neutral_exclude(pattern):
	return filter(lambda x: x !=0,pattern)

def check_cue_words(text):
	CUES=[
		"stupid",
		"shit",
		"oh",
		"yeah",
		"sure",
		"forget",
		"supposed",
		"dont waste your",
		"all of my",
		"go back to",
		"a pair of",
		"needless to say",
		"are looking",
		"!",
		"..."
	]
	return any(imap(text.lower().__contains__, CUES))

def check_patterns(text):
	PATTERNS={(1,-1),(-1,1),(-1,-1),(-1,0),(1,0,-1),(-1,0,1)}
	pattern=sentiment_pattern(text)
	crushed_pattern=tuple(crush(pattern))
	return crushed_pattern in PATTERNS	

def sarcasm_test(text):
	cues=check_cue_words(text)
	patterns=check_patterns(text)
	return cues or patterns


# text="I haven't had fun"
# blob=TextBlob(text)
# print(blob.sentiment)

# text="Absolutely mind blowing, pushing has never been so easy or so exciting. No doubt Apple will copy it on their 2018 iphones and tout it as the next big thing!"
text="Yeah, I definitely believe this is the best alarm app. It didn't wake me up three days in a row!!!"
print(sarcasm_test(text))