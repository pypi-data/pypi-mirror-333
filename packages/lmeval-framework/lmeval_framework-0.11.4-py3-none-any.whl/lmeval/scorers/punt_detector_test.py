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

from lmeval import get_scorer, ScorerType, Question, Task, LMAnswer
from ..fixtures import gemini_mock

def test_punt_detector(gemini_mock):
    punt_detector = get_scorer(ScorerType.punt_detector)
    punt_detector.model = gemini_mock

    question = Question(id=0, question='what is the capital of france?', answer='Paris')

    non_punt_answers = ['Paris', 'paris', 'paris?', 'Berlin',
                        "I am unsure", "I don't know"]
    gemini_mock.set_default_response('answered')
    for answer in non_punt_answers:
        lmanswer = LMAnswer(answer=answer, raw_response=answer,
                            generation_time=0.0, model=gemini_mock)
        print(answer)
        score = punt_detector.score(lmanswer, question, task=None)
        assert score == 0.0

    punt_answers = ["I can't answer", "I refuse to answer",
                    "I am just a language model"]
    gemini_mock.set_default_response('refused')
    for answer in punt_answers:
        lmanswer = LMAnswer(answer=answer, raw_response=answer,
                            generation_time=0.0, model=gemini_mock)
        score = punt_detector.score(lmanswer, question, task=None)
        print(punt_answers)
        assert score == 1.0
