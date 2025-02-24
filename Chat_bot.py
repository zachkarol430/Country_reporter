from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2:1b")

def generate_fun_facts(country_name: str) -> str:
    """Generate fun facts about a country"""
    prompt = f"""
    Generate two fun facts about {country_name}.
    Keep them brief and interesting.
    DO NOT include any sensitive topics.
    """
    
    try:
        return model.invoke(
            prompt,
            config={
                'timeout': 30,
                'max_tokens': 200
            }
        )
    except Exception as e:
        return "Unable to generate fun facts at this time."
    
def summarize_news(news_list: list, country_name) -> str:
    """Summarize a list of news articles"""
    prompt = f"""
    Summarize the following news articles and 
    only include important stuff!   Start report by saying "Here is {country_name}'s report" and then begin summary. No more than three sentences. 
    {news_list}
    """
    try:
        return model.invoke(
            prompt,
            config={
                'timeout': 30,
                'max_tokens': 200
            }
        )
    except Exception as e:
        return "Unable to summarize the news at this time."
