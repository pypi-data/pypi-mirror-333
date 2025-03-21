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

def test_boolean():
    # !you need to test symetrically to test both sides (model answer and true answer) are properly processed

    scorer = get_scorer(ScorerType.boolean_answer)
    # expected good
    #     "Is Paris the capital of France? -> True not in Yes, Paris is the capital of France."

    GOOD_ANSWERS_PAIRS = [
            ['True', 'Yes, Paris is the capital of France'],
            ['true', 'Yes, Paris is the capital of France'],
            ['True', 'True, Paris is the capital of France'],
            ['True', 'Paris is the capital of France that is true'],
            ['True', 'You are correct Paris is the capital of France'],
            ['True', 'You are right Paris is the capital of France'],
            ['False', 'No Paris is not the capital of France'],
            ['False', 'False, Paris is the capital of France'],
            ['Wrong', 'Wrong, Paris is the capital of France'],
            ['No', 'Paris is the capital of France that is false'],
            ['no', 'You are wrong Paris is not the capital of France'],
            ]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

    # # bad answers
    # BAD_ANSWERS_PAIRS = [['no', 'yes'], ['no', 'No'], ['No', 'no'],  ['no', 'N o']]
    BAD_ANSWERS_PAIRS = [
        ['False', 'Yes, Paris is the capital of France'],
        ['Wrong', 'Yes, Paris is the capital of France'],
        ['No', 'True, Paris is the capital of France'],
        ['no', 'Paris is the capital of France that is true'],
        ['incorrect', 'You are correct Paris is the capital of France'],
        ['false', 'You are right Paris is the capital of France'],
        ['True', 'No Paris is not the capital of France'],
        ['yes', 'False, Paris is the capital of France'],
        ['correct', 'Wrong, Paris is the capital of France'],
        ['right', 'Paris is the capital of France that is false'],
        ['CorrEct', 'You are wrong Paris is not the capital of France'],
        ]

    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0