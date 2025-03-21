from collections import defaultdict
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def sm_create_model_selector(benchmark_data):
    """
    Creates the model selection component with single dropdown
    """
    available_models = list(benchmark_data['overall'].keys())

    return dbc.Row([
        dbc.Col([
            html.H5("Select Model"),
            dcc.Dropdown(
                id='sm-model-dropdown',
                options=available_models,
                value=available_models[0] if available_models else None,
                clearable=False
            )
        ], width=6)
    ], className="mb-4")

def sm_create_radar_chart(benchmark_data, model, min_questions=10):
    """
    Creates a radar chart showing model performance across categories
    """
    categories = []
    scores = []

    for cat in benchmark_data['by_category'].keys():
        if benchmark_data['category_num_questions'].get(cat, 0) < min_questions:
            continue

        score = benchmark_data['by_category'][cat].get(model)
        if score is not None:
            categories.append(cat)
            scores.append(score)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[s * 100 for s in scores],  # Convert to percentages
        theta=categories,
        fill='toself',
        name=model
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Percentage scale
            )),
        showlegend=False,
        title=f"Performance by Category: {model}"
    )

    return dcc.Graph(id='sm-radar-chart', figure=fig)

def sm_create_failures_table(benchmark_data, model):
    """
    Creates a table showing questions where model got wrong answers
    """
    question_data = []

    for q in benchmark_data['by_question']:
        if q['model'] == model and q['score'] < 1:  # Only show incorrect answers
            question_data.append({
                'Question': q['question'],
                'Model Answer': q['model_answer'],
                'Expected Answer': q['real_answer'],
                'Category': q['category']
            })

    # Sort by category to group related failures
    question_data.sort(key=lambda x: x['Category'])

    return dash_table.DataTable(
        id='sm-failures-table',
        columns=[
            {'name': 'Category', 'id': 'Category'},
            {'name': 'Question', 'id': 'Question'},
            {'name': 'Expected A', 'id': 'Expected Answer'},
            {'name': 'Model A', 'id': 'Model Answer'}
        ],
        data=question_data,
        page_size=20,
        style_table={'overflowY': 'auto'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '8px',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Question'},
                'width': '30%',
                'minWidth': '300px'
            },
            {
                'if': {'column_id': 'Model Answer'},
                'width': '25%',
                'minWidth': '250px'
            },
            {
                'if': {'column_id': 'Expected Answer'},
                'width': '25%',
                'minWidth': '250px'
            },
            {
                'if': {'column_id': 'Category'},
                'width': '20%'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )
