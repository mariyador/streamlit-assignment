import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Olympic Podium Dashboard", layout="wide")

st.title("Who Rules the Podium 1896-2012?")
st.markdown("""
Explore the top Olympic athletes of all time!  
Use the filters below to explore who dominates the podium by country and sport.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("summer.csv")
    df = df.dropna(subset=['Athlete', 'Country', 'Sport', 'Medal'])
    return df

df = load_data()

st.subheader("Dataset Overview")
st.dataframe(df)

st.subheader("Data Cleaning Summary")
st.markdown("""
- Removed rows with missing values in the `Athlete`, `Country`, `Sport`, or `Medal` columns.  
""")

# sidebar with filters
st.sidebar.header("Filters")
countries = sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("Choose a Country", countries, index=countries.index("USA") if "USA" in countries else 0)

available_sports = sorted(df[df['Country'] == selected_country]['Sport'].unique())
selected_sport = st.sidebar.selectbox("Choose a Sport", available_sports)

# filter
filtered_df = df[(df['Country'] == selected_country) & (df['Sport'] == selected_sport)]

st.markdown(f"### {selected_country}: {selected_sport}")

# top
top_athletes = (
    filtered_df.groupby('Athlete')
    .Medal.count()
    .reset_index(name='Total Medals')
    .sort_values(by='Total Medals', ascending=False)
    .head(10)
)

# visualization
if top_athletes.empty:
    st.warning("No data found for the selected country and sport.")
else:
    fig1 = px.bar(top_athletes, x='Athlete', y='Total Medals', title='Top 10 Athletes by Medal Count')
    st.plotly_chart(fig1, use_container_width=True)

    top_name = top_athletes.iloc[0]['Athlete']
    medals_dist = (
        filtered_df[filtered_df['Athlete'] == top_name]
        .groupby('Medal')
        .size()
        .reset_index(name='Count')
    )

    fig2 = px.pie(medals_dist, names='Medal', values='Count',
                  title=f"Medal Breakdown for {top_name}")
    st.plotly_chart(fig2, use_container_width=True)