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

UNITED_STATES=143441

def get_reviews(result):
	the_id=result.get_id()
	reviews=app_look.getReviews(UNITED_STATES,the_id,maxReviews=1)
	return reviews 

pp = pprint.PrettyPrinter(indent=4)
apps = itunes.search(query='strategy games', media='software')
app=apps[0]
pp.pprint(get_reviews(app))
# print(dir(itunes))
# the_id=app.get_id()
# print(app_look.getReviews(143441,the_id,maxReviews=100))