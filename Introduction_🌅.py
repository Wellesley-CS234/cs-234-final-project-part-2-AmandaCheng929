import streamlit as st
import base64

st.set_page_config(
    page_title="Movies in 2024",
    layout="wide"
)


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


st.title("🎬 Movies in 2024: Performance, Attention, and Genre")



st.markdown(
    
"""
**What makes a movie successful in 2024?**  
Is it box office performance, audience attention, or how well it embodies its genre?

This project combines **IMDb performance**, **Wikipedia pageviews**, as well as **plot analysis**
to explore how films performed — and how audiences engaged with them — throughout 2024.

"""
)

st.markdown("<p style='font-size:20px;'><strong>How well does wikipedia act as a proxy for audience interest and genre depiction for movies?</p>", unsafe_allow_html=True)


st.metric("Movies Analyzed:", "23k+ 🎞️")



with open("watching.gif", "rb") as f:
    data = f.read()
    b64_data = base64.b64encode(data).decode()

st.markdown(
    f'<img src="data:image/gif;base64,{b64_data}" width="600">',
    unsafe_allow_html=True
)

st.markdown("---")
st.subheader("🧭 Page Navigation Guide")
st.success("Use the **mode selection** in the sidebar to see progress, datasets and steps taken in each page.")
st.markdown(
"""
Explore different parts of the analysis:
""")
st.page_link("pages/2_Movies_in_Wikipedia_📊.py", label="📊 Movies in Wikipedia")
st.markdown(
"""
- See how wikipedia reflect audience interest in different genres of movies?
- See how a movie's pageview for Wikipedia relates to its rating, popularity, and revenue as reported by IMDb.

""")
st.page_link("pages/3_Film_Genre_Classification_🎭.py", label="🎭 Film Genre Classification")
st.markdown(
"""
- Explore top films in each genre and look at keywords in the plot representing this genre.
""")
st.page_link("pages/4_Movie_Composition_🧩.py", label="🧩 Movie Composition")

st.markdown(
"""
- Select up to 10 movies to compare their score in each genre to better understand their multidimensional composition.
""")

st.markdown("---")
st.subheader("📖 Project Premise")

st.markdown(
"""
Movies don’t just succeed in theaters—they live online.

Especially after the global COVID-19 pandemic, more and more audiences choose to view movies at home! 
As we live in a society with more and more rapid lifestyles, people seem to be more cautious and selective with what movies are "worth" their time investment.""")
st.image("watching_movie.jpeg", width=500)
st.markdown(
"""
Think about how you would approach watching a movie now a days.
_Will you look up its rating? Its reviews? Its plot? Its genre?_
If you do, your engagement with movies are no longer limited to watching the movie itself, but also all this research that goes before watching them.
""")

st.markdown("<p style='font-size:20px;'><strong>I hypothesize that wikipedia engagment is much higher for films released in the 21st century than those released in the 20th century.</p>", unsafe_allow_html=True)
st.markdown("Is that true? Let's find out!")

st.markdown(
"""
In this project, we examine film engagement in **2024** by:
- Measuring **performance metrics** from IMDb
- Tracking **public attention** through Wikipedia pageviews
- Analyzing **Wikipedia plot summaries** to quantify how strongly a movie represents different genres

By connecting these data sources, we aim to understand how **content, popularity, and audience interest**
interact in the modern movie ecosystem.
"""
)


st.markdown("---")
st.subheader("🗂️ Data Sources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⭐ IMDb")
    st.markdown(
    """
    - Only representing year 2024
    - Ratings, revenue, popularity as indicators of movie performance
    - Release year and metadata  
    - Genre labels as training data for genre evaluation
    """
    )

with col2:
    st.markdown("### 📊 Wikipedia Pageviews")
    st.markdown(
    """
    - Daily pageview counts
    - Proxy for public attention and engagement with movie research
    """
    )

with col3:
    st.markdown("### 📝 Wikipedia Plot Sections")
    st.markdown(
    """
    - Extracted from wikipedia pages
    - Text-based genre representation
    - Use to evaluate genre scores
    """
    )


















