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

def test_regex_sensitive():
    # !you need to test symetrically to test both sides (model answer and true answer) are properly processed

    scorer = get_scorer(ScorerType.text_regex_sensitive)
    scorer.regex = r'answer: +(.{2,3})'

    # expected good
    # format: [[real_answer, model_answer], ...]
    GOOD_ANSWERS_PAIRS = [['no', 'answer: no'],
                          ['no', 'answer:  no '],
]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

    # bad answers
    # format: [[real_answer, model_answer], ...]

    BAD_ANSWERS_PAIRS = [['no', 'yes'],
                         ['no', 'answer: No'],
                         ['No', 'Answer: no'],
                         ['nO', 'AnSwer: No'],
                         ['no', 'AnSwer: No'],
                         ['no', 'No']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0


def test_regex_insensitive():
    # !you need to test symetrically to test both sides (model answer and true answer) are properly processed

    scorer = get_scorer(ScorerType.text_regex_insensitive)
    scorer.regex = r'answer: +(.{2,3})'

    # expected good
    # format: [[real_answer, model_answer], ...]
    GOOD_ANSWERS_PAIRS = [['no', 'answer: no'],
                          ['no', 'answer: No'],
                          ['No', 'answer: no'],
                          ['no', 'answer:  no '],
                          ['No', 'answer:  no '],
                          ['no', 'AnSwer: No']]
    for pair in GOOD_ANSWERS_PAIRS:
        print(pair)
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

    # bad answers
    # format: [[real_answer, model_answer], ...]
    BAD_ANSWERS_PAIRS = [['no', 'yes'],
                         ['No', 'no']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0
