# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from functools import cache
from pathlib import Path

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.PULSE])


@cache
def load_sentiment_data() -> pd.DataFrame:
    data_path = Path.cwd() / "data" / "sentiment_data.csv"
    return pd.read_csv(data_path)


@cache
def load_dod_counts_data() -> pd.DataFrame:
    data_path = Path.cwd() / "data" / "dod_counts.csv"
    return pd.read_csv(data_path)


def get_by_month_summarization(
    add_branch: bool = False, ignore_neutrals: bool = True
) -> pd.DataFrame:
    df = load_sentiment_data()
    branch = ["branch"] if add_branch else []
    df = (
        df[branch + ["date", "polarity", "score"]]
        .groupby(branch + ["date", "polarity"])
        .count()
        .reset_index()
        .rename(columns={"score": "count"})
    )
    if ignore_neutrals:
        df = df[df["polarity"] != "NEU"]
    full_count_df = (
        df.groupby(branch + ["date"])
        .sum("count")
        .reset_index()
        .rename(columns={"count": "sum"})
    )
    df = df.merge(full_count_df, on=branch + ["date"])
    df["prop"] = df["count"] / df["sum"]
    return df


@app.callback(
    Output("sentiment_graph", "figure"),
    [
        Input("data-format", "value"),
        Input("breakdown", "value"),
        Input("ignore-netural", "value"),
    ],
)
def make_sentiment_graph(y, breakdown, ignore_neut):
    additional_options = {}

    if breakdown == "branch":
        additional_options["facet_col"] = "branch"
        additional_options["facet_col_wrap"] = 2

    return px.area(
        get_by_month_summarization(
            add_branch=breakdown == "branch", ignore_neutrals=ignore_neut == "yes"
        ),
        x="date",
        y=y,
        color="polarity",
        template="ggplot2",
        **additional_options
    )


@app.callback(
    Output("dod-graph", "figure"),
    [
        Input("service", "value"),
        Input("branch", "value"),
    ],
)
def make_dod_graph(service, branch):
    df = load_dod_counts_data()
    if service != "none":
        df = df[df["Service"] == service]
    if branch != "none":
        df = df[df["Branch"] == branch]
    df = df.groupby(["Year", "Service"]).sum("Count").reset_index()
    return px.area(
        df,
        x="Year",
        y="Count",
        color="Service",
        log_y=True,
        title="Department of Defense Member Count (Y-axis Log scaled)",
    )


sentiment_controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Y Data (Proportional or Count)"),
                dcc.Dropdown(
                    id="data-format",
                    options=[
                        {"label": "Count", "value": "count"},
                        {"label": "Proportion", "value": "prop"},
                    ],
                    value="count",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Breakdown"),
                dcc.Dropdown(
                    id="breakdown",
                    options=[
                        {"label": "None", "value": "none"},
                        {"label": "By Branch", "value": "branch"},
                    ],
                    value="none",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Ignore Neutrals?"),
                dcc.Dropdown(
                    id="ignore-netural",
                    options=[
                        {"label": "Yes", "value": "yes"},
                        {"label": "No", "value": "no"},
                    ],
                    value="no",
                ),
            ]
        ),
    ],
    body=True,
)


dod_controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Select Branch"),
                dcc.Dropdown(
                    id="branch",
                    options=[
                        {"label": "None", "value": "none"},
                    ]
                    + [
                        {"label": k, "value": k}
                        for k in load_dod_counts_data()["Branch"].unique().tolist()
                    ],
                    value="none",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Select Service"),
                dcc.Dropdown(
                    id="service",
                    options=[
                        {"label": "None", "value": "none"},
                    ]
                    + [
                        {"label": k, "value": k}
                        for k in load_dod_counts_data()["Service"].unique().tolist()
                    ],
                    value="none",
                ),
            ]
        ),
    ],
    body=True,
)

app.layout = html.Div(
    children=[
        dbc.NavbarSimple(
            brand="Impact of Major World Events on the Moral of US Service Members Analysis - CSE 6424 Final Project",
            brand_href="/",
            color="primary",
            dark=True,
            id="navbar",
        ),
        dbc.Container(
            [
                dbc.Row(html.H3("Sentiment Data Analysis")),
                dbc.Row(
                    [
                        dbc.Col(sentiment_controls, md=4),
                        dbc.Col(
                            dcc.Graph(id="sentiment_graph"),
                            md=8,
                        ),
                    ],
                    align="center",
                ),
                html.Hr(),
                dbc.Row(html.H3("Current Member Count of DoD")),
                dbc.Row(
                    [
                        dbc.Col([dod_controls], md=4),
                        dbc.Col(
                            dcc.Graph(id="dod-graph"),
                            md=8,
                        ),
                    ],
                    align="center",
                ),
            ],
            fluid=False,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
