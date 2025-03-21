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


# try:
#     import ollama
# except ImportError:
#     raise ImportError("To use ollama please install dependencies with: pip install llmeval[ollama]")



## subclasses per provider

class OllamaModel(LiteLLMModel):
    """
        Model names: https://ollama.com/library
        https://github.com/ollama/ollama

    Args:
        LiteLLMModel: _description_
    """

    def __init__(self,
                 model_version: str = "gemma2",
                 publisher: str = "Google",
                 endpoint: str = ""):



        modalities = [Modality.text, Modality.code]
        litellm_model = f'ollama_chat/{model_version}' # https://docs.litellm.ai/docs/providers/ollama#using-ollama-apichat
        publisher = model_version.split('-')[0].capitalize()
        super().__init__(model_version=model_version,
                         modalities=modalities,
                         publisher=publisher,
                         litellm_model=litellm_model)
