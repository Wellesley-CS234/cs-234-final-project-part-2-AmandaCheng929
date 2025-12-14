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
genre_col = df_score.columns.tolist()[1:]
df_poster = pd.read_csv('all_movies_poster.csv')

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
    "Tv Movie": "📺",
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
st.title("Movie Composition 🧩")


if st.session_state.progress:
    st.subheader('🔮 Visualzing Movie Composition')
    st.markdown("""
                Following the steps described in the page _Film Genre Classficiation_ the genre scores of each movie can be used to compare characterstics of different films.

                The **radar chart** is a common method of multi-dimension comparison, and can highlight the genre characterstics of different films. 
                It shows a gestalt view of a movie's genre identity, and reveal if a movie has a balanced or spiky profile.

                The **heat map** uses gradients of colors to visualize the magnitudes of each genre score, and is visually intuitive for comparing more movies.                    
                """)
    st.markdown("""

        """)



st.subheader('🎰 Compare Movie Compositions')
selected = st.multiselect(
    "Choose Movies to View Composition (Max 5)",
    df_score['title'],
    default=['Inception', 'Now You See Me 2','La La Land'],
    max_selections = 10,
    key = 'cool'
)

image = df_poster[df_poster['title'].isin(selected)]['poster_path'].tolist()
names = df_poster[df_poster['title'].isin(selected)]['title'].tolist()

images = [f"https://image.tmdb.org/t/p/w500{x}" for x in image]

if len(selected) <=5:
    cols = st.columns(5)

    n=0
    for col, img in zip(cols, images):
        try:
            with col:
                st.write(names[n])
                st.image(img, use_container_width=True)
                n+=1
        except:
            break
else:
    cols = st.columns(5)

    n=0
    for col, img in zip(cols, images[:5]):
        try:
            with col:
                st.write(names[n])
                st.image(img, use_container_width=True)
                n+=1
        except:
            break
    
    cols2 = st.columns(5)

    n=5
    for col, img in zip(cols2, images[5:]):
        try:
            with col:
                st.write(names[n])
                st.image(img, use_container_width=True)
                n+=1
        except:
            break
    
    

mode = st.segmented_control(
    "Mode",
    options=["Radar", "Heat"],
    default="Radar"
)


if mode == 'Radar':
    fig_r = go.Figure()
    for choice in selected:

        categories = list(score_dict[choice].keys())
        values = list(score_dict[choice].values())

        fig_r.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=choice
        ))

        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(
                    color="black"
                )
                )
            ),
            showlegend=True
        )

    st.plotly_chart(fig_r, use_container_width=True, key = 'radar')
else:
    df = df_score[df_score['title'].isin(selected)].set_index("title")
    fig = px.imshow(df,text_auto=False,color_continuous_scale="cividis")
    st.plotly_chart(fig, use_container_width=True, key = 'heat' )

    
with st.expander("View exact scores for each genre"):
    # st.dataframe(df_score[df_score['title'].isin(selected)])
    def highlight_max(s):
        return ["background-color: lightgreen; color: black" if v == s.max() else "" for v in s]

    styled = df_score[df_score['title'].isin(selected)].style.apply(highlight_max, subset=genre_col, axis=0)
    st.dataframe(styled)
    st.markdown("<p style='color: gray; font-size:14px;'>*green highlighting showing highest score for each genre</p>", unsafe_allow_html=True)