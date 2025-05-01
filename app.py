import streamlit as st
import streamlit.components.v1 as components
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
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-title'>MBTI Personality Data Visualization</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Exploring how personality types vary across people, cultures and countries</p>",
            unsafe_allow_html=True)

# Display team on the left, animation on the right
col1, col2 = st.columns([1, 2])  # Adjust width ratio as needed

with col1:
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

with col2:
    components.html("""
    <div class="container" style="position: relative; width: 400px; height: 400px; margin: 0 auto;">
      <div class="center" style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 60px;
          height: 60px;
          font-size: 18px;
          font-weight: bold;
          text-align: center;
          line-height: 60px;
          border-radius: 50%;
          background: #333;
          color: #fff;
          z-index: 2;
      ">MBTI</div>
      <div class="orbit" id="orbit" style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
      "></div>
    </div>

    <script>
    const mbtiTypes = [
      'ESFP', 'ESTP', 'ESFJ', 'ENFP', 'ENFJ', 'ESTJ', 'ENTP', 'ENTJ',
      'ISTP', 'ISFP', 'ISTJ', 'ISFJ', 'INTP', 'INTJ', 'INFP', 'INFJ'
    ];

    const orbit = document.getElementById('orbit');

    mbtiTypes.forEach((type, index) => {
      const el = document.createElement('div');
      el.className = 'type';
      el.textContent = type;

      const colorMap = {
        Analysts: ['INTJ','INTP','ENTJ','ENTP'],
        Diplomats: ['INFJ','INFP','ENFJ','ENFP'],
        Sentinels: ['ISTJ','ISFJ','ESTJ','ESFJ'],
        Explorers: ['ISTP','ISFP','ESTP','ESFP']
      };

      let bgColor = '#3498db';
      if (colorMap.Analysts.includes(type)) bgColor = '#8e44ad';
      else if (colorMap.Diplomats.includes(type)) bgColor = '#27ae60';
      else if (colorMap.Sentinels.includes(type)) bgColor = '#2980b9';
      else if (colorMap.Explorers.includes(type)) bgColor = '#f1c40f';

      el.style.cssText = `
        position: absolute;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        color: white;
        text-align: center;
        line-height: 30px;
        font-size: 10px;
        font-weight: bold;
        background-color: ${bgColor};
        animation: rotate${index} ${8 + index}s linear infinite;
      `;

      orbit.appendChild(el);

      const baseRadius = 80;
      const layer = Math.floor(index / 4);
      const radius = baseRadius + layer * 25;
      const angleOffset = (Math.PI / 2) / 5;
      const angle = (index % 4) * (Math.PI / 2) + (index % 2 === 0 ? -angleOffset : angleOffset);

      const keyframes = `
        @keyframes rotate${index} {
          from {
            transform: rotate(0deg) translate(${radius * Math.cos(angle)}px, ${radius * Math.sin(angle)}px) rotate(0deg);
          }
          to {
            transform: rotate(360deg) translate(${radius * Math.cos(angle)}px, ${radius * Math.sin(angle)}px) rotate(-360deg);
          }
        }
      `;

      const styleSheet = document.styleSheets[0];
      if (styleSheet) {
        styleSheet.insertRule(keyframes, styleSheet.cssRules.length);
      } else {
        const style = document.createElement('style');
        style.innerHTML = keyframes;
        document.head.appendChild(style);
      }
    });
    </script>
    """, height=450)

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
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🌍 World Map", "📊 World Data Analysis", "☁️ Word Cloud"])

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

with tab2:
    show_map_tab()

with tab3:
    show_analysis_tab()

with tab4:
    show_nlp_data()

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Team_C_TBD | Columbia University | QMSS Program", unsafe_allow_html=True)
st.markdown("A class project for QMSS GR 5063: Data Visualization", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
