import streamlit as st

st.title("🎬 Closing Reflections & Takeaways")


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


st.markdown(
"""
What can movie performance, public attention, and narrative structure tell us
about films released in 2024?

This page summarizes the **key insights** and reflects on **data limitations**
"""
)


st.subheader("⭐ Key Findings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📊 Performance & Attention**
    - Higher IMDb ratings, popularity and revenue does reflect with higher Wikipedia pageviews
    - Pageview varies with different genres, highest in adventure, sci-fi and fantasy films
    - Popularity reflects *attention*, not necessarily *quality*
    """)

with col2:
    st.markdown("""
    **🎭 Genre Representation**
    - Wikipedia Plot sections reflect movie genres very well
    - Many films strongly express multiple genres
    - Genre scoring reveals nuances lost in single-label classification
    """)


st.subheader("⚠️ Limitations")

with st.expander("View known limitations and caveats"):
    st.markdown("""
    - IMDb dataset was filtered to only consider english-language films, and a large part of the dataset is lost when the movie title doest correlate exactly with the wikipedai article title
    - Wikipedai dataset only reflects EN Wikipedia pageviews in the US
    - Wikipedia pageviews are an imperfect proxy for audience engagement
    - Plot summaries vary in length, detail, and writing style
    - Analysis is limited to films released in 2024
    """)


st.page_link("Introduction_🌅.py", label="⬅️ Return to Introduction")