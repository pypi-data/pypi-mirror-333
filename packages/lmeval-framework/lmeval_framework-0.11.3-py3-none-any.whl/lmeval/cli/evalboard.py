import typer
from pathlib import Path
from typing import Optional, Annotated
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
from plotly import graph_objects as go
from collections import defaultdict
import pandas as pd
import dash_bootstrap_components as dbc

from .data import get_benchmarks_info, get_benchmark_data
from .ui_headtohead import h2h_create_model_selector, h2h_create_diff_chart
from .ui_headtohead import h2h_create_matchup_analysis, h2h_create_question_table
from .ui_singlemodel import sm_create_model_selector, sm_create_radar_chart, sm_create_failures_table

def plot_overall_results(benchmark_path):
    "Bar plot showing the overall accuracy per model"
    data = get_benchmark_data(benchmark_path)
    df = pd.DataFrame(data['overall'].items(), columns=["model", "score"])
    fig = px.bar(df, x="model", y="score")
    fig.update_layout(
        xaxis_title="Model",
        yaxis_title="Accuracy",
        xaxis_tickformat=".21s%",
        xaxis={'categoryorder':'total ascending'}
    )
    return fig


BENCHMARK_DIR = ""


def create_navbar():
    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    BENCHMARKS_NAMES = list(BENCHMARKS.keys())
    return dbc.NavbarSimple(
        children=[
            dbc.Row([
                dbc.Col(
                    dbc.Row([
                        dbc.Col(
                            html.Div("Min Questions:",
                                    style={"lineHeight": "38px", "color": "white"}),
                            width="auto"
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="number",
                                id="min-questions-filter",
                                value=10,
                                min=0,
                                step=1,
                                style={"width": "80px"}
                            ),
                            width="auto"
                        )
                    ],
                    className="align-items-center",
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dcc.Dropdown(
                        BENCHMARKS_NAMES,
                        BENCHMARKS_NAMES[0],
                        id='benchmarks-dropdown',
                        style={"width": "250px"}
                    ),
                    className="ms-3",  # Add margin to the left
                    width="auto"
                ),
            ],
            className="ms-auto align-items-center g-0",  # Push to right, center vertically, remove gutters
            ),
        ],
        brand="LMEvalboard",
        brand_href="#",
        color="primary",
        dark=True,
    )


def app(dir: Annotated[Path,
                       typer.Option(exists=True, file_okay=False, dir_okay=True,
                                    writable=False, readable=True, resolve_path=True)],
                                    port: int = typer.Option(8050, help="Port for the Dash server"),
                                    host: str = typer.Option("127.0.0.1", help="Host for the Dash server")):
    """
    Launch the LMEval Dashboard with the specified benchmark path.
    """
    global BENCHMARK_DIR
    BENCHMARK_DIR = dir

    # let's first load the benchmarks
    # FIXME: use values and options so we can add info to the dropdown
    typer.echo(f"Starting LMEvalBoard with benchmarks from {dir}")


    app = app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)
    app.layout = html.Div([
        create_navbar(),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Tabs(id="tabs", value='overall-tab', children=[
                        dcc.Tab(label='Overall Performance', value='overall-tab'),
                        dcc.Tab(label='Single Model Analysis', value='single-model-tab'),
                        dcc.Tab(label='Head-to-Head Comparison', value='head-to-head-tab'),
                    ]),
                    html.Div(id='tabs-content')
                ])
            ])
        ])
    ])
    app.run(debug=True)

# --- Tab Main Content Renderers ---
# TODO: add model correlation graph
# TODO: add graph with results per category
def render_overall_tab(benchmark):
    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    path = BENCHMARKS[benchmark]["path"]
    typer.echo(f"Rendering overall tab for {benchmark} > {path}")
    overall_fig = plot_overall_results(path)
    return html.Div([
        html.H3("Overall Performance"),
        dcc.Graph(figure=overall_fig)
    ])


# --- Tab main Callback ---
@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'),
          Input('benchmarks-dropdown', 'value'),
          prevent_initial_call=False)
def render_content(tab, benchmark):
    if tab == 'overall-tab':
        return render_overall_tab(benchmark)
    elif tab == 'single-model-tab':
        return render_single_model_tab(benchmark)
    elif tab == 'head-to-head-tab':
        return render_head_to_head_tab(benchmark)
    return html.Div("No content selected.")

## -- Single Model UI --

def render_single_model_tab(benchmark):
    """
    Main render function for single model analysis tab
    """
    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    path = BENCHMARKS[benchmark]["path"]
    data = get_benchmark_data(path)

    return html.Div([
        html.H3("Single Model Analysis"),
        sm_create_model_selector(data),
        html.Div(id='sm-radar-container'),
        html.Div(id='sm-failures-container')
    ])

# Add the callback for the single model tab
@callback(
    [Output('sm-radar-container', 'children'),
     Output('sm-failures-container', 'children')],
    [Input('sm-model-dropdown', 'value'),
     Input('min-questions-filter', 'value')],
    [State('benchmarks-dropdown', 'value')]
)
def sm_update_analysis(model, min_questions, benchmark):
    if not all([model, benchmark]):
        return html.Div("Please select a model"), html.Div()

    min_q = min_questions if min_questions is not None else 10

    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    path = BENCHMARKS[benchmark]["path"]
    data = get_benchmark_data(path)

    return [
        sm_create_radar_chart(data, model, min_q),
        sm_create_failures_table(data, model)
    ]



## --- Head-to-Head UI ---
def render_head_to_head_tab(benchmark):
    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    path = BENCHMARKS[benchmark]["path"]
    data = get_benchmark_data(path)

    return html.Div([
        html.H3("Head-to-Head Model Comparison"),
        h2h_create_model_selector(data),  # This creates the dropdowns
        html.Div(id='h2h-diff-container'),
        html.Div(id='h2h-matchup-container'),
        html.Div(id='h2h-question-container')  # Add container for question table
    ])

@callback(
    [Output('h2h-diff-container', 'children'),
     Output('h2h-matchup-container', 'children'),
     Output('h2h-question-container', 'children')],  # Add output for question table
    [Input('h2h-model1-dropdown', 'value'),
     Input('h2h-model2-dropdown', 'value'),
     Input('min-questions-filter', 'value')],
    [State('benchmarks-dropdown', 'value')]
)
def h2h_update_charts(model1, model2, min_questions, benchmark):
    if not all([model1, model2, benchmark]):
        return html.Div("Please select both models to compare"), html.Div(), html.Div()

    min_q = min_questions if min_questions is not None else 10

    BENCHMARKS = get_benchmarks_info(BENCHMARK_DIR)
    path = BENCHMARKS[benchmark]["path"]
    data = get_benchmark_data(path)

    return [
        h2h_create_diff_chart(data, model1, model2, min_q),
        h2h_create_matchup_analysis(data, model1, model2, min_q),
        h2h_create_question_table(data, model1, model2)
    ]


def main():
    typer.run(app)

def entry_point():
    main()

if __name__ == "__main__":
    main()
