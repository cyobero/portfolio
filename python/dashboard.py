from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
from datetime import date

tickers = yf.Tickers("nvda bx coin btc-usd eth-usd").history(period="max").Close
df = pd.DataFrame(tickers).asfreq("D")

app = Dash(__name__)

app.layout = html.Div(
    [
        # main app
        html.Div(
            [
                # time series chart
                html.Div(
                    [
                        dcc.Dropdown(
                            tickers.columns,
                            ["NVDA", "BX"],
                            multi=True,
                            id="asset-dropdown",
                        ),
                        dcc.Graph("time-series"),
                        dcc.Graph("histogram"),
                        html.H4("select date"),
                        dcc.DatePickerRange(
                            start_date=date(2017, 12, 31),
                            end_date=df.index.max(),
                            min_date_allowed=df.index.min(),
                            max_date_allowed=df.index.max(),
                            id="date-picker",
                        ),
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    Output("histogram", "figure"),
    Input("asset-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_histogram(assets, start_date, end_date):
    filtered_df = df[start_date:end_date][assets]
    filtered_df = 100 * np.log(1 + filtered_df.pct_change())
    fig = px.histogram(filtered_df.dropna(), nbins=300)
    return fig


@app.callback(
    Output("time-series", "figure"),
    Input("asset-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_time_series(assets, start_date, end_date):
    filtered_df = df[start_date:end_date]
    filtered_df = (
        100 * filtered_df[assets].pct_change().cumsum()
        if len(assets) > 1
        else filtered_df[assets]
    )
    fig = px.line(filtered_df.dropna())
    yaxis_title = "dollars ($)" if len(assets) == 1 else "total return (%)"
    fig.update_layout(yaxis_title=yaxis_title)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
