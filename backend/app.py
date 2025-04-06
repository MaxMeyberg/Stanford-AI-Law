import os
import json
from flask_cors import CORS #allows you to call the flask functions
from flask import Flask, request, jsonify

from dotenv import load_dotenv

from API_services.apify import APIFY_LinkedIn_WebScrape
from API_services.gemini import GEMINI_Response

load_dotenv("../.env")

app = Flask(__name__)
CORS(app)


@app.route('/scrape-linkedin', methods=['POST']) #call from the frontend to ask to webscrape
def scrape_linkedin():
    userInput = request.get_json()
    """ Looks like this:
        userInput = {
                    'url': 'https://www.linkedin.com/username', 
                    'prompt': 'I want to message this person to tell them that I want to work with them'
                    }
    """
    #helper function to check and make sure the UserInput isn't messed up (EX: the url is not there)
    validateUserInput(userInput)
    
    url = userInput['url']
    prompt = userInput['prompt']
    
    try:
        #WS_info is shorthand for web scrape info
        WS_info = APIFY_LinkedIn_WebScrape(url)

        aiResponse = GEMINI_Response(WS_info, prompt)

        return jsonify({
            'email_address': WS_info.get("email"), #gets the email from the Web Scraping
            'email_body': aiResponse['email_output'], #Generated email body via Gemeni
            'analysis_rationale': aiResponse['analysis_rationale'], #generated analysis built by Gemeni
        })

    #If this is ran, you definatly blundered somewhere
    except Exception as e:
        return jsonify({'error located in app.py/sceape_linkedin': str(e)}), 500


"""[Handwritten] This is used to validate the User Input to make sure it's legit"""
def validateUserInput(userInput):
    #Check to see if backend even received the userInput:
    if not userInput:
        return jsonify({'error': 'backend didnt receive userInput'}), 400
    
    # Check to see if url was received by backend
    if 'url' not in userInput:
        return jsonify({'error': 'Missing URL in request'}), 400

    # Check to see if prompt was received by backend
    if 'prompt' not in userInput:
        return jsonify({'error': 'Missing prompt in request'}), 400


if __name__ == '__main__':
    app.run(debug=True)
