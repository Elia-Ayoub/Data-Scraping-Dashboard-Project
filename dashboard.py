import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Output, Input

app = dash.Dash(__name__)


def load_data():
    df = pd.read_csv("gold_prices.csv", names=["timestamp", "price"], parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["price"] = pd.to_numeric(df["price"], errors='coerce')
    return df



# Define layout
app.layout = html.Div([
    html.H1("Gold Price Dashboard"),
    html.Div(id="current-price", style={"fontSize": 24, "marginBottom": "20px"}),
    dcc.Graph(id="price-graph"),
    dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0, max_intervals=1)
])

# Update dashboard on page load
@app.callback(
    [Output("current-price", "children"),
     Output("price-graph", "figure")],
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


    return current_price, figure


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)