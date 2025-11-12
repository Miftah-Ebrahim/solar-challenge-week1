"""
Solar Challenge Interactive Dashboard
======================================
A professional, interactive dashboard for exploring solar energy potential
across West African countries (Benin, Sierra Leone, Togo).

Features:
- Multi-country comparison
- Interactive time series visualization
- Statistical analysis with boxplots
- Top-N records analysis
- Data export functionality

Author: Miftah
Date: 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import custom utilities
from utils import (
    load_all_countries,
    preprocess_data,
    filter_data,
    get_metric_info,
    calculate_summary_stats,
    get_top_n_records,
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Solar Challenge Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown(
    '<p class="main-header" style="font-size:40px; font-weight:bold;">☀️ Solar Challenge Dashboard</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header" style="font-size:24px; color:gray;">Interactive Analysis of Climate Data for Solar Energy Potential</p>',
    unsafe_allow_html=True,
)

st.markdown("---")


# ============================================================================
# DATA LOADING
# ============================================================================


@st.cache_data(show_spinner=False)
def load_and_preprocess_data():
    """Load and preprocess all country data."""
    try:
        # Load all countries - uses actual file names: benin, sierra_leone, togo
        raw_data = load_all_countries()

        # Preprocess data
        processed_data = preprocess_data(raw_data)

        return processed_data
    except Exception as e:
        st.error(f"❌ **Error loading data:** {e}")
        st.error("""
        **Troubleshooting Tips:**
        - Ensure CSV files are in the `data/` folder
        - Check file names: `benin_clean.csv`, `sierra_leone_clean.csv`, `togo_clean.csv`
        - Verify columns: YEAR, MO, DY, T2M, WS10M_MIN
        """)
        st.stop()


# Load data with spinner
with st.spinner("🔄 Loading solar challenge data..."):
    df_full = load_and_preprocess_data()

st.success(
    f"✅ Successfully loaded {len(df_full):,} records from {df_full['Country'].nunique()} countries"
)


# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

st.sidebar.header("⚙️ Dashboard Controls")

# Country selection
st.sidebar.subheader("📍 Country Selection")
available_countries = sorted(df_full["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select countries to analyze:",
    options=available_countries,
    default=available_countries,
    help="Choose one or more countries for comparison",
)

# Validate country selection
if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar.")
    st.stop()

# Metric selection
st.sidebar.subheader("📊 Metric Selection")
metric_options = {
    "T2M": "Temperature at 2 Meters (°C)",
    "WS10M_MIN": "Minimum Wind Speed at 10m (m/s)",
}
selected_metric = st.sidebar.radio(
    "Choose a metric to analyze:",
    options=list(metric_options.keys()),
    format_func=lambda x: metric_options[x],
    help="Select the climate variable to visualize",
)

# Date range selection
st.sidebar.subheader("📅 Date Range")
min_date = df_full.index.min().date()
max_date = df_full.index.max().date()

date_range = st.sidebar.date_input(
    "Select date range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter data by date range",
)

# Handle single date selection
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

# Convert to pandas Timestamp
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Top-N slider
st.sidebar.subheader("🔢 Top Records")
top_n = st.sidebar.slider(
    "Number of top records to display:",
    min_value=5,
    max_value=50,
    value=10,
    step=5,
    help="Select how many top records to show in the table",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip:** Use the controls above to customize your analysis and explore different aspects of the data."
)


# ============================================================================
# FILTER DATA
# ============================================================================

df_filtered = filter_data(df_full, selected_countries, (start_date, end_date))

if df_filtered.empty:
    st.error(
        "❌ No data available for the selected filters. Please adjust your selection."
    )
    st.stop()


# ============================================================================
# MAIN DASHBOARD - TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Time Series Analysis",
        "📊 Statistical Comparison",
        "🏆 Top Records",
        "📋 Data Summary",
    ]
)


# ============================================================================
# TAB 1: TIME SERIES ANALYSIS
# ============================================================================

with tab1:
    st.header(f"📈 {get_metric_info(selected_metric)['name']} Over Time")

    st.markdown(f"""
    This chart shows the temporal variation of **{get_metric_info(selected_metric)["name"].lower()}** 
    across the selected countries. Use this view to identify trends, seasonal patterns, and anomalies.
    """)

    # Create time series plot using Plotly
    fig_timeseries = px.line(
        df_filtered.reset_index(),
        x="Timestamp",
        y=selected_metric,
        color="Country",
        title=f"{get_metric_info(selected_metric)['name']} Trends by Country",
        labels={
            "Timestamp": "Date",
            selected_metric: f"{get_metric_info(selected_metric)['name']} ({get_metric_info(selected_metric)['unit']})",
            "Country": "Country",
        },
        template="plotly_white",
        height=500,
    )

    # Customize layout
    fig_timeseries.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig_timeseries.update_traces(line=dict(width=2))

    st.plotly_chart(fig_timeseries, use_container_width=True)

    # Key insights
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_value = df_filtered[selected_metric].mean()
        st.metric(
            label=f"Average {get_metric_info(selected_metric)['name']}",
            value=f"{avg_value:.2f} {get_metric_info(selected_metric)['unit']}",
        )

    with col2:
        max_value = df_filtered[selected_metric].max()
        st.metric(
            label=f"Maximum Value",
            value=f"{max_value:.2f} {get_metric_info(selected_metric)['unit']}",
        )

    with col3:
        min_value = df_filtered[selected_metric].min()
        st.metric(
            label=f"Minimum Value",
            value=f"{min_value:.2f} {get_metric_info(selected_metric)['unit']}",
        )


# ============================================================================
# TAB 2: STATISTICAL COMPARISON
# ============================================================================

with tab2:
    st.header(
        f"📊 Statistical Distribution of {get_metric_info(selected_metric)['name']}"
    )

    st.markdown("""
    Box plots provide a comprehensive view of data distribution, showing the median, 
    quartiles, and outliers for each country. This helps identify differences in 
    climate conditions across regions.
    """)

    # Create boxplot
    fig_box = px.box(
        df_filtered.reset_index(),
        x="Country",
        y=selected_metric,
        color="Country",
        title=f"Distribution Comparison: {get_metric_info(selected_metric)['name']}",
        labels={
            "Country": "Country",
            selected_metric: f"{get_metric_info(selected_metric)['name']} ({get_metric_info(selected_metric)['unit']})",
        },
        template="plotly_white",
        height=500,
    )

    fig_box.update_layout(showlegend=False)

    st.plotly_chart(fig_box, use_container_width=True)

    # Summary statistics table
    st.subheader("📋 Summary Statistics by Country")

    summary_stats = calculate_summary_stats(df_filtered, selected_metric)

    st.dataframe(
        summary_stats.style.format("{:.2f}").background_gradient(cmap="YlOrRd", axis=0),
        use_container_width=True,
    )

    st.markdown("""
    **Legend:**
    - **Mean:** Average value
    - **Median:** Middle value (50th percentile)
    - **Min/Max:** Extreme values
    - **Std Dev:** Standard deviation (measure of variability)
    """)


# ============================================================================
# TAB 3: TOP RECORDS
# ============================================================================

with tab3:
    st.header(f"🏆 Top {top_n} Records for {get_metric_info(selected_metric)['name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🔥 Highest {top_n} Values")
        top_highest = get_top_n_records(
            df_filtered, selected_metric, n=top_n, ascending=False
        )

        st.dataframe(
            top_highest.style.format(
                {"Date": lambda x: x.strftime("%Y-%m-%d"), selected_metric: "{:.2f}"}
            ).background_gradient(subset=[selected_metric], cmap="Reds"),
            use_container_width=True,
            height=400,
        )

    with col2:
        st.subheader(f"❄️ Lowest {top_n} Values")
        top_lowest = get_top_n_records(
            df_filtered, selected_metric, n=top_n, ascending=True
        )

        st.dataframe(
            top_lowest.style.format(
                {"Date": lambda x: x.strftime("%Y-%m-%d"), selected_metric: "{:.2f}"}
            ).background_gradient(subset=[selected_metric], cmap="Blues"),
            use_container_width=True,
            height=400,
        )

    # Visualization of top records
    st.subheader("📊 Visual Comparison of Extremes")

    fig_extremes = go.Figure()

    # Add highest values
    fig_extremes.add_trace(
        go.Bar(
            name="Highest",
            x=top_highest["Date"].astype(str),
            y=top_highest[selected_metric],
            marker_color="#FF6B35",
        )
    )

    # Add lowest values
    fig_extremes.add_trace(
        go.Bar(
            name="Lowest",
            x=top_lowest["Date"].astype(str),
            y=top_lowest[selected_metric],
            marker_color="#4ECDC4",
        )
    )

    fig_extremes.update_layout(
        title=f"Top {top_n} Extreme Values Comparison",
        xaxis_title="Date",
        yaxis_title=f"{get_metric_info(selected_metric)['name']} ({get_metric_info(selected_metric)['unit']})",
        barmode="group",
        template="plotly_white",
        height=400,
        showlegend=True,
    )

    st.plotly_chart(fig_extremes, use_container_width=True)


# ============================================================================
# TAB 4: DATA SUMMARY
# ============================================================================

with tab4:
    st.header("📋 Data Summary and Export")

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{len(df_filtered):,}")

    with col2:
        st.metric("Countries", len(selected_countries))

    with col3:
        st.metric("Date Range", f"{(end_date - start_date).days + 1} days")

    with col4:
        st.metric(
            "Data Completeness",
            f"{(1 - df_filtered[selected_metric].isna().sum() / len(df_filtered)) * 100:.1f}%",
        )

    st.markdown("---")

    # Data preview
    st.subheader("🔍 Filtered Data Preview")
    st.markdown(f"Showing first 100 rows of {len(df_filtered):,} total records")

    preview_df = df_filtered.reset_index()[
        ["Timestamp", "Country", "YEAR", "MO", "DY", selected_metric]
    ].head(100)

    st.dataframe(
        preview_df.style.format(
            {"Timestamp": lambda x: x.strftime("%Y-%m-%d"), selected_metric: "{:.2f}"}
        ),
        use_container_width=True,
        height=400,
    )

    # Download button
    st.subheader("💾 Export Data")

    csv_data = df_filtered.reset_index().to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"solar_challenge_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Download the currently filtered dataset",
    )

    st.info("""
    **Dataset Information:**
    - **Source:** Solar Challenge Project - Week 1
    - **Countries:** Benin, Sierra Leone, Togo
    - **Metrics:** Temperature (T2M), Wind Speed (WS10M_MIN)
    - **Purpose:** Analysis of solar energy potential in West Africa
    """)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Solar Challenge Dashboard</strong> | Built with Streamlit & Plotly</p>
    <p>Data-driven insights for renewable energy planning in West Africa 🌍</p>
</div>
""",
    unsafe_allow_html=True,
)
