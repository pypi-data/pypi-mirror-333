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

from lmeval.prompts.text_generation_prompts import QuestionOnlyPrompt

def test_custom_prompt():
    name = "mycustom prompt"
    template = "this is a custom prompt - question: {{question}} -  answer: {{answer}}"
    prompt = QuestionOnlyPrompt(name=name, template=template)
    assert prompt.name == name
    assert prompt.template == template
