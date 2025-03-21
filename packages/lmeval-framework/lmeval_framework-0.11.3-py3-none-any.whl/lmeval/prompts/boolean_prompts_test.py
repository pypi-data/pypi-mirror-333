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

from lmeval.prompts import TrueOrFalseAnswerPrompt
from lmeval import Question, Task, TaskType
from lmeval import get_scorer, ScorerType

def test_true_false():
    prompt = TrueOrFalseAnswerPrompt()
    question_text = "France is the capital of France?"
    question = Question(id=1, question=question_text, answer="True")
    task = Task(name="City capital", type=TaskType.boolean,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    rendered_prompt =  prompt.render(question, task)
    assert question_text in rendered_prompt
    assert 'false' in rendered_prompt.lower()

