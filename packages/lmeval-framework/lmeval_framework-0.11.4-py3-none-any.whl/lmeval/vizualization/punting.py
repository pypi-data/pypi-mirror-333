# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from pandas.core.frame import DataFrame
from IPython.display import display, clear_output
from ipywidgets import widgets
import matplotlib.pyplot as plt

from ..benchmark import Benchmark


def punt_rate_overall_plot(benchmark: Benchmark, figsize=(10, 6)):
    "plot the overall punt rate for each model evaluated in the benchmark"
    BENCHMARK_STATS = benchmark.get_stats()
    df = benchmark.to_dataframe()
    num_questions = BENCHMARK_STATS['questions']
    agg_col_name = "punt rate"
    punt_df = df.groupby(['model'])['punting'].sum().reset_index()
    punt_df[agg_col_name] = (punt_df['punting'] / num_questions) * 100
    punt_df = punt_df.sort_values(agg_col_name)
    punt_df.plot.bar(x='model', y=agg_col_name, rot=90,
                    title=f'Models punt rate for {benchmark.name}',
                    figsize=figsize)

_DF: DataFrame = None
_MODEL_SELECT = None


def _update_model_chart(model_name: str):
    "plot the punt rate by category for the selected model"
    # Filter data for the selected model
    filtered_df = _DF[_DF['model'] == model_name]

    # Group the data by category and prompt, calculate the punt rate for each combination
    grouped_df = filtered_df.groupby(['category', 'prompt']).agg({'punting': 'mean', 'qid': 'count'}).reset_index()
    grouped_df = grouped_df.rename(columns={'punting': 'punt_rate'})

    # Pivot the data to create separate columns for each prompt
    pivoted_df = grouped_df.pivot(index='category', columns='prompt', values='punt_rate')

    # Clear the previous chart and display the new one
    clear_output(wait=True)
    display(_MODEL_SELECT)

    # Create the horizontal bar chart
    ax = pivoted_df.plot.barh(figsize=(15, 10))
    ax.set_ylabel('Category')
    ax.set_xlabel('Punt Rate')
    ax.set_title(f"Model '{model_name}' punt rate by category and prompt")
    ax.legend(title='Prompt')

    plt.tight_layout()
    plt.show()

def punt_rate_per_model_widget(benchmark: Benchmark, figsize=(15, 10)):
    "create an interactive widget to display punt rate by category for each model in the benchmark"
    global _DF, _MODEL_SELECT
    # Get the list of unique models
    _DF = benchmark.to_dataframe()
    models = _DF['model'].unique()

    # Create a Jupyter select box for model selection
    _MODEL_SELECT = widgets.Dropdown(options=models, description='Select Model:')

    # Display the select box and bind the update_chart function to the selection change event
    display(_MODEL_SELECT)
    _MODEL_SELECT.observe(lambda change: _update_model_chart(change['new']), names='value')

    # Initialize the chart with the first model
    _update_model_chart(models[0])
