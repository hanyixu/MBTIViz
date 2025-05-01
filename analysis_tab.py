import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

from map_tab import (
    load_and_process_data,
    calculate_global_stats,
    get_temperament,
    temperament_colors,
    type_colors,
    temperament_groups,
    temperament_descriptions
)


def create_country_comparison(df, countries, feature_type='temperament'):
    if df is None or df.empty or not countries:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            height=400
        )
        return fig

    filtered_df = df[df['country'].isin(countries)]

    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Selected countries not found in dataset",
            height=400
        )
        return fig

    if feature_type == 'temperament':
        fig = go.Figure()

        temp_cols = {
            'NF': 'temperament_nf',
            'NT': 'temperament_nt',
            'SP': 'temperament_sp',
            'SJ': 'temperament_sj'
        }

        for country in filtered_df['country'].unique():
            country_data = filtered_df[filtered_df['country'] == country].iloc[0]

            fig.add_trace(go.Bar(
                x=list(temp_cols.keys()),
                y=[country_data[col] for col in temp_cols.values()],
                name=country,
                marker_color=[temperament_colors[t] for t in temp_cols.keys()],
                opacity=0.7
            ))

        if 'global_stats' in st.session_state and 'Global Average' in countries:
            global_temps = st.session_state.global_stats['temperaments']

            fig.add_trace(go.Bar(
                x=list(temp_cols.keys()),
                y=[global_temps.get(t, 0) for t in temp_cols.keys()],
                name="Global Average",
                marker_color=[temperament_colors[t] for t in temp_cols.keys()],
                opacity=0.4,
                marker_pattern_shape="x"
            ))

        fig.update_layout(
            barmode='group',
            xaxis_title="Temperament",
            yaxis_title="Percentage (%)",
            title="Temperament Distribution Comparison",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=20, r=20, t=50, b=80),
            height=500
        )

    elif feature_type == 'personality_traits':

        categories = ['Extraversion', 'Intuition', 'Thinking', 'Judging']
        fig = go.Figure()

        for country in filtered_df['country'].unique():
            country_data = filtered_df[filtered_df['country'] == country].iloc[0]

            e_percent = 0
            n_percent = 0
            t_percent = 0
            j_percent = 0

            total_percent = 0
            for col in filtered_df.columns:
                if col.startswith('type_'):
                    type_name = col.replace('type_', '').upper()
                    percent = country_data[col]
                    total_percent += percent

                    if 'E' in type_name[0]:
                        e_percent += percent
                    if 'N' in type_name[1]:
                        n_percent += percent
                    if 'T' in type_name[2]:
                        t_percent += percent
                    if 'J' in type_name[3]:
                        j_percent += percent

            if total_percent > 0:
                values = [
                    e_percent / total_percent * 100,
                    n_percent / total_percent * 100,
                    t_percent / total_percent * 100,
                    j_percent / total_percent * 100
                ]

                categories_full = categories + ['Introversion', 'Sensing', 'Feeling', 'Perceiving']
                values_full = values + [
                    100 - values[0],
                    100 - values[1],
                    100 - values[2],
                    100 - values[3]
                ]

                fig.add_trace(go.Scatterpolar(
                    r=values_full,
                    theta=categories_full,
                    fill='toself',
                    name=country
                ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="Personality Trait Comparison",
            height=600,
            margin=dict(l=80, r=80, t=80, b=80),
        )

    else:

        data = []

        if 'global_stats' in st.session_state and 'Global Average' in countries:
            global_types = st.session_state.global_stats['types']

            type_row = {'country': 'Global Average'}
            for t, v in global_types.items():
                type_row[t] = v

            data.append(type_row)
            countries = [c for c in countries if c != 'Global Average']

        for country in filtered_df['country'].unique():
            country_data = filtered_df[filtered_df['country'] == country].iloc[0]

            type_row = {'country': country}

            for col in filtered_df.columns:
                if col.startswith('type_'):
                    type_name = col.replace('type_', '').upper()
                    type_row[type_name] = country_data[col]

            data.append(type_row)

        heatmap_df = pd.DataFrame(data)

        mbti_types = []
        for temp in ['NF', 'NT', 'SP', 'SJ']:
            mbti_types.extend(temperament_groups[temp])

        existing_types = [t for t in mbti_types if t in heatmap_df.columns]

        melt_df = pd.melt(
            heatmap_df,
            id_vars=['country'],
            value_vars=existing_types,
            var_name='type',
            value_name='percentage'
        )

        fig = px.density_heatmap(
            melt_df,
            x='type',
            y='country',
            z='percentage',
            color_continuous_scale='Viridis',
            category_orders={"type": existing_types},
            labels={'type': 'MBTI Type', 'percentage': 'Percentage (%)'}
        )

        fig.update_layout(
            title="MBTI Type Distribution by Country",
            xaxis_title="MBTI Type",
            yaxis_title="Country",
            height=400 + (len(countries) * 30),
            margin=dict(l=20, r=20, t=50, b=20),
        )

        fig.update_traces(
            text=melt_df['percentage'].round(1).astype(str) + '%',
            texttemplate='%{text}',
            textfont={'size': 10}
        )

    return fig


def create_correlation_analysis(df, analysis_type='temperament'):
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            height=400
        )
        return fig

    if analysis_type == 'temperament':
        temp_cols = ['temperament_nf', 'temperament_nt', 'temperament_sp', 'temperament_sj']

        corr_df = df[temp_cols].corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=['NF', 'NT', 'SP', 'SJ'],
            y=['NF', 'NT', 'SP', 'SJ'],
            colorscale='RdBu_r',
            zmid=0,
            text=corr_df.round(2).values,
            texttemplate='%{text}',
            colorbar=dict(title='Correlation')
        ))

        fig.update_layout(
            title="Temperament Correlation Matrix",
            height=500,
            margin=dict(l=60, r=50, t=80, b=50),
        )

    else:
        type_cols = [col for col in df.columns if col.startswith('type_')]

        if len(type_cols) > 16:
            type_cols = type_cols[:16]

        corr_df = df[type_cols].corr()

        display_cols = [col.replace('type_', '').upper() for col in type_cols]

        fig = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=display_cols,
            y=display_cols,
            colorscale='RdBu_r',
            zmid=0,
            colorbar=dict(title='Correlation')
        ))

        fig.update_layout(
            title="MBTI Type Correlation Matrix",
            height=700,
            width=700,
            margin=dict(l=60, r=50, t=80, b=50),
        )

    return fig


def create_regional_analysis(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            height=400
        )
        return fig

    regions = {
        'North America': ['United States', 'Canada', 'Mexico'],
        'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands',
                   'Sweden', 'Norway', 'Finland', 'Denmark', 'Poland', 'Switzerland',
                   'Belgium', 'Austria', 'Portugal', 'Greece', 'Ireland'],
        'East Asia': ['Japan', 'China', 'South Korea', 'Taiwan'],
        'South Asia': ['India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal'],
        'Latin America': ['Brazil', 'Argentina', 'Colombia', 'Chile', 'Peru', 'Venezuela',
                          'Ecuador', 'Cuba', 'Dominican Republic', 'Costa Rica'],
        'Middle East': ['Turkey', 'Saudi Arabia', 'Iran', 'Israel', 'United Arab Emirates',
                        'Egypt', 'Iraq', 'Jordan', 'Lebanon', 'Qatar'],
        'Africa': ['South Africa', 'Nigeria', 'Kenya', 'Morocco', 'Ghana', 'Ethiopia',
                   'Tanzania', 'Uganda', 'Zimbabwe', 'Algeria']
    }

    region_data = []

    for region, countries in regions.items():
        region_df = df[df['country'].isin(countries)]

        if len(region_df) > 0:
            region_row = {
                'region': region,
                'country_count': len(region_df),
                'NF': region_df['temperament_nf'].mean(),
                'NT': region_df['temperament_nt'].mean(),
                'SP': region_df['temperament_sp'].mean(),
                'SJ': region_df['temperament_sj'].mean()
            }

            region_data.append(region_row)

    region_df = pd.DataFrame(region_data)

    if region_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No regional data available",
            height=400
        )
        return fig

    fig = go.Figure()

    for temp in ['NF', 'NT', 'SP', 'SJ']:
        fig.add_trace(go.Bar(
            x=region_df['region'],
            y=region_df[temp],
            name=temp,
            marker_color=temperament_colors[temp]
        ))

    fig.update_layout(
        barmode='group',
        title="Temperament Distribution by Region",
        xaxis_title="Region",
        yaxis_title="Percentage (%)",
        legend_title="Temperament",
        height=500,
        margin=dict(l=60, r=50, t=80, b=50),
    )

    for i, row in region_df.iterrows():
        fig.add_annotation(
            x=row['region'],
            y=max([row['NF'], row['NT'], row['SP'], row['SJ']]) + 3,
            text=f"n={row['country_count']}",
            showarrow=False,
            font=dict(size=10)
        )

    return fig


def show_analysis_tab():
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>MBTI Data Analysis</div>", unsafe_allow_html=True)

    countries_file = 'data/countries.csv'
    types_file = 'data/types.csv'

    if 'df' not in st.session_state or 'types_info' not in st.session_state:
        with st.spinner("Loading data..."):
            df, types_info = load_and_process_data(countries_file, types_file)

            if df is None or types_info is None:
                st.error("Failed to load data. Please ensure the CSV files are in the correct location.")
                return

            global_stats = calculate_global_stats(df)

            st.session_state.df = df
            st.session_state.types_info = types_info
            st.session_state.global_stats = global_stats
    else:
        df = st.session_state.df
        types_info = st.session_state.types_info
        global_stats = st.session_state.global_stats

    analysis_type = st.radio(
        "Select Analysis Type:",
        ["Country Comparison", "Correlation Analysis", "Regional Trends"],
        horizontal=True
    )

    if analysis_type == "Country Comparison":
        st.markdown("### Compare MBTI Distributions Between Countries")

        col1, col2 = st.columns([3, 1])

        with col1:
            default_countries = ["United States", "Japan", "Global Average"]
            available_countries = ["Global Average"] + sorted(df['country'].unique())

            selected_countries = st.multiselect(
                "Select countries to compare:",
                available_countries,
                default=default_countries
            )

        with col2:
            comparison_type = st.selectbox(
                "Comparison Type:",
                ["Temperament", "Type Distribution", "Personality Traits"],
                index=0
            )

            feature_type = comparison_type.lower().replace(" ", "_")

        if selected_countries:
            comparison_fig = create_country_comparison(df, selected_countries, feature_type)
            st.plotly_chart(comparison_fig, use_container_width=True)

            if feature_type == 'temperament':
                st.markdown("""
                ### About Temperaments

                Temperaments are broader categories that group the 16 MBTI types based on shared characteristics:
                """)

                for temp, desc in temperament_descriptions.items():
                    st.markdown(
                        f"<div style='margin-bottom: 10px; padding-left: 10px; border-left: 4px solid {temperament_colors[temp]};'>",
                        unsafe_allow_html=True)
                    st.markdown(desc, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            elif feature_type == 'personality_traits':
                st.markdown("""
                ### About Personality Traits

                This radar chart shows the relative distribution of the four dichotomies in MBTI:

                - **Extraversion (E)** vs **Introversion (I)**: Where you focus your attention and get energy
                - **Intuition (N)** vs **Sensing (S)**: How you take in information and what you pay attention to
                - **Thinking (T)** vs **Feeling (F)**: How you make decisions
                - **Judging (J)** vs **Perceiving (P)**: How you organize your world

                Higher percentages indicate a stronger presence of that trait in the population.
                """)
        else:
            st.info("Please select at least one country to compare")

    elif analysis_type == "Correlation Analysis":
        st.markdown("### Correlation Analysis")

        correlation_type = st.radio(
            "Select correlation level:",
            ["Temperament Groups", "Individual MBTI Types"],
            horizontal=True
        )

        corr_type = 'temperament' if correlation_type == "Temperament Groups" else 'type'

        corr_fig = create_correlation_analysis(df, corr_type)
        st.plotly_chart(corr_fig, use_container_width=True)

        st.markdown("""
        ### Understanding Correlations

        This heatmap shows the correlation between different personality types or temperaments across countries:

        - **Positive values (blue)** indicate that when one type is common in a country, the other tends to be common too
        - **Negative values (red)** indicate that when one type is common, the other tends to be rare
        - **Values close to zero** indicate little or no relationship

        Strong correlations may suggest underlying cultural or environmental factors that influence personality distributions.
        """)

    else:
        st.markdown("### Regional Trends in MBTI Distribution")

        region_fig = create_regional_analysis(df)
        st.plotly_chart(region_fig, use_container_width=True)

        st.markdown("""
        ### Regional Patterns

        This chart shows how personality temperaments vary by geographic region. Some observations:

        - **North America and Europe** tend to have higher percentages of Intuitive types (NT and NF)
        - **East Asia** shows a preference for SJ temperaments (Guardians) 
        - **Latin America** has relatively higher proportions of SP and NF temperaments

        These variations may reflect cultural values, educational systems, and social norms that differ between regions.

        *Note: The number of countries (n) in each region is shown above each group of bars.*
        """)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    show_analysis_tab()
