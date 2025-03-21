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

from lmeval import LMAnswer, LMModel
from lmeval import Task, Question, QuestionSource
from lmeval.enums import TaskType
from lmeval.scorers import Scorer

def eval_question_answer(real_answer: str, model_answer: str, scorer: Scorer) -> float:
    "boiler code to evaluate a question and answer pair with a given scorer"
    question = Question(id=0, answer = real_answer, question ='Is the sky red?', source = QuestionSource(name="demo", description="Demo question source"))
    task = Task(name="task demo", type=TaskType.boolean,
                scorer=scorer)

    mld = LMModel(name="demo", publisher='test', version_string="demo-1.0")
    mdl_answer = LMAnswer(answer=model_answer, raw_response=model_answer,
                          generation_time=1.0, model=mld)

    score = scorer.score(mdl_answer, question, task)
    return score
