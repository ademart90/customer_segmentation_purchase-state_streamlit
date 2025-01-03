import app as st
import pandas as pd
import streamlit as st
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# Load the dataset
@st.cache_data
def load_data():
    # Load your dataset here
    data = pd.read_csv("data/segmented_customers.csv")
    return data


# Load data
data = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_state =st.sidebar.multiselect("Select State", data["State"].unique(), default=data["State"].unique(), key="state_selectbox")
selected_segment = st.sidebar.multiselect("Select Segment(s)", data["Segment"].unique(), default=data["Segment"].unique(), key="shopper_type_selectbox")

# Filter data based on selection
filtered_data = data[(data["State"].isin(selected_state)) & (data["Segment"].isin(selected_segment))]

# Main Dashboard
st.title("Customer Segmentation Dashboard")

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data)

# Pie Chart for Segments
st.subheader("Customer Segmentation Distribution")
fig_pie = px.pie(filtered_data, names="Segment", title="Segmentation Distribution",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_pie)

# Line Chart for Purchase Trends
st.subheader("Purchase Trends Over Time")
fig_line = px.line(filtered_data, x="Date", y="PurchaseAmount", color="Segment",
                   title="Purchase Amount Over Time",
                   labels={"Date": "Date", "PurchaseAmount": "Purchase Amount"},
                   markers=True)
st.plotly_chart(fig_line)

# Bar Chart for Purchase Frequency by Segment
st.subheader("Average Purchase Frequency by shoppers Segment")
avg_freq = filtered_data.groupby("Segment")["PurchaseFrequency"].mean().reset_index()
fig_bar = px.bar(avg_freq, x="Segment", y="PurchaseFrequency", title="Average Purchase Frequency by Segment",
                 color="Segment", color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig_bar)
