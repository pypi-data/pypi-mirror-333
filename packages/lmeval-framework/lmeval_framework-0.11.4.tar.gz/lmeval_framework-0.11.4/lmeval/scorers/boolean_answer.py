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

from .scorer import Scorer
from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality


class BooleanAnswerScorer(Scorer):
    name: str = ScorerType.boolean_answer.name
    description: str  = "Returns 1.0 if the model answer yes or true when the real answer is true and no or false when the real answer is false. This avoid the issue that sometime the model answer in various ways"
    type: ScorerType = ScorerType.boolean_answer
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer).lower()

        # various words that convey yes or no
        istrue = ["yes", "true", "correct", "right"]
        isfalse = ["no", "false", "incorrect", "wrong"]

        if qa in istrue:
            expected = istrue
        elif qa in isfalse:
            expected = isfalse
        else:
            raise ValueError(f"Question answer {qa} is not a valid boolean answer - must be in {istrue} or {isfalse}")

        # check various ways the model could have answered
        for v in expected:
            if v in ma:
                return 1.0
        return 0.0