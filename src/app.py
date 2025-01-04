import requests
import streamlit as st

# Function to fetch news from NewsAPI
def fetch_news(api_key, category=None, search_query=None):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    if category:
        url += f"&category={category}"

    if search_query:
        url += f"&q={search_query}"

    try:
        response = requests.get(url)
        news_data = response.json()

        if news_data["status"] == "ok" and news_data["totalResults"] > 0:
            return news_data["articles"]
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return None

# Set up the Streamlit app
st.set_page_config(page_title="Latest News", layout="wide")
st.title("🌍 Latest News")

# Add description
st.markdown("""
Welcome to the **Latest News** app! Here, you can read the latest headlines from around the world. 
Stay updated with current events from various categories including politics, sports, business, and more.
""")

# Create a filter for news category
category = st.selectbox("Choose a news category:", ["General", "Business", "Entertainment", "Health", "Science", "Sports", "Technology"])

# Create a search bar
search_query = st.text_input("Search for news articles:")

# Adding a spinner while data is loading
with st.spinner("Fetching the latest news..."):
    # Hardcoding the API key here
    api_key = "800efd0db3e64f85a6176a0b0f5eac8f"  # Replace with your actual API key
    news_articles = fetch_news(api_key, category, search_query)

# Displaying the news articles
if news_articles:
    # Layout using columns for each article
    for idx, article in enumerate(news_articles):
        # Create a two-column layout
        col1, col2 = st.columns([3, 1])

        with col1:
            # Show the article title
            st.subheader(article['title'])
            st.write(article['description'])

            # Show the link to read more
            st.markdown(f"[Read more]({article['url']})")

        with col2:
            # Show the article's image if available
            if article['urlToImage']:
                st.image(article['urlToImage'], caption='Article Image', use_column_width=True)

        # Add a line separator after each article for better spacing
        st.markdown("---")

else:
    st.write("No news found or unable to fetch the news.")

# Add a footer with information about the app
st.markdown("""
---
Built with ❤️ by **Ami** | Powered by [NewsAPI](https://newsapi.org/)
""")
