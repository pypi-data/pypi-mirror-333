import typer
from collections import defaultdict
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from .utils import pretty_model_name

def h2h_create_model_selector(benchmark_data):
    """
    Creates the model selection component with two dropdowns
    """
    available_models = list(benchmark_data['overall'].keys())

    return dbc.Row([
        dbc.Col([
            html.H5("Model 1"),
            dcc.Dropdown(
                id='h2h-model1-dropdown',
                options=available_models,
                value=available_models[0] if available_models else None,
                clearable=False
            )
        ], width=6),

        dbc.Col([
            html.H5("Model 2"),
            dcc.Dropdown(
                id='h2h-model2-dropdown',
                options=available_models,
                value=available_models[1] if len(available_models) > 1 else available_models[0],
                clearable=False
            )
        ], width=6)
    ], className="mb-4")

def h2h_create_diff_chart(benchmark_data, model1, model2, min_questions=10):
    """
    Creates a vertical chart comparing two models performance across different categories
    """
    # Get categories and scores, but only include categories where both models have scores
    # AND have enough questions
    categories = []
    differences = []

    for cat in benchmark_data['by_category'].keys():
        # Skip if not enough questions in this category
        if benchmark_data['category_num_questions'].get(cat, 0) < min_questions:
            continue

        score1 = benchmark_data['by_category'][cat].get(model1)
        score2 = benchmark_data['by_category'][cat].get(model2)

        if score1 is not None and score2 is not None:  # Only include if both models have scores
            categories.append(cat)
            differences.append(score2 - score1)

    # Create horizontal bar chart
    diff_fig = go.Figure()
    diff_fig.add_trace(go.Bar(
        y=categories,
        x=[d * 100 for d in differences],
        orientation='h',
        marker_color=['blue' if d < 0 else 'orange' for d in differences]
    ))

    # Sort by absolute difference
    sorted_indices = [i for i, _ in sorted(enumerate(differences),
                                         key=lambda x: abs(x[1]),
                                         reverse=True)]

    diff_fig.update_layout(
        title="Performance Difference by Category",
        xaxis_title=f"Score Difference (%) - favors {model1} / + favors {model2}",
        showlegend=False,
        height=800,
        margin=dict(l=200),
        xaxis=dict(
            range=[-100, 100],
            tickformat='d',
            ticksuffix='%'
        ),
        yaxis=dict(
            categoryorder='array',
            categoryarray=[categories[i] for i in sorted_indices]  # Sort categories by difference magnitude
        )
    )
    return dcc.Graph(id='h2h-diff-chart', figure=diff_fig)


def h2h_create_matchup_analysis(benchmark_data, model1, model2, min_questions=10):
    """
    Creates a summary table showing wins/losses/ties and accuracy per category
    """

    results = defaultdict(lambda: {
        'model1_score': 0,
        'model2_score': 0,
        'model1_wins': 0,
        'model2_wins': 0,
        'ties': 0,
        'count': 0
    })

    # Count how many questions we process per category
    processed_counts = defaultdict(int)

    # Create lookup dictionary for quick access
    questions = defaultdict(dict)
    for q in benchmark_data['by_question']:
        questions[q['qid']][q['model']] = q

    # Process each unique question once
    for qid, models_data in questions.items():
        # if model1 in models_data and model2 in models_data:
        q1 = models_data[model1]
        q2 = models_data[model2]
        category = q1['category']
        processed_counts[category] += 1

        # Accumulate scores
        results[category]['model1_score'] += q1['score']
        results[category]['model2_score'] += q2['score']
        results[category]['count'] += 1

        # Track wins/losses/ties
        if q1['score'] > q2['score']:
            results[category]['model1_wins'] += 1
        elif q2['score'] > q1['score']:
            results[category]['model2_wins'] += 1
        else:
            results[category]['ties'] += 1


    # Convert to table format and sort by total
    table_data = []
    for cat, data in results.items():
        if data['count'] < min_questions:
            continue
        m1_acc = (data['model1_score'] / data['count']) * 100 if data['count'] > 0 else 0
        m2_acc = (data['model2_score'] / data['count']) * 100 if data['count'] > 0 else 0
        edge = m1_acc - m2_acc
        table_data.append({
            'Category': cat,
            'M1 Edge': f"{edge:.1f}%" if data['count'] > 0 else "N/A",
            'M1 Wins': data['model1_wins'],
            'M2 Wins': data['model2_wins'],
            'Gap': data['model1_wins'] + data['model2_wins'],
            'Ties': data['ties'],
            'Total': data['count'],
            'M1 Acc': f"{m1_acc:.1f}%" if data['count'] > 0 else "N/A",
            'M2 Acc': f"{m2_acc:.1f}%" if data['count'] > 0 else "N/A",
        })

    # Sort by Total in descending order
    table_data.sort(key=lambda x: x['M1 Edge'], reverse=True)
    return dash_table.DataTable(
        id='h2h-matchup-table',
        columns=[
            {'name': 'Category', 'id': 'Category'},
            {'name': 'M1 Edge', 'id': 'M1 Edge'},
            {'name': 'Q gap', 'id': 'Gap'},
            {'name': 'M1 Wins', 'id': 'M1 Wins'},
            {'name': 'M2 Wins', 'id': 'M2 Wins'},
            {'name': 'Ties', 'id': 'Ties'},
            {'name': 'Total', 'id': 'Total'},
            {'name': 'M1 Acc', 'id': 'M1 Acc'},
            {'name': 'M2 Acc', 'id': 'M2 Acc'},
        ],
        data=table_data,
        sort_action='native',
        style_table={ 'overflowY': 'auto'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '8px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

def h2h_create_question_table(benchmark_data, model1, model2):
    """
    Creates a table showing questions where models disagree
    """
    questions = defaultdict(dict)
    for q in benchmark_data['by_question']:
        questions[q['qid']][q['model']] = q

    question_data = []
    for qid, models_data in questions.items():
        if model1 in models_data and model2 in models_data:
            q1 = models_data[model1]
            q2 = models_data[model2]

            if q1['score'] != q2['score']:
                score_diff = abs(q1['score'] - q2['score'])
                winner = "M1" if q1['score'] > q2['score'] else "M2"

                question_data.append({
                    'Question': q1['question'],
                    'M1 Score': f"{q1['score']:.2f}",
                    'M2 Score': f"{q2['score']:.2f}",
                    'Diff': f"{score_diff:.2f}",
                    'Winner': winner
                })

    question_data.sort(key=lambda x: float(x['Diff']), reverse=True)

    return dash_table.DataTable(
        id='h2h-question-table',
        columns=[
            {'name': 'Question', 'id': 'Question'},
            {'name': 'Winner', 'id': 'Winner'},
            {'name': 'Diff', 'id': 'Diff'},
            {'name': 'M1 Score', 'id': 'M1 Score'},
            {'name': 'M2 Score', 'id': 'M2 Score'},


        ],
        data=question_data,
        page_size=10,
        style_table={'overflowY': 'auto', 'margin-top': '50px'},
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
                'width': '80%',
                'minWidth': '400px'
            },
            {
                'if': {'column_id': 'M1 Score'},
                'width': '5%'
            },
            {
                'if': {'column_id': 'M2 Score'},
                'width': '5%'
            },
            {
                'if': {'column_id': 'Diff'},
                'width': '5%'
            },
            {
                'if': {'column_id': 'Winner'},
                'width': '5%'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )
