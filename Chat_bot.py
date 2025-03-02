import requests
import json
import os

from dotenv import load_dotenv

#load access and secret keys
load_dotenv()   

open_router_api_key = os.getenv('MY_ROUTER_KEY')

def generate_fun_facts(country_name: str) -> str:
    """Generate fun facts about a country using OpenRouter API"""
    prompt = f"""
    Generate two fun facts about {country_name}.
    Keep them brief and interesting.
    DO NOT include any sensitive topics. No chinese characters
    """
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization":  f"Bearer {open_router_api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "moonshotai/moonlight-16b-a3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            })
        )
        response_data = response.json()
        return response_data.get('choices', [{}])[0].get('message', {}).get('content', "No response content.")
    except Exception as e:
        return "Unable to generate fun facts at this time."

def summarize_news(news_list: list, country_name: str) -> str:
    """Summarize a list of news articles using OpenRouter API"""
    prompt = f"""
    Summarize the following news articles and 
    only include important stuff! Start report by saying "Here is {country_name}'s report" and then begin summary. No more than three sentences. 
    {news_list}. No chinese characters!
    """
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {open_router_api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "moonshotai/moonlight-16b-a3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            })
        )
        response_data = response.json()
        return response_data.get('choices', [{}])[0].get('message', {}).get('content', "No response content.")
    except Exception as e:
        return "Unable to summarize the news at this time."
    