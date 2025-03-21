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

from lmeval import LMModel
from lmeval.enums import Modality
def test_lmmodel():
    mdl = LMModel(name='test', publisher='publisher', modalities=[Modality.text])
    json = mdl.model_dump_json()
    mdl2 = LMModel.model_validate_json(json)
    assert Modality.text.value in mdl2.modalities
    assert len(mdl2.modalities) == 1