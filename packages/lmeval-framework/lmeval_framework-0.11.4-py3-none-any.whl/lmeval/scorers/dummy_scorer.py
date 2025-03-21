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

from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality
from .scorer import Scorer

class Always0Scorer(Scorer):
    name: str = ScorerType.always_0.name
    description: str = "Always return 0.0 as score."
    type: ScorerType = ScorerType.always_0
    modality: Modality = Modality.multimodal

    def _score(self, model_answer: LMAnswer, question: Question, task) -> float:
        return 0.0

class Always1Scorer(Scorer):
    name: str = ScorerType.always_1.name
    description: str = "Always return 1.0 as score."
    type: ScorerType = ScorerType.always_1
    modality: Modality = Modality.multimodal

    def _score(self, model_answer: LMAnswer, question: Question, task) -> float:
        return 1.0
