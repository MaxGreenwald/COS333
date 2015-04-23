from flask import Flask, send_from_directory, render_template, request
#from flask.ext.pymongo import PyMongo
import pymongo

MONGODB_URI = 'mongodb://maxgreenwald:oliver11@ds061621.mongolab.com:61621/ftc-cases' 

# Database(MongoClient('mongodb://maxgreenwald:oliver11@ds061621.mongolab.com:61621/ftc-cases', 27017), u'test_database')
app = Flask(__name__)
# mongo = PyMongo(app)

# app.config['MONGO3_HOST'] = 'ds061621.mongolab.com:61621/ftc-cases'
#app.config['MONGO3_PORT'] = 27017
#app.config['MONGO3_DBNAME'] = 'ftc-cases'
#mongo3 = PyMongo(app, config_prefix='MONGO3')
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
cases = db['cases']

@app.route('/')
def homepage():
	return send_from_directory('templates', 'index.html')

@app.route('/add', methods=['GET', 'POST'])
def addCase():
	if request.method == 'POST':
		print "hello"
		print request.form.values()

	SEED_DATA = [
    {
        'case': '1970s',
        'date': 'yoyoyo',
        'company name': 'You Light Up My Life',
        'act violated': 99,
        'categoryPC': 'Oldfield worked with Miller, who developed and built \ncarburetors in Los Angeles, to create a racing machine\n that would not only be fast and durable, but that would also protect the driver\n in the event of an accident. Bob Burman, one of Oldfields top rivals and closest friends, was killed in a wreck during a race in Corona, California. Burman died from severe injuries suffered while rolling over in his open-cockpit car. Oldfield and Miller joined forces to build a race car that incorporated an enclosed roll cage inside a streamlined drivers compartment to completely enclose the driver.[2][3]',
        'summaryPC': 99,
        'redressObtained': 10,
        'financial': 10,
        'audit': 10,
        'prohibitions': 10,
        'pressCoverage': 10
    }
	]

	
	
		#print projectpath
	cases.insert(SEED_DATA)
	cursor = cases.find({'categoryPC': {'$gte': 7}})

	return send_from_directory('templates', 'add.html')
@app.route('/view')
def viewTable():

	caseFinder = cases.find({'summaryPC': {'$gte': 7}})
	tableData = []
	for x in caseFinder:
		newCase = [x['case'], x['date'], x['company name'], x['act violated'], x['categoryPC'], x['summaryPC'], x['redressObtained'], x['financial'], x['audit'], x['prohibitions'], x['pressCoverage']]
		tableData.append(newCase)
	return render_template('view.html', tableData = tableData)


if __name__ == '__main__':
    app.run(debug = True)