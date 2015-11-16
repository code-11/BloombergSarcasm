import httplib, urllib, json
import os
import flask, flask.views
from flask import Markup
from flask import jsonify

app = flask.Flask(__name__)

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


@app.route('/search')
def compute():
	query = flask.request.args.get('q')
	connection = httplib.HTTPConnection('itunes.apple.com')
	r = {}
	r['term'] = query
	r['media'] = 'software'
	r['limit'] = 5
	connection.request('GET', '/search?' + urllib.urlencode(r))
	response = connection.getresponse()
	t = json.loads(response.read().decode('utf-8'))

	newt = {}
	newt['resultCount'] = t['resultCount']
	newt['results'] = []
	for i in t['results']:
		f = open("xxx.txt","w")
		f.write(str(i) + "\n")

		tt = {}
		tt['trackName'] = i['trackName']
		tt['description'] = i['description']
		tt['artistName'] = i['artistName']
		if 'averageUserRating' in i:
			tt['averageUserRating'] = i['averageUserRating']
		if 'averageUserRatingForCurrentVersion' in i:
			tt['averageUserRating'] = i['averageUserRatingForCurrentVersion']
		newt['results'].append(tt)

	connection = httplib.HTTPConnection('trueratr-backend2.herokuapp.com')
	appids = {}
	appids['id'] = []
	for i in t['results']:
		appids['id'].append(i['trackId'])

	connection.request('GET', '/rating?q=' + urllib.quote_plus(flask.json.dumps(appids)))
	print flask.json.dumps(appids)
	response = connection.getresponse()
	t2 = json.loads(response.read().decode('utf-8'))

	for (i, j) in zip(newt['results'], t2['rating']):
		i['trueRating'] = j

	resp = jsonify(newt)
	resp.headers['Access-Control-Allow-Origin'] = "*"
	return resp
	
