from flask import Flask, send_from_directory, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
    return 'hello'
    #return send_from_directory('templates', 'index.html')

@app.route('/add')
def addCase():
    return 'addCases!'

@app.route('/view')
def viewTable():
	tableData = [['Snapchat', '10.1.1.1', '1/15/16'],['Facebook', '10.1.1.1', '1/15/16'],['Yolo', '10.1.1.1', '1/15/16']]
	return 'hello'
	#return render_template('view.html', tableData=tableData)


if __name__ == '__main__':
    app.run(debug = True)