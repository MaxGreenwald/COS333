from flask import Flask, send_from_directory, render_template
app = Flask(__name__)

@app.route('/home')
def home():
    #return 'hello'
    return send_from_directory('templates', 'mainPage.html')

@app.route('/userView')
def user():
    #return 'hello'
    return send_from_directory('templates', 'userView.html')


@app.route('/fb')
def fb():
    #return 'hello'
    return send_from_directory('templates', 'fbLogin.html')

@app.route('/about')
def about():
    return send_from_directory('templates', 'about.html')

if __name__ == '__main__':
    app.run(debug = True)