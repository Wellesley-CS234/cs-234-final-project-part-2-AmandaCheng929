import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

st.set_page_config(page_title="Fun Interactive Streamlit App", layout="wide")

# --- Sidebar ---
st.sidebar.title("Controls 🎛️")
st.sidebar.markdown("Play with the sliders and filters!")

num_points = st.sidebar.slider("Number of data points", 50, 500, 150)
noise = st.sidebar.slider("Noise level", 0.0, 5.0, 1.0)
seed = st.sidebar.number_input("Random seed", value=42, step=1)

np.random.seed(seed)

# --- Generate Data ---
x = np.linspace(0, 10, num_points)
y = np.sin(x) + noise * np.random.randn(num_points)
category = np.where(x < 3, "Low", np.where(x < 7, "Mid", "High"))

df = pd.DataFrame({
    "x": x,
    "y": y,
    "category": category
})

# --- Header ---
st.title("🚀 Fun Interactive Streamlit Dashboard")
st.caption("Sliders, charts, tables, and a little chaos")

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Mean y", f"{df['y'].mean():.2f}")
col2.metric("Std y", f"{df['y'].std():.2f}")
col3.metric("Points", len(df))

# --- Chart Section ---
st.subheader("📈 Interactive Chart")

chart = (
    alt.Chart(df)
    .mark_circle(size=60, opacity=0.7)
    .encode(
        x=alt.X("x", title="X value"),
        y=alt.Y("y", title="Y value"),
        color=alt.Color("category", legend=alt.Legend(title="Region")),
        tooltip=["x", "y", "category"]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

# --- Data Table ---
st.subheader("📊 Data Explorer")

filter_cat = st.multiselect(
    "Filter by category",
    options=df["category"].unique(),
    default=list(df["category"].unique())
)

filtered_df = df[df["category"].isin(filter_cat)]

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)

# --- Expander ---
with st.expander("🔍 Show summary statistics"):
    st.write(filtered_df.describe())

# --- Progress + Animation ---
st.subheader("⏳ Fake but Satisfying Progress Bar")

if st.button("Run analysis"):
    progress = st.progress(0)
    status = st.empty()
    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)
        status.text(f"Processing step {i + 1}/100")
    status.success("Done! 🎉")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
