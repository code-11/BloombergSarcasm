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
import json
import urllib2

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

pp = pprint.PrettyPrinter(indent=4)


csvfile=open('sarcastic_reviews.csv', 'wb')
fieldnames = ['app_id','app_name','rating','review_title','username','price','category']
writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
writer.writerow(fieldnames)

for app_num in SARCASTIC_APP_NUMS:

	reviews_str=urllib2.urlopen("https://itunes.apple.com/rss/customerreviews/id="+str(app_num)+"/json").read()
	json_dic=json.loads(reviews_str)
	reviews_and_meta=json_dic["feed"]["entry"]

	#First entry should contain metadata about app itself.
	possible_meta=reviews_and_meta[0]
	category=possible_meta["category"]["attributes"]["label"].encode('utf-8')
	name=possible_meta["im:name"]["label"].encode('utf-8')

	#can be in things other than USD
	price=possible_meta["im:price"]["attributes"]["amount"].encode('utf-8')
	reviews=reviews_and_meta[1:]
	for review in reviews:
		username=review["author"]["name"]["label"].encode('utf-8')
		review_text=review["content"]["label"].encode('utf-8')
		rating=review["im:rating"]["label"].encode('utf-8')
		title=review["title"]["label"].encode('utf-8')
		writer.writerow([app_num,name,rating,title,username,price,category])