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

import random
from string import ascii_uppercase
from ..template_engine import TemplateEngine
from ..question import Question
from ..task import Task
from .prompt import Prompt
from ..enums import TaskType

MULTI_ANSWER_TEMPLATE = """
        Accurately answer the following question:

        {{question.question}}

        Choices:
        {{question.multi_choices}}

        Instructions:
        - Carefully read the question and all options.
        - Select all the correct answers.
        - Respond ONLY with the letters ({{question.letters}}) corresponding to the correct answers.
        - Do not include any explanations, additional text, or punctuation in your response.
        - If there are multiple correct answers, separate them with a comma (,). For example "A, B, C".
        Your answer ({{question.letters}}):
    """


class MultiChoicesMultiAnswersPrompt(Prompt):
    use_original_letters: bool = False

    def __init__(self,
                template: str = MULTI_ANSWER_TEMPLATE,
                name: str = "Multi Choices Multi Answer Picker",
                description: str = "Ask the model to return the letters associated with potentially multiple correct answers",
                task_type = TaskType.multiple_choices_multiple_answers,
                url: str = '',
                version: str = '1.0',
                use_original_letters: bool = False):

            super().__init__(name=name, description=description,
                            task_type=task_type, template=template, url=url,
                            version=version)
            self.use_original_letters = use_original_letters

    def render(self, question: Question, task: Task) -> str:
        "Render prompt for a given question and task"

        if task.type != self.task_type:
            raise ValueError(f"Task type {task.type} does not match prompt task type {self.task_type}")

        assert question.answer not in question.choices, f"Answer {question.answer} should not be in other choices. {question.choices}"


        version = self.version_string()

        if version in question.prompt_cache:
            question.multi_choices = question.prompt_cache[version]['multi_choices']
            question.letters = question.prompt_cache[version]['letters']
            question.answer_letter = question.prompt_cache[version]['answer_letter']
            question.letter_mapping = question.prompt_cache[version]['letter_mapping']
        else:
            possible_answers = [question.answer] + question.additional_answers +  question.choices
            if self.use_original_letters:
                assert len(possible_answers) == len(question.original_letters), f"Original letters {question.original_letters} should match the number of possible answers {possible_answers}"
            else:    
                random.shuffle(possible_answers)

            # Construct the list of possible answers
            choices_list = []
            letters_list = []
            letter_mapping = {}
            correct_letters = []
            for idx, answer in enumerate(possible_answers):
                letter = question.original_letters[idx] if self.use_original_letters else ascii_uppercase[idx]
                # don't put space between letter and answer it decrease accuracy...
                choices_list.append(f"{letter}:{answer}")
                letters_list.append(letter)
                letter_mapping[letter] = answer

                # mark the answer and additional answers as correct
                if answer == question.answer:
                    correct_letters.append(letter)
                if answer in question.additional_answers:
                    correct_letters.append(letter)
            if self.use_original_letters:
                choices_list.sort()
                letters_list.sort()
                correct_letters.sort()

            question.answer_letter = ', '.join(correct_letters)

            # flatten
            multi_choices = "\n".join(choices_list)
            letters = ', '.join(letters_list)

            # assign to the current question
            question.multi_choices = multi_choices
            question.letters = letters
            question.letter_mapping = letter_mapping

            # store assignements for reuse accross models to have the exact same question
            question.prompt_cache[version] = {
                'multi_choices': multi_choices,
                'letters': letters,
                'answer_letter': question.answer_letter,
                'letter_mapping': letter_mapping
            }

        # render full template
        template = TemplateEngine(self.template)
        return template.render(question=question, task=task)


TEMPLATE = """
        Accurately answer the following question:

        {{question.question}}

        Choices:
        {{question.multi_choices}}

        Instructions:
        - Carefully read the question and all options.
        - Select the single most correct answer.
        - Respond ONLY with the letter ({{question.letters}}) corresponding to the correct answer.
        - Do not include any explanations, additional text, or punctuation in your response.

        Your answer ({{question.letters}}):
    """


class MultiChoicesPrompt(Prompt):
    use_original_letters: bool = False

    def __init__(self,
                template: str = TEMPLATE,
                name: str = "Multi Choices Picker",
                description: str = "Ask the model to return the letter associated with the correct answer",
                task_type = TaskType.multiple_choices,
                url: str = '',
                version: str = '1.0',
                use_original_letters: bool = False):

            super().__init__(name=name, description=description,
                            task_type=task_type, template=template, url=url,
                            version=version)
            self.use_original_letters = use_original_letters

    def render(self, question: Question, task: Task) -> str:
        "Render prompt for a given question and task"

        if task.type != self.task_type:
            raise ValueError(f"Task type {task.type} does not match prompt task type {self.task_type}")

        assert question.answer not in question.choices, f"Answer {question.answer} should not be in other choices. {question.choices}"

        version = self.version_string()

        if version in question.prompt_cache:
            question.multi_choices = question.prompt_cache[version]['multi_choices']
            question.letters = question.prompt_cache[version]['letters']
            question.answer_letter = question.prompt_cache[version]['answer_letter']
            question.letter_mapping = question.prompt_cache[version]['letter_mapping']
        else:
            possible_answers = [question.answer] + question.choices
            if self.use_original_letters:
                assert len(possible_answers) == len(question.original_letters), f"Original letters {question.original_letters} should match the number of possible answers {possible_answers}"
            else:    
                random.shuffle(possible_answers)

            # Construct the list of possible answers
            choices_list = []
            letters_list = []
            letter_mapping = {}
            for idx, answer in enumerate(possible_answers):
                letter = question.original_letters[idx] if self.use_original_letters else ascii_uppercase[idx]
                # don't put space between letter and answer it decrease accuracy...
                choices_list.append(f"{letter}:{answer}")
                letters_list.append(letter)
                letter_mapping[letter] = answer
                if answer == question.answer:
                    question.answer_letter = letter
            if self.use_original_letters:
                choices_list.sort()
                letters_list.sort()

            # flatten
            multi_choices = "\n".join(choices_list)
            letters = ', '.join(letters_list)

            # assign to the current question
            question.multi_choices = multi_choices
            question.letters = letters
            question.letter_mapping = letter_mapping

            # store assignements for reuse accross models to have the exact same question
            question.prompt_cache[version] = {
                'multi_choices': multi_choices,
                'letters': letters,
                'answer_letter': question.answer_letter,
                'letter_mapping': letter_mapping
            }

        # render full template
        template = TemplateEngine(self.template)
        return template.render(question=question, task=task)