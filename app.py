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
        file_path = Path(__file__).parent / "Keyword Analysis_ DeDecker Keukens _ 202603.xlsx"
        if not file_path.exists():
            return None, []
        df = pd.read_excel(file_path, sheet_name='BENL')
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            'Positions DeDecker': 'pos_dedecker',
            'URL DeDecker': 'url_dedecker',
            'Presence AI_Overview': 'has_ai',
            'Presence AI_Overview DeDecker': 'dedecker_in_ai',
            'Sources AI_Overview_DeDecker': 'ai_sources'
        })
        competitors = ['Eggo', 'Ixina', 'Kvik', 'Dovy']
    else:  # BEFR
        file_path = Path(__file__).parent / "Keyword_Research_DeDecker_BEFR.xlsx"
        if not file_path.exists():
            return None, []
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            'client_pos': 'pos_dedecker',
            'client_url': 'url_dedecker',
            'has_ai_overview': 'has_ai',
            'client_in_ai': 'dedecker_in_ai',
            'client_ai_sources': 'ai_sources',
            'eggo.be_pos': 'Eggo',
            'ixina.be_pos': 'Ixina',
            'kvik.be_pos': 'Kvik',
            'cuisinesdovy.be_pos': 'Dovy'
        })
        competitors = ['Eggo', 'Ixina', 'Kvik', 'Dovy']
    
    # Normalize category names
    if 'category' in df.columns:
        df['category'] = df['category'].str.strip()
        df['category'] = df['category'].replace({'keukens': 'Keukens'})
    if 'subcategory' in df.columns:
        df['subcategory'] = df['subcategory'].str.strip()
    
    for col in ['pos_dedecker', 'Eggo', 'Ixina', 'Kvik', 'Dovy']:
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
    available_comp = [c for c in competitors if c in df.columns]
    
    return df, available_comp

# ============================================
# HEADER with logo and market selector
# ============================================
logo_path = Path(__file__).parent / "dedecker-logo-1741616178.png"

header_col1, header_col2, header_col3 = st.columns([2, 4, 1])
with header_col3:
    market = st.selectbox("Market", ["Belgium NL", "Belgium FR"], label_visibility="collapsed")
market_code = 'BENL' if market == "Belgium NL" else 'BEFR'

df, available_comp = load_data(market_code)
if df is None:
    st.error("File not found")
    st.stop()

st.markdown("""
<div style="display: flex; align-items: center; gap: 1.5rem; padding: 1rem 0 1.5rem 0; border-bottom: 3px solid #B8A99A; margin-bottom: 1.5rem;">
    <img src="data:image/png;base64,{logo}" style="height: 60px; width: auto;" />
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; font-weight: 600; color: #2d2d2d;">DeDecker Keukens — Semantic Analysis</h1>
        <p style="margin: 0.2rem 0 0 0; font-size: 0.95rem; color: #666;">{market} · March 2026</p>
    </div>
</div>
""".format(
    logo=__import__('base64').b64encode(open(str(logo_path), 'rb').read()).decode(),
    market=market
), unsafe_allow_html=True)

# ============================================
# 1. KPIs (original 6 cards)
# ============================================
total_volume = df['volume'].sum()
total_kw = len(df)
dedecker_top10 = len(df[df['pos_dedecker'] <= 10])
# Avg position on ALL keywords (not ranked = 100)
avg_pos = df['pos_dedecker'].fillna(100).mean()
ai_presence = df['has_ai'].sum() if 'has_ai' in df.columns else 0
dedecker_in_ai = df['dedecker_in_ai'].sum() if 'dedecker_in_ai' in df.columns else 0
ai_pct = (ai_presence / total_kw * 100) if total_kw > 0 else 0
dedecker_ai_pct = (dedecker_in_ai / ai_presence * 100) if ai_presence > 0 else 0
sov = (dedecker_top10 / total_kw * 100) if total_kw > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    st.metric("Total Volume", f"{total_volume:,}")
with kpi2:
    st.metric("Keywords", f"{total_kw}")
with kpi3:
    st.metric("Keywords in Top 10", f"{dedecker_top10}", help=f"{dedecker_top10/total_kw*100:.1f}% of total")
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

# Toggle and filter for category view
cat_col1, cat_col2 = st.columns([1, 3])
with cat_col1:
    view_level = st.radio("View by", ["Categories", "Subcategories"], horizontal=True)
with cat_col2:
    if view_level == "Categories":
        cat_filter_options = ['All'] + sorted(df['category'].dropna().unique().tolist())
        selected_cats = st.multiselect("Filter categories", cat_filter_options, default=['All'])
    else:
        subcat_filter_options = ['All'] + sorted(df['subcategory'].dropna().unique().tolist())
        selected_cats = st.multiselect("Filter subcategories", subcat_filter_options, default=['All'])

# Determine grouping column
group_col = 'category' if view_level == "Categories" else 'subcategory'

# Filter data if needed
df_cat_view = df.copy()
if 'All' not in selected_cats and len(selected_cats) > 0:
    df_cat_view = df_cat_view[df_cat_view[group_col].isin(selected_cats)]

# Calculate position distribution per category/subcategory
bucket_order = ['Top 3', '4-10', '11-20', '20+', 'Not ranked']
cat_bucket = df_cat_view.groupby([group_col, 'position_bucket']).size().reset_index(name='count')
cat_totals = df_cat_view.groupby(group_col).size().reset_index(name='total')
cat_bucket = cat_bucket.merge(cat_totals, on=group_col)
cat_bucket['pct'] = (cat_bucket['count'] / cat_bucket['total'] * 100).round(1)
cat_bucket['position_bucket'] = pd.Categorical(cat_bucket['position_bucket'], categories=bucket_order, ordered=True)

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
        category_orders={'position_bucket': bucket_order},
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
    col_name = 'Category' if view_level == "Categories" else 'Subcategory'
    cat_display.columns = [col_name, 'Volume', 'Keywords', 'Top 10', 'Avg Pos', 'Not Ranked']
    cat_display = cat_display.sort_values('Volume', ascending=False)
    cat_display['Avg Pos'] = cat_display['Avg Pos'].round(1)
    st.dataframe(cat_display, use_container_width=True, height=400, hide_index=True)

# ============================================
# 3. COMPETITIVE LANDSCAPE - SOV global + SOV by category
# ============================================
st.markdown('<p class="section-header">Competitive Landscape</p>', unsafe_allow_html=True)

comp1, comp2 = st.columns(2)

with comp1:
    # Global SOV (Top 10 presence)
    visibility_data = [{'Competitor': 'DeDecker', 'Top 10': dedecker_top10, 'Share': sov}]
    for c in available_comp:
        count = len(df[df[c] <= 10])
        pct = (count / total_kw * 100) if total_kw > 0 else 0
        visibility_data.append({'Competitor': c, 'Top 10': count, 'Share': pct})
    
    vis_df = pd.DataFrame(visibility_data).sort_values('Top 10', ascending=True)
    
    fig = px.bar(
        vis_df, 
        y='Competitor', 
        x='Top 10',
        orientation='h',
        text='Share',
        color='Competitor',
        color_discrete_map={'DeDecker': '#8B7355', 'Eggo': '#B8A99A', 'Ixina': '#D4C4B5', 'Kvik': '#a39485', 'Dovy': '#c9b8a8'}
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        height=300, 
        margin=dict(l=0,r=0,t=30,b=0),
        title=dict(text="Global Share of Visibility (Top 10)", font=dict(size=14)),
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#f0f0f0')
    )
    st.plotly_chart(fig, use_container_width=True)

with comp2:
    # SOV by category (grouped bar)
    sov_by_cat = []
    for cat in df['category'].dropna().unique():
        df_cat = df[df['category'] == cat]
        cat_total = len(df_cat)
        
        # DeDecker
        dd_top10 = len(df_cat[df_cat['pos_dedecker'] <= 10])
        sov_by_cat.append({'Category': cat, 'Competitor': 'DeDecker', 'Top 10 %': (dd_top10/cat_total*100) if cat_total > 0 else 0})
        
        # Competitors
        for c in available_comp:
            c_top10 = len(df_cat[df_cat[c] <= 10])
            sov_by_cat.append({'Category': cat, 'Competitor': c, 'Top 10 %': (c_top10/cat_total*100) if cat_total > 0 else 0})
    
    sov_cat_df = pd.DataFrame(sov_by_cat)
    
    fig = px.bar(
        sov_cat_df,
        x='Category',
        y='Top 10 %',
        color='Competitor',
        barmode='group',
        color_discrete_map={'DeDecker': '#8B7355', 'Eggo': '#B8A99A', 'Ixina': '#D4C4B5', 'Kvik': '#a39485', 'Dovy': '#c9b8a8'}
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

# Leader by category table
st.markdown("**Category Leaders**")
leader_data = []
for cat in df['category'].dropna().unique():
    df_cat = df[df['category'] == cat]
    cat_total = len(df_cat)
    
    scores = {'DeDecker': len(df_cat[df_cat['pos_dedecker'] <= 10])}
    for c in available_comp:
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
    ai_yes = int(df['has_ai'].sum()) if 'has_ai' in df.columns else 0
    ai_no = len(df) - ai_yes
    
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
    if 'dedecker_in_ai' in df.columns:
        df_ai = df[df['has_ai'] == True]
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
    df_ai_table = df[df['has_ai'] == True][['keyword', 'volume', 'category', 'pos_dedecker', 'dedecker_in_ai']].copy()
    df_ai_table.columns = ['Keyword', 'Volume', 'Category', 'Position', 'In AI']
    df_ai_table = df_ai_table.sort_values('Volume', ascending=False).head(12)
    df_ai_table['In AI'] = df_ai_table['In AI'].apply(lambda x: 'Yes' if x else 'No')
    st.dataframe(df_ai_table, use_container_width=True, height=250, hide_index=True)

# ============================================
# 5. KEYWORD EXPLORER (with heatmap moved here)
# ============================================
st.markdown('<p class="section-header">Keyword Explorer</p>', unsafe_allow_html=True)

# Filters
flt1, flt2, flt3, flt4 = st.columns(4)

with flt1:
    cat_options = ['All'] + sorted(df['category'].dropna().unique().tolist())
    filter_cat = st.selectbox("Category", cat_options)
with flt2:
    subcat_options = ['All'] + sorted(df['subcategory'].dropna().unique().tolist())
    filter_subcat = st.selectbox("Subcategory", subcat_options)
with flt3:
    bucket_options = ['All', 'Top 3', '4-10', '11-20', '20+', 'Not ranked']
    filter_bucket = st.selectbox("Position", bucket_options)
with flt4:
    ai_options = ['All', 'With AI Overview', 'DeDecker in AI', 'AI Gap']
    filter_ai = st.selectbox("AI Filter", ai_options)

# Apply filters
dff = df.copy()
if filter_cat != 'All':
    dff = dff[dff['category'] == filter_cat]
if filter_subcat != 'All':
    dff = dff[dff['subcategory'] == filter_subcat]
if filter_bucket != 'All':
    dff = dff[dff['position_bucket'] == filter_bucket]
if filter_ai == 'With AI Overview':
    dff = dff[dff['has_ai'] == True]
elif filter_ai == 'DeDecker in AI':
    dff = dff[dff['dedecker_in_ai'] == True]
elif filter_ai == 'AI Gap':
    dff = dff[(dff['has_ai'] == True) & (dff['dedecker_in_ai'] != True)]

# Results summary
col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.markdown(f"**{len(dff)} keywords**")
with col_res2:
    st.markdown(f"**{dff['volume'].sum():,} volume**")
with col_res3:
    filtered_top10 = len(dff[dff['pos_dedecker'] <= 10])
    st.markdown(f"**{filtered_top10} in Top 10**")

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
display_cols = ['keyword', 'volume', 'category', 'subcategory', 'pos_dedecker']
for c in available_comp:
    display_cols.append(c)
if 'has_ai' in dff.columns:
    display_cols.append('has_ai')

# Prepare dataframe for display - clean all numeric columns
df_display = dff[display_cols].sort_values('volume', ascending=False).copy()

# Convert position columns to integers (no decimals)
pos_cols = ['pos_dedecker'] + available_comp
for col in pos_cols:
    if col in df_display.columns:
        df_display[col] = df_display[col].apply(lambda x: int(x) if pd.notna(x) else None)

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
    na_rep=''
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
    csv = dff.to_csv(index=False).encode('utf-8')
    st.download_button("Export CSV", csv, "dedecker_keywords.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;font-size:0.8rem;'>DeDecker Keukens · Semantic Analysis · March 2026</div>", unsafe_allow_html=True)
