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
df_poster = pd.read_csv('all_movies_poster.csv')
df_classed = pd.read_csv('title_genre_classed.csv')


df_keywords = pd.read_csv('genre_keywords.csv')

d = df_score.to_dict(orient="index")
score_dict = {inner["title"]: {k: v for k, v in inner.items() if k != "title"} for inner in d.values()}
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
    "Family": "🏡",
    "Tv Movie": "📺",
    "Documentary": "🎥"
}

# ------------------------------------------------------------------


st.title("Film Genre Classification 🎭")

if st.session_state.progress:
    st.subheader('💯 Obtaining Genre Scores')
    st.markdown(
        """
            The IMDb dataset provides **genre labels** for each film—but what do those genres actually *look like* in the story itself?

To explore this, we extract the **“Plot” section** from each film’s Wikipedia page and use it as narrative data. These plot summaries are then used to **train a text-based classifier**, with IMDb’s genre labels serving as the ground truth.

Using a **One-vs-Rest multiclass classification approach**, each movie is no longer confined to a yes/no for each genre. Instead, it receives a **continuous score between 0 and 1 for every genre**, indicating how strongly its plot reflects that genre’s themes.

Below, you can compare a portion of the dataset **before and after classification** to see how discrete genre labels are transformed into a richer, multidimensional representation of each film.


        """
    )

    dataset = st.segmented_control(
        "Dataset",
        options=["Input", "Output"],
        default="Input"
    )

    if dataset == 'Input':
        view = df_classed.drop(columns = ['genres', 'plot_text'])
        st.dataframe(view.head(10))
    else:
        st.dataframe(df_score.head(10))

    
    st.markdown("""
    **Evaluation*:* To evaluate the efficiency of classification, the percentage of accuracy is determined by whether or not the model obtains a value greater than 0.5 for a class 1 and less than 0.5 for a class 0 for each genre.
    """)
    st.metric("Accuracy", "79.3%✅")


st.subheader('🏆 See Top Genre-Scoring Movies')
genre_emo = []
genre_col = df_score.columns.tolist()[1:]
for each in genre_col:
    genre_emo.append(f"{each}  {emojis[each]}")
choice = st.selectbox(
    'Select Genre', genre_emo
)


choice = choice.split('  ')[0]
temp_df = df_score[['title', choice]].sort_values(choice, ascending = False)
temp_df[choice] = temp_df[choice].apply(lambda x: str(round(x,4)))
temp_df = temp_df.rename(columns={choice: f"{choice} Genre Score"})
merged = temp_df.merge(df_allviews_ori[['title','pageid']], on="title", how="left")
merged['pageid'] = merged['pageid'].apply(lambda x: f"https://en.wikipedia.org/?curid={x}")
merged = merged.rename(columns={'pageid': "English Wikipedia Link"})

movies = merged.head(5)['title'].tolist()

image = df_poster[df_poster['title'].isin(movies)]['poster_path'].tolist()
images = [f"https://image.tmdb.org/t/p/w500{x}" for x in image]

cols = st.columns(len(images))

for col, img in zip(cols, images):
    with col:
        st.image(img, use_container_width=True)

size = st.slider(
    f"Select number of top movies to view for {choice}:",
    min_value=1,
    max_value=50,
    value=10,
    step=1
)

df = merged.head(size)
# st.dataframe(df)
st.write('Click on the links to see each wikiepedia page!')
st.data_editor(
    df,
    column_config={
        "English Wikipedia Link": st.column_config.LinkColumn(
            "Wikipedia Page",
            display_text="Open 🔍"
        )
    },
    disabled=True
)

st.markdown("""

""")

sliced = df_keywords[df_keywords['genre']==choice.lower()]

if st.session_state.progress:
    st.subheader('⚖️ Calculating Feature Weights')
    st.markdown("""
    In order to calcualte the genre scores, the multiclass classifier assigned **weights** to each word based on its training, representing how important a word is for identifying a text as describing a genre.
            
    These weights are continuous, and the magnitudes of which are used to generate the word cloud below, with larger words being more crucial for this genre.
    
    Below, you can see the generated weights for the genre you selected:            
                """)
    st.dataframe(sliced[['word', 'weight']])


st.subheader(f"📌 Keywords for {choice} Movies {emojis[choice]}")

# st.write(sliced[['word', 'weight']])

word_freq = dict(zip(sliced["word"], sliced["weight"]))

wc = WordCloud(
    width=800,
    height=400,
    background_color=None,
    mode="RGBA",
    colormap="cividis",
    max_words=100
).generate_from_frequencies(word_freq)

fig, ax = plt.subplots(figsize=(4,3))
fig.patch.set_alpha(0.0)
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig, transparent=True)