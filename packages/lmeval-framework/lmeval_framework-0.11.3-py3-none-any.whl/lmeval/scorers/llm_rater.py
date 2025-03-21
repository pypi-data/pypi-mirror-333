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

import json
from string import Template
from pydantic import Field
from typing_extensions import override

from ..enums import Modality, ScorerType
from ..logger import log
from ..models import LMAnswer
from ..question import Question
from .scorer import Scorer

DEFAULT_RATER_TEMPLATE = Template('''
You are an impartial evaluator whose job is to determine if two sets of answer to a question are equivalent.
The question is this:

<question>
$question
</question>

Here are two sets of answers:

<answer1>
$expected
</answer1>

<answer2>
$actual
</answer2>

Rate on the scale from 0.0 to 1.0 how similar answer1 is to answer2.  Here 0.0 means they are completely different
and 1.0 means they are semantically equivalent. Here are some rubrics to help you:

1. Using the question as the context, list all the relevant facts from answer1 and compare them with the facts
presented in answer2 to see if they are the equivalent. 
2. Do both answers come to the same conclusion?
3. Do not consider stylistic differences such as the tone, the writing presentation (for instance bullet points vs paragraph).

Write your rating and reasoning for the rateing in json format 
like this:
 
 {
    "score": the rating score between 0 and 1,
    "reasoning": explain how you arrived at this rating
 }
 
''')


def _parse_response_as_json(val:str):
    jline = val.split('\n')
    start = 1 if jline[0].startswith("```") else 0
    end = -1 if jline[-1].startswith("```") else len(jline)
    j = '\n'.join(jline[start:end])
    return json.loads(j)


class LLMRater(Scorer):
    """A scorer using a LLM to rate the similiarity between the expected and actual answers.
    """
    class Config:
        arbitrary_types_allowed = True  # to enable Template as an attribute
    name: str = ScorerType.llm_rater.name
    description: str = 'Calling a model to rate the answer on the scale from 0 to 1'
    type: ScorerType = ScorerType.llm_rater
    modality: Modality = Modality.text  # assume text for now
    # The template is expect to have 3 parmeters: $question, $expectd, $actual. $question
    # is the question asked, expected is the right answer and actual is the received answer.
    # The prompt shoudl return JSON with a field "rating"
    rater_prompt_template: Template = DEFAULT_RATER_TEMPLATE
    temperature: float = Field(default=0.0)
    max_tokens: int = Field(default=4096)

    @override
    def _score(self,
               model_answer: LMAnswer,
               question: Question,
               task,
               debug: bool = False) -> float:
        # if model for the class is set, use it, else use the model from the answer
        model = self.model if self.model else model_answer.model
        assert model  # must have a model
        prompt = self.rater_prompt_template.safe_substitute(
            question=question.question,
            expected=question.answer,
            actual=model_answer.answer)
        ans = model.generate_text(prompt=prompt,
                                  temperature=self.temperature,
                                  max_tokens=self.max_tokens)
        if ans.iserror:
            log.error('Rater failed with error %s', ans.error_reason)
            return -1.0
        if ans.ispunting:
            log.error('Rater punted')
            return 0.0
        try:
            jans = _parse_response_as_json(ans.answer)
            score = jans.get('score', None)
            assert score is not None
            return score
        except Exception as e:  # pylint: disable=broad-except
            log.error('Rater json parsing failed: ans = %s, exception = %s',
                      ans.answer, e)
            return -1.0
