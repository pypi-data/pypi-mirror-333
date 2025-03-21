# Copyright 2025 Google LLC
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

from dotenv import load_dotenv
from lmeval.models.httpmodel import SecLmModel
from .tests_utils import eval_single_text_generation, eval_batch_text_generation

load_dotenv()

def test_vertex_single_text_generation():
    eval_single_text_generation(SecLmModel())

def test_vertex_batch_text_generation():
    eval_batch_text_generation(SecLmModel())
