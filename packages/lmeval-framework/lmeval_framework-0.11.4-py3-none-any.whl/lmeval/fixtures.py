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
import pytest
import os
from dotenv import load_dotenv
from lmeval.models import lmmodel
from lmeval.models import mock_model
from typing import Dict, Union, Any

eu_countries = [
    ("Germany", "Berlin"),
    ("France", "Paris"),
    ("Italy", "Rome"),
    ("Spain", "Madrid"),
    ("Poland", "Warsaw"),
    ("Romania", "Bucharest"),
    ("Netherlands", "Amsterdam"),
    ("Belgium", "Brussels"),
    ("Greece", "Athens"),
    ("Portugal", "Lisbon"),
    ("Sweden", "Stockholm"),
    ("Czech Republic", "Prague"),
    ("Hungary", "Budapest"),
    ("Austria", "Vienna"),
    ("Denmark", "Copenhagen"),
    ("Finland", "Helsinki"),
    ("Ireland", "Dublin"),
    ("Croatia", "Zagreb"),
    ("Slovakia", "Bratislava"),
    ("Lithuania", "Vilnius")
]

def get_country_generation() -> Dict[str, Union[str, str]]:
    "Generate a random question about European country capitals."

    country, capital = random.choice(eu_countries)
    question = f"What is the capital of {country}?"
    return {"question": question, "answer": capital}



def get_country_boolean() -> Dict[str, Union[str, str]]:
    """
    Generate a random boolean question about European country capitals.

    Returns:
        Dict[str, Union[str, bool]]: A dictionary containing:
            - 'question' (str): The generated question.
            - 'answer' (bool): The correct answer (True or False).
    """
    country, capital = random.choice(eu_countries)
    is_true = random.choice([True, False])

    if is_true:
        question = f"Is {capital} the capital of {country}?"
        answer = True
    else:
        wrong_capital = random.choice([c for _, c in eu_countries if c != capital])
        question = f"Is {wrong_capital} the capital of {country}?"
        answer = False

    return {"question": question, "answer": str(answer)}

def get_country_multi_choice(num_choices: int = 4) -> Dict[str, Any]:
    """
    Generate a multiple-choice question about European country capitals.

    Args:
        num_choices (int, optional): Number of choices to generate. Defaults to 4.

    Raises:
        ValueError: If num_choices is less than 2 or greater than the number of countries.

    Returns:
        Dict[str, Union[str, List[str]]]: A dictionary containing:
            - 'question' (str): The generated question.
            - 'choices' (List[str]): List of possible answers.
            - 'correct_answer' (str): The correct capital.
    """
    if num_choices < 2:
        raise ValueError("Number of choices must be at least 2")

    if num_choices > len(eu_countries):
        raise ValueError(f"Number of choices cannot exceed {len(eu_countries)}")

    country, correct_capital = random.choice(eu_countries)

    wrong_capitals = random.sample([c for _, c in eu_countries if c != correct_capital], num_choices - 1)
    random.shuffle(wrong_capitals)

    question = f"Which of the following cities is the capital of {country}?"

    return {
        "question": question,
        "choices": wrong_capitals,
        "answer": correct_capital
    }


@pytest.fixture
def gemini_mock() -> lmmodel.LMModel:
  return mock_model.MockGeminiModel(model_version="gemini-1.5-flash-001")


@pytest.fixture
def gemini_pro15_mock() -> lmmodel.LMModel:
  return mock_model.MockGeminiModel(model_version="gemini-1.5-pro-001")