# import flask dependencies
from flask import Flask, request, make_response, jsonify
from library.df_response_lib import * 

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    if action == "get_results":
        # return a fulfillment response
        fulfillmentText = 'Basic card Response from webhook'

		aog = actions_on_google_response()
		aog_sr = aog.simple_response([
			[fulfillmentText, fulfillmentText, False]
		])

		basic_card = aog.basic_card("Title", "Subtitle", "This is formatted text", image=["https://www.pragnakalp.com/wp-content/uploads/2018/12/logo-1024.png", "this is accessibility text"])

		ff_response = fulfillment_response()
		ff_text = ff_response.fulfillment_text(fulfillmentText)
		ff_messages = ff_response.fulfillment_messages([aog_sr, basic_card])

		reply = ff_response.main_response(ff_text, ff_messages)
    return reply

        

    
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
