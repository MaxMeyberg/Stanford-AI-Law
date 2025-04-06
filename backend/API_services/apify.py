from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json

load_dotenv("../.env")

def APIFY_LinkedIn_WebScrape(url: str) -> str: 
    API_TOKEN = os.getenv("APIFY_API_TOKEN")
    client = ApifyClient(API_TOKEN)

    if API_TOKEN is None:
        return json.dumps({"error": "No API token found"})


    """
    API DOCS STUFF, DONT TOUCH
    -----
    """
    # Prepare the Actor input .
    run_input = { "profileUrls": [
            url
        ] }

    # Max: The "2SyF0bVxmgGr8IVCZ" is just the ID for Apify ,DONT be stupid and touch it, I got it from the Docs
    run = client.actor("2SyF0bVxmgGr8IVCZ").call(run_input=run_input)

    """ Max:
    If you are asking why tf this works w "next", imagine vibe coding for a project to semi-work, then going back to fix it
    But then a pro python developer comes and says "Why are't you using next?", and walks up to me to fix this issue
    The worst part is that everything inside of that "next" is actuallu from the Docs
    from the API, so if you genuinely want to hurt yourself worse than my first time creating an account for Microsoft Azure, be my guest, but be warned 

    This witchcraft was the old code:
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        break

    Truly a Claude 3.7 moment.
    
    TLDR: Dont touch this line, it works
    """
    item = next(client.dataset(run["defaultDatasetId"]).iterate_items())
    """
    TOUCHING CODE BELOW THIS POINT IS OK
    -----
    """
    # Ensure keys exist before accessing them
    fullName = item.get("fullName", "")
    headline = item.get("headline", "")
    email = item.get("email", "")
    about = item.get("about", "")
    

    result = {
        "fullName": fullName,
        "headline": headline,
        "email": email,
        "about": about,
        
    }
    return result
