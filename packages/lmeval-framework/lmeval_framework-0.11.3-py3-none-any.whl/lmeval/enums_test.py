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

from lmeval.enums import ScorerType, TaskType, TaskLevel, FileType


def test_scorer_type_consistency():
    for s in ScorerType:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)

def test_task_type_consistency():
    for s in TaskType:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)

def test_task_level_consistency():
    for s in TaskLevel:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)
