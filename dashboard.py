import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Output, Input
import datetime

app = dash.Dash(__name__)


def load_data():
    df = pd.read_csv("gold_prices.csv", names=["timestamp", "price"], parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["price"] = pd.to_numeric(df["price"], errors='coerce')
    return df


def compute_daily_report(df):
    now = datetime.datetime.now()
    today = now.date()
    
    # Use yesterday's data if it's before 8 pm; after 8 pm, use today's data.
    if now.hour < 20:
        report_date = today - datetime.timedelta(days=1)
    else:
        report_date = today


    df_daily = df[df["timestamp"].dt.date == report_date]
    
    if df_daily.empty:
        return f"No data available for {report_date}"

    
    if not df_daily.empty:
        open_price = df_daily["price"].iloc[0]
        close_price = df_daily["price"].iloc[-1]
        change = ((close_price - open_price) / open_price) * 100
        high = df_daily["price"].max()
        low = df_daily["price"].min()
        volatility = df_daily["price"].std()
        report = html.Div([
            html.H3("Daily Report"),
            html.P(f"Date: {today}"),
            html.P(f"Open: US${open_price:,.2f}"),
            html.P(f"Close: US${close_price:,.2f}"),
            html.P(f"High: US${high:,.2f}"),
            html.P(f"Low: US${low:,.2f}"),
            html.P(f"Volatility: {volatility:.2f}%"),
            html.P(f"Change: {change:.2f}%")
        ])
    else:
        report = "No data available for today"


    return report


# Define layout
app.layout = html.Div([
    html.H1("Gold Price Dashboard"),
    html.Div(id="current-price", style={"fontSize": 24, "marginBottom": "20px"}),
    dcc.Graph(id="price-graph"),
    html.Div(id="daily-report", style={"marginTop": "30px", "fontSize": 18}),
    dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0, max_intervals=1)
])

# Update dashboard on page load
@app.callback(
    [Output("current-price", "children"),
     Output("price-graph", "figure"),
     Output("daily-report", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()

    if df.empty:
        return "No data available", {}, "No report available"


    current_price = f"Current Gold Price: US${df['price'].iloc[-1]:,.2f}"

    # Time series graph
    figure = {
        "data": [{"x": df["timestamp"], "y": df["price"], "type": "line", "name": "Gold Price"}],
        "layout": {"title": "Gold Price Over Time"}
    }

    # Daily report for today
    report = compute_daily_report(df)

    return current_price, figure, report


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
