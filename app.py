import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

st.set_page_config(
    page_title="DeDecker Keukens - Semantic Analysis",
    page_icon="🍳",
    layout="wide"
)

# Password protection
def check_password():
    """Returns True if the user has entered the correct password."""
    def password_entered():
        if st.session_state["password"] == "dedecker2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <style>
            .block-container {max-width: 400px; margin: auto; padding-top: 5rem;}
        </style>
        """, unsafe_allow_html=True)
        st.image(str(Path(__file__).parent / "dedecker-logo-1741616178.png"), width=150)
        st.markdown("### Semantic Analysis Dashboard")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <style>
            .block-container {max-width: 400px; margin: auto; padding-top: 5rem;}
        </style>
        """, unsafe_allow_html=True)
        st.image(str(Path(__file__).parent / "dedecker-logo-1741616178.png"), width=150)
        st.markdown("### Semantic Analysis Dashboard")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# DeDecker brand colors: taupe #B8A99A, dark #1a1a1a, warm white #f9f7f5
DEDECKER_TAUPE = '#B8A99A'
DEDECKER_DARK = '#2d2d2d'
DEDECKER_LIGHT = '#f9f7f5'
DEDECKER_ACCENT = '#8B7355'

st.markdown("""
<style>
    /* Hide Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {padding: 1rem 2rem; background: #f9f7f5;}
    .main-title {font-size: 1.6rem; font-weight: 600; color: #2d2d2d; margin-bottom: 0; font-family: sans-serif;}
    .subtitle {font-size: 0.9rem; color: #666; margin-bottom: 1rem;}
    .section-header {
        font-size: 1.1rem; font-weight: 600; color: #2d2d2d;
        margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
        border-bottom: 2px solid #B8A99A;
    }
    .insight-box {
        background: #f0ebe6; border-left: 4px solid #B8A99A;
        padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
        margin: 0.5rem 0; font-size: 0.9rem; color: #2d2d2d;
    }
    .warning-box {
        background: #f5e6e4; border-left: 4px solid #c9a59a;
        padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
        margin: 0.5rem 0; font-size: 0.9rem; color: #2d2d2d;
    }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e5e0db;
        border-radius: 8px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetric"] label {color: #666; font-size: 0.85rem;}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {color: #2d2d2d; font-size: 1.8rem;}
    .stDataFrame {background: white; border-radius: 8px; border: 1px solid #e5e0db;}
    section[data-testid="stSidebar"] {background: #f0ebe6;}
    .stRadio > div {gap: 0.5rem;}
    /* DeDecker style for multiselect tags */
    .stMultiSelect > div {border-color: #e5e0db;}
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #B8A99A !important;
        color: #2d2d2d !important;
    }
    .stMultiSelect span[data-baseweb="tag"] span {
        color: #2d2d2d !important;
    }
    /* Radio button accent color */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
        color: #2d2d2d;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_data(market='BENL'):
    if market == 'BENL':
        file_path = Path(__file__).parent / "Keyword_Research_DeDecker_BENL_FINAL .xlsx"
        if not file_path.exists():
            return None, {}
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            'client_pos': 'pos_dedecker',
            'client_url': 'url_dedecker',
            'has_ai_overview': 'has_ai',
            'client_in_ai': 'dedecker_in_ai',
            'client_ai_sources': 'ai_sources',
            'vika.be_pos': 'Vika',
            'dsmkeukens.be_pos': 'DSM Keukens',
            'dovykeukens.be_pos': 'Dovy',
            'diapal.be_pos': 'Diapal',
            'ilwa.be_pos': 'Ilwa'
        })
        keukens_comp = ['Vika', 'DSM Keukens', 'Dovy', 'Diapal']
        bad_comp = []
        
        # Load badkamers competitor file and merge
        bad_path = Path(__file__).parent / "Keywords_SERP_Final_badkamers_dedecker.xlsx"
        if bad_path.exists():
            df_bad = pd.read_excel(bad_path)
            df_bad.columns = df_bad.columns.str.strip()
            df_bad = df_bad.rename(columns={
                'groepwouters.be_pos': 'Groep Wouters',
                'debadbeke.be_pos': 'De Badbeke',
                'x2o.be_pos': 'X2O',
                'facq.be_pos': 'Facq',
                'vanmarcke.com_pos': 'Vanmarcke'
            })
            bad_comp = ['Groep Wouters', 'De Badbeke', 'X2O', 'Facq', 'Vanmarcke']
            bad_cols = ['keyword'] + [c for c in bad_comp if c in df_bad.columns]
            df = df.merge(df_bad[bad_cols], on='keyword', how='left')
        
        comp_map = {
            'Badkamers': [c for c in bad_comp if c in df.columns],
            'default': [c for c in keukens_comp if c in df.columns],
        }
    else:  # BEFR
        file_path = Path(__file__).parent / "Keywords_SERP_Final_FR-Dedecker.xlsx"
        if not file_path.exists():
            return None, {}
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            'client_pos': 'pos_dedecker',
            'client_url': 'url_dedecker',
            'has_ai_overview': 'has_ai',
            'client_in_ai': 'dedecker_in_ai',
            'client_ai_sources': 'ai_sources',
            'Category': 'category',
            'cuisinesdovy.be_pos': 'Dovy',
            'ixina.be_pos': 'Ixina',
            'vandenborrekitchen.be_pos': 'Vandenborre',
            'dsmcuisines.be_pos': 'DSM Cuisines'
        })
        cuisine_comp = ['Dovy', 'Ixina', 'Vandenborre', 'DSM Cuisines']
        sdb_comp = []
        
        # Load salle de bains competitor file and merge
        sdb_path = Path(__file__).parent / "Keywords_SERP_Final_salle_de_bains.xlsx"
        if sdb_path.exists():
            df_sdb = pd.read_excel(sdb_path)
            df_sdb.columns = df_sdb.columns.str.strip()
            df_sdb = df_sdb.rename(columns={
                'sanijura.be_pos': 'Sanijura',
                'mobalpa.be_pos': 'Mobalpa',
                'x2o.be_pos': 'X2O',
                'facq.be_pos': 'Facq',
                'vanmarcke.com_pos': 'Vanmarcke'
            })
            sdb_comp = ['Sanijura', 'Mobalpa', 'X2O', 'Facq', 'Vanmarcke']
            sdb_cols = ['keyword'] + [c for c in sdb_comp if c in df_sdb.columns]
            df = df.merge(df_sdb[sdb_cols], on='keyword', how='left')
        
        comp_map = {
            'Salle de bains': [c for c in sdb_comp if c in df.columns],
            'default': [c for c in cuisine_comp if c in df.columns],
        }
    
    # Add default columns if missing (e.g. BEFR SERP-only file)
    if 'volume' not in df.columns:
        df['volume'] = 0
    if 'category' not in df.columns:
        df['category'] = 'Non catégorisé'
    if 'cpc' not in df.columns:
        df['cpc'] = 0.0
    
    # Convert boolean string columns to actual booleans
    for bool_col in ['has_ai', 'dedecker_in_ai']:
        if bool_col in df.columns:
            df[bool_col] = df[bool_col].astype(str).str.lower().isin(['true', '1', 'yes', 'vrai'])
    
    # Convert cpc to numeric (handle commas as decimal separator)
    if 'cpc' in df.columns:
        df['cpc'] = df['cpc'].astype(str).str.replace(',', '.', regex=False)
        df['cpc'] = pd.to_numeric(df['cpc'], errors='coerce')
    
    # Normalize category names
    if 'category' in df.columns:
        df['category'] = df['category'].str.strip()
        df['category'] = df['category'].replace({
            'keukens': 'Keukens',
            'Intérieur & sur-mesure': 'Intérieur & Sur-mesure'
        })
    if 'subcategory' in df.columns:
        df['subcategory'] = df['subcategory'].str.strip()
    
    # All competitor columns (union of all sets)
    all_comp = list({c for comps in comp_map.values() for c in comps})
    
    # Convert position columns to numeric
    pos_cols = ['pos_dedecker'] + all_comp
    for col in pos_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Position bucket
    def get_position_bucket(pos):
        if pd.isna(pos):
            return "Not ranked"
        elif pos <= 3:
            return "Top 3"
        elif pos <= 10:
            return "4-10"
        elif pos <= 20:
            return "11-20"
        else:
            return "20+"
    
    df['position_bucket'] = df['pos_dedecker'].apply(get_position_bucket)
    
    return df, comp_map

def get_comp_for_cat(cat, comp_map):
    """Return the competitor list relevant for a given category."""
    return comp_map.get(cat, comp_map.get('default', []))

# ============================================
# HEADER with logo and market selector
# ============================================
logo_path = Path(__file__).parent / "dedecker-logo-1741616178.png"

header_col1, header_col2, header_col3 = st.columns([2, 4, 1])
with header_col3:
    market = st.selectbox("Market", ["Belgium NL", "Belgium FR"], label_visibility="collapsed")
market_code = 'BENL' if market == "Belgium NL" else 'BEFR'

df, comp_map = load_data(market_code)
if df is None:
    st.error("File not found")
    st.stop()
# All competitor columns across all categories
all_comp = list({c for comps in comp_map.values() for c in comps})

st.markdown("""
<div style="display: flex; align-items: center; gap: 1.5rem; padding: 1rem 0 1.5rem 0; border-bottom: 3px solid #B8A99A; margin-bottom: 1.5rem;">
    <img src="data:image/png;base64,{logo}" style="height: 60px; width: auto;" />
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; font-weight: 600; color: #2d2d2d;">DeDecker Keukens — Semantic Analysis</h1>
        <p style="margin: 0.2rem 0 0 0; font-size: 0.95rem; color: #666;">{market} · April 2026</p>
    </div>
</div>
""".format(
    logo=__import__('base64').b64encode(open(str(logo_path), 'rb').read()).decode(),
    market=market
), unsafe_allow_html=True)

# ============================================
# GLOBAL CATEGORY FILTER
# ============================================
_branding_cats = {'Branding', 'Marque et valeurs'}
_all_cats = [c for c in sorted(df['category'].dropna().unique().tolist()) if c not in _branding_cats]

gf1, gf2 = st.columns([1, 4])
with gf1:
    global_cat = st.selectbox("Category", ['All'] + _all_cats, key='global_cat')

# Filtered dataframe used everywhere
if global_cat == 'All':
    dff = df[~df['category'].isin(_branding_cats)].copy()
    active_comp = all_comp
else:
    dff = df[df['category'] == global_cat].copy()
    active_comp = get_comp_for_cat(global_cat, comp_map)

# ============================================
# 1. KPIs
# ============================================
total_volume = dff['volume'].sum()
total_kw = len(dff)
dedecker_ranked = int(dff['pos_dedecker'].notna().sum())
dedecker_top20 = int((dff['pos_dedecker'] <= 20).sum())
dedecker_top10 = int((dff['pos_dedecker'] <= 10).sum())
avg_pos = dff['pos_dedecker'].fillna(100).mean()
ai_presence = dff['has_ai'].sum() if 'has_ai' in dff.columns else 0
dedecker_in_ai = dff['dedecker_in_ai'].sum() if 'dedecker_in_ai' in dff.columns else 0
ai_pct = (ai_presence / total_kw * 100) if total_kw > 0 else 0
dedecker_ai_pct = (dedecker_in_ai / ai_presence * 100) if ai_presence > 0 else 0

# Position filter
pos_filter_col, kpi_cols_spacer = st.columns([2, 5])
with pos_filter_col:
    pos_range = st.radio("Position filter", ['All Ranked', 'Top 20', 'Top 10'], horizontal=True, label_visibility='collapsed')

if pos_range == 'Top 10':
    _kpi_count = dedecker_top10
    _kpi_label = 'DeDecker in Top 10'
elif pos_range == 'Top 20':
    _kpi_count = dedecker_top20
    _kpi_label = 'DeDecker in Top 20'
else:
    _kpi_count = dedecker_ranked
    _kpi_label = 'DeDecker Ranked'
_kpi_pct = (_kpi_count / total_kw * 100) if total_kw > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    st.metric("Total Volume", f"{total_volume:,}")
with kpi2:
    st.metric("Keywords", f"{total_kw}")
with kpi3:
    st.metric(_kpi_label, f"{_kpi_count}", help=f"{_kpi_pct:.1f}% of {total_kw} keywords")
with kpi4:
    st.metric("Avg Position", f"{avg_pos:.1f}" if pd.notna(avg_pos) else "N/A")
with kpi5:
    st.metric("AI Overview", f"{ai_pct:.0f}%", help=f"{int(ai_presence)} keywords with AI")
with kpi6:
    st.metric("DeDecker in AI", f"{dedecker_ai_pct:.0f}%", help=f"{int(dedecker_in_ai)} citations")

# ============================================
# 2. CATEGORY PERFORMANCE - Stacked bar position distribution
# ============================================
st.markdown('<p class="section-header">Category Performance</p>', unsafe_allow_html=True)

group_col = 'category'
df_cat_view = dff.copy()

# Calculate position distribution per category/subcategory
bucket_order = ['Top 3', '4-10', '11-20', '20+', 'Not ranked']
cat_bucket = df_cat_view.groupby([group_col, 'position_bucket']).size().reset_index(name='count')
cat_totals = df_cat_view.groupby(group_col).size().reset_index(name='total')
cat_bucket = cat_bucket.merge(cat_totals, on=group_col)
cat_bucket['pct'] = (cat_bucket['count'] / cat_bucket['total'] * 100).round(1)
cat_bucket['position_bucket'] = cat_bucket['position_bucket'].astype(str)
cat_bucket['_bucket_sort'] = cat_bucket['position_bucket'].map({b: i for i, b in enumerate(bucket_order)})
cat_bucket = cat_bucket.sort_values('_bucket_sort').drop(columns='_bucket_sort')

# Category stats for table
cat_stats = df_cat_view.groupby(group_col).agg({
    'keyword': 'count',
    'volume': 'sum'
}).rename(columns={'keyword': 'keywords'}).reset_index()

# Avg position on all keywords (not ranked = 100)
cat_avg_pos = df_cat_view.copy()
cat_avg_pos['pos_for_avg'] = cat_avg_pos['pos_dedecker'].fillna(100)
cat_avg_pos = cat_avg_pos.groupby(group_col)['pos_for_avg'].mean().reset_index(name='avg_pos')
cat_stats = cat_stats.merge(cat_avg_pos, on=group_col, how='left')

cat_top10 = df_cat_view[df_cat_view['pos_dedecker'] <= 10].groupby(group_col).size().reset_index(name='top10')
cat_stats = cat_stats.merge(cat_top10, on=group_col, how='left').fillna(0)
cat_stats['top10'] = cat_stats['top10'].astype(int)

cat_not_ranked = df_cat_view[df_cat_view['pos_dedecker'].isna()].groupby(group_col).size().reset_index(name='not_ranked')
cat_stats = cat_stats.merge(cat_not_ranked, on=group_col, how='left').fillna(0)
cat_stats['not_ranked'] = cat_stats['not_ranked'].astype(int)

chart1, chart2 = st.columns(2)

with chart1:
    # Stacked bar: position distribution by category/subcategory
    fig = px.bar(
        cat_bucket,
        x=group_col,
        y='count',
        color='position_bucket',
        color_discrete_map={
            'Top 3': '#8B7355',
            '4-10': '#B8A99A',
            '11-20': '#D4C4B5',
            '20+': '#E5DDD4',
            'Not ranked': '#c9a59a'
        },
        labels={'count': 'Keywords', group_col: '', 'position_bucket': 'Position'},
        barmode='stack'
    )
    fig.update_layout(
        height=400,
        margin=dict(l=0,r=0,t=30,b=0),
        title=dict(text="Position Distribution by Category", font=dict(size=14)),
        plot_bgcolor='white',
        legend=dict(orientation='h', y=-0.15),
        yaxis=dict(gridcolor='#f0f0f0')
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    # Category table
    cat_display = cat_stats[[group_col, 'volume', 'keywords', 'top10', 'avg_pos', 'not_ranked']].copy()
    cat_display.columns = ['Category', 'Volume', 'Keywords', 'Top 10', 'Avg Pos', 'Not Ranked']
    cat_display = cat_display.sort_values('Volume', ascending=False)
    cat_display['Avg Pos'] = cat_display['Avg Pos'].round(1)
    st.dataframe(cat_display, use_container_width=True, height=400, hide_index=True)

# ============================================
# 3. COMPETITIVE LANDSCAPE - SOV global + SOV by category
# ============================================
st.markdown('<p class="section-header">Competitive Landscape</p>', unsafe_allow_html=True)

comp1, comp2 = st.columns(2)

# Color palettes per universe
# DeDecker — signature brown
# Cuisine / Keukens — warm terracotta & sand tones
# Salle de bains / Badkamers — cool ocean blues
# Intérieur — muted sage greens
_color_map = {
    'DeDecker': '#8B7355',
    # Cuisine / Keukens
    'Vika': '#C4956A', 'DSM Keukens': '#D4A87C', 'Dovy': '#B07D56',
    'Diapal': '#D9B99B', 'Ixina': '#C48B5C', 'Vandenborre': '#DDB892',
    'DSM Cuisines': '#CB9B6A', 'Eggo': '#D1A57E', 'Kvik': '#BA8E6E',
    # Salle de bains / Badkamers
    'X2O': '#4A90A4', 'Facq': '#6AAFC3', 'Vanmarcke': '#82C0D2',
    'Groep Wouters': '#3D7A8C', 'De Badbeke': '#5B9FB3',
    'Sanijura': '#4E8FA0', 'Mobalpa': '#72B5C8',
}

# Build visibility data using filtered dff + active_comp
_vis_rows = [{'Competitor': 'DeDecker',
    'Ranked': int(dff['pos_dedecker'].notna().sum()),
    'Top 20': int((dff['pos_dedecker'] <= 20).sum()),
    'Top 10': int((dff['pos_dedecker'] <= 10).sum())}]
for c in active_comp:
    _vis_rows.append({'Competitor': c,
        'Ranked': int(dff[c].notna().sum()),
        'Top 20': int((dff[c] <= 20).sum()),
        'Top 10': int((dff[c] <= 10).sum())})
_vis_df = pd.DataFrame(_vis_rows)

with comp1:
    chart_df = _vis_df.copy()
    chart_df['Label'] = chart_df['Ranked'].astype(str) + ' / ' + str(total_kw)
    chart_df = chart_df.sort_values('Ranked', ascending=True)
    
    fig = px.bar(
        chart_df, 
        y='Competitor', 
        x='Ranked',
        orientation='h',
        text='Label',
        color='Competitor',
        color_discrete_map=_color_map
    )
    fig.update_traces(textposition='outside', cliponaxis=False)
    fig.update_layout(
        height=350, 
        margin=dict(l=0,r=80,t=30,b=0),
        title=dict(text="Share of Visibility", font=dict(size=14)),
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#f0f0f0')
    )
    st.plotly_chart(fig, use_container_width=True)

with comp2:
    # SOV by category — uses categories present in filtered data
    sov_by_cat = []
    for cat in dff['category'].dropna().unique():
        df_cat = dff[dff['category'] == cat]
        cat_total = len(df_cat)
        cat_comps = get_comp_for_cat(cat, comp_map)
        
        dd_top10 = len(df_cat[df_cat['pos_dedecker'] <= 10])
        sov_by_cat.append({'Category': cat, 'Competitor': 'DeDecker', 'Top 10 %': (dd_top10/cat_total*100) if cat_total > 0 else 0})
        
        for c in cat_comps:
            c_top10 = len(df_cat[df_cat[c] <= 10])
            sov_by_cat.append({'Category': cat, 'Competitor': c, 'Top 10 %': (c_top10/cat_total*100) if cat_total > 0 else 0})
    
    sov_cat_df = pd.DataFrame(sov_by_cat)
    
    fig = px.bar(
        sov_cat_df,
        x='Category',
        y='Top 10 %',
        color='Competitor',
        barmode='group',
        color_discrete_map=_color_map
    )
    fig.update_layout(
        height=350,
        margin=dict(l=0,r=0,t=30,b=0),
        title=dict(text="Share of Visibility by Category", font=dict(size=14)),
        plot_bgcolor='white',
        legend=dict(orientation='h', y=-0.2),
        yaxis=dict(gridcolor='#f0f0f0')
    )
    st.plotly_chart(fig, use_container_width=True)

# Visibility summary table
st.markdown("**Share of Visibility**")
_tbl = _vis_df.copy()
_tbl['Ranked %'] = (_tbl['Ranked'] / total_kw * 100).round(1).astype(str) + '%'
_tbl['Top 20 %'] = (_tbl['Top 20'] / total_kw * 100).round(1).astype(str) + '%'
_tbl['Top 10 %'] = (_tbl['Top 10'] / total_kw * 100).round(1).astype(str) + '%'
_tbl = _tbl.rename(columns={'Ranked': f'Ranked / {total_kw}', 'Top 20': f'Top 20 / {total_kw}', 'Top 10': f'Top 10 / {total_kw}'})
_tbl = _tbl[['Competitor', f'Ranked / {total_kw}', 'Ranked %', f'Top 20 / {total_kw}', 'Top 20 %', f'Top 10 / {total_kw}', 'Top 10 %']]
_tbl = _tbl.sort_values(f'Ranked / {total_kw}', ascending=False)
st.dataframe(_tbl, use_container_width=True, hide_index=True)

# Leader by category table
st.markdown("**Category Leaders**")
leader_data = []
for cat in dff['category'].dropna().unique():
    df_cat = dff[dff['category'] == cat]
    cat_total = len(df_cat)
    cat_comps = get_comp_for_cat(cat, comp_map)
    
    scores = {'DeDecker': len(df_cat[df_cat['pos_dedecker'] <= 10])}
    for c in cat_comps:
        scores[c] = len(df_cat[df_cat[c] <= 10])
    
    # Only consider as leader if someone has at least 1 position in top 10
    max_score = max(scores.values())
    if max_score == 0:
        leader = '-'
        leader_pct = 0
    else:
        leader = max(scores, key=scores.get)
        leader_pct = (scores[leader] / cat_total * 100) if cat_total > 0 else 0
    
    dedecker_pct = (scores['DeDecker'] / cat_total * 100) if cat_total > 0 else 0
    gap = leader_pct - dedecker_pct if leader != 'DeDecker' and leader != '-' else 0
    
    leader_data.append({
        'Category': cat,
        'Leader': leader,
        'Leader %': round(leader_pct, 1),
        'DeDecker %': round(dedecker_pct, 1),
        'Gap %': round(gap, 1)
    })

leader_df = pd.DataFrame(leader_data).sort_values('Gap %', ascending=False)
st.dataframe(leader_df, use_container_width=True, hide_index=True)

# ============================================
# 4. AI OVERVIEW ANALYSIS
# ============================================
st.markdown('<p class="section-header">AI Overview Analysis</p>', unsafe_allow_html=True)

ai1, ai2, ai3 = st.columns([1, 1, 2])

with ai1:
    ai_yes = int(ai_presence)
    ai_no = total_kw - ai_yes
    
    fig = px.pie(
        values=[ai_yes, ai_no], 
        names=['With AI Overview', 'Without'],
        color_discrete_sequence=['#8B7355', '#e5e0db'],
        hole=0.5
    )
    fig.update_layout(
        height=250, 
        margin=dict(l=0,r=0,t=30,b=0),
        title=dict(text=f"AI Overview ({ai_pct:.0f}%)", font=dict(size=14)),
        showlegend=True,
        legend=dict(orientation='h', y=-0.1)
    )
    fig.update_traces(textinfo='value')
    st.plotly_chart(fig, use_container_width=True)

with ai2:
    if 'dedecker_in_ai' in dff.columns:
        df_ai = dff[dff['has_ai'] == True].copy()
        cited = int(df_ai['dedecker_in_ai'].sum())
        not_cited = len(df_ai) - cited
        
        fig = px.pie(
            values=[cited, not_cited], 
            names=['DeDecker Cited', 'Not Cited'],
            color_discrete_sequence=['#8B7355', '#c9a59a'],
            hole=0.5
        )
        fig.update_layout(
            height=250, 
            margin=dict(l=0,r=0,t=30,b=0),
            title=dict(text=f"DeDecker in AI ({dedecker_ai_pct:.0f}%)", font=dict(size=14)),
            showlegend=True,
            legend=dict(orientation='h', y=-0.1)
        )
        fig.update_traces(textinfo='value')
        st.plotly_chart(fig, use_container_width=True)

with ai3:
    df_ai_table = dff[dff['has_ai'] == True][['keyword', 'volume', 'category', 'pos_dedecker', 'dedecker_in_ai']].copy()
    df_ai_table.columns = ['Keyword', 'Volume', 'Category', 'Position', 'In AI']
    df_ai_table = df_ai_table.sort_values('Volume', ascending=False)
    df_ai_table['In AI'] = df_ai_table['In AI'].apply(lambda x: 'Yes' if x else 'No')
    st.dataframe(df_ai_table, use_container_width=True, height=300, hide_index=True)

# ============================================
# 5. KEYWORD EXPLORER (with heatmap moved here)
# ============================================
st.markdown('<p class="section-header">Keyword Explorer</p>', unsafe_allow_html=True)

# Filters (category is already global)
flt1, flt2 = st.columns(2)

with flt1:
    bucket_options = ['All', 'Top 3', '4-10', '11-20', '20+', 'Not ranked']
    filter_bucket = st.selectbox("Position", bucket_options)
with flt2:
    ai_options = ['All', 'With AI Overview', 'DeDecker in AI', 'AI Gap']
    filter_ai = st.selectbox("AI Filter", ai_options)

# Apply sub-filters on already category-filtered dff
dff_explorer = dff.copy()
if filter_bucket != 'All':
    dff_explorer = dff_explorer[dff_explorer['position_bucket'] == filter_bucket]
if filter_ai == 'With AI Overview':
    dff_explorer = dff_explorer[dff_explorer['has_ai'] == True]
elif filter_ai == 'DeDecker in AI':
    dff_explorer = dff_explorer[dff_explorer['dedecker_in_ai'] == True]
elif filter_ai == 'AI Gap':
    dff_explorer = dff_explorer[(dff_explorer['has_ai'] == True) & (dff_explorer['dedecker_in_ai'] != True)]

# Legend for position colors
st.markdown("""
<div style="display: flex; gap: 1rem; margin-bottom: 0.5rem; font-size: 0.8rem;">
    <span><span style="background: #c8e6c9; padding: 2px 8px; border-radius: 3px;">1-3</span> Top 3</span>
    <span><span style="background: #dcedc8; padding: 2px 8px; border-radius: 3px;">4-10</span> Top 10</span>
    <span><span style="background: #fff9c4; padding: 2px 8px; border-radius: 3px;">11-20</span> Page 2</span>
    <span><span style="background: #ffe0b2; padding: 2px 8px; border-radius: 3px;">21-50</span> Low</span>
    <span><span style="background: #ffcdd2; padding: 2px 8px; border-radius: 3px;">50+</span> Very low</span>
    <span><span style="background: #f5f5f5; padding: 2px 8px; border-radius: 3px;">—</span> Not ranked</span>
</div>
""", unsafe_allow_html=True)

# Table with conditional coloring for positions (pastel red to green)
display_cols = ['keyword', 'volume', 'category', 'pos_dedecker']
for c in active_comp:
    if c in dff_explorer.columns:
        display_cols.append(c)
if 'has_ai' in dff_explorer.columns:
    display_cols.append('has_ai')

# Prepare dataframe for display - clean all numeric columns
df_display = dff_explorer[display_cols].sort_values('volume', ascending=False).copy()

# Convert position columns to integers (no decimals)
# Use NaN (not None) so Streamlit sorts them to the bottom
pos_cols = ['pos_dedecker'] + [c for c in active_comp if c in df_display.columns]
for col in pos_cols:
    if col in df_display.columns:
        df_display[col] = pd.to_numeric(df_display[col], errors='coerce')
        df_display[col] = df_display[col].where(df_display[col].notna(), np.nan)

# Convert volume to integer
df_display['volume'] = df_display['volume'].astype(int)

# Color function: pastel green (low position = good) to pastel red (high position = bad)
def color_position(val):
    if pd.isna(val):
        return 'background-color: #f5f5f5'  # Light gray for no rank
    val = float(val)
    if val <= 3:
        return 'background-color: #c8e6c9'  # Pastel green
    elif val <= 10:
        return 'background-color: #dcedc8'  # Light green
    elif val <= 20:
        return 'background-color: #fff9c4'  # Pastel yellow
    elif val <= 50:
        return 'background-color: #ffe0b2'  # Pastel orange
    else:
        return 'background-color: #ffcdd2'  # Pastel red

# Apply styling with format to remove decimals
styled_df = df_display.style.map(color_position, subset=pos_cols).format(
    {col: lambda x: '' if pd.isna(x) else f'{int(x)}' for col in pos_cols},
    na_rep='-'
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=400,
    hide_index=True
)

# Export
col_exp1, col_exp2 = st.columns([4, 1])
with col_exp2:
    csv = dff_explorer.to_csv(index=False).encode('utf-8')
    st.download_button("Export CSV", csv, "dedecker_keywords.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;font-size:0.8rem;'>DeDecker Keukens · Semantic Analysis · April 2026</div>", unsafe_allow_html=True)
