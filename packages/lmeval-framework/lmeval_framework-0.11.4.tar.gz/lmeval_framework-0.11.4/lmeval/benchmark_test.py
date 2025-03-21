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

"""Unit tests for benchmark."""
import os
import pytest
from time import time
from lmeval import Benchmark, Category, load_benchmark, list_benchmarks
from lmeval import Task, Question, LMAnswer, LMModel
from lmeval.scorers import TextExactSensitive
from lmeval import TaskType, QuestionSource
from lmeval.prompts import QuestionOnlyPrompt
from lmeval.utils import Path
from lmeval import get_scorer
from lmeval import ScorerType


@pytest.fixture
def bench():
    "benchmark fixture"
    prompt = QuestionOnlyPrompt()
    benchmark = Benchmark(name="demo", description="Demo benchmark")
    category = Category(name="demo_category", description="Demo category")
    benchmark.categories.append(category)

    task = Task(name="task demo", type=TaskType.boolean, scorer=TextExactSensitive())
    category.tasks.append(task)

    source = QuestionSource(name="demo", description="Demo question source")
    question = Question(id=1, source=source, question="Is the sky red?", answer='no')
    task.questions.append(question)

    model = LMModel(name="demo", publisher='test', version_string="demo-1.0")
    lmanswer = LMAnswer(answer="Answer: no", raw_response="Answer: No",
                        generation_time=1, score=1.0, model=model)

    question.lm_answers[str(prompt)] = {}
    question.lm_answers[str(prompt)][model.version_string] = lmanswer

    return benchmark

def test_querying(bench):
    "test querying"
    assert bench.get_category("demo_category").name == "demo_category"
    assert bench.get_task("demo_category","task demo").name == "task demo"

    for name in  ['task Q/A', 'task /a /a']:
        bench.categories[0].tasks[0].name = name
        assert bench.get_task("demo_category", name).name == name


def test_summary(bench):
    "test summary"
    bench.summary()


def test_to_dataframe(bench):
    bench.to_dataframe()


def test_creation_and_serialization(tmp_path_factory):

    # create a benchmark
    benchmark = Benchmark(name="demo", description="Demo benchmark")

    # select a prompt
    prompt = QuestionOnlyPrompt()

    # add a category
    category = Category(name="demo", description="Demo category")
    category = Category(name="demo2", description="Demo category2")
    benchmark.categories.append(category)

    # add a task to the cateogry
    # prompt use a template so you can access all the fields of question

    task = Task(name="task demo",
                type=TaskType.boolean,
                scorer=TextExactSensitive())
    category.tasks.append(task)

    question_text = "Is the sky red?"
    source = QuestionSource(name="demo", description="Demo question source")
    for i in range(10):

        question = Question(id=i,  # id is needed to identify the question
                            source=source,
                            question=question_text,
                            answer='no')
        task.questions.append(question)


    model = LMModel(name="demo", publisher='test', version_string="demo-1.0")
    lmanswer = LMAnswer(answer="Answer: no", raw_response='Answer: no', generation_time=1.0, score=-1.0, model=model)
    task.questions[0].lm_answers[prompt.version_string()] = {model.version_string: lmanswer}


    print(task.scorer.name)
    print(task.scorer)
    assert benchmark.categories[0].tasks[0].questions[0].question == question_text

    # serialize the benchmark
    bench_dir = tmp_path_factory.mktemp("benchamrk_files") / f"{int(time())}"
    path = bench_dir / "benchmark_test.db"
    path = path.as_posix()
    benchmark.save(path)

    # reload
    benchmark2 = load_benchmark(path)
    assert benchmark.name == benchmark2.name

    # category
    assert benchmark.categories[0].name == benchmark2.categories[0].name

    # task group
    assert benchmark.categories[0].name == benchmark2.categories[0].name

    # tasks
    assert benchmark.categories[0].tasks[0].name == benchmark2.categories[0].tasks[0].name
    assert benchmark.categories[0].tasks[0].type == benchmark2.categories[0].tasks[0].type
    assert benchmark.categories[0].tasks[0].scorer.name == benchmark2.categories[0].tasks[0].scorer.name

    # questions
    assert benchmark.categories[0].tasks[0].questions[0].question == benchmark2.categories[0].tasks[0].questions[0].question

    # test list_benchmarks
    bechmarks_paths = list_benchmarks(bench_dir.as_posix())
    assert len(bechmarks_paths) == 1
    assert bechmarks_paths[0] == path


def test_double_save(tmp_path_factory, bench):
    # serialize the benchmark
    bench_dir = tmp_path_factory.mktemp("benchamrk_files") / f"{int(time())}"
    path = bench_dir / "benchmark_test.db"
    path = path.as_posix()
    bench.save(path)

    # reload
    benchmark2 = load_benchmark(path)
    assert bench.name == benchmark2.name

    # save again
    benchmark2.save(path)
    benchmark3 = load_benchmark(path)
    assert benchmark2.name == benchmark3.name

def test_save_load_multimedia_benchmark(tmp_path_factory):
    bench_dir = tmp_path_factory.mktemp("benchmark_files") / f"{int(time())}"
    path = bench_dir / "benchmark_test.db"
    SAVE_PATH = path.as_posix()
    # create a benchmark object
    benchmark = Benchmark(name='Cat Visual Questions',
                        description='Ask questions about cats picture')

    # define category
    category = Category(name='cat Q/A')
    benchmark.categories.append(category)

    # define task
    scorer = get_scorer(ScorerType.contain_text_insensitive)
    task = Task(name='Eyes color', type=TaskType.text_generation, scorer=scorer)
    category.tasks.append(task)

    # add questions
    source = QuestionSource(name='cookbook')
    # cat 1 question - create question then add media image
    qtxt = "what is the colors of eye?"
    question = Question(id=0, question=qtxt,
                        answer='blue', source=source)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'models/data/cat.jpg')
    question.add_media(image_path)
    task.questions.append(question)

    # save benchmark
    benchmark.save(SAVE_PATH)
    filename = benchmark.categories[0].tasks[0].questions[0].medias[0].filename
    content_len = len(benchmark.categories[0].tasks[0].questions[0].medias[0].content)

    benchmark2 = load_benchmark(SAVE_PATH)
    assert benchmark.categories[0].tasks[0].questions[0].question == qtxt
    assert benchmark2.categories[0].tasks[0].questions[0].medias[0].modality == 'image'
    assert benchmark2.categories[0].tasks[0].questions[0].medias[0].filename == filename
    content_len2 = len(benchmark2.categories[0].tasks[0].questions[0].medias[0].content)
    assert content_len2 == content_len

    benchmark2.save(SAVE_PATH)
    assert benchmark2.categories[0].tasks[0].questions[0].medias[0].modality == 'image'
    assert benchmark2.categories[0].tasks[0].questions[0].medias[0].filename == filename


    benchmark3 = load_benchmark(SAVE_PATH)
    assert benchmark.name == benchmark3.name
    assert benchmark3.categories[0].tasks[0].questions[0].question == qtxt
    assert benchmark3.categories[0].tasks[0].questions[0].medias[0].modality == 'image'