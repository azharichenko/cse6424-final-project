# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from functools import cache
from pathlib import Path

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.COSMO])


@cache
def load_sentiment_data() -> pd.DataFrame:
    data_path = Path.cwd() / "data" / "sentiment_data.csv"
    return pd.read_csv(data_path)


def get_by_month_summarization() -> pd.DataFrame:
    df = load_sentiment_data()
    df = df[["branch", "date", "polarity", "score"]].groupby(["branch", "date", "polarity"]).count().reset_index().rename(columns={"score": "count"})
    return df

fig = px.line(get_by_month_summarization(), x="date", y="count", facet_col="branch", color="polarity")

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
                    html.Div(
                        children="""
        Dash: A web application framework for your data.
    """
                    ),
                    dcc.Graph(id="example-graph", figure=fig),
                ],
            ),
            fluid=True,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
