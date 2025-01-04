import requests
import streamlit as st
from streamlit import components
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Cache the news fetching function for better performance using st.cache_data
@st.cache_data
def fetch_news(api_key, category='us'):
    url = f'https://newsapi.org/v2/top-headlines?country={category}&apiKey={api_key}'
    try:
        response = requests.get(url)
        news_data = response.json()

        if news_data["status"] == "ok" and news_data["totalResults"] > 0:
            return news_data["articles"]
        else:
            logging.warning(f"No news found or API response was empty for {category}.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        st.error("Error fetching news. Please try again later.")
        return None
    except Exception as e:
        logging.error(f"General error: {e}")
        st.error("An unexpected error occurred.")
        return None

# Set up the Streamlit app
st.set_page_config(page_title="Latest News", layout="wide")
st.title("🌍 Latest News")

# Add description
st.markdown("""
Welcome to the **Latest News** app! Here, you can read the latest headlines from around the world. 
Stay updated with current events from various categories including politics, sports, business, and more.
""")

# User interface for filtering and searching
categories = ['All', 'Business', 'Entertainment', 'Health', 'Science', 'Sports', 'Technology']
selected_category = st.selectbox('Choose Category:', categories)
search_query = st.text_input('Search for news:')

# Clear Filters Button
if st.button('Clear Filters'):
    st.session_state.search_query = ""
    st.session_state.category = 'all'
    st.experimental_rerun()  # Refresh the page to reset everything

# Show a loading spinner while data is being fetched
with st.spinner("Fetching the latest news, please wait..."):
    api_key = '800efd0db3e64f85a6176a0b0f5eac8f'
    news_articles = fetch_news(api_key, category='us')

# Filter articles based on search query and category selection
if news_articles:
    filtered_articles = []
    for article in news_articles:
        if (search_query.lower() in article['title'].lower() or 
            search_query.lower() in article['description'].lower()):
            if selected_category == 'All' or selected_category.lower() in article['category'].lower():
                filtered_articles.append(article)

    # Displaying filtered articles
    if filtered_articles:
        for article in filtered_articles:
            col1, col2 = st.columns([4, 1])

            with col1:
                # Show the article title and description
                st.subheader(article['title'])
                st.write(article['description'])
                st.markdown(f"[Read more]({article['url']})")

            with col2:
                # Show the article's image if available
                if article['urlToImage']:
                    st.image(article['urlToImage'], caption='Article Image', use_column_width=True)

            # Add a line separator after each article for better spacing
            st.markdown("---")
    else:
        st.write("No articles found matching your criteria.")
else:
    st.write("No news found or unable to fetch the news.")

# Add a footer with information about the app
st.markdown("""
---
Built with ❤️ by **Your Name** | Powered by [NewsAPI](https://newsapi.org/)
""")
