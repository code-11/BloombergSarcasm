"""
Sarcasm Finder (itunes app review scraper)

To Install, need the following:
	-This code (presumably obtained by now)
	-easy_install python-itunes
	-sudo easy_install elementtree
 	-sudo easy_install argparse
Github taken from:
	https://github.com/ocelma/python-itunes
	https://github.com/grych/AppStoreReviews
"""

#Note ids are sparse so we can't just iterate through them

import itunes
import AppStoreReviews as app_look
import pprint
import csv

UNITED_STATES=143441

SARCASTIC_APP_NUMS=[
	834335592,
	336536208,
	929779844,
	423942748,
	788438899,
	376919110,
	297048779,
	522273825,
	907037398,
	564226056,
	321586038,
	294785375,
	317367752,
	284963359,
	547160634,
	346204860
]


def get_reviews(result):
	the_id=result.get_id()
	reviews=app_look.getReviews(UNITED_STATES,the_id,maxReviews=1)
	return reviews 

pp = pprint.PrettyPrinter(indent=4)


csvfile=open('sarcastic_reviews.csv', 'wb')
fieldnames = ['id','rank', 'review','topic','user','version']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

for app_num in SARCASTIC_APP_NUMS:
	reviews=app_look.getReviews(UNITED_STATES,app_num,maxReviews=-1)
	for review in reviews:
		review["id"]=app_num
		writer.writerow(dict((k, v.encode('utf-8') if type(v) is unicode else v) for k, v in review.iteritems()))
	print(app_num)


# apps = itunes.search(query='strategy games', media='software')
# app=apps[0]
# pp.pprint(get_reviews(app))

# reviews=app_look.getReviews(UNITED_STATES,834335592,maxReviews=1)
# pp.pprint(reviews)

# print(dir(itunes))
# the_id=app.get_id()
# print(app_look.getReviews(143441,the_id,maxReviews=100))