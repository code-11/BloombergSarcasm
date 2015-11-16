import csv
with open('MTurkData_for_Model.csv', 'rb') as csvfile:
	spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		print row
