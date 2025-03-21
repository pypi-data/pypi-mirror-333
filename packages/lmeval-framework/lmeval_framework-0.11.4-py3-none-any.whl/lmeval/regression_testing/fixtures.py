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

"""Fixture for regression tests."""

import pytest
import os
from dotenv import load_dotenv
from lmeval.models.gemini import GeminiModel


@pytest.fixture
def gemini() -> GeminiModel:
    "Gemini model fixture"
    load_dotenv()  # take environment variables from .env.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    model = GeminiModel(api_key=GEMINI_API_KEY)
    return model

@pytest.fixture
def gemini_pro15() -> GeminiModel:
    "Gemini model fixture"
    load_dotenv()  # take environment variables from .env.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    model = GeminiModel(api_key=GEMINI_API_KEY, model_version="gemini-1.5-pro")
    return model