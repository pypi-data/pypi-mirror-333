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

import os

from lmeval import LMModel
from lmeval import Evaluator
from lmeval import get_scorer, ScorerType, Question, Task, TaskType
from lmeval import Category, LMModel
from lmeval.evaluator import EvalTask
from lmeval.prompts import SingleWordAnswerPrompt


def many_text_only_tasks(model: LMModel, num_tasks: int = 5) -> list[EvalTask]:
    "return a list of text only tasks"
    questions = [
        ["what is the capital of france?", "paris"],
        ["what is the capital of spain?", "madrid"],
        ["what is the capital of germany?", "berlin"],
        ["what is the capital of italy?", "rome"],
        ["what is the capital of netherlands?", "amsterdam"],
        ["what is the capital of switzerland?", "bern"],
        ["what is the capital of austria?", "vienna"],
        ["what is the capital of portugal?", "lisbon"],
        ["what is the capital of poland?", "warsaw"],
        ["what is the capital of sweden?", "stockholm"],
        ["what is the capital of norway?", "oslo"],
        ["what is the capital of finland?", "helsinki"],
        ["what is the capital of denmark?", "copenhagen"],
        ["what is the capital of greece?", "athens"],
        ["what is the capital of russia?", "moscow"],
        ["what is the capital of turkey?", "ankara"],
        ["what is the capital of ukraine?", "kiev"],
        ["what is the capital of united kingdom?", "london"],
        ["what is the capital of ireland?", "dublin"],
        ["what is the capital of iceland?", "reykjavik"],
        ["what is the capital of czech republic?", "prague"],
        ["what is the capital of slovakia?", "bratislava"],
        ["what is the capital of hungary?", "budapest"],
        ["what is the capital of romania?", "bucharest"],
        ["what is the capital of bulgaria?", "sofia"],
        ["what is the capital of serbia?", "belgrade"],
        ["what is the capital of croatia?", "zagreb"],
        ["what is the capital of bosnia and herzegovina?", "sarajevo"],
        ["what is the capital of albania?", "tirana"],
        ["what is the capital of macedonia?", "skopje"],
        ["what is the capital of montenegro?", "podgorica"],
        ["what is the capital of kosovo?", "pristina"],
        ["what is the capital of slovenia?", "ljubljana"],
        ["what is the capital of estonia?", "tallinn"],
        ["what is the capital of latvia?", "riga"],
        ["what is the capital of lithuania?", "vilnius"],
        ["what is the capital of belarus?", "minsk"],
        ["what is the capital of moldova?", "chisinau"],
        ["what is the capital of armenia?", "yerevan"],
        ["what is the capital of azerbaijan?", "baku"],
        ["what is the capital of georgia?", "tbilisi"],
    ]

    if num_tasks > len(questions):
        raise ValueError(f"num_tasks should be less than {len(questions)}")

    tasks = []
    for id in range(num_tasks):
        task = text_only_task(model, question_id=id, question=questions[id][0],
                              answer=questions[id][1])
        tasks.append(task)
    return tasks


def text_only_task(model: LMModel,
                   question_id: int = 0,
                   question: str = "what is the captial of france?",
                   answer: str = "paris") -> EvalTask:
    # prompt
    prompt = SingleWordAnswerPrompt()

    # create task
    scorer = get_scorer(ScorerType.text_regex_insensitive)
    scorer.regex = r'([a-zA-Z]+)'

    category_name = 'eu'
    category = Category(name=category_name, description='European geography questions')
    task = Task(name='geo', type=TaskType.text_generation, scorer=scorer)
    qst = Question(id=question_id, question=question, answer=answer)
    task = EvalTask(task=task, category=category, question=qst,
                    prompt=prompt, lm_model=model)

    return task


def text_img_task(model: LMModel) -> EvalTask:
    "return a task witn a single question that have text and image"
    # prompt
    prompt = SingleWordAnswerPrompt()

    # create task
    scorer = get_scorer(ScorerType.contain_text_insensitive)
    category_name = 'animal'
    category = Category(name=category_name, description='cat questions')
    task = Task(name='image', type=TaskType.text_generation, scorer=scorer)
    question = Question(id=0, question='what is the animal in the photo?',
                        answer='cat')

    # add images
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'data/cat.jpg')
    question.add_media(image_path)

    task = EvalTask(task=task, category=category, question=question,
                    prompt=prompt, lm_model=model)
    return task

def eval_single_text_generation(model: LMModel):
    # check moded creation and serialization
    assert isinstance(model.model_dump_json(), str)
    task = text_only_task(model)
    task = Evaluator.generate_answer(task)
    task = Evaluator.score_answer(task)
    assert task.score == 1.0
    assert not task.punted
    assert task.question.answer.lower() in task.lm_answer.answer.lower()

def eval_batch_text_generation(model: LMModel):
    "check ability to answer text questions in batch"
    assert isinstance(model.model_dump_json(), str)
    tasks = many_text_only_tasks(model, 5)
    prompts = []
    medias = []
    for task in tasks:
        prompts.append(task.prompt.render(task.question, task.task))
        medias.append(task.question.medias)
    answers = model.batch_generate_text(prompts, medias)
    answers = [a for a in answers if a is not None]
    assert len(answers) == len(tasks)
    for a in answers:
        tasks[a[0]].lm_answer = a[1]
        Evaluator.score_answer(tasks[a[0]])
        print(tasks[a[0]].lm_answer)
    for t in tasks:
        assert t.score == 1.0
        assert not t.punted
        assert t.question.answer.lower() in t.lm_answer.answer.lower()

def eval_image_analysis(model: LMModel):
    "check ability to answer questions about images"
    assert isinstance(model.model_dump_json(), str)
    task = text_img_task(model)
    task = Evaluator.generate_answer(task)
    task = Evaluator.score_answer(task)
    assert task.score == 1.0
    assert not task.punted
    assert task.question.answer.lower() in task.lm_answer.answer.lower()
