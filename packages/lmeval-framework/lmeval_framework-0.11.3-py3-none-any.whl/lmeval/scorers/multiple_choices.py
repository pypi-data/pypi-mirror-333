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

class ContainAnswerLettersInsensitive(Scorer):
    name: str = ScorerType.contains_answer_letters_insensitive.name
    description: str = "Returns a score between 0 and 1 based on the number of correct answer letters present in the model answer"
    type: ScorerType = ScorerType.contains_answer_letters_insensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        assert question.answer_letter is not None, "Answer letter is not provided - this is scorer can only be used with Multiple Choice question Prompts."

        # track mapping for later display
        model_answer.additional_data = question.letter_mapping

        qa = self._cleanup(question.answer_letter).lower().split(',')
        qa_len = len(qa)
        correct = 0

        ma = self._cleanup(model_answer.answer).lower() # don't split this one
        ma = ma.replace(' ', '').split(',') # a,b,c -> [a, b, c]
        ma_len = len(ma)

        # print(f"model answer: {ma}")
        # print(f"question answer: {qa}")

        if not qa:
            return 0.0

        for c in qa:
            c = c.strip()
            # print(f"'{c}' in '{ma}' -> {c in ma}")
            if c in ma:
                correct += 1
        # model has more answers than question
        # and penalize over answering
        numerator = max(ma_len, qa_len)
        return correct / numerator

class ContainAnswerLetterInsensitive(Scorer):
    name: str = ScorerType.contains_answer_letter_insensitive.name
    description: str  = "Returns 1.0 if the answer letter is present in the model answer"
    type: ScorerType = ScorerType.contains_answer_letter_insensitive
    modality: Modality = Modality.text

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        assert question.answer_letter is not None, "Answer letter is not provided - this is scorer can only be used with Multiple Choice question Prompts."

        # track mapping for later display
        model_answer.additional_data = question.letter_mapping

        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer_letter).lower()

        if qa and ma and qa in ma[0]:
            return 1.0
        else:
            return 0.0
