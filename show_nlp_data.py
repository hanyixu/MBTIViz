import streamlit as st

def show_nlp_data():
    st.title("NLP Analysis of MBTI Personality Types")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3>1. MBTI Personality Type Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.components.v1.html(
            f"<div style='width: 900px;'>{open('data/NLP/mbti_distribution.html', 'r', encoding='utf-8').read()}</div>",
            height=400,
            scrolling=True
        )

    with col2:
        st.markdown("<h3>2. Text Length Distribution by MBTI Type</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.image("data/NLP/Text Length Distribution by MBTI Type.png", use_column_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<h3>3. TF-IDF Weighted WordClouds by MBTI Type</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.image("data/NLP/TF-IDF Weighted WordClouds by MBTI Type.png", use_column_width=True)

    with col4:
        st.markdown("<h3>4. 2D PCA of Balanced BERT Embeddings Grouped by MBTI Cognitive Types</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.image("data/NLP/2D PCA of Balanced BERT Embeddings Grouped by MBTI Cognitive Types.png", use_column_width=True)

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("<h3>5. Cluster Analysis Overview</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.image("data/NLP/Cluster Analysis Overview.png", use_column_width=True)

    with col6:
        st.markdown("<h3>6. MBTI Sentiment Score Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.components.v1.html(
            f"<div style='width: 900px;'>{open('data/NLP/mbti_sentiment_score_distribution.html', 'r', encoding='utf-8').read()}</div>",
            height=400,
            scrolling=True
        )
