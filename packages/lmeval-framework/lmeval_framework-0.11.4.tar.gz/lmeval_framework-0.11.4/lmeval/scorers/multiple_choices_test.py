# Copyright 2025 Google LLC
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

from lmeval import LMAnswer, LMModel
from lmeval import Task, Question, QuestionSource
from lmeval.enums import TaskType
from lmeval.scorers import Scorer
from .multiple_choices import ContainAnswerLetterInsensitive, ContainAnswerLettersInsensitive


def _eval_multiple_choice(answer_letter: str,
                          model_answer: str, scorer: Scorer) -> float:
    question = Question(id=0,
                        answer = 'not_used',
                        answer_letter=answer_letter,
                        question ='Is the sky red?',
                        source = QuestionSource(name="demo", description="Demo question source"))
    task = Task(name="task demo", type=TaskType.boolean,
                scorer=scorer)

    mld = LMModel(name="demo", publisher='test', version_string="demo-1.0")
    mdl_answer = LMAnswer(answer=model_answer, raw_response=model_answer,
                          generation_time=1.0, model=mld)

    return scorer.score(mdl_answer, question, task)

def test_single_answer():

    scorer = ContainAnswerLetterInsensitive()
    # expected good
    GOOD_ANSWERS_PAIRS = [['C', 'C'], ['C', 'c'], ['c', 'C'], ['c', 'c'],
                          ['C ', ' c'], [' c ', 'C']]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert _eval_multiple_choice(real_answer, model_answer, scorer) == 1.0

    BAD_ANSWERS_PAIRS = [['C', 'A'], ['C', 'B'], ['C', 'D'], ['C', 'E']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert _eval_multiple_choice(real_answer, model_answer, scorer) == 0.0

def test_multiple_answers():

    scorer = ContainAnswerLettersInsensitive()
    # expected good
    GOOD_ANSWERS_PAIRS = [['C', 'C'], ['C', 'c'], ['c', 'C'], ['c', 'c'],
                          ['C ', ' c'], [' c ', 'C'], ['a,b,c', 'c,a,b'],
                          ['a,b,c', 'A,B,c'], ['a, b, c,', 'a, c, b ,'], ['A,B,C', 'c,a,b']]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert _eval_multiple_choice(real_answer, model_answer, scorer) == 1.0

    BAD_ANSWERS_PAIRS = [['C,D', 'A'], ['C', 'B,A'], ['C', 'A,d']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert _eval_multiple_choice(real_answer, model_answer, scorer) == 0.0

    # 0.5 score
    assert _eval_multiple_choice('C,D', 'C', scorer) == 0.5
    assert _eval_multiple_choice('D', 'D,C', scorer) == 0.5
