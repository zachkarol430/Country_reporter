import os
import requests
import feedparser  # You may need to install this library
from urllib.parse import quote



# Function to fetch Google News via RSS feed
def fetch_google_news_rss(country_name: str):
    """Fetch news articles from Google News using an RSS feed."""
    query = quote(country_name)  # URL encode the country name
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(rss_url)
        if response.status_code == 200:
            # Parse the RSS feed
            feed = feedparser.parse(response.content)
            # Extract and return the titles of the top three articles
            titles = [entry.title for entry in feed.entries[:10]]  # Get titles of the first three articles
            # Remove any words after the first dash in the title
            titles = [title.split(' - ')[0] for title in titles]
            return titles
        else:
            print(f"Error fetching news from Google News RSS: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception occurred while fetching news from Google News RSS: {str(e)}")
        return []


# Example usage
if __name__ == "__main__": # Example country code for the United States (use lowercase)
    country_name = "Palau"  # Example country name (for Tuvalu)
    
    # Fetch news using the get_news method
    print("Fetching news using get_news (News API fallback to Google News RSS):")
    news_titles = fetch_google_news_rss(country_name)
    if news_titles:
        for idx, title in enumerate(news_titles, start=1):
            print(f"{idx}. {title}")
