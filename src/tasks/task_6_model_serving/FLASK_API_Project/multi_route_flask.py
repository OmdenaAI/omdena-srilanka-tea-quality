#If we will not add jsonify here then the output will be of "html/text" content type

from flask import Flask, jsonify , request
app = Flask(__name__)

#This decorator immediately converts the function into URI end point and we can have several different routes
@app.route('/' , methods=['GET', 'POST'])

def index():

	# Here i am tring to access the content from the post first and then we are sending it back as a response
	if(request.method == 'POST'):
		some_json = request.get_json()
		return jsonify({'you sent' : some_json}) , 201
	else:
		return jsonify({'about' : "Hello World!"})

# If you will not specifically declare any method then the default will be GET
@app.route('/multl/<int:num>' , methods = ['GET'])
def get_multiply(num=None):
	return jsonify({"result" : num * 10})

if __name__ == '__main__':
	app.run(debug=True)