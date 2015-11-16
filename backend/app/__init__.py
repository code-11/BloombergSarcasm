import httplib, urllib, json
import os
import flask, flask.views
from flask import Markup
from flask import jsonify
import cPickle, dill
import truerating
from samr.predictor import PhraseSentimentPredictor
import nltk


app = flask.Flask(__name__)
predictor = cPickle.load(open("./app/predictor.pickle","rb"))
MIN_CORPORA = [
	'brown',  # Required for FastNPExtractor
	'punkt',  # Required for WordTokenizer
	'wordnet',  # Required for lemmatization
	'averaged_perceptron_tagger',  # Required for NLTKTagger
]

for each in MIN_CORPORA:
	nltk.download(each)


class Main(flask.views.MethodView):
	def get(self):
		return flask.render_template('index.html')
	

class About(flask.views.MethodView):
	def get(self):
		return flask.render_template('about.html')
	
class Contact(flask.views.MethodView):
	def get(self):
		return flask.render_template('contact.html')   

app.add_url_rule('/',view_func=Main.as_view('main'), methods=["GET"])
app.add_url_rule('/about/',view_func=About.as_view('about'), methods=["GET"])
app.add_url_rule('/contact/',view_func=Contact.as_view('contact'), methods=["GET"])


@app.route('/rating')
def compute():
	query = flask.request.args.get('q')
	q = json.loads(query)
	r = {}
	r['rating'] = []
	for i in q['id']:
		connection = httplib.HTTPConnection('itunes.apple.com')
		reviews = []
		for j in range(1, 2):
			connection.request('GET', '/rss/customerreviews/page=' + str(j) + '/id=' + str(i) +'/json')
			response = connection.getresponse()
			try:
				t = json.loads(response.read().decode("utf8"))
				for x in t["feed"]["entry"][1:]:
					if "content" in x:
						reviews.append(x["content"]["label"])
						if len(reviews) > 20:
							break
			except:
				continue
			
			
			
			
		r['rating'].append(truerating.sentiment_reviews(reviews, predictor = predictor))

	
	return jsonify(r)
	
