import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  —  dark futuristic theme, RTL Arabic support
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --bg:        #080818;
  --surface:   #10102a;
  --card:      #161630;
  --border:    #2a2a5a;
  --accent1:   #38bdf8;
  --accent2:   #34d399;
  --accent3:   #fb923c;
  --accent4:   #f472b6;
  --text:      #e2e8f0;
  --muted:     #64748b;
  --gold:      #facc15;
}

html, body, [class*="css"] {
  font-family: 'Cairo', sans-serif !important;
  direction: rtl;
}

.stApp { background: var(--bg); color: var(--text); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--surface);
  border-left: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { direction: rtl; text-align: right; }

/* ── Top header bar ── */
.hero-banner {
  background: linear-gradient(135deg, #0f0f2e 0%, #1a1a4e 50%, #0d0d2b 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px 36px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
  text-align: right;
}
.hero-banner::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(56,189,248,0.15) 0%, transparent 70%);
}
.hero-banner::after {
  content: '';
  position: absolute;
  bottom: -30px; left: -30px;
  width: 160px; height: 160px;
  background: radial-gradient(circle, rgba(52,211,153,0.1) 0%, transparent 70%);
}
.hero-title {
  font-size: 2rem; font-weight: 900;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin: 0 0 6px 0;
}
.hero-sub { color: var(--muted); font-size: 0.95rem; margin: 0; }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px 22px;
  text-align: right;
  position: relative;
  overflow: hidden;
  transition: transform .2s, border-color .2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-card::before {
  content: '';
  position: absolute; top: 0; right: 0;
  width: 4px; height: 100%;
  background: var(--accent-color, var(--accent1));
  border-radius: 0 14px 14px 0;
}
.kpi-icon { font-size: 1.6rem; margin-bottom: 8px; }
.kpi-label { font-size: 0.8rem; color: var(--muted); margin-bottom: 4px; }
.kpi-value { font-size: 1.9rem; font-weight: 900; color: var(--accent-color, var(--accent1)); }
.kpi-sub { font-size: 0.75rem; color: var(--muted); margin-top: 4px; }

/* ── Section headers ── */
.section-header {
  display: flex; align-items: center; gap: 10px;
  margin: 32px 0 16px 0;
  direction: rtl;
}
.section-header h2 {
  font-size: 1.2rem; font-weight: 700;
  color: var(--text); margin: 0;
}
.section-divider {
  flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}
.section-tag {
  background: var(--accent1);
  color: #000; font-size: 0.7rem; font-weight: 700;
  padding: 3px 10px; border-radius: 20px;
}

/* ── Chart containers ── */
.chart-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 6px;
  margin-bottom: 16px;
}

/* ── Upload area ── */
.upload-zone {
  background: linear-gradient(135deg, #10102a, #161630);
  border: 2px dashed var(--accent1);
  border-radius: 20px;
  padding: 50px 40px;
  text-align: center;
  margin: 40px auto;
  max-width: 600px;
}
.upload-icon { font-size: 3.5rem; margin-bottom: 16px; }
.upload-title { font-size: 1.5rem; font-weight: 700; color: var(--accent1); margin-bottom: 8px; }
.upload-sub { color: var(--muted); font-size: 0.9rem; }

/* ── Streamlit overrides ── */
.stFileUploader > div { background: transparent !important; }
div[data-testid="stFileUploadDropzone"] {
  background: var(--surface) !important;
  border: 2px dashed var(--border) !important;
  border-radius: 12px !important;
}
.stSelectbox > div > div {
  background: var(--card) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}
.stMultiSelect > div > div {
  background: var(--card) !important;
  border-color: var(--border) !important;
}
.stButton > button {
  background: linear-gradient(135deg, var(--accent1), #0ea5e9) !important;
  color: #000 !important; font-weight: 700 !important;
  border: none !important; border-radius: 10px !important;
  padding: 10px 28px !important;
  font-family: 'Cairo', sans-serif !important;
  font-size: 1rem !important;
  transition: opacity .2s !important;
  width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }
div[data-testid="stMetric"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px !important;
}
div[data-testid="stMetricValue"] { color: var(--accent1) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Cairo', sans-serif !important; }
.stTabs [aria-selected="true"] { color: var(--accent1) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#10102a",
    font=dict(family="Cairo, sans-serif", color="#e2e8f0"),
    title_font=dict(size=14, color="#e2e8f0"),
    legend=dict(bgcolor="rgba(22,22,48,0.8)", bordercolor="#2a2a5a", borderwidth=1),
    margin=dict(t=50, b=40, l=40, r=40),
    colorway=["#38bdf8","#34d399","#fb923c","#f472b6","#a78bfa","#facc15","#f87171","#67e8f9"],
    xaxis=dict(gridcolor="#1e1e3f", zerolinecolor="#2a2a5a"),
    yaxis=dict(gridcolor="#1e1e3f", zerolinecolor="#2a2a5a"),
)

def styled_fig(fig, title=""):
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14)))
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, sub="", color="var(--accent1)"):
    return f"""
    <div class="kpi-card" style="--accent-color:{color};">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {"<div class='kpi-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

def section_header(title, tag=""):
    tag_html = f'<span class="section-tag">{tag}</span>' if tag else ""
    return f"""
    <div class="section-header">
      {tag_html}
      <h2>{title}</h2>
      <div class="section-divider"></div>
    </div>"""

def fmt_number(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{int(n):,}"

# ─────────────────────────────────────────────────────────────────────────────
# DETECT COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
def detect_columns(df):
    """Auto-detect relevant columns from the dataframe."""
    cols = {c.lower(): c for c in df.columns}

    qty_col   = next((cols[c] for c in cols if any(k in c for k in ['qty','quantity','billed qty','كمية','عدد'])), None)
    date_col  = next((cols[c] for c in cols if any(k in c for k in ['date','billing date','تاريخ'])), None)
    mg_cols   = [c for c in df.columns if str(c).upper().startswith('MG')]
    value_col = next((cols[c] for c in cols if any(k in c for k in ['amount','value','revenue','sales','قيمة','مبيعات','total'])), None)

    return qty_col, date_col, mg_cols, value_col

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px; border-bottom: 1px solid #2a2a5a; margin-bottom: 20px;">
      <div style="font-size:2.2rem;">📊</div>
      <div style="font-size:1.1rem; font-weight:700; color:#38bdf8;">لوحة تحليل المبيعات</div>
      <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Sales Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📁 رفع الملف")
    uploaded_file = st.file_uploader(
        "ارفع ملف Excel أو CSV",
        type=["xlsx", "xls", "csv","parquet"],
        help="يدعم Excel و CSV,parquet"
    )

    st.markdown("---")
    st.markdown("### ⚙️ إعدادات العرض")
    top_n = st.slider("أعلى N تصنيف", 5, 20, 10)
    chart_type = st.radio("نوع المخطط", ["عمودي أفقي", "عمودي رأسي", "دائري"], index=0)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#64748b; text-align:center; padding-top:10px;">
      Built with ❤️ using Streamlit + Plotly<br/>
      يدعم اللغة العربية بالكامل
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-sub">ارفع بياناتك وشاهد التحليل الفوري • Upload your data and see instant analytics</p>
  <h1 class="hero-title">📊 لوحة تحليل المبيعات التفاعلية</h1>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────────────────────────────────────
if uploaded_file is None:
    # ── WELCOME STATE ──
    st.markdown("""
    <div class="upload-zone">
      <div class="upload-icon">⬆️</div>
      <div class="upload-title">ارفع ملف البيانات من الشريط الجانبي</div>
      <div class="upload-sub">يدعم ملفات Excel (.xlsx / .xls) وملفات CSV</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(section_header("🔑 الأعمدة المطلوبة في ملفك", "دليل"), unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="chart-card" style="padding:16px; text-align:right;">
        <div style="font-size:1.5rem;">📅</div>
        <div style="font-weight:700; color:#38bdf8;">عمود التاريخ</div>
        <div style="color:#64748b; font-size:0.85rem;">Billing Date أو أي عمود تاريخ</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="chart-card" style="padding:16px; text-align:right;">
        <div style="font-size:1.5rem;">🔢</div>
        <div style="font-weight:700; color:#34d399;">عمود الكمية</div>
        <div style="color:#64748b; font-size:0.85rem;">Billed Quantity أو Qty</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="chart-card" style="padding:16px; text-align:right;">
        <div style="font-size:1.5rem;">🏷️</div>
        <div style="font-weight:700; color:#fb923c;">أعمدة التصنيف</div>
        <div style="color:#64748b; font-size:0.85rem;">MG1, MG2, MG3 … إلخ</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="chart-card" style="padding:16px; text-align:right;">
        <div style="font-size:1.5rem;">💰</div>
        <div style="font-weight:700; color:#f472b6;">عمود القيمة (اختياري)</div>
        <div style="color:#64748b; font-size:0.85rem;">Amount أو Revenue أو Sales</div>
        </div>""", unsafe_allow_html=True)

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file, encoding="utf-8-sig")
    return pd.read_excel(file)
with st.spinner("⏳ جاري تحليل البيانات..."):
    try:
        df = load_data(uploaded_file)
    except Exception as e:
        st.error(f"❌ خطأ في قراءة الملف: {e}")
        st.stop()

qty_col, date_col, mg_cols, value_col = detect_columns(df)

# ── SIDEBAR: manual column selection if auto-detect misses ──
with st.sidebar:
    st.markdown("### 🔧 تحديد الأعمدة")
    all_cols = df.columns.tolist()

    qty_col = st.selectbox("عمود الكمية", all_cols,
        index=all_cols.index(qty_col) if qty_col in all_cols else 0)
    date_col = st.selectbox("عمود التاريخ", [None] + all_cols,
        index=([None]+all_cols).index(date_col) if date_col in all_cols else 0)
    value_col = st.selectbox("عمود القيمة (اختياري)", [None] + all_cols,
        index=([None]+all_cols).index(value_col) if value_col in all_cols else 0)
    mg_cols = st.multiselect("أعمدة التصنيف (MG)", all_cols,
        default=mg_cols if mg_cols else [])

# Prep
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["_year"]  = df[date_col].dt.year
    df["_month"] = df[date_col].dt.month
    df["_month_name"] = df[date_col].dt.strftime("%b %Y")

df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)
if value_col:
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce").fillna(0)

# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
total_qty   = df[qty_col].sum()
total_rows  = len(df)
total_cats  = sum(df[m].nunique() for m in mg_cols) if mg_cols else 0
total_value = df[value_col].sum() if value_col else 0

kpi_html = '<div class="kpi-grid">'
kpi_html += kpi_card("📦", "إجمالي الكميات", fmt_number(total_qty), "Billed Quantity", "#38bdf8")
kpi_html += kpi_card("📋", "إجمالي السجلات", f"{total_rows:,}", "عدد الصفوف", "#34d399")
kpi_html += kpi_card("🏷️", "إجمالي التصنيفات", f"{total_cats:,}", f"عبر {len(mg_cols)} مجموعات", "#fb923c")
if value_col:
    kpi_html += kpi_card("💰", "إجمالي القيمة", fmt_number(total_value), value_col, "#f472b6")
else:
    years = df["_year"].nunique() if date_col else "-"
    kpi_html += kpi_card("📅", "عدد السنوات", str(years), "في البيانات", "#a78bfa")
kpi_html += "</div>"
st.markdown(kpi_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
if not mg_cols:
    st.warning("⚠️ لم يتم اختيار أعمدة تصنيف (MG). اختر الأعمدة من الشريط الجانبي.")
    st.stop()

tab_labels = ["🏷️ مقارنة التصنيفات", "📅 الاتجاه الزمني", "🥧 التوزيع النسبي", "🔥 خريطة التقاطع", "📋 البيانات الخام"]
tabs = st.tabs(tab_labels)

COLORS = ["#38bdf8","#34d399","#fb923c","#f472b6","#a78bfa","#facc15","#f87171","#67e8f9","#4ade80","#e879f9"]

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – Classification Comparison
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown(section_header("مقارنة المبيعات لكل تصنيف", "TOP N"), unsafe_allow_html=True)

    for mg in mg_cols:
        grp = df.groupby(mg)[qty_col].sum().sort_values(ascending=False).head(top_n).reset_index()
        grp.columns = ["التصنيف", "الكمية"]
        grp["التصنيف"] = grp["التصنيف"].astype(str)
        grp["النسبة"] = (grp["الكمية"] / grp["الكمية"].sum() * 100).round(1)

        with st.container():
            st.markdown(f'<div class="chart-card">', unsafe_allow_html=True)

            if chart_type == "عمودي أفقي":
                fig = px.bar(grp, x="الكمية", y="التصنيف", orientation="h",
                             color="التصنيف", color_discrete_sequence=COLORS,
                             text="الكمية", hover_data=["النسبة"])
                fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                                  textfont_size=10)
                fig.update_layout(yaxis=dict(categoryorder="total ascending"),
                                  showlegend=False, height=max(350, top_n * 40))
            elif chart_type == "عمودي رأسي":
                fig = px.bar(grp, x="التصنيف", y="الكمية",
                             color="التصنيف", color_discrete_sequence=COLORS,
                             text="الكمية")
                fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                                  textfont_size=10)
                fig.update_layout(showlegend=False, height=450)
            else:
                fig = px.pie(grp, names="التصنيف", values="الكمية",
                             color_discrete_sequence=COLORS, hole=0.4)
                fig.update_traces(textposition="inside", textinfo="percent+label",
                                  textfont_size=11)
                fig.update_layout(height=450)

            styled_fig(fig, f"📊 {mg}  —  أعلى {top_n} تصنيف بإجمالي المبيعات")
            st.plotly_chart(fig, use_container_width=True, key=f"tab1_{mg}")
            st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – Yearly Trend
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if not date_col:
        st.warning("⚠️ لم يتم اختيار عمود تاريخ. اختره من الشريط الجانبي.")
    else:
        st.markdown(section_header("الاتجاه الزمني السنوي", "TREND"), unsafe_allow_html=True)

        view_mode = st.radio("عرض حسب", ["سنوي", "شهري"], horizontal=True, key="trend_view")

        for mg in mg_cols:
            top_cats = df.groupby(mg)[qty_col].sum().sort_values(ascending=False).head(8).index.tolist()
            sub = df[df[mg].isin(top_cats)].copy()
            sub[mg] = sub[mg].astype(str)

            if view_mode == "سنوي":
                pivot = sub.groupby(["_year", mg])[qty_col].sum().reset_index()
                pivot.columns = ["السنة", "التصنيف", "الكمية"]
                x_col = "السنة"
            else:
                pivot = sub.groupby(["_month_name", "_month", mg])[qty_col].sum().reset_index()
                pivot = pivot.sort_values("_month")
                pivot.columns = ["الشهر", "_m", "التصنيف", "الكمية"]
                x_col = "الشهر"

            fig = px.bar(pivot, x=x_col, y="الكمية", color="التصنيف",
                         color_discrete_sequence=COLORS, barmode="group",
                         height=420)
            styled_fig(fig, f"📅 {mg}  —  اتجاه المبيعات {view_mode}")
            with st.container():
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, key=f"tab2_{mg}_{view_mode}")
                st.markdown("</div>", unsafe_allow_html=True)

            # Line trend (total)
            if view_mode == "سنوي":
                total_trend = df.groupby("_year")[qty_col].sum().reset_index()
                total_trend.columns = ["السنة", "الإجمالي"]
                fig2 = px.line(total_trend, x="السنة", y="الإجمالي",
                               markers=True, color_discrete_sequence=["#facc15"], height=280)
                fig2.update_traces(line_width=3, marker_size=10)
                styled_fig(fig2, f"📈 {mg}  —  إجمالي المبيعات السنوي")
                st.plotly_chart(fig2, use_container_width=True, key=f"tab2_total_{mg}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 – Distribution
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(section_header("التوزيع النسبي للتصنيفات", "SHARE"), unsafe_allow_html=True)

    cols_row = st.columns(min(len(mg_cols), 2))
    for i, mg in enumerate(mg_cols):
        grp = df.groupby(mg)[qty_col].sum().sort_values(ascending=False).head(top_n).reset_index()
        grp.columns = ["التصنيف", "الكمية"]
        grp["التصنيف"] = grp["التصنيف"].astype(str)

        fig = px.pie(grp, names="التصنيف", values="الكمية",
                     color_discrete_sequence=COLORS, hole=0.45)
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        fig.update_layout(annotations=[dict(text=mg, x=0.5, y=0.5,
                                            font_size=16, font_color="white",
                                            showarrow=False)])
        styled_fig(fig, f"🥧 {mg}  —  التوزيع النسبي")

        col = cols_row[i % 2]
        with col:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, key=f"tab3_{mg}")
            st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 – Heatmap / Crosstab
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(section_header("خريطة التقاطع بين التصنيفات", "HEATMAP"), unsafe_allow_html=True)

    if len(mg_cols) >= 2:
        c1, c2 = st.columns(2)
        with c1:
            mg_x = st.selectbox("المحور الأفقي (X)", mg_cols, key="hm_x")
        with c2:
            mg_y = st.selectbox("المحور الرأسي (Y)", [m for m in mg_cols if m != mg_x], key="hm_y")

        top_x = df.groupby(mg_x)[qty_col].sum().nlargest(12).index
        top_y = df.groupby(mg_y)[qty_col].sum().nlargest(12).index

        sub = df[df[mg_x].isin(top_x) & df[mg_y].isin(top_y)]
        pivot = sub.pivot_table(index=mg_y, columns=mg_x, values=qty_col, aggfunc="sum", fill_value=0)

        fig = px.imshow(pivot,
                        color_continuous_scale=["#0d0d2b","#164e63","#0ea5e9","#38bdf8","#facc15"],
                        aspect="auto", height=500)
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_coloraxes(colorbar_tickfont_color="#e2e8f0")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="heatmap")
        st.markdown("</div>", unsafe_allow_html=True)

        # Scatter if value col exists
        if value_col:
            st.markdown(section_header("العلاقة بين الكمية والقيمة", "SCATTER"), unsafe_allow_html=True)
            scat = df.groupby(mg_cols[0]).agg(
                الكمية=(qty_col, "sum"),
                القيمة=(value_col, "sum")
            ).reset_index()
            fig2 = px.scatter(scat, x="الكمية", y="القيمة", color=mg_cols[0],
                              size="الكمية", hover_name=mg_cols[0],
                              color_discrete_sequence=COLORS, height=420)
            styled_fig(fig2, f"📌 العلاقة بين الكمية والقيمة حسب {mg_cols[0]}")
            st.plotly_chart(fig2, use_container_width=True, key="scatter")
    else:
        st.info("تحتاج لاختيار عمودين أو أكثر من أعمدة التصنيف لعرض خريطة التقاطع.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 – Raw Data
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown(section_header("البيانات الخام", "RAW"), unsafe_allow_html=True)

    search = st.text_input("🔍 بحث في البيانات", placeholder="اكتب للفلترة...")
    if search:
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        display_df = df[mask]
    else:
        display_df = df

    st.markdown(f"**إجمالي السجلات المعروضة: {len(display_df):,}**")
    st.dataframe(display_df.head(500), use_container_width=True, height=400)

    # Download
    buf = io.BytesIO()
    display_df.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    st.download_button(
        label="⬇️ تحميل البيانات المفلترة (Excel)",
        data=buf,
        file_name="filtered_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:30px; color:#334155; font-size:0.8rem; border-top: 1px solid #1e1e3f; margin-top:40px;">
  📊 Sales Analytics Dashboard  •  Built with Streamlit & Plotly  •  يدعم اللغة العربية
</div>
""", unsafe_allow_html=True)
