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
from .fixtures import gemini

def test_gemini_fixture(gemini):

    # check our model is working
    answer = gemini.generate_text('Say hello in french!')
    assert 'bonjour' in answer.answer.lower()
    assert not answer.iserror
    assert not answer.error_reason
    assert not answer.ispunting
    assert not answer.punting_reason
    assert answer.steps[0].execution_time > 0.1
    assert answer.score == 0.0  # no scoring yet
    assert 'gemini' in answer.model.name.lower()
    assert 'gemini' in answer.model.version_string.lower()
