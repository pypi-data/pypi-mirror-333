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

from lmeval.scorers import get_scorer
from lmeval import ScorerType

from .utils import eval_question_answer

def test_always_1():
    scorer = get_scorer(ScorerType.always_1)

    # correct
    real_answer = 'no'
    model_answer = 'no'
    assert eval_question_answer(real_answer, model_answer, scorer)== 1.0

    # incorrect
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['No', 'no']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

def test_always_0():
    scorer = get_scorer(ScorerType.always_0)

    # correct
    real_answer = 'no'
    model_answer = 'no'
    assert eval_question_answer(real_answer, model_answer, scorer)== 0.0

    # incorrect
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['No', 'no']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0