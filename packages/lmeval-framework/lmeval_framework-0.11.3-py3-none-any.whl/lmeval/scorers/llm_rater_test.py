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

from string import Template

from lmeval.fixtures import gemini_mock
from ..models import LMAnswer
from ..question import Question
from .llm_rater import LLMRater


def test_llm_rater(gemini_mock):
    # make a simple template for the rater prompt
    dummy_template = Template("($question) ($expected) ($actual)")
    q1 = 'random question 1'
    a1 = 'random answer 1'
    question_1 = Question(question=q1, answer=a1)
    q2 = 'random question 2'
    a2 = 'random answer 2'
    question_2 = Question(question=q2, answer=a2)
    actual_answer = 'whatever'
    request_response = {
        dummy_template.substitute(question=q1,
                                  expected=a1,
                                  actual=actual_answer):
        '{ "score": 0.5 }',
        dummy_template.substitute(question=q2,
                                  expected=a2,
                                  actual=actual_answer):
        '{ "score": 1.0 }',
    }
    gemini_mock.set_request_response(request_response)
    rater = LLMRater(model=gemini_mock, rater_prompt_template=dummy_template)

    ans_1 = LMAnswer(answer=actual_answer, model=gemini_mock)
    ans_2 = LMAnswer(answer=actual_answer, model=gemini_mock)
    assert rater.score(ans_1, question_1, None) == 0.5
    assert rater.score(ans_2, question_2, None) == 1.0
