import streamlit as st
import os
import sys
from show_nlp_data import show_nlp_data

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from setup_data import setup_data_directory, verify_csv_structure

setup_data_directory()

from map_tab import show_map_tab
from analysis_tab import show_analysis_tab

st.set_page_config(
    page_title="MBTI Personality Distribution",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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


st.markdown("<h1 class='main-title'>MBTI Personality Data Visualization</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Exploring how personality types vary across people, cultures and countries</p>", unsafe_allow_html=True)

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
with col_right:
    import streamlit.components.v1 as components
    components.html('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MBTI Orbit Animation</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #fff;
    }
    .container {
      position: relative;
      width: 800px;
      height: 800px;
    }
    .center {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100px;
      height: 100px;
      font-size: 32px;
      font-weight: bold;
      text-align: center;
      line-height: 100px;
      border-radius: 50%;
      background: #333;
      color: #fff;
      z-index: 2;
    }
    .orbit {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
    .type {
      position: absolute;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      color: white;
      text-align: center;
      line-height: 50px;
      font-size: 14px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="center">MBTI</div>
    <div class="orbit" id="orbit"></div>
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

      // 配色按四大类
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
      el.style.backgroundColor = bgColor;

      orbit.appendChild(el);

      // 轨道半径分层，每个 MBTI 类型有不同半径
      const baseRadius = 150;
      const layer = Math.floor(index / 4);
      const radius = baseRadius + layer * 50;
      const angleOffset = (Math.PI / 2) / 5;
      const angle = (index % 4) * (Math.PI / 2) + (index % 2 === 0 ? -angleOffset : angleOffset);

      // 精确控制速度：外向快，内向慢
      const speedMap = {
        'ESFP': 1,
        'ESTP': 2,
        'ESFJ': 3,
        'ENFP': 4,
        'ENFJ': 5,
        'ESTJ': 6,
        'ENTP': 7,
        'ENTJ': 8,
        'ISTP': 9,
        'ISFP': 10,
        'ISTJ': 11,
        'ISFJ': 12,
        'INTP': 13,
        'INTJ': 14,
        'INFP': 15,
        'INFJ': 16,
      };

      const duration = speedMap[type] || 20;
      el.style.animation = `rotate${index} ${duration}s linear infinite`;

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
      styleSheet.insertRule(keyframes, styleSheet.cssRules.length);
    });
  </script>
</body>
</html>

    ''', height=340)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "🌍 World Map", "📊 World Data Analysis", "☁️ Word Cloud", "📈 Playground"])

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
    
    # Add MBTI explanation if not already present
    st.markdown("""
    The **Myers-Briggs Type Indicator (MBTI)** is a widely used personality framework that classifies individuals into **16 unique personality types** based on their preferences in four dimensions:
    - **Extraversion (E) vs. Introversion (I)** – Where you focus your attention
    - **Sensing (S) vs. Intuition (N)** – How you process information
    - **Thinking (T) vs. Feeling (F)** – How you make decisions
    - **Judging (J) vs. Perceiving (P)** – How you structure your life
    
    You can explore your own MBTI type by taking a free test here:
    👉 [Take the MBTI Test](https://www.16personalities.com/free-personality-test)
    """)
    
    # MBTI Types at a Glance
    st.markdown("""
    ### 🌟 MBTI Personality Types at a Glance:
    - **ISTJ – The Logistician**: Responsible, serious, and detail-oriented.
    - **ISFJ – The Defender**: Loyal, warm, and protective of others.
    - **INFJ – The Advocate**: Insightful, creative, and idealistic.
    - **INTJ – The Architect**: Strategic, logical, and independent.
    - **ISTP – The Virtuoso**: Practical, adventurous, and analytical.
    - **ISFP – The Adventurer**: Gentle, flexible, and artistic.
    - **INFP – The Mediator**: Empathetic, deep, and imaginative.
    - **INTP – The Logician**: Intellectual, curious, and abstract.
    - **ESTP – The Entrepreneur**: Energetic, action-oriented, and bold.
    - **ESFP – The Entertainer**: Fun-loving, spontaneous, and sociable.
    - **ENFP – The Campaigner**: Enthusiastic, expressive, and open-minded.
    - **ENTP – The Debater**: Inventive, witty, and outspoken.
    - **ESTJ – The Executive**: Organized, practical, and leadership-driven.
    - **ESFJ – The Consul**: Caring, social, and harmony-focused.
    - **ENFJ – The Protagonist**: Charismatic, inspiring, and supportive.
    - **ENTJ – The Commander**: Assertive, strategic, and goal-oriented.
    """)
    
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

with tab5:
    st.markdown("## Word Cloud Playground")
    st.write("""
    Create your own word cloud! Enter your text below and see it transformed into a beautiful visualization.
    """)
    
    user_text = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Type or paste your text here...",
        help="The more text you enter, the more interesting your word cloud will be!"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_words = st.slider("Maximum number of words", 50, 500, 200)
        background_color = st.color_picker("Background color", "#FFFFFF")
    
    with col2:
        colormap = st.selectbox(
            "Color scheme",
            ["viridis", "plasma", "inferno", "magma", "cividis"]
        )
        width = st.slider("Width", 400, 1200, 800)
    
    if user_text:
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            
            wordcloud = WordCloud(
                width=width,
                height=width//2,
                background_color=background_color,
                max_words=max_words,
                colormap=colormap
            ).generate(user_text)
            
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            
            st.download_button(
                label="Download Word Cloud",
                data=fig,
                file_name="wordcloud.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please make sure you have entered valid text.")
    else:
        st.info("👆 Enter some text above to generate your word cloud!")

st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Team_C_TBD | Columbia University | QMSS Program", unsafe_allow_html=True)
st.markdown("A class project for QMSS GR 5063: Data Visualization", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
