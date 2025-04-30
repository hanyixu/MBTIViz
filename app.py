import streamlit as st
import os
import sys
from show_nlp_data import show_nlp_data

# Add the current directory to the path so we can import from local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import data setup functionality
from setup_data import setup_data_directory, verify_csv_structure

# Setup data directory and ensure CSV files are in the right location
setup_data_directory()

# Import tab modules
from map_tab import show_map_tab
from analysis_tab import show_analysis_tab

# Set page configuration
st.set_page_config(
    page_title="MBTI Personality Distribution",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #333;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6B46C1;
        text-align: center;
        margin-bottom: 0;
        padding-top: 1rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #656565;
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .team-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4B5563;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .team-members-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        width: 100%;
        background-color: #f8f9fa; /* Match the team-section background */
    }

    .team-member {
        text-align: center;
        padding: 15px;
        flex: 1;
        min-width: 150px;
    }
    
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-title'>MBTI Personality Data Visualization</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Exploring how personality types vary across people, cultures and countries</p>", unsafe_allow_html=True)

# Team information
st.markdown("<h2 class='team-title'>Team Members</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='team-members-container'>
    <div class='team-member'>
        <h3>Burui Chen</h3>
    </div>
    <div class='team-member'>
        <h3>Hanyi Xu</h3>
    </div>
    <div class='team-member'>
        <h3>Min Zhuang</h3>
    </div>
    <div class='team-member'>
        <h3>Xiaorong Yu</h3>
    </div>
</div>
""", unsafe_allow_html=True)


# Project description
st.markdown("## Project Overview")
st.write("""
The Myers-Briggs Type Indicator (MBTI) is one of the most widely used personality assessments in the world, 
categorizing people into 16 distinct personality types based on psychological preferences in how people perceive 
the world and make decisions.

Our project explores how these personality types are distributed globally, examining patterns and trends across 
different countries and cultures. By visualizing MBTI data on a world map and conducting comparative analyses, 
we aim to uncover insights about personality diversity around the world.

### Key Questions Explored:
- How do personality types vary by geographic region?
- Which countries share similar personality distributions?
- Are there correlations between cultural factors and personality trends?
- What is the global distribution of the four temperament groups (NF, NT, SP, SJ)?

This interactive dashboard allows you to explore these questions and discover patterns in personality distribution 
across the globe.
""")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🌍 World Map", "📊 World Data Analysis", "Word Cloud"])

with tab1:
    st.markdown("## Welcome to the MBTI World Distribution Dashboard")
    st.write("""
    This dashboard provides interactive visualizations of Myers-Briggs Type Indicator (MBTI) 
    personality distributions across different countries worldwide.
    
    ### How to Use This Dashboard:
    1. Navigate through the tabs above to explore different visualizations
    2. Use the **World Map** tab to see global distributions of personality types
    3. Explore the **Data Analysis** tab for deeper insights and comparisons
    
    The data in this dashboard is based on a comprehensive collection of self-reported MBTI test 
    results from 158 countries, allowing for a global comparison of personality traits.
    """)
    
    # Sample key findings
    st.markdown("### Key Findings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Regional Patterns**: Northern European countries show higher percentages of introverted intuitive types
        - **Cultural Connections**: Related cultures often display similar personality distributions
        - **Global Trends**: Some personality types have significantly higher representation worldwide
        """)
    
    # with col2:
    #     st.image("image/sample_viz.png", caption="Sample visualization")

with tab2:
    # Call the map tab function from the imported module
    show_map_tab()
    
with tab3:
    # Call the analysis tab function from the imported module
    show_analysis_tab()
    
with tab4:
    show_nlp_data()

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Team_C_TBD | Columbia University | QMSS Program", unsafe_allow_html=True)
st.markdown("A class project for QMSS GR 5063: Data Visualization", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
