#If we will not add jsonify here then the output will be of "html/text" content type
from flask import Flask, jsonify 
app = Flask(__name__)

#This decorator immediately converts the function into URI end point and we can have several different routes
@app.route('/') 
def hello():
	return jsonify({"about" : "Hello World!"})

if __name__ == '__main__':
	app.run(debug=True)
