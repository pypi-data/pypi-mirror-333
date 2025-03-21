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

from .benchmark import Benchmark, Category, Task
from .question import Question
from .models import LMModel, LMAnswer
from .prompts import Prompt

class Callback():

    benchmark: Benchmark | None = None

    # called when the evaluation starts
    def on_evaluation_start(self, model: LMModel, prompt: Prompt) -> None:
        "Trigger when the evaluation starts"
        pass

    def on_evaluation_end(self, model: LMModel, prompt: Prompt) -> None:
        "Trigger when the evaluation ends"
        pass

    def on_category_start(self, category: Category) -> None:
        "Trigger when a category starts"
        pass

    def on_category_end(self, category: Category) -> None:
        "Trigger when a category ends"
        pass

    def on_task_start(self, task: Task) -> None:
        "Trigger when a task starts"
        pass

    def on_task_end(self, task: Task) -> None:
        "Trigger when a task ends"
        pass

    def on_question_start(self, question: Question, model: LMModel,
                          prompt: Prompt) -> None:
        "Trigger when a question starts"
        pass
    def on_question_end(self, question: Question, answer: LMAnswer,
                        model: LMModel, prompt: Prompt) -> None:
        "Trigger when a question ends"
        pass