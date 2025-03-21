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


class TextExactSensitive(Scorer):
    name: str = ScorerType.text_exact_sensitive.name
    description: str  = "Returns 1.0 if the case-sensitive real answer and the model answer are exactly the same case sensitive"
    type: ScorerType = ScorerType.text_exact_sensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer)
        qa = self._cleanup(question.answer)

        if ma == qa:
            return 1.0
        else:
            return 0.0


class TextExactInsensitive(Scorer):
    name: str = ScorerType.text_exact_insensitive.name
    description: str  = "Returns 1.0 if the case-insensitive real answer and the model answer text are exactly the same"
    type: ScorerType = ScorerType.text_exact_insensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer).lower()

        if ma == qa:
            return 1.0
        else:
            return 0.0
