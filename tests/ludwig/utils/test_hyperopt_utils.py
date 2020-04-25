# -*- coding: utf-8 -*-
# Copyright (c) 2019 Uber Technologies, Inc.
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
# ==============================================================================
import pytest
import numpy as np
from ludwig.utils.hyperopt_utils import GridStrategy, RandomStrategy


HYPEROPT_PARAMS = {
    "test_1": {
        "params": {
            "training.learning_rate": {
                "type": "float",
                "low": 0.0001,
                "high": 0.1,
                "steps": 4,
                "scale": "log"
            },
            "combiner.num_fc_layers": {
                "type": "int",
                "low": 0,
                "high": 4
            },
            "utterance.cell_type": {
                "type": "category",
                "values": ["rnn", "gru", "lstm"]
            }
        },
        "expected_search_space": {
            'training.learning_rate': [0.0001, 0.001, 0.01, 0.1],
            'combiner.num_fc_layers': [0, 4],
            'utterance.cell_type': ['rnn', 'gru', 'lstm']
        },
        "goal": "minimize",
        "expected_len_grids": 24,
        "num_samples": 10
    },
    "test_2": {
        "params": {
            "training.learning_rate": {
                "type": "float",
                "low": 0.001,
                "high": 0.1,
                "steps": 4,
                "scale": "linear"
            },
            "combiner.num_fc_layers": {
                "type": "int",
                "low": 2,
                "high": 6,
                "steps": 3
            }
        },
        "expected_search_space": {
            "training.learning_rate": [0.001, 0.034, 0.067, 0.1],
            "combiner.num_fc_layers": [2, 4, 6]
        },
        "goal": "maximize",
        "expected_len_grids": 12,
        "num_samples": 5
    }
}


@pytest.mark.parametrize('key', ['test_1', "test_2"])
def test_grid_strategy(key):

    hyperopt_test_params = HYPEROPT_PARAMS[key]
    goal = hyperopt_test_params["goal"]
    grid_strategy_params = hyperopt_test_params["params"]

    grid_strategy = GridStrategy(goal=goal, parameters=grid_strategy_params)

    search_space_dict = {}

    for key, values in grid_strategy.search_space.items():
        if isinstance(values, np.ndarray):
            values = values.tolist()
        search_space_dict[key] = values

    actual_params_keys = grid_strategy.sample().keys()
    expected_params_keys = search_space_dict.keys()

    assert actual_params_keys == expected_params_keys
    assert search_space_dict == hyperopt_test_params["expected_search_space"]
    assert len(
        grid_strategy.samples) == hyperopt_test_params["expected_len_grids"]


@pytest.mark.parametrize('key', ['test_1', "test_2"])
def test_random_strategy(key):

    hyperopt_test_params = HYPEROPT_PARAMS[key]
    goal = hyperopt_test_params["goal"]
    random_strategy_params = hyperopt_test_params["params"]
    num_samples = hyperopt_test_params["num_samples"]

    random_strategy = RandomStrategy(
        goal=goal, parameters=random_strategy_params, num_samples=num_samples)

    actual_params_keys = random_strategy.sample().keys()
    expected_params_keys = hyperopt_test_params["params"].keys()

    assert actual_params_keys == expected_params_keys
    assert len(random_strategy.samples) == num_samples
