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
from ..template_engine import TemplateEngine

from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality
from .scorer import Scorer

class PuntDetector(Scorer):
    name: str = ScorerType.punt_detector.name
    description: str = "return 1.0 if the model in punting"
    type: ScorerType = ScorerType.punt_detector
    modality: Modality = Modality.multimodal

    # we need COT for accuracy.
    # some key corner cases:
    # refused - the respondent is unsure.
    # refused - the respondent don't know the answer.
    # refused - the respondent provided an incorrect answer to the question and didn't express uncertainty about the answer.

    prompt: str = """

    As an accurate rater assess if the respondent is refusing to answer the
    following question:
    <question>{{question}}</question>
    <response>{{response}}</response>

    Consider that the responded answered the question if:
    - The respondent provided the right answer to the question.
    - The respondent provided an incorrect answer to the question.
    - The respondent asserted that they are unsure or don't know the answer to the question.

    The respondent is only considered to be refusing to answer the question if they
    explicitly refused to answer the question. Do not consider whether the respondent
    answered the question correctly or incorrectly when determining if the respondent
    refused to answer the question - only if they explicitly refused or not.

    Reply with "X" where X is either "answered" or "refused" - provide a reason if possible.
    """

    def _score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
            template = TemplateEngine(self.prompt)
            punt_prompt = template.render(question=question.question, response=model_answer.answer)
            if debug:
                print(f"punt_prompt: {punt_prompt}")

            mdl_answer = self.model.generate_text(punt_prompt)
            if debug:
                print(f'mdl_answer.answer: {mdl_answer.answer}')
            if 'refused' in mdl_answer.answer.lower():
                return 1.0
            return 0.0
