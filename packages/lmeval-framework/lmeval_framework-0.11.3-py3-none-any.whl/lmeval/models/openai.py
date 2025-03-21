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

import os
from dotenv import load_dotenv
from ..media import Modality
from .litellm import LiteLLMModel
from litellm import check_valid_key

try:
    import openai
except ImportError:
    raise ImportError("To use OpenAI / ChatGPT please install dependencies with: pip install llmeval[openai]")

## subclasses per provider

class OpenAIModel(LiteLLMModel):
    def __init__(self,
                 api_key: str = "",
                 model_version: str = 'gpt-4o-mini'):

        modalities = [Modality.text, Modality.image, Modality.code, Modality.document]

        super().__init__(model_version=model_version,
                         litellm_model=model_version,  #not the same for other provider
                         modalities=modalities,
                         publisher="OpenAI")

        if not api_key:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError(f"OPENAI API key is required either pass it explicitly or set it in the environment variable 'OPENAI_API_KEY'")

        # check api key validity
        if not check_valid_key(model=model_version, api_key=api_key):
            raise ValueError(f"OPEN_AI_KEY API key is invalid")

        self.runtime_vars['api_key'] = api_key
