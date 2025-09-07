import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# --- 1. Load and Clean Data ---
try:
    df = pd.read_csv('travel_agency_dataset.csv')
except FileNotFoundError:
    print("Error: 'travel_agency_dataset.csv' not found. Please generate the dataset first.")
    exit()

# Clean 'Total Cost (SAR)' column
df['Total Cost (SAR)'] = df['Total Cost (SAR)'].replace({',': ''}, regex=True).astype(float)

# Convert 'Departure Date' to datetime
df['Departure Date'] = pd.to_datetime(df['Departure Date'], format='%d/%m/%Y')

# Clean 'Client Rating (1-5 stars)'
df['Client Rating (1-5 stars)'] = pd.to_numeric(df['Client Rating (1-5 stars)'], errors='coerce')

# --- 2. Create Visualizations ---
pio.templates.default = "plotly_dark"

# Chart 1: Booking Volume by Destination
dest_counts = df['Destination'].value_counts().reset_index()
dest_counts.columns = ['Destination', 'Number of Bookings']
fig1 = px.bar(dest_counts, x='Destination', y='Number of Bookings', title='Booking Volume by Destination',
              text='Number of Bookings')
fig1.update_traces(marker_color='skyblue', textposition='outside')
fig1.update_layout(xaxis_tickangle=-45)

# Chart 2: Revenue by Package Type
revenue_by_package = df.groupby('Package Type')['Total Cost (SAR)'].sum().reset_index()
fig2 = px.pie(revenue_by_package, names='Package Type', values='Total Cost (SAR)',
              title='Revenue by Package Type', hole=0.3)
fig2.update_traces(textinfo='percent+label', pull=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05])

# Chart 3: Payment Status Distribution
payment_status_counts = df['Payment Status'].value_counts().reset_index()
payment_status_counts.columns = ['Status', 'Count']
fig3 = px.pie(payment_status_counts, names='Status', values='Count', title='Payment Status Distribution',
              color_discrete_sequence=px.colors.sequential.RdBu)

# Chart 4: Seasonal Travel Trends
df['Booking Month'] = df['Departure Date'].dt.to_period('M').astype(str)
monthly_bookings = df['Booking Month'].value_counts().sort_index().reset_index()
monthly_bookings.columns = ['Month', 'Number of Bookings']
fig4 = px.line(monthly_bookings, x='Month', y='Number of Bookings', title='Seasonal Travel Trends (Monthly Bookings)',
               markers=True)
fig4.update_layout(xaxis_title="Month", yaxis_title="Number of Bookings")

# Chart 5: Client Ratings Distribution
fig5 = px.histogram(df.dropna(subset=['Client Rating (1-5 stars)']), x='Client Rating (1-5 stars)',
                    title='Distribution of Client Ratings', nbins=5,
                    labels={'x':'Rating (1-5 stars)'})
fig5.update_traces(marker_color='lightgreen')

# Chart 6: Agent Performance Dashboard
agent_performance = df.groupby('Agent Name').agg(
    Bookings=('Booking ID', 'count'),
    TotalRevenue=('Total Cost (SAR)', 'sum'),
    AverageRating=('Client Rating (1-5 stars)', 'mean')
).reset_index()
agent_performance['AverageRating'] = agent_performance['AverageRating'].round(2)
agent_performance = agent_performance.sort_values(by='TotalRevenue', ascending=False)

# Create the table for the leaderboard
fig6_table = go.Figure(data=[go.Table(
    header=dict(values=['Agent Name', 'Total Bookings', 'Total Revenue (SAR)', 'Average Rating'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[agent_performance['Agent Name'], agent_performance.Bookings, agent_performance.TotalRevenue.map('{:,.2f}'.format), agent_performance.AverageRating],
               fill_color='lavender',
               align='left'))
])
fig6_table.update_layout(title_text='Agent Performance Leaderboard')


# --- 3. Assemble Dashboard HTML ---
# Helper to convert figure to HTML div
def fig_to_div(fig):
    return pio.to_html(fig, full_html=False, include_plotlyjs=False)

dashboard_html = f"""
<html>
<head>
    <title>Travel Agency Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #111; color: #fff; }}
        h1 {{ text-align: center; }}
        .grid-container {{ display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 20px; padding: 20px; }}
        .grid-item {{ background-color: #222; padding: 20px; border-radius: 8px; }}
        .full-width {{ grid-column: 1 / -1; }}
    </style>
</head>
<body>
    <h1>Travel Agency Performance Dashboard</h1>
    <div class="grid-container">
        <div class="grid-item">{fig_to_div(fig1)}</div>
        <div class="grid-item">{fig_to_div(fig2)}</div>
        <div class="grid-item">{fig_to_div(fig3)}</div>
        <div class="grid-item">{fig_to_div(fig4)}</div>
        <div class="grid-item">{fig_to_div(fig5)}</div>
        <div class="grid-item full-width">{fig_to_div(fig6_table)}</div>
    </div>
</body>
</html>
"""

# --- 4. Save HTML File ---
with open("dashboard.html", "w", encoding='utf-8') as f:
    f.write(dashboard_html)

print("Dashboard created successfully as 'dashboard.html'")
