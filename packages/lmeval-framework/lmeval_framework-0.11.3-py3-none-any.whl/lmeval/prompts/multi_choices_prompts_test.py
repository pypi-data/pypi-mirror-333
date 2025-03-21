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

import pytest
from lmeval.prompts import MultiChoicesPrompt, MultiChoicesMultiAnswersPrompt
from lmeval import Question, Task, TaskType
from lmeval import get_scorer, ScorerType


def test_multi_choices_multi_answers():
    prompt = MultiChoicesMultiAnswersPrompt()
    question_text = "What is true about Paris"
    question = Question(id=1,
                        question=question_text,
                        answer="It is the capital of France",
                        additional_answers=["The Louvre is there",
                                            "The effeil tower is there"],
                        choices=["It is the capital of Portugal",
                                 "It is the capital of Germany",
                                 "The Guggenheim museum is there",
                                 "THe MoMa is there"])

    task = Task(name="Paris Info", type=TaskType.multiple_choices_multiple_answers,
                scorer=get_scorer(ScorerType.contains_answer_letters_insensitive))
    rendered_prompt =  prompt.render(question, task)
    print(prompt.template)
    print(rendered_prompt)

    assert question_text in rendered_prompt
    for choice in question.choices:
        assert choice in rendered_prompt
    for answer in question.answer:
        assert answer in rendered_prompt
    for c in  ['A', 'B', 'C', 'D', 'E']:
        assert f"\n{c}:" in rendered_prompt

    # check that the answer letter is tied to the correct answer

    assert f"{answer}" in rendered_prompt

    # check that the additional answers are in the prompt
    for additional_answer in question.additional_answers:
        assert additional_answer in rendered_prompt

    # check the mapping from letter to answer exist
    for letter, answer in question.letter_mapping.items():
        assert f"{letter}:{answer}" in rendered_prompt

def test_multi_choices_multi_answers_original_letters():
    prompt = MultiChoicesMultiAnswersPrompt(use_original_letters=True)
    question_text = "What is true about Paris"
    question = Question(id=1,
                        question=question_text,
                        answer="It is the capital of France",
                        additional_answers=["The Louvre is there",
                                            "The effeil tower is there"],
                        choices=["It is the capital of Portugal",
                                 "It is the capital of Germany",
                                 "The Guggenheim museum is there",
                                 "THe MoMa is there"],
                        original_letters=['G', 'F', 'E', 'D', 'C', 'B', 'A'])

    task = Task(name="Paris Info", type=TaskType.multiple_choices_multiple_answers,
                scorer=get_scorer(ScorerType.contains_answer_letters_insensitive))
    rendered_prompt =  prompt.render(question, task)
    print(prompt.template)
    print(rendered_prompt)

    assert question_text in rendered_prompt
    for choice in question.choices:
        assert choice in rendered_prompt
    for answer in question.answer:
        assert answer in rendered_prompt
    for c in  ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        assert f"\n{c}:" in rendered_prompt

    # check that the answer letter is tied to the correct answer

    assert f"{answer}" in rendered_prompt

    # check that the additional answers are in the prompt
    for additional_answer in question.additional_answers:
        assert additional_answer in rendered_prompt

    # check the mapping from letter to answer exist
    for letter, answer in question.letter_mapping.items():
        assert f"{letter}:{answer}" in rendered_prompt
    # test the original order is preserved
    for idx, answer in enumerate(
        [question.answer] + question.additional_answers + question.choices
    ):
        assert f"{question.original_letters[idx]}:{answer}"in rendered_prompt

def test_multi_choices():
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["London", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    rendered_prompt =  prompt.render(question, task)
    print(prompt.template)
    print(rendered_prompt)


    assert question_text in rendered_prompt
    for choice in question.choices:
        assert choice in rendered_prompt
    assert question.answer in rendered_prompt
    for c in  ['A', 'B', 'C', 'D']:
        assert f"\n{c}:" in rendered_prompt

    # check that the answer letter is tied to the correct answer
    assert f"{question.answer_letter}:{question.answer}" in rendered_prompt
    for letter, answer in question.letter_mapping.items():
        assert f"{letter}:{answer}" in rendered_prompt

def test_multi_choices_original_letters():
    prompt = MultiChoicesPrompt(use_original_letters=True)
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["London", "Berlin", "Madrid"],
                        original_letters=["D", "B", "A", "C"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    rendered_prompt =  prompt.render(question, task)
    print(prompt.template)
    print(rendered_prompt)


    assert question_text in rendered_prompt
    for choice in question.choices:
        assert choice in rendered_prompt
    assert question.answer in rendered_prompt
    for c in  ['A', 'B', 'C', 'D']:
        assert f"\n{c}:" in rendered_prompt

    # check that the answer letter is tied to the correct answer
    assert f"{question.answer_letter}:{question.answer}" in rendered_prompt
    for letter, answer in question.letter_mapping.items():
        assert f"{letter}:{answer}" in rendered_prompt
    # test the original order is preserved
    for idx, answer in enumerate([question.answer] + question.choices):
        assert f"{question.original_letters[idx]}:{answer}"in rendered_prompt

def test_repeated_used_multi_choices():
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["London", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))

    initial_answer_letter = ""
    for _ in range(5):
        rendered_prompt = prompt.render(question, task)
        print(prompt.template)
        print(rendered_prompt)

        if not initial_answer_letter:
            initial_answer_letter = question.answer_letter

        # check the order doesn't change
        assert question.answer_letter == initial_answer_letter

        assert question_text in rendered_prompt
        for choice in question.choices:
            assert choice in rendered_prompt
        assert question.answer in rendered_prompt
        for c in  ['A', 'B', 'C', 'D']:
            assert f"\n{c}:" in rendered_prompt

        # check that the answer letter is tied to the correct answer
        assert f"{question.answer_letter}:{question.answer}" in rendered_prompt

def test_answer_in_choice_fail():
    "Ensure that the generation fail if the answers is in the list of other choices"
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["Paris", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    with pytest.raises(AssertionError):
        prompt.render(question, task)
