import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Set up the page layout
st.set_page_config(layout="wide")

# Dummy Data for Performance View
np.random.seed(42)
num_stores = 50

# List of US state abbreviations
us_state_abbrev = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]

data = {
    "Store": [f"Store {i}" for i in range(1, num_stores + 1)],
    "DMA": np.random.choice(us_state_abbrev, num_stores),  # Use state abbreviations for DMAs
    "ZIP": np.random.randint(10000, 99999, num_stores),
    "Region": np.random.choice(["North", "South", "East", "West"], num_stores),
    "Channel": np.random.choice(["Search", "Social", "Display"], num_stores),
    "Tier Label": np.random.choice(["Tier 1", "Tier 2", "Tier 3"], num_stores),
    "Spend": np.random.randint(1000, 10000, num_stores),
    "Impressions": np.random.randint(10000, 100000, num_stores),
    "Media Tracked Bookings": np.random.randint(100, 1000, num_stores),
    "Media CAC": np.random.uniform(5, 50, num_stores).round(2),
    "Online Bookings": np.random.randint(50, 500, num_stores),
    "Offline Bookings": np.random.randint(50, 500, num_stores),
    "Total Bookings": np.random.randint(100, 1000, num_stores),
    "Open 14": np.random.randint(10, 100, num_stores),
    "Patient to Slot Ratio": np.random.uniform(0.5, 2.0, num_stores).round(2),
    "BO Rate 14": np.random.uniform(0.1, 0.9, num_stores).round(2),
    "BO Rate L30": np.random.uniform(0.1, 0.9, num_stores).round(2),
    "SPA L30": np.random.uniform(0.5, 3.0, num_stores).round(2),
    "SPA 3.0": np.random.uniform(0.5, 3.0, num_stores).round(2),
    "Online CAC": np.random.uniform(5, 50, num_stores).round(2),
    "Total CAC": np.random.uniform(10, 100, num_stores).round(2),
}
df = pd.DataFrame(data)

# Move filters to main page and add goals filter
st.title("Media Performance Dashboard")

# New Overview Section
with st.expander("Overview", expanded=True):
    # Top line metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Online Bookings", f"{df['Online Bookings'].sum():,}")
    col2.metric("Total Revenue", f"${df['Spend'].sum() * 2:,.2f}")  # Dummy revenue calculation
    col3.metric("Average CAC", f"${df['Total CAC'].mean():.2f}")
    col4.metric("Goal Attainment", "85%")  # Dummy value, replace with actual calculation

    # Performance Trend Line Graph
    st.subheader("Performance Trend")

    # Generate dummy data for performance trend
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    actual = np.cumsum(np.random.randn(30) * 10 + 1)
    predicted = actual + np.random.randn(30) * 5

    trend_df = pd.DataFrame({"Date": dates, "Actual": actual, "Predicted": predicted})

    fig_trend = px.line(trend_df, x="Date", y=["Actual", "Predicted"])
    fig_trend.update_layout(legend_title_text="Performance")
    st.plotly_chart(fig_trend, use_container_width=True)

    # Time Series of SOV by Region
    st.subheader("Time Series of SOV by Region")

    # Generate dummy data for SOV by Region
    regions = df["Region"].unique()
    weeks = pd.date_range(start="2024-01-01", periods=20, freq="W")
    sov_data = {
        "Week": np.tile(weeks, len(regions)),
        "Region": np.repeat(regions, len(weeks)),
        "Share of Voice": np.random.uniform(0.1, 0.5, len(regions) * len(weeks)),
    }
    sov_df = pd.DataFrame(sov_data)

    # Create the line plot
    fig_sov = px.line(sov_df, x="Week", y="Share of Voice", color="Region")
    fig_sov.update_layout(legend_title_text="Region")
    st.plotly_chart(fig_sov, use_container_width=True)

# Existing content wrapped in an expandable section
with st.expander("Performance View", expanded=True):
    # Performance View Table
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dma_filter = st.multiselect("Select DMA", options=df["DMA"].unique()[:5], default=df["DMA"].unique()[:5])
    with col2:
        region_filter = st.multiselect(
            "Select Region", options=df["Region"].unique()[:5], default=df["Region"].unique()[:5]
        )
    with col3:
        goals_filter = st.selectbox("Goals Filter", ["Bookings", "Revenue", "Patient-to-Slot Ratio"])
    with col4:
        goal_value = st.text_input("Goal Value", "")

    # Filter DataFrame
    filtered_df = df[(df["DMA"].isin(dma_filter)) & (df["Region"].isin(region_filter))]

    st.dataframe(filtered_df)

    # Media Performance Heatmap and Revenue per Office Bar Chart side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Media Performance Map")
        # Aggregate data by DMA
        dma_performance = filtered_df.groupby("DMA")["Spend"].sum().reset_index()

        # Create a choropleth map
        fig_map = px.choropleth(
            dma_performance,
            locations="DMA",
            color="Spend",
            scope="usa",
            locationmode="USA-states",
            color_continuous_scale="Blues",
            labels={"Spend": "Media Spend"},
        )
        fig_map.update_layout(geo_scope="usa")
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        st.subheader("Revenue per Office")
        filtered_df["Revenue"] = filtered_df["Spend"] * np.random.uniform(1.5, 3.0, len(filtered_df))
        fig_bar = px.bar(
            filtered_df.head(20).sort_values(by="Revenue", ascending=True), x="Revenue", y="Store", orientation="h"
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# New Scenario Modeling + Planning Section
with st.expander("Scenario Modeling + Planning", expanded=True):
    st.subheader("Optimal Media Mix")
    # Dummy data for media mix recommendation
    recommendation_data = {
        "Channel": ["Search", "Social", "Display"],
        "Current Spend": [5000, 3000, 2000],
        "Recommended Additional Spend": [1000, 500, 200],
        "Projected ROI": [2.5, 1.8, 1.3],
    }
    recommendation_df = pd.DataFrame(recommendation_data)
    st.table(recommendation_df)

    st.subheader("Scenario Modeling (based on MMM)")
    col1, col2, col3 = st.columns(3)
    search_spend = col1.slider("Search Spend", 0, 10000, 5000)
    social_spend = col2.slider("Social Spend", 0, 10000, 3000)
    display_spend = col3.slider("Display Spend", 0, 10000, 2000)

    # Dummy calculation for forecasted impact
    total_spend = search_spend + social_spend + display_spend
    forecasted_bookings = int(total_spend * 0.1)  # Dummy calculation
    forecasted_revenue = total_spend * 2  # Dummy calculation

    st.metric("Forecasted Bookings", forecasted_bookings)
    st.metric("Forecasted Revenue", f"${forecasted_revenue:,.2f}")

    st.subheader("Inventory Utilization")
    # Dummy data for inventory availability
    channels = ["Search", "Social", "Display"]
    weeks = pd.date_range(start="2024-01-01", periods=12, freq="W")
    inventory_data = np.random.randint(50, 100, size=(len(channels), len(weeks)))
    inventory_df = pd.DataFrame(inventory_data, index=channels, columns=weeks)
    fig_inventory = px.imshow(inventory_df, color_continuous_scale="YlGn")
    st.plotly_chart(fig_inventory, use_container_width=True)

    st.subheader("Incremental Spend Recommendation")
    incremental_spend = st.number_input("Enter incremental spend amount", min_value=0, value=1000, step=100)
    st.write(f"Recommended allocation for ${incremental_spend:,}:")
    allocation = {"Search": 0.5, "Social": 0.3, "Display": 0.2}  # Dummy allocation
    for channel, percentage in allocation.items():
        st.write(f"{channel}: ${incremental_spend * percentage:,.2f}")

    st.subheader("Seasonality Chart")
    # Dummy data for seasonality
    dates = pd.date_range(start="2024-01-01", periods=365, freq="D")

    # Create a straight line for the trend
    trend = np.linspace(100, 200, 365)  # Assuming an upward trend from 100 to 200

    # Create monthly seasonality
    monthly_seasonality = 20 * np.sin(np.linspace(0, 2 * np.pi * 12, 365))  # 12 cycles per year

    # Create residual (random noise)
    residual = np.random.normal(0, 5, 365)

    # Combine trend, seasonality, and residual
    observed = trend + monthly_seasonality + residual

    seasonality_df = pd.DataFrame(
        {
            "Date": dates,
            "Observed": observed,
            "Trend": trend,
            "Seasonality": monthly_seasonality,
            "Residual": residual,  # Include residual in the DataFrame but don't plot it
        }
    )

    fig_seasonality = px.line(seasonality_df, x="Date", y=["Observed", "Trend", "Seasonality"])
    fig_seasonality.update_layout(yaxis_title="Value", legend_title="Component")
    st.plotly_chart(fig_seasonality, use_container_width=True)

    st.subheader("Diminishing Returns Curves")
    # Dummy data for diminishing returns by channel
    spend = np.linspace(0, 10000, 100)
    channels = ["Search", "Social", "Display"]
    diminishing_returns_df = pd.DataFrame({"Spend": spend})

    for channel in channels:
        # Different parameters for each channel to simulate varying diminishing returns
        a = np.random.uniform(800, 1200)
        b = np.random.uniform(0.0003, 0.0007)
        diminishing_returns_df[channel] = a * (1 - np.exp(-b * spend))

    fig_returns = px.line(diminishing_returns_df, x="Spend", y=channels)
    fig_returns.update_layout(xaxis_title="Spend ($)", yaxis_title="Returns ($)", legend_title="Channel")
    st.plotly_chart(fig_returns, use_container_width=True)
