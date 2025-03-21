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

from lmeval import list_scorers, get_scorer
from lmeval import ScorerType
from lmeval.scorers import Always0Scorer
def test_list_scorers():
    list_scorers()  # just making sure it doesn't crash as it is a display function


def test_get_scorer():
    c = get_scorer(ScorerType.always_0)
    assert isinstance(c, Always0Scorer)