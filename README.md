README for TrueRatr, a sarcasm correcting sentiment powered web rating system for apple store apps.

Ignore all other READMEs, this one is authoritative.

FRONT END
Repo: https://github.com/kshreyas91/trueratr

The important files are:

	trueratr.html- Landing page

	searchlisting.html- Which has most of the communication logic with the server as well as how to display the received information.

	assets/main.css- Handles some of the custom css

	assets/materialize.css- Handles most of the default, pretty css

	search_listing/css/materialize.css- Handles the rest of the custom css

BACK END
Repo: https://github.com/code-11/BloombergSarcasm

The important files are:

	backend/app/__init__.py - The main file for the backend. Has all the routes for the http requests. If you want to modify what gets returned, you would probably want to do it here. Also where we get the information about the app from ituens and where we respond to the front end's request.

	backend/app/truerating.py - Actually performs the model on the input data and generates the true rating

	trueratr/app/appstore.py - UNUSED but one way of getting the reviews from the apple store. Can switch to this is our current way fails, since this is just a scraper.



MODEL
	sentinet/sentiment_analysis.py - How we tested and refined the model. It can do cross validation or run against the test data depending on whats commented out. Uses pickle files to shorten runtime but may lead to unexpected behavior if the pickle files are out of date / missing. Most of the other stuff in this folder is not used. This is the file we generated our F1 score with.
