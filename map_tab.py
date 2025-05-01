import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pycountry
import os

# Define color schemes
temperament_colors = {
    'NF': '#4CAF50',  # Green for Idealists
    'NT': '#2196F3',  # Blue for Rationals
    'SP': '#FFC107',  # Amber for Artisans
    'SJ': '#F44336'  # Red for Guardians
}

type_colors = {
    # NF group - Green shades
    'INFJ': '#388E3C', 'INFP': '#4CAF50', 'ENFJ': '#66BB6A', 'ENFP': '#81C784',
    # NT group - Blue shades
    'INTJ': '#1565C0', 'INTP': '#1976D2', 'ENTJ': '#42A5F5', 'ENTP': '#64B5F6',
    # SP group - Amber shades
    'ISTP': '#FF8F00', 'ISFP': '#FFA000', 'ESTP': '#FFB300', 'ESFP': '#FFC107',
    # SJ group - Red shades
    'ISTJ': '#C62828', 'ISFJ': '#D32F2F', 'ESTJ': '#E53935', 'ESFJ': '#F44336'
}

variant_colors = {
    'A': '#9C27B0',
    'T': '#FF5722'
}

temperament_groups = {
    'NF': ['INFJ', 'INFP', 'ENFJ', 'ENFP'],
    'NT': ['INTJ', 'INTP', 'ENTJ', 'ENTP'],
    'SP': ['ISTP', 'ISFP', 'ESTP', 'ESFP'],
    'SJ': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']
}

temperament_descriptions = {
    'NF': "**Idealists (NF)** are abstract and cooperative. They focus on personal growth, relationships, and meaningful connections.",
    'NT': "**Rationals (NT)** are abstract and utilitarian. They value competence, logic, and strategic problem-solving.",
    'SP': "**Artisans (SP)** are concrete and utilitarian. They focus on the present moment, freedom, and practical skills.",
    'SJ': "**Guardians (SJ)** are concrete and cooperative. They value stability, tradition, and fulfilling responsibilities."
}


def get_temperament(mbti_type):
    base_type = mbti_type.split('-')[0] if '-' in mbti_type else mbti_type
    for temp, types in temperament_groups.items():
        if base_type in types:
            return temp
    return None


def get_country_code(country_name):
    try:
        special_cases = {
            'United States': 'USA',
            'Russia': 'RUS',
            'South Korea': 'KOR',
            'United Kingdom': 'GBR',
            'Czech Republic': 'CZE'
        }

        if country_name in special_cases:
            return special_cases[country_name]

        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_3

        countries = pycountry.countries.search_fuzzy(country_name)
        if countries:
            return countries[0].alpha_3
    except:
        pass

    return None


@st.cache_data
def load_and_process_data(countries_path, types_path):
    if not os.path.exists(countries_path):
        st.error(f"File not found: {countries_path}")
        return None, None

    if not os.path.exists(types_path):
        st.error(f"File not found: {types_path}")
        return None, None

    try:
        countries_df = pd.read_csv(countries_path)
        types_df = pd.read_csv(types_path)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

    mbti_cols = [col for col in countries_df.columns if col != 'Country']

    results = []

    for _, row in countries_df.iterrows():
        country_name = row['Country']
        country_code = get_country_code(country_name)

        if not country_code:
            continue

        temperaments = {'NF': 0, 'NT': 0, 'SP': 0, 'SJ': 0}
        variants = {'A': 0, 'T': 0}
        types = {}

        total = 0
        for col in mbti_cols:
            if not pd.isna(row[col]):
                total += row[col]

        if total == 0:
            continue

        for col in mbti_cols:
            if pd.isna(row[col]) or row[col] == 0:
                continue

            parts = col.split('-')
            if len(parts) != 2:
                continue

            base_type, variant = parts
            value = row[col]

            if base_type not in types:
                types[base_type] = 0
            types[base_type] += value

            if variant in variants:
                variants[variant] += value

            temp = get_temperament(base_type)
            if temp:
                temperaments[temp] += value

        dominant_type = max(types.items(), key=lambda x: x[1])[0] if types else ""
        dominant_temp = max(temperaments.items(), key=lambda x: x[1])[0] if temperaments else ""

        type_percentages = {t: (v / total) * 100 for t, v in types.items()}
        temp_percentages = {t: (v / total) * 100 for t, v in temperaments.items()}
        variant_percentages = {v: (val / total) * 100 for v, val in variants.items()}

        result = {
            'country': country_name,
            'country_code': country_code,
            'dominant_type': dominant_type,
            'dominant_temperament': dominant_temp,
            'temperament_nf': temp_percentages.get('NF', 0),
            'temperament_nt': temp_percentages.get('NT', 0),
            'temperament_sp': temp_percentages.get('SP', 0),
            'temperament_sj': temp_percentages.get('SJ', 0),
            'variant_a': variant_percentages.get('A', 0),
            'variant_t': variant_percentages.get('T', 0)
        }

        for t, v in type_percentages.items():
            result[f'type_{t.lower()}'] = v

        results.append(result)

    types_info = {}
    for _, row in types_df.iterrows():
        mbti_type = row['Type']
        if pd.isna(mbti_type) or not mbti_type:
            continue

        types_info[mbti_type] = {
            'nickname': row.get('Nickname', ''),
            'description': row.get('Description', ''),
            'e_i': 'Extraverted' if row.get('E') == 1 else 'Introverted',
            'n_s': 'Intuitive' if row.get('N') == 1 else 'Sensing',
            't_f': 'Thinking' if row.get('T') == 1 else 'Feeling',
            'j_p': 'Judging' if row.get('J') == 1 else 'Prospecting',
            'temperament': get_temperament(mbti_type)
        }

    return pd.DataFrame(results), types_info


@st.cache_data
def calculate_global_stats(df):
    if df is None or df.empty:
        return {
            'temperaments': {'NF': 0, 'NT': 0, 'SP': 0, 'SJ': 0},
            'types': {},
            'variants': {'A': 0, 'T': 0}
        }

    global_stats = {
        'temperaments': {},
        'types': {},
        'variants': {}
    }

    for temp in ['NF', 'NT', 'SP', 'SJ']:
        col_name = f'temperament_{temp.lower()}'
        if col_name in df.columns:
            global_stats['temperaments'][temp] = float(df[col_name].mean())
        else:
            global_stats['temperaments'][temp] = 0.0

    type_cols = [col for col in df.columns if col.startswith('type_')]
    for col in type_cols:
        type_name = col.replace('type_', '').upper()
        if col in df.columns:
            global_stats['types'][type_name] = float(df[col].mean())
        else:
            global_stats['types'][type_name] = 0.0

    if 'variant_a' in df.columns:
        global_stats['variants']['A'] = float(df['variant_a'].mean())
    else:
        global_stats['variants']['A'] = 0.0

    if 'variant_t' in df.columns:
        global_stats['variants']['T'] = float(df['variant_t'].mean())
    else:
        global_stats['variants']['T'] = 0.0

    return global_stats


def create_world_map(df, color_by='dominant_temperament', selected_country=None):
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            height=600
        )
        return fig

    if color_by == 'dominant_temperament':
        fig = px.choropleth(
            df,
            locations='country_code',
            color='dominant_temperament',
            color_discrete_map=temperament_colors,
            hover_name='country',
            title='',
            labels={'dominant_temperament': 'Dominant Temperament'},
            hover_data={
                'dominant_type': True,
                'country_code': False
            }
        )
    elif color_by == 'dominant_type':
        type_color_map = {t: type_colors.get(t, '#808080') for t in df['dominant_type'].unique()}

        fig = px.choropleth(
            df,
            locations='country_code',
            color='dominant_type',
            color_discrete_map=type_color_map,
            hover_name='country',
            title='',
            labels={'dominant_type': 'Dominant Type'},
            hover_data={
                'dominant_temperament': True,
                'country_code': False
            }
        )

    if selected_country:
        selected_row = df[df['country'] == selected_country]
        if not selected_row.empty:
            selected_code = selected_row.iloc[0]['country_code']
            fig.add_trace(
                go.Choropleth(
                    locations=[selected_code],
                    z=[1],
                    colorscale=[[0, 'rgba(255,255,255,0)'], [1, 'rgba(255,255,255,0.5)']],
                    showscale=False,
                    hoverinfo='skip',
                    marker_line_color='white',
                    marker_line_width=2
                )
            )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            showland=True,
            landcolor='rgba(240, 240, 240, 1)',
            showcountries=True,
            countrycolor='rgba(200, 200, 200, 0.5)',
            oceancolor='rgba(230, 250, 255, 1)',
        ),
        autosize=True,
        height=600,
    )

    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>%{z}<extra></extra>'
    )

    return fig


def create_temperament_chart(data, chart_type='pie'):
    if data is None:
        return go.Figure()

    if isinstance(data, dict):
        temp_data = data
    elif isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        temp_data = {
            'NF': data.get('temperament_nf', 0),
            'NT': data.get('temperament_nt', 0),
            'SP': data.get('temperament_sp', 0),
            'SJ': data.get('temperament_sj', 0)
        }
    else:
        temp_data = {'NF': 0, 'NT': 0, 'SP': 0, 'SJ': 0}

    if chart_type == 'pie':
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(temp_data.keys()),
                    values=list(temp_data.values()),
                    hole=0.4,
                    marker_colors=[temperament_colors[t] for t in temp_data.keys()],
                    textinfo='percent+label',
                    textfont_size=14,
                    hoverinfo='label+percent+value',
                    hovertemplate='<b>%{label}</b><br>%{percent}<br>Value: %{value:.1f}%<extra></extra>'
                )
            ]
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=350,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            title={
                'text': 'Temperament Distribution',
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18}
            }
        )
    else:  # bar chart
        sorted_data = sorted(temp_data.items(), key=lambda x: x[1], reverse=True)
        fig = go.Figure(
            data=[
                go.Bar(
                    x=[item[0] for item in sorted_data],
                    y=[item[1] for item in sorted_data],
                    marker_color=[temperament_colors[item[0]] for item in sorted_data],
                    text=[f"{item[1]:.1f}%" for item in sorted_data],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>%{y:.1f}%<extra></extra>'
                )
            ]
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=350,
            xaxis_title="Temperament",
            yaxis_title="Percentage (%)",
            title={
                'text': 'Temperament Distribution',
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18}
            }
        )

    return fig


def show_map_tab():
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>MBTI World Distribution Map</div>", unsafe_allow_html=True)

    countries_file = 'data/countries.csv'
    types_file = 'data/types.csv'

    with st.spinner("Loading data..."):
        df, types_info = load_and_process_data(countries_file, types_file)

        if df is None or types_info is None:
            st.error("""
            Failed to load data. Please ensure the CSV files are in the correct location.

            For testing purposes, you can download the files from your GitHub repository or use sample data.
            """)

            if st.button("Use Sample Data"):
                st.info("Using sample data for demonstration. The visualization will be limited.")
                st.markdown("Sample data visualization would appear here.")
                return
            return

        global_stats = calculate_global_stats(df)

        if 'df' not in st.session_state:
            st.session_state.df = df
        if 'types_info' not in st.session_state:
            st.session_state.types_info = types_info
        if 'global_stats' not in st.session_state:
            st.session_state.global_stats = global_stats

    col1, col2 = st.columns([3, 1])

    with col1:
        map_view = st.radio(
            "Map visualization:",
            ["Dominant Temperament", "Dominant Type"],
            horizontal=True,
            key="map_view"
        )

        color_by = map_view.lower().replace(" ", "_")

    with col2:
        show_selected = st.checkbox("Highlight Selected Country", value=False, key="show_selected")

        selected_country = None
        if show_selected:
            selected_country = st.selectbox(
                "Select a country:",
                sorted(df['country'].unique()),
                key="selected_country_highlight"
            )

    map_fig = create_world_map(df, color_by=color_by, selected_country=selected_country if show_selected else None)

    st.plotly_chart(map_fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("### Select a country to explore")
    country_select = st.selectbox(
        "Choose a country:",
        sorted(df['country'].unique()),
        key="country_details_selector"
    )

    if country_select:
        country_data = df[df['country'] == country_select].iloc[0]

        st.markdown(f"<div class='card-title'>Selected Country: {country_select}</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>Dominant Type</div>", unsafe_allow_html=True)

            dominant_type = country_data['dominant_type']
            st.markdown(
                f"<h2 style='text-align: center; color: {type_colors.get(dominant_type, '#808080')};'>{dominant_type}</h2>",
                unsafe_allow_html=True)

            if dominant_type in types_info:
                st.markdown(f"<p style='text-align: center;'><i>{types_info[dominant_type]['nickname']}</i></p>",
                            unsafe_allow_html=True)
                st.markdown(f"<p>{types_info[dominant_type]['description']}</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>Temperament Distribution</div>", unsafe_allow_html=True)

            temp_chart = create_temperament_chart(country_data)
            st.plotly_chart(temp_chart, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>A/T Variant Distribution</div>", unsafe_allow_html=True)

            variant_data = {
                'A': country_data['variant_a'],
                'T': country_data['variant_t']
            }

            st.markdown(f"""
            <div style='text-align: center; margin-top: 30px;'>
                <div style='font-size: 1.8rem; color: {variant_colors['A']}; margin-bottom: 10px;'>
                    Assertive: {variant_data['A']:.1f}%
                </div>
                <div style='font-size: 1.8rem; color: {variant_colors['T']}; margin-bottom: 10px;'>
                    Turbulent: {variant_data['T']:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    show_map_tab()


