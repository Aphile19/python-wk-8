# CORD-19 Data Analysis

This project analyzes the CORD-19 research dataset containing metadata about COVID-19 research papers and presents the findings through an interactive Streamlit application.

## Project Structure

- `data/`: Contains the metadata.csv file (not included in repo due to size)
- `notebooks/`: Jupyter notebook with exploratory data analysis
- `app.py`: Streamlit application
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation

## Setup Instructions

1. Clone this repository
2. Download the metadata.csv file from [Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) and place it in the data/ folder
3. Create a virtual environment: `python -m venv cord19_env`
4. Activate the environment: `source cord19_env/bin/activate` (Linux/Mac) or `cord19_env\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run the Streamlit app: `streamlit run app.py`

## Key Findings

1. **Publication Trends**: COVID-19 research publications exploded in 2020, with thousands of papers published.
2. **Top Journals**: Major medical and scientific journals published the most COVID-19 research.
3. **Word Frequency**: Common terms in titles include "COVID", "pandemic", "coronavirus", and "clinical".
4. **Abstract Length**: Most abstracts are between 100-300 words.

## Challenges Faced

1. **Data Cleaning**: The publish_time column had inconsistent formats that required careful processing.
2. **Memory Management**: The dataset is large, requiring efficient memory usage in the Streamlit app.
3. **Visualization Optimization**: Creating informative visualizations that load quickly in the web app.

## Learning Outcomes

1. Gained experience with cleaning and preprocessing real-world data
2. Practiced creating interactive visualizations with Streamlit
3. Improved skills in data analysis and presentation
4. Learned to handle large datasets efficiently

## Future Enhancements

1. Add topic modeling to identify research themes
2. Incorporate natural language processing for deeper text analysis
3. Add more interactive filters and visualizations
4. Implement a search functionality for papers
