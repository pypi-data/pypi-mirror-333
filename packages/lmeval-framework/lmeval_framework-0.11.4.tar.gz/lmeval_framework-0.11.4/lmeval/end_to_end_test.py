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

"end to end unit test"

import re
from pprint import pprint
from lmeval import Benchmark, Category
from lmeval import Task, Question
from lmeval.models.gemini import GeminiModel
from lmeval import get_scorer, list_scorers, ScorerType
from lmeval import TaskType, QuestionSource, LMAnswer, LMModel
from lmeval.prompts import QuestionOnlyPrompt, MultiChoicesPrompt, TrueOrFalseAnswerPrompt
from lmeval.prompts import MultiChoicesPrompt, MultiChoicesMultiAnswersPrompt
from lmeval import Question, Task, TaskType, ScorerType, Evaluator
from lmeval.evaluator import EvalTask
from lmeval.fixtures import gemini_mock, gemini_pro15_mock, get_country_boolean, get_country_multi_choice, get_country_generation


def _find_letter(answer: str, prompt: str):
  "Find the letter associated with the answer in the prompt."
  match = re.search(f'(.):{answer}', prompt)
  assert match
  return match.group(1)


def test_e2e_benchmarking(gemini_mock, gemini_pro15_mock):
    NUM_QUESTIONS = 2  # per task

    request_response = {}  # prompt and answers exptected

    ## benchmark creation
    benchmark = Benchmark(name='geo', description='Geography questions')

    # add category
    category_name = 'eu'
    category = Category(name=category_name, description='European geography questions')
    benchmark.categories.append(category)

    # add boolean task and questions
    task = Task(name='capital_bool', type=TaskType.boolean, scorer=get_scorer(ScorerType.boolean_answer))
    for idx in range(NUM_QUESTIONS):
        # random capital question
        data = get_country_boolean()
        question = Question(question=data['question'], answer=data['answer'])
        rendered_question = TrueOrFalseAnswerPrompt().render(question, task)
        request_response[rendered_question] = data['answer']
        task.add_question(question)
    benchmark.categories[0].tasks.append(task)

    # adding a 2nd task with generation text to check heterogenous tasks support
    task2 = Task(name='capital_gen', type=TaskType.text_generation, scorer=get_scorer(ScorerType.contain_text_insensitive))
    for idx in range(NUM_QUESTIONS):
        # random capital question
        data = get_country_generation()
        question = Question(question=data['question'], answer=data['answer'])
        rendered_question = QuestionOnlyPrompt().render(question, task2)
        request_response[rendered_question] = data['answer']
        task2.add_question(question)

        # question id is assigned by add_question so must be after
        assert isinstance(question.id, int) and question.id >= 0


    benchmark.categories[0].tasks.append(task2)

    for category in benchmark.categories:
        for task in category.tasks:
            print(f"Category: {category.name}, Task: {task.name}")
            for question in task.questions:
                print(f"Question: {question.question}, Answer: {question.answer}")


    # check benchmark creation
    stats = benchmark.get_stats()
    assert stats['questions'] == NUM_QUESTIONS * 2
    assert stats['answers'] == 0
    assert stats['prompts'] == {}
    assert len(stats['categories_stats']) == 1
    assert category_name in stats['categories_stats']
    assert len(stats['tasks_stats'][category_name]) == 2
    assert 'capital_bool' in stats['tasks_stats'][category_name]
    assert 'capital_gen' in stats['tasks_stats'][category_name]
    assert stats['tasks_stats'][category_name]['capital_bool']['questions'] == NUM_QUESTIONS
    assert stats['tasks_stats'][category_name]['capital_gen']['questions'] == NUM_QUESTIONS


    # setup eval
    models = [gemini_mock, gemini_pro15_mock]   # two models to check multiple models support
    gemini_mock.set_request_response(request_response)
    gemini_pro15_mock.set_request_response(request_response)
    # adding irrelevant prompt to check proper prompt selection
    prompts = [QuestionOnlyPrompt(), TrueOrFalseAnswerPrompt(), MultiChoicesPrompt()]
    evaluator = Evaluator(benchmark)

    # plan execution
    plan_report = evaluator.plan(models=models, prompts=prompts)
    assert len(plan_report) == 2
    for _, model_report in plan_report.items():
        assert len(model_report) == len(models)
        for t in model_report:
            assert t['category'] == category_name
            assert t['planned'] == NUM_QUESTIONS
            assert t['existing'] == 0

    # execute
    evaluated_benchmark = evaluator.execute()
    evaluated_benchmark.summary()

    # check results
    assert len(evaluated_benchmark.categories) == 1
    assert len(evaluated_benchmark.categories[0].tasks) == 2
    for task in evaluated_benchmark.categories[0].tasks:
        assert len(task.questions) == NUM_QUESTIONS
        for question in task.questions:
            assert len(question.lm_answers) == 1 # num expected prompts
            for prompt_name, prompt_answers in question.lm_answers.items():
                assert len(prompt_answers) == len(models)  # num models
                for model_name, answer in prompt_answers.items():

                    assert isinstance(answer, LMAnswer)
                    assert answer.score == 1.0, f"{question.question} -> {question.answer} not in {answer.answer}"
                    assert not answer.ispunting
                    assert question.answer.lower() in answer.answer.lower()
                    assert answer.id  # do we preserve the model completion id?
                    print(f"Model: {model_name}, Prompt: {prompt_name}, Question: {question.question}, Answer: {answer.answer}, Score: {answer.score}")

def test_e2e_boolean(gemini_mock):
    NUM_QUESTIONS = 3
    category = Category(name='geo', description='Geography questions')
    task = Task(name='Cities', type=TaskType.boolean, scorer=get_scorer(ScorerType.boolean_answer))
    request_response = {}

    for idx in range(NUM_QUESTIONS):
        # random capital question
        data = get_country_boolean()
        question = Question(id=0, question=data['question'], answer=data['answer'])

        # check prompt rendering
        rendered_question = TrueOrFalseAnswerPrompt().render(question, task)
        assert data['question'] in rendered_question
        assert data['answer'] not in rendered_question
        print('question:\n',  question)
        print('rendered_template:\n', rendered_question)
        # set mock data
        request_response[rendered_question] = data['answer']
        gemini_mock.set_request_response(request_response)
        # check prompt works correctly
        answer = gemini_mock.generate_text(rendered_question)
        assert data['answer'].lower() in answer.answer.lower()

        # check evaluator works correctly
        etask = EvalTask(benchmark_name='test_e2e_boolean',
                         category=category, task=task, question=question,
                         lm_model=gemini_mock,
                         prompt=TrueOrFalseAnswerPrompt())

        etask = Evaluator.generate_answer(etask)
        assert data['answer'].lower() in etask.lm_answer.answer.lower()
        assert rendered_question == etask.lm_answer.text_prompt
        assert etask.lm_answer.steps[0].execution_time > 0

def test_e2e_multi(gemini_mock):
    NUM_QUESTIONS = 5
    category = Category(name='geo', description='Geography questions')
    task = Task(name='Cities', type=TaskType.multiple_choices, scorer=get_scorer(ScorerType.contains_answer_letter_insensitive))
    request_response = {}

    for idx in range(NUM_QUESTIONS):
        # random capital question
        data = get_country_multi_choice()
        assert data['answer'] not in data['choices']  # sanity check
        question = Question(id=0, question=data['question'], choices=data['choices'],
                            answer=data['answer'])

        # check prompt rendering
        rendered_question = MultiChoicesPrompt().render(question, task)
        assert data['question'] in rendered_question
        for choice in data['choices']:
            assert choice in rendered_question
        for letter, answer in question.letter_mapping.items():
            assert f"{letter}:{answer}" in rendered_question

        print('question:\n',  question)
        print('rendered_template:\n', rendered_question)

        # extract the correct answer for the mock
        letter = _find_letter(data['answer'], rendered_question)
        request_response[rendered_question] = letter
        gemini_mock.set_request_response(request_response)

        # double check that it match the letter mapping
        assert letter in question.letter_mapping
        assert question.letter_mapping[letter] == data['answer']

        # check evaluator works correctly
        etask = EvalTask(benchmark_name='test_e2e_multi',
                         category=category, task=task, question=question,
                         lm_model=gemini_mock, prompt=MultiChoicesPrompt())

        etask = Evaluator.generate_answer(etask)
        etask = Evaluator.score_answer(etask)

        print('lm_amswer:', etask.lm_answer.answer)
        assert etask.lm_answer.score == 1.0
        assert rendered_question == etask.lm_answer.text_prompt

def test_e2e_multi_answers():
    "We need the real Gemini for this one"
    real_gemini = GeminiModel()
    prompt = MultiChoicesMultiAnswersPrompt()
    question_text = "What is true about Paris"
    question = Question(id=1,
                        question=question_text,
                        answer="It is the capital of France",
                        additional_answers=["The Louvre is there",
                                            "The effeil tower is there"],
                        choices=["It is the capital of Portugal",
                                 "It is the capital of Germany",
                                 "The Guggenheim museum is there",
                                 "THe MoMa is there"])
    category = Category(name='geo', description='Geography questions')

    task = Task(name="Paris Info",
                type=TaskType.multiple_choices_multiple_answers,
                scorer=get_scorer(ScorerType.contains_answer_letters_insensitive))
      # check prompt rendering
    rendered_question = prompt.render(question, task)
    assert question.question in rendered_question
    assert question.answer in rendered_question
    assert question.answer in question.letter_mapping.values()
    for choice in question.choices:
        assert choice in rendered_question
        assert choice in question.letter_mapping.values()

    for answer in question.additional_answers:
        assert answer in rendered_question
        assert answer in question.letter_mapping.values()

    # check evaluator works correctly on a real model
    etask = EvalTask(benchmark_name='test_e2e_multi_answers',
                    category=category, task=task, question=question,
                    lm_model=real_gemini,
                    prompt=MultiChoicesMultiAnswersPrompt())

    etask = Evaluator.generate_answer(etask)
    etask = Evaluator.score_answer(etask)

    print('\nrendered:', rendered_question)
    print('question_letter:', question.letters)
    print("answer_letter", question.answer_letter)
    print('lm_amswer:', etask.lm_answer.answer)
    print('scorer_type', type(etask.task.scorer))
    assert etask.lm_answer.score == 1.0


def test_e2e_text_generation(gemini_mock):
    NUM_QUESTIONS = 3
    category = Category(name='geo', description='Geography questions')
    task = Task(name='Cities', type=TaskType.text_generation, scorer=get_scorer(ScorerType.contain_text_insensitive))
    request_response = {}

    for idx in range(NUM_QUESTIONS):
        # random capital question
        data = get_country_generation()
        question = Question(id=0, question=data['question'], answer=data['answer'])

        # check prompt rendering
        rendered_question = QuestionOnlyPrompt().render(question, task)
        assert data['question'] in rendered_question
        assert data['answer'] not in rendered_question

        print('question:\n',  question)
        print('rendered_template:\n', rendered_question)
        request_response[rendered_question] = data['answer']
        gemini_mock.set_request_response(request_response)

        # check prompt works correctly
        answer = gemini_mock.generate_text(rendered_question)
        assert data['answer'].lower() in answer.answer.lower()

        # check evaluator works correctly
        etask = EvalTask(benchmark_name='test_e2e_text_generation', category=category,
                         task=task, question=question, lm_model=gemini_mock,
                         prompt=QuestionOnlyPrompt())

        etask = Evaluator.generate_answer(etask)
        etask = Evaluator.score_answer(etask)

        print('lm_amswer:', etask.lm_answer.answer)
        assert etask.lm_answer.score == 1.0
        assert rendered_question == etask.lm_answer.text_prompt