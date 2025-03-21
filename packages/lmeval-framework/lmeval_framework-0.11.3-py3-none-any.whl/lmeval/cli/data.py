import typer
from functools import cache
from pathlib import Path
from collections import defaultdict
from ..benchmark import load_benchmark, get_benchmarks_metadata, list_benchmarks


@cache
def get_benchmarks_info(dir: str|Path) -> dict:

    tmp = get_benchmarks_metadata(dir)
    BENCHMARKS = {}
    for benchmark in tmp:
        print(benchmark['name'])
        BENCHMARKS[benchmark["name"]] = benchmark

    if not len(BENCHMARKS):
        typer.echo("[red]No benchmarks found")
        exit(1)
    typer.echo(f"Found {len(BENCHMARKS)} benchmarks")
    return BENCHMARKS


@cache
def get_benchmark_data(benchmark_path: str):
    typer.echo(f'Loading benchmark from {benchmark_path}')
    benchmark = load_benchmark(benchmark_path)
    metadata = benchmark.get_stats()
    # for k,v in metadata.items():
    #     print(k,v)

    # overall num questions
    total_num_questions = metadata['questions']
    # questions per category
    cat_num_questions = defaultdict(int)
    for cat, data in metadata['categories_stats'].items():
        cat_num_questions[cat] += data['questions']

    # questions per category/task
    tasks_num_questions = defaultdict(dict)
    for cat, task_data in metadata['tasks_stats'].items():
        for task, data in task_data.items():
            num_questions = data['questions']
            tasks_num_questions[cat][task] = num_questions

    typer.echo(f'Total number of questions: {total_num_questions}')


    # compute scores
    records = benchmark.to_records()
    overall_scores= defaultdict(int)
    category_scores = defaultdict(lambda: defaultdict(int))

    for record in records:
        overall_scores[record["model"]] += record["score"]
        category_scores[record["model"]][record["category"]] += record["score"]


    # normalize scores and convert in records
    categories_records = []
    by_category = defaultdict(dict)
    for model, data in category_scores.items():
        for category, score in data.items():
            num_questions = cat_num_questions[category]
            score = max(category_scores[model][category] / num_questions, 0)
            categories_records.append({
                "model": model,
                "category": category,
                "score": score,
                "num_questions": num_questions
            })
            # invert order
            by_category[category][model] = score

    for model in overall_scores.keys():
        overall_scores[model] /= total_num_questions
        overall_scores[model] = max(overall_scores[model], 0)

    # FIXME: return the categories records if needed
    return {
        "overall": overall_scores, # used for overall bar plot
        "category_records": categories_records,
        "category_num_questions": cat_num_questions,
        "by_category": by_category,  # used for radar chart
        "by_question": records  # used for questions tables and matchup
    }