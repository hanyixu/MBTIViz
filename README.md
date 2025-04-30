# MBTI World Distribution Visualization

## Overview
This project visualizes the global distribution of Myers-Briggs Type Indicator (MBTI) personality types across different countries and cultures. The interactive dashboard allows users to explore personality type distributions, compare countries, and discover patterns in how personality traits vary worldwide.

## Team DataMind
Created by Team DataMind for the Quantitative Methods in the Social Sciences program at Columbia University.

## Features
- Interactive world map showing dominant personality types and temperaments by country
- Country comparison tool for analyzing personality type distributions
- Detailed breakdown of MBTI types, temperaments, and their global distributions
- Insights into cultural and regional patterns in personality type distribution

## Project Structure
- `app.py` - Main application file with the Streamlit dashboard
- `map_tab.py` - Module containing the map visualization functionality
- `analysis_tab.py` - Module containing data analysis visualizations
- `setup_data.py` - Helper script for setting up the data directory
- `requirements.txt` - List of required Python packages
- `data/` - Directory containing the dataset files:
  - `countries.csv` - MBTI data by country
  - `types.csv` - MBTI type descriptions and attributes

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone this repository:
```
git clone https://github.com/your-username/mbti-visualization.git
cd mbti-visualization
```

2. Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Create a data directory and place your CSV files:
```
mkdir -p data
# Place countries.csv and types.csv in the data directory
```

5. Run the Streamlit app:
```
streamlit run app.py
```

## Data Sources
The data used in this project is based on self-reported MBTI test results from 158 countries. The dataset includes:
- Distribution of all 16 MBTI types across countries
- Variant distributions (Assertive vs. Turbulent)
- Temperament group distributions (NF, NT, SP, SJ)

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- Pycountry

## Future Enhancements
- Adding demographic analysis by age and gender
- Incorporating time-series data to show changes in personality distributions over time
- Adding correlation analysis with cultural and socioeconomic factors
- Implementing machine learning to predict personality type distributions based on various country-level factors

## License
[Specify your license here]

## Acknowledgments
- MBTI theory and type descriptions based on the work of Isabel Briggs Myers and Katharine Cook Briggs
- [Add any other acknowledgments]
