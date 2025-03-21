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

from collections.abc import Generator
import time
from typing import Optional, Tuple
from litellm import completion, completion_cost, batch_completion
from litellm import ModelResponse, CustomStreamWrapper

from ..enums import Modality
from .lmmodel import LMModel
from .lmmodel import LMAnswer
from ..media import Media
from ..logger import log


class LiteLLMModel(LMModel):
    """
    Documentation at: https://docs.litellm.ai/
    """

    def __init__(self,
                 model_version: str,
                 litellm_model: str,
                 publisher: str,
                 modalities: list[Modality] = [Modality.text],
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 max_workers: Optional[int] = 20,
                 benchmark_name: str = "unknown"):
        """Init a LiteLLMModel compatible model

        Args:
            model_version: the name of the model as stored in the benchmark
            litellm_model: the internal name used by litellm
            publisher: the publisher name of the model as stored in the benchmark
            modalities: Which modality are supported by the model. Defaults to [Modality.text].
            base_url: Custom hosted endpoint. Defaults to "".
            api_key: Model API key. Defaults to "".
            max_workers: Number of workers to use for batch completion. Defaults to 100 (Litellm default).
        """

        # clean up the name
        name = ' '.join(model_version.split('-'))
        name = name.lower()

        super().__init__(name=name,
                         publisher=publisher,
                         version_string=model_version,
                         modalities=modalities)

        # store the litellm version name to call it in completions
        self.runtime_vars['litellm_version_string'] = litellm_model
        self.runtime_vars['api_key'] = api_key
        self.runtime_vars['base_url'] = base_url
        self.runtime_vars['is_custom'] = True if base_url else False
        self.runtime_vars['max_workers'] = max_workers
        self.runtime_vars['benchmark_name'] = benchmark_name

    def batch_generate_text(
            self,
            prompts: list[str],
            medias: list[list[Media]],
            temperature: float = 0,
            max_tokens: int = 4096,
            completions: int = 1
    ) -> Generator[Tuple[int, LMAnswer], None, None]:
        model = self.runtime_vars['litellm_version_string']
        assert len(prompts) == len(
            medias), "prompts and medias should have the same length"
        messages_batch = []
        for i, (prompt, media) in enumerate(zip(prompts, medias)):
            messages_batch.append(self._make_messages(prompt, media))

        try:
            batch_responses = self._batch_completion(model, messages_batch,
                                                     temperature, max_tokens,
                                                     completions)
        except:
            batch_responses = [None for _ in prompts]

        for i, resp in enumerate(batch_responses):
            answer = self._make_answer(resp, prompts[i])
            yield i, answer

    def generate_text(self,
                      prompt: str,
                      medias: list[Media] | Media | None = None,
                      temperature: float = 0.0,
                      max_tokens: int = 4096,
                      completions: int = 1) -> LMAnswer:
        # FIXME: finish multi-completion support
        model = self.runtime_vars['litellm_version_string']
        messages = self._make_messages(prompt, medias)

        try:
            resp = self._completion(model=model,
                                    messages=messages,
                                    temperature=temperature,
                                    max_tokens=max_tokens,
                                    completions=completions)
        except Exception as e:
            resp = None
            print("Can't get response from model:", e)

        answer = self._make_answer(resp, prompt)
        return answer

    def _make_messages(
            self,
            prompt: str,
            medias: list[Media] | Media | None = None) -> list[dict]:
        "build the message to send to the model"
        if medias is None:
            medias = []
        # boxing medias if needed
        if not isinstance(medias, list):
            medias = [medias]

        # build request
        content = []

        # ! some text model struggle with arrays of message so we have to do a if
        if len(medias) > 0:
            # process media files
            for media in medias:
                # image
                if media.modality == Modality.image.value:
                    # FIXME use llmlite
                    image_base64 = self._img2base64(media.content)
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url":
                            f"data:image/{media.filetype};base64,{image_base64}"
                        }
                    })

            # text prompt
            content.append({"type": "text", "text": prompt})
            return [{"role": "user", "content": content}]
        else:
            # for model that don't support complex messages structure
            return [{"role": "user", "content": prompt}]

    def _make_answer(self,
                     resp: ModelResponse | CustomStreamWrapper | Exception
                     | None,
                     prompt: str = "") -> LMAnswer:
        iserror = False
        error_reason = ""
        raw_response = ""
        cost = total_tokens = prompt_tokens = completion_tokens = 0
        total_time = 0
        model_name = self.runtime_vars['litellm_version_string']
        response_id = ""

        if isinstance(resp, ModelResponse):
            response = resp
            response_id = resp.id

            log.debug("response: %s", response)
            try:
                raw_response = response.choices[0].message.content
            except Exception as e:
                try:
                    iserror = True
                    error_reason = f"{error_reason} - {repr(response)} - {(e)}"
                except Exception as f:
                    iserror = True
                    error_reason = f"{error_reason} - {f}"
            total_time = time.time() - response.created
            if not iserror:
                try:
                    # compute cost for known models
                    if not self.runtime_vars['is_custom']:
                        try:
                            cost = completion_cost(response)
                        except Exception as e:
                            cost = 0
                            msg = f"Failed to get cost for model: {model_name}, error: {e}"
                            log.error(msg)
                except Exception as e:
                    msg = f"Failed to get cost for model: {model_name}, error: {e}"
                    log.error(msg)
                try:
                    total_tokens = response.usage.total_tokens
                    prompt_tokens = response.usage.prompt_tokens
                    completion_tokens = response.usage.completion_tokens
                except Exception as e:
                    msg = f"Failed to get usage from response for {model_name}, error: {e}"
                    log.error(msg)
            else:
                iserror = True
                error_reason = f'{resp}'
                raw_response = ''
        elif isinstance(resp, Exception):
            iserror = True
            error_reason = repr(resp)
        elif resp is None:
            iserror = True
            error_reason = "Batch completion failed."
        else:
            iserror = True
            error_reason = "Not implemented"

        answer = self._build_answer(text=raw_response,
                                    generation_time=total_time,
                                    iserror=iserror,
                                    error_reason=error_reason,
                                    cost=cost,
                                    total_tokens=total_tokens,
                                    completion_tokens=completion_tokens,
                                    prompt_tokens=prompt_tokens,
                                    isunsafe=self.isunsafe,
                                    prompt=prompt,
                                    id=response_id)
        return answer

    def _batch_completion(self,
                          model: str,
                          messages_batch: list[dict],
                          temperature: float = 0.0,
                          max_tokens: int = 4096,
                          completions: int = 1) -> list[ModelResponse]:

        #! we need to isolate the batch completion to allow various implementation to pass additonals parameters
        batch_responses = batch_completion(
            model=model,
            messages=messages_batch,
            temperature=temperature,
            max_tokens=max_tokens,
            n=completions,
            api_key=self.runtime_vars.get('api_key'),
            base_url=self.runtime_vars.get('base_url'),
            max_workers=self.runtime_vars.get('max_workers'),
            extra_headers=self._make_headers())
        return batch_responses

    def _completion(self,
                    model: str,
                    messages: list[dict],
                    temperature: float = 0.0,
                    max_tokens: int = 4096,
                    completions: int = 1) -> ModelResponse:
        #! we need to isolate the batch completion to allow various implementation to pass additonals parameters
        resp = completion(model=model,
                          messages=messages,
                          temperature=temperature,
                          max_tokens=max_tokens,
                          n=completions,
                          api_key=self.runtime_vars.get('api_key'),
                          base_url=self.runtime_vars.get('base_url'),
                          extra_headers=self._make_headers())
        return resp

    def _make_headers(self) -> dict[str, str]:
        headers = {
            'x-lmeval-benchmark': self.runtime_vars['benchmark_name'],
        }
        return headers