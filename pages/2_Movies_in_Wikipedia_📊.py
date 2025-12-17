import streamlit as st
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go
import time
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt


df_allviews_ori = pd.read_csv('all_movies_totalViews.csv')
df_allviews = df_allviews_ori[df_allviews_ori['Revenue']!=0]
df_allviews = df_allviews[df_allviews['total_pageview']!=0]
df_rank = pd.read_csv('genre_view_rank.csv')
df_rank = df_rank.sort_values('total_view', ascending = False)
df_score = pd.read_csv('title_genre_scored.csv')

df_keywords = pd.read_csv('genre_keywords.csv')

d = df_score.to_dict(orient="index")
score_dict = {inner["title"]: {k: v for k, v in inner.items() if k != "title"} for inner in d.values()}


path1 = os.path.join('demo_data', 'oriData_short.csv')
df_oriData = pd.read_csv(path1)


emojis = {
    "Action": "🔥",
    "Science Fiction": "👽",
    "Adventure": "🧭",
    "Drama": "🎭",
    "Crime": "🚔",
    "Thriller": "😱",
    "Comedy": "😂",
    "Romance": "❤️",
    "Western": "🤠",
    "Fantasy": "🧙‍♂️",
    "War": "⚔️",
    "Mystery": "🕵️‍♂️",
    "Horror": "👻",
    "Animation": "🎨",
    "History": "📜",
    "Music": "🎵",
    "Family": "👨‍👩‍👧‍👦",
    "TV Movie": "📺",
    "Documentary": "🎥"
}

if "progress" not in st.session_state:
    mode = st.sidebar.segmented_control(
    'Choose "Show Process" to see datasets and steps for each page:',
    options=["Results Only", "Show Process"],
    default="Results Only"
    )
    if mode == "Show Process":
        st.session_state.progress = True
    else:
        st.session_state.progress = False

else:
    if st.session_state.progress == True:
        default = 'Show Process'
    else:
        default = "Results Only"

    mode = st.sidebar.segmented_control(
        'Choose "Show Process" to see datasets and steps for each page:',
        options=["Results Only", "Show Process"],
        default=default
    )

if mode == "Show Process":
    st.session_state.progress = True
else:
    st.session_state.progress = False

# ------------------------------------------------------------------
st.header('Movies in Wikipedia 📊')

if st.session_state.progress:
    st.subheader('🕵🏻 Finding Wikipedia Pages for Each Movie')
    st.markdown(
         """
            The IMDb dataset provides movie titles and release years, but **does not include direct links to their corresponding Wikipedia pages**.
            Naively querying Wikipedia using only movie titles can lead to incorrect matches, as many titles are ambiguous or shared by non-film entities.

            For example, searching for *“Titanic”* returns the Wikipedia page for the **RMS Titanic**, the historic passenger ship, rather than the **1997 film directed by James Cameron** that most users would expect.

            To ensure accuracy, we relied on **Wikidata identifiers** associated with each Wikipedia page.  
            Specifically, we verified that:
            - The page's *instance of* property corresponds to a **film**
            - The film's **release year** matches the year recorded in the IMDb dataset

            This filtering step was essential for reliably mapping each movie to its correct Wikipedia article.
    """)
    st.subheader('👁️ Collecting Wikipedia Pageviews')
    st.markdown(
        """
            Wikipedia pageview statistics were obtained from a dataset containing all **Desktop Pageview Dataset Project (DPDP)** records for **January–December 2024** for *en.wikipedia* traffic in the United States.  
            This dataset was provided by **Professor Eni Mustafaraj**.

            Using the unique **pageid** for each verified Wikipedia article, we extracted the total number of pageviews for every movie.

            Movie genres were taken from the IMDb dataset, and pageviews were aggregated at the **genre level**. Since most movies belong to multiple genres, a movie's pageviews were **counted toward each of its associated genres**.

            The table below shows a sample of the processed dataset used in this analysis.
        """)
    
    st.dataframe(df_allviews.head(25))



st.subheader("🏅 Most Viewed Genre on Wikipedia")
col1, col2, col3 = st.columns(3)
col1.metric("Top 1", f"{df_rank.iloc[0][0]} {emojis[df_rank.iloc[0][0]]}")
col2.metric("Top 2", f"{df_rank.iloc[1][0]} {emojis[df_rank.iloc[1][0]]}")
col3.metric("Top 3", f"{df_rank.iloc[2][0]} {emojis[df_rank.iloc[2][0]]}")

genre_col = df_rank['genre'].tolist()
per = st.toggle("Average Views Per Work")
if per:
    y = 'view_work' 
else:
    y = 'total_view'

fig = px.bar(
    df_rank,
    x="genre",
    y=y,
    text=[f"{emojis[x]}" for x in genre_col],
)
fig.update_traces(textposition="outside",)

fig.update_xaxes(
    title = "Genre",
)
fig.update_yaxes(
    title= 'Wikipedia Pageviews'
)
st.plotly_chart(fig, use_container_width=True, key = 'rank')

if per:
    st.markdown("The number of works for each genre is different: ")
    df_dis = df_rank.rename(columns={
        'genre': "Genre",
        'total_view': "Total Pageviews",
        'number': "Number of Works",
        'view_work': "Average Pageview per Work"
    })
    st.dataframe(df_dis)

st.markdown("""
            


    By comparing the two bar charts above, we can conclude that **adventure, sci-fi, fantasy and animation films** appear to have high average interest, despite lower overall number in movies.
    This does align with the **general demographic** of wikipedia users!
            


            
""")

# -------------------------------------------------------------------------
st.markdown("""




""")
st.subheader('📺 IMDb Performance vs Wikipedia')

choice = st.selectbox(
    'Select Variable', ['Rating 💯','Popularity 🏙️','Revenue 💰']
)
st.write(f"Showing movie {choice.split(' ')[0]} and their wikipedia pageviews.")
st.markdown("<p style='color: gray; font-size:16px;'>*user cursor to select parts of the figure to zoom into</p>", unsafe_allow_html=True)

fig2 = px.scatter(df_allviews, x=choice.split(' ')[0], y="total_pageview", hover_data=["title"])

fig2.update_yaxes(title = 'Total Pageview')
st.plotly_chart(fig2, use_container_width=True, key = 'scatter for views')


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💯 Rating")
    st.markdown(
    """
    - Filtered IMDb dataset to only include movies with 10+ reviews
    - **Clear positive relationship**
        - Most movies with high pageviews have high rating
        - Not all high-rating movies have high pageviews
    """
    )

with col2:
    st.markdown("### 🏙️ Popularity")
    st.markdown(
    """
    - According to IMDb's webiste, the popularity score reflects the number of hits/page views, the average user rating, any awards won by the title and several other indicators
    - Large variation in the data, with some **very high outliers**
    - Looking at the large body of data, follows an overall positive correlation
    """
    )

with col3:
    st.markdown("### 💰 Revenue")
    st.markdown(
    """
    - Overall positive relationship, and high revenue appears to guaruntee high wikipedia page views
    - High revenue outliers generally represent **high-popularity IPs**
    """
    )

st.markdown("---")
st.header('Hypothesis Testing: 20th-Century vs 21st-Century 📊')
st.markdown(
        """
            Is it true that the audience tends to browse the wikipedia pages of newer (21st century released films) more than older (20th century released) movies?

            Below is a boxplot demonstrating the 
        """)

def checkCent(date):
    year = int(date[:4])
    if year>=2000:
        return "21st-Century"
    else:
        return "20th-Century"

df_sub = df_allviews[['release_date','total_pageview']]
df_sub['century'] = df_sub['release_date'].apply(lambda x: checkCent(x))
df_sub = df_sub[['century','total_pageview']]
df_sub = df_sub[df_sub['total_pageview']!=0]

fig = px.box(
    df_sub,
    x="century",
    y="total_pageview",
    category_orders={
        "century": ["20th-Century", "21st-Century"]
    },
    labels={
        "century": "Century",
        "total_pageview": "Total Pageviews"
    }
)

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("20th-Century:", "38713 👁")
    st.markdown('views/movie')

with col2:
    st.metric("21th-Century:", "51228 👁")
    st.markdown('views/movie')

with col3:
    st.metric("p-value:", "2.61e-09 ✅")
    st.markdown(
    """
    - Two-sample hypothesis testing
    - This p value rejects the null hypothesis and indicates that **there is significant difference** between 20th and 21st century released films!

    """
    )

