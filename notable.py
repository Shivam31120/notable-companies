import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Notable Indian Companies – Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.3rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; }
    .metric-label { font-size: 0.85rem; opacity: 0.9; }
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a2e;
        border-left: 4px solid #667eea;
        padding-left: 10px;
        margin: 1.2rem 0 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Load & clean data ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("notable_companies (1).csv")

    # Clean Founded column
    df["Founded_clean"] = (
        df["Founded"].astype(str)
        .str.extract(r"(\d{4})")[0]
        .pipe(pd.to_numeric, errors="coerce")
    )

    # Readable labels
    df["Ownership"] = df["Private/State"].map({"P": "Private", "S": "State-owned"})
    df["Status"]    = df["Active/Defunct"].map({"A": "Active", "D": "Defunct"})

    # Era buckets
    bins   = [1700, 1900, 1950, 1975, 1990, 2000, 2010, 2030]
    labels = ["Pre-1900", "1900–1950", "1950–1975", "1975–1990", "1990–2000", "2000–2010", "2010+"]
    df["Era"] = pd.cut(df["Founded_clean"], bins=bins, labels=labels)

    return df

df_raw = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg", width=60)
    st.title("Filters")

    industries = ["All"] + sorted(df_raw["Industry"].dropna().unique().tolist())
    sel_industry = st.selectbox("Industry", industries)

    cities = ["All"] + sorted(df_raw["Headquarters"].dropna().unique().tolist())
    sel_city = st.multiselect("Headquarters city", cities, default=["All"])

    ownership_opts = ["All", "Private", "State-owned"]
    sel_ownership  = st.selectbox("Ownership type", ownership_opts)

    status_opts = ["All", "Active", "Defunct"]
    sel_status  = st.selectbox("Status", status_opts)

    year_min = int(df_raw["Founded_clean"].dropna().min())
    year_max = int(df_raw["Founded_clean"].dropna().max())
    sel_years = st.slider("Founded between", year_min, year_max, (year_min, year_max))

    st.markdown("---")
    st.caption("Data: Notable Indian companies dataset")

# ── Apply filters ──────────────────────────────────────────────────────────────
df = df_raw.copy()

if sel_industry != "All":
    df = df[df["Industry"] == sel_industry]

if "All" not in sel_city and sel_city:
    df = df[df["Headquarters"].isin(sel_city)]

if sel_ownership != "All":
    df = df[df["Ownership"] == sel_ownership]

if sel_status != "All":
    df = df[df["Status"] == sel_status]

df = df[
    (df["Founded_clean"] >= sel_years[0]) |
    df["Founded_clean"].isna()
]
df = df[
    (df["Founded_clean"] <= sel_years[1]) |
    df["Founded_clean"].isna()
]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🏢 Notable Indian Companies</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive analytics dashboard · 493 companies across industries, cities & eras</div>', unsafe_allow_html=True)

# ── KPI cards ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-label">Companies</div></div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
        <div class="metric-value">{df['Industry'].nunique()}</div>
        <div class="metric-label">Industries</div></div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
        <div class="metric-value">{df['Headquarters'].nunique()}</div>
        <div class="metric-label">Cities</div></div>""", unsafe_allow_html=True)

with k4:
    pct_private = round(100 * (df["Ownership"] == "Private").sum() / max(len(df), 1))
    st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#43e97b,#38f9d7)">
        <div class="metric-value">{pct_private}%</div>
        <div class="metric-label">Private-owned</div></div>""", unsafe_allow_html=True)

with k5:
    oldest = int(df["Founded_clean"].dropna().min()) if not df["Founded_clean"].dropna().empty else "–"
    st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#fa709a,#fee140)">
        <div class="metric-value">{oldest}</div>
        <div class="metric-label">Oldest Founded</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Industry bar + City bubble ─────────────────────────────────────────
st.markdown('<div class="section-title">Industry & City Distribution</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

with col1:
    ind_counts = df["Industry"].value_counts().reset_index()
    ind_counts.columns = ["Industry", "Count"]
    fig_ind = px.bar(
        ind_counts, x="Count", y="Industry", orientation="h",
        color="Count", color_continuous_scale="Purples",
        title="Companies per Industry",
        template="plotly_white",
    )
    fig_ind.update_layout(
        height=420, showlegend=False, coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_ind, use_container_width=True)

with col2:
    city_counts = df["Headquarters"].value_counts().head(12).reset_index()
    city_counts.columns = ["City", "Count"]
    fig_city = px.bar(
        city_counts, x="City", y="Count",
        color="Count", color_continuous_scale="Blues",
        title="Top 12 Headquarters Cities",
        template="plotly_white",
    )
    fig_city.update_layout(
        height=420, showlegend=False, coloraxis_showscale=False,
        xaxis_tickangle=-35,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_city, use_container_width=True)

# ── Row 2: Ownership pie + Status donut ───────────────────────────────────────
st.markdown('<div class="section-title">Ownership & Status Breakdown</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

with col3:
    own_counts = df["Ownership"].value_counts()
    fig_own = px.pie(
        values=own_counts.values, names=own_counts.index,
        title="Ownership Split",
        color_discrete_sequence=["#667eea", "#f5576c"],
        hole=0.45, template="plotly_white",
    )
    fig_own.update_layout(height=340, margin=dict(t=50, b=10))
    fig_own.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_own, use_container_width=True)

with col4:
    stat_counts = df["Status"].value_counts()
    fig_stat = px.pie(
        values=stat_counts.values, names=stat_counts.index,
        title="Active vs Defunct",
        color_discrete_sequence=["#43e97b", "#fa709a"],
        hole=0.45, template="plotly_white",
    )
    fig_stat.update_layout(height=340, margin=dict(t=50, b=10))
    fig_stat.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_stat, use_container_width=True)

with col5:
    # Ownership × Status stacked bar
    cross = (
        df.groupby(["Industry", "Ownership"])
        .size().reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .head(20)
    )
    fig_cross = px.bar(
        cross, x="Count", y="Industry", color="Ownership",
        orientation="h", title="Top Industries by Ownership",
        color_discrete_map={"Private": "#667eea", "State-owned": "#f5576c"},
        template="plotly_white",
    )
    fig_cross.update_layout(
        height=340, margin=dict(l=10, r=10, t=50, b=10),
        yaxis=dict(categoryorder="total ascending"),
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig_cross, use_container_width=True)

# ── Row 3: Timeline ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Founding Timeline</div>', unsafe_allow_html=True)

df_year = df.dropna(subset=["Founded_clean"]).copy()
df_year["Founded_clean"] = df_year["Founded_clean"].astype(int)
year_hist = df_year.groupby("Founded_clean").size().reset_index(name="Count")

fig_time = px.area(
    year_hist, x="Founded_clean", y="Count",
    title="Number of Companies Founded per Year",
    template="plotly_white",
    color_discrete_sequence=["#667eea"],
)
fig_time.update_traces(fill="tozeroy", line_color="#667eea", fillcolor="rgba(102,126,234,0.2)")
fig_time.update_layout(
    height=300,
    xaxis_title="Year Founded",
    yaxis_title="Companies",
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig_time, use_container_width=True)

# ── Row 4: Era breakdown ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Era-wise Breakdown</div>', unsafe_allow_html=True)
col6, col7 = st.columns(2)

with col6:
    era_counts = df["Era"].value_counts().sort_index().reset_index()
    era_counts.columns = ["Era", "Count"]
    fig_era = px.funnel(
        era_counts.sort_values("Count", ascending=False),
        x="Count", y="Era",
        title="Companies by Era (Funnel)",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Purples_r,
    )
    fig_era.update_layout(height=370, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_era, use_container_width=True)

with col7:
    era_ind = (
        df.dropna(subset=["Era"])
        .groupby(["Era", "Industry"])
        .size().reset_index(name="Count")
    )
    top_ind = df["Industry"].value_counts().head(6).index.tolist()
    era_ind = era_ind[era_ind["Industry"].isin(top_ind)]
    fig_era_ind = px.line(
        era_ind, x="Era", y="Count", color="Industry",
        title="Top 6 Industries Across Eras",
        markers=True, template="plotly_white",
    )
    fig_era_ind.update_layout(
        height=370, margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=-0.25, font_size=11),
        xaxis_tickangle=-20,
    )
    st.plotly_chart(fig_era_ind, use_container_width=True)

# ── Row 5: Treemap ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Industry → City Treemap</div>', unsafe_allow_html=True)

treemap_df = (
    df.groupby(["Industry", "Headquarters"])
    .size().reset_index(name="Count")
    .sort_values("Count", ascending=False)
)
fig_tree = px.treemap(
    treemap_df, path=["Industry", "Headquarters"],
    values="Count",
    color="Count", color_continuous_scale="Purples",
    title="Company distribution: Industry → City",
    template="plotly_white",
)
fig_tree.update_layout(height=450, margin=dict(l=10, r=10, t=50, b=10))
st.plotly_chart(fig_tree, use_container_width=True)

# ── Row 6: Sunburst ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Ownership × Industry × City Sunburst</div>', unsafe_allow_html=True)

sun_df = (
    df.groupby(["Ownership", "Industry", "Headquarters"])
    .size().reset_index(name="Count")
)
fig_sun = px.sunburst(
    sun_df, path=["Ownership", "Industry", "Headquarters"],
    values="Count",
    color="Ownership",
    color_discrete_map={"Private": "#667eea", "State-owned": "#f5576c"},
    title="Ownership → Industry → City",
    template="plotly_white",
)
fig_sun.update_layout(height=520, margin=dict(l=10, r=10, t=50, b=10))
st.plotly_chart(fig_sun, use_container_width=True)

# ── Filterable data table ──────────────────────────────────────────────────────
st.markdown('<div class="section-title"> Explore the Data</div>', unsafe_allow_html=True)

search = st.text_input("🔍 Search by company name or notes", "")
display_df = df.copy()
if search:
    mask = (
        display_df["Name"].str.contains(search, case=False, na=False) |
        display_df["Notes"].str.contains(search, case=False, na=False)
    )
    display_df = display_df[mask]

st.dataframe(
    display_df[["Name", "Industry", "Sector", "Headquarters",
                "Founded_clean", "Ownership", "Status", "Notes"]]
    .rename(columns={"Founded_clean": "Founded"})
    .reset_index(drop=True),
    use_container_width=True,
    height=350,
)
st.caption(f"Showing {len(display_df):,} of {len(df_raw):,} companies")