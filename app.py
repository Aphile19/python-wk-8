import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon=":microscope:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/metadata.csv')
    
    # Clean the data (similar to notebook)
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['title'])
    df_clean['abstract'] = df_clean['abstract'].fillna('No abstract available')
    
    def extract_year(date_str):
        if pd.isnull(date_str):
            return np.nan
        try:
            if isinstance(date_str, str):
                if len(date_str) == 4:
                    return int(date_str)
                else:
                    date_obj = pd.to_datetime(date_str, errors='coerce')
                    if pd.isnull(date_obj):
                        year_match = re.search(r'\d{4}', date_str)
                        if year_match:
                            return int(year_match.group())
                        else:
                            return np.nan
                    else:
                        return date_obj.year
            else:
                return np.nan
        except:
            return np.nan
    
    df_clean['year'] = df_clean['publish_time'].apply(extract_year)
    df_clean = df_clean.dropna(subset=['year'])
    df_clean['year'] = df_clean['year'].astype(int)
    df_clean['journal'] = df_clean['journal'].fillna('Unknown')
    df_clean['authors'] = df_clean['authors'].fillna('Unknown authors')
    df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))
    df_clean['title_word_count'] = df_clean['title'].apply(lambda x: len(str(x).split()))
    
    return df_clean

df = load_data()

# Sidebar
st.sidebar.title("CORD-19 Data Explorer")
st.sidebar.write("Filter the data to customize the visualizations")

# Year range selector
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Journal selector
journals = ['All'] + sorted(df['journal'].unique().tolist())
selected_journal = st.sidebar.selectbox("Select journal", journals)

# Apply filters
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
if selected_journal != 'All':
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

# Main content
st.title("CORD-19 Research Dataset Analysis")
st.write("""
This interactive dashboard explores the CORD-19 dataset, which contains metadata about COVID-19 research papers.
Use the filters in the sidebar to customize the visualizations.
""")

# Display dataset info
st.header("Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Papers", df.shape[0])
col2.metric("Years Covered", f"{min_year} - {max_year}")
col3.metric("Unique Journals", df['journal'].nunique())

st.write(f"Filtered dataset: {filtered_df.shape[0]} papers")

# Visualizations
st.header("Visualizations")

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(year_counts.index, year_counts.values)
ax.set_title('Number of Publications by Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Publications')
plt.xticks(rotation=45)
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
ax.set_title('Top 10 Journals by Number of Publications')
ax.set_xlabel('Number of Publications')
st.pyplot(fig)

# Word cloud
st.subheader("Word Cloud of Paper Titles")
all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
ax.set_title('Word Cloud of Paper Titles')
st.pyplot(fig)

# Abstract word count distribution
st.subheader("Abstract Word Count Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_df['abstract_word_count'], bins=50, kde=True, ax=ax)
ax.set_title('Distribution of Abstract Word Count')
ax.set_xlabel('Word Count')
ax.set_xlim(0, 500)
st.pyplot(fig)

# Sample data
st.header("Sample Data")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head(10))

# Footer
st.markdown("---")
st.markdown("CORD-19 Dataset from [Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)")
