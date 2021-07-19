# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import torch
from parameterized import parameterized

from monai.transforms import ThresholdIntensityd
from tests.utils import TEST_NDARRAYS

TESTS = []
for p in TEST_NDARRAYS:
    TESTS.append(
        [
            p,
            {"keys": ["image", "label", "extra"], "threshold": 5, "above": True, "cval": 0},
            (0, 0, 0, 0, 0, 0, 6, 7, 8, 9),
        ]
    )
    TESTS.append(
        [
            p,
            {"keys": ["image", "label", "extra"], "threshold": 5, "above": False, "cval": 0},
            (0, 1, 2, 3, 4, 0, 0, 0, 0, 0),
        ]
    )
    TESTS.append(
        [
            p,
            {"keys": ["image", "label", "extra"], "threshold": 5, "above": True, "cval": 5},
            (5, 5, 5, 5, 5, 5, 6, 7, 8, 9),
        ]
    )


class TestThresholdIntensityd(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_value(self, in_type, input_param, expected_value):
        test_data = {"image": in_type(np.arange(10)), "label": in_type(np.arange(10)), "extra": in_type(np.arange(10))}
        result = ThresholdIntensityd(**input_param)(test_data)
        for k, v in result.items():
            if isinstance(result[k], torch.Tensor):
                result[k] = v.cpu()
        np.testing.assert_allclose(result["image"], expected_value)
        np.testing.assert_allclose(result["label"], expected_value)
        np.testing.assert_allclose(result["extra"], expected_value)


if __name__ == "__main__":
    unittest.main()
