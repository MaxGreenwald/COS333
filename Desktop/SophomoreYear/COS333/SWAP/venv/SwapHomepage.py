from flask import Flask, send_from_directory, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
    #return 'hello'
    return send_from_directory('templates', 'mainPage.html')

@app.route('/about')
def about():
    return send_from_directory('templates', 'about.html')

if __name__ == '__main__':
    app.run(debug = True)