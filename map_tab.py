import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pycountry
import os

temperament_colors = {
    'NF': '#4CAF50',
    'NT': '#2196F3',
    'SP': '#FFC107',
    'SJ': '#F44336'
}

type_colors = {
    'INFJ': '#388E3C', 'INFP': '#4CAF50', 'ENFJ': '#66BB6A', 'ENFP': '#81C784',
    'INTJ': '#1565C0', 'INTP': '#1976D2', 'ENTJ': '#42A5F5', 'ENTP': '#64B5F6',
    'ISTP': '#FF8F00', 'ISFP': '#FFA000', 'ESTP': '#FFB300', 'ESFP': '#FFC107',
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
