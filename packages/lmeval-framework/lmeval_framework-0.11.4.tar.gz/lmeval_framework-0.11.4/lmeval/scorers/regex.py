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

import re
from .scorer import Scorer
from ..question import Question
from ..models import LMAnswer
from ..enums import ScorerType, Modality

class TextSensitiveRegex(Scorer):
    name: str = ScorerType.text_regex_sensitive.name
    description: str  = "Returns 1.0 if the case sensitive model answer match the regex extraction"
    type: ScorerType = ScorerType.text_exact_sensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        mdl_answer = self._cleanup(model_answer.answer)
        answer_match = re.search(self.regex, mdl_answer)
        qa = self._cleanup(question.answer)

        if debug:
            print(answer_match, qa, mdl_answer)

        if answer_match:
            if answer_match.group(1) == qa:
                return 1.0
        return 0.0

class TextInsensitiveRegex(Scorer):
    name: str = ScorerType.text_regex_insensitive.name
    description: str  = "Returns 1.0 if the case insensitive answer match the regex extraction"
    type: ScorerType = ScorerType.text_regex_insensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        mdl_answer = self._cleanup(model_answer.answer).lower()
        answer_match = re.search(self.regex, mdl_answer)
        qa = self._cleanup(question.answer).lower()

        if debug:
            print(answer_match, qa, mdl_answer)

        if answer_match:
            if answer_match.group(1) == qa:
                return 1.0
        return 0.0