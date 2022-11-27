# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from functools import cache
from pathlib import Path

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.DARKLY])


@cache
def load_sentiment_data() -> pd.DataFrame:
    data_path = Path.cwd() / "data" / "sentiment_data.csv"
    return pd.read_csv(data_path)


def get_by_month_summarization() -> pd.DataFrame:
    df = load_sentiment_data()
    df = df[["branch", "date", "polarity", "score"]].groupby(["branch", "date", "polarity"]).count().reset_index().rename(columns={"score": "count"})
    df = df[df["polarity"] != "NEU"]
    full_count_df = df.groupby(["branch", "date"]).sum("count").reset_index().rename(columns={"count": "sum"})
    df = df.merge(full_count_df, on=["branch", "date"])
    df["prop"] = df["count"] / df["sum"]
    return df

fig = px.area(get_by_month_summarization(), x="date", y="prop", facet_col="branch", color="polarity", template="plotly_dark")

app.layout = html.Div(
    children=[
        dbc.NavbarSimple(
            brand="CSE 6424 Final Project",
            brand_href="/",
            color="primary",
            dark=True,
            id="navbar",
        ),
        dbc.Container(
            html.Div(
                id="page-content",
                children=[
                    dcc.Graph(id="example-graph", figure=fig),
                ],
            ),
            fluid=True,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
