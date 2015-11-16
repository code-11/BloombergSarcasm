"""
Generate a tsv submission file to kaggle's 'Sentiment Analysis on Movie Reviews' (samr)
competition using the samr module with a given json configuration file.
"""

import pickle
import dill

def fix_json_dict(config):
    new = {}
    for key, value in config.items():
        if isinstance(value, dict):
            value = fix_json_dict(value)
        elif isinstance(value, str):
            if value == "true":
                value = True
            elif value == "false":
                value = False
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
        new[key] = value
    return new


if __name__ == "__main__":
    import argparse
    import json
    import csv
    import sys

    from samr.corpus import iter_corpus, iter_test_corpus, iter_test2_corpus
    from samr.predictor import PhraseSentimentPredictor

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename")
    config = parser.parse_args()
    config = json.load(open(config.filename))

    print "Building the Predictor"

    #predictor = PhraseSentimentPredictor(**config)
    #predictor.fit(list(iter_corpus()))

    predictor = pickle.load(open("predictor.pickle", "rb" ) )

    test = list(iter_test_corpus())
    test2 = list(iter_test2_corpus())

    print "Start to Predict"

    prediction = predictor.predict(test2)

    writer = csv.writer(sys.stdout)
    writer.writerow(("PhraseId", "Sentiment"))
    for datapoint, sentiment in zip(test2, prediction):
        print sentiment
        #writer.writerow((datapoint.phraseid, sentiment))
