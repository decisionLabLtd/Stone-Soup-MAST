import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
from stonesoup.models.transition.linear import *
from stonesoup.platform.base import *
from stonesoup.types.groundtruth import *

from ReinforcementLearning.scripts.yaml_generator import generate_default_yaml
from ReinforcementLearning.utils.scenario_utils import _get_yaml_scenario


def test_yaml(scenario_config="ReinforcementLearning/configs/scenario_config.yaml"):
    """
    This function is run with pytest to perform checks on
    all the values generated by the scenario yaml generator.

    This includes checking the existence of required keys,
    such as the 'transiition_model', 'targets', sensor_manager,
    scenario_dimensions, etc.

    After this type checks are performed to make sure, the
    key values index expected variable types.


    """
    generate_default_yaml(scenario_config)

    scenario = _get_yaml_scenario(scenario_config)

    """
    Before any other tests are done on the data,
    existence checks are performed to make sure that
    all expected keys are present within the scenario
    dictionary.

    If a key is not present, an assertion error will
    be raised.
    """
    # Existence checks
    assert scenario.get("transition_model") is not None
    assert scenario.get("targets") is not None
    assert scenario.get("sensor_manager") is not None
    assert scenario["sensor_manager"].get("max_sensors_per_platform") is not None
    assert scenario["sensor_manager"].get("platform") is not None
    assert scenario.get("unknown_targets") is not None
    assert scenario.get("episode_threshold") is not None
    assert scenario.get("scenario_dimensions") is not None
    assert scenario.get("velocity_limit") is not None

    """
    These are type checks for making sure the keys index
    to the expected variable types.

    Some of these types are specfic and are subject to
    change as the framework becomes more dynamic and
    accepts more types.

    These are marked with inline comments saying
    "Strict test, can be updated"
    """
    # Strict test, can be updated
    assert isinstance(scenario["transition_model"], LinearModel)

    # Strict test, can be updated
    assert isinstance(scenario["targets"], list)

    # Strict test, can be updated
    for target in scenario["targets"]:
        assert isinstance(target, GroundTruthPath)

    assert isinstance(scenario["sensor_manager"], dict)
    assert isinstance(scenario["sensor_manager"]["max_sensors_per_platform"], int)
    assert isinstance(scenario["sensor_manager"]["platform"], MovingPlatform)
    assert isinstance(scenario["unknown_targets"], int)
    assert isinstance(scenario["episode_threshold"], int)
    assert isinstance(scenario["scenario_dimensions"], list)
    for dim in scenario["scenario_dimensions"]:
        assert isinstance(dim, int)
    assert isinstance(scenario.get("velocity_limit"), int)

    """
    These are range checks for making sure the
    values are within an expected range. This
    includes making sure values are greater than
    a certain while others are less than a certain number.

    For example, the velocity limit, should not be infinite.
    """
    assert scenario["unknown_targets"] < 5
    assert scenario["episode_threshold"] > 10
    for dim in scenario["scenario_dimensions"]:
        assert dim > 0
    assert scenario["velocity_limit"] < np.inf

    """
    These are length checks for maing sure lists are
    of an expected and acceptable size.

    For example, there must be at least 1 known
    target in the scenario.
    """
    assert len(scenario["targets"]) > 0
    assert len(scenario["scenario_dimensions"]) == 2

    """
    This has pre-condition requirements, meaning
    this test requires the above assertions to pass in
    order for it to function successfully.

    This loop checks to see if each target starts within the scenario dimensions.
    """
    # Strict test, can be updated
    for target in scenario["targets"]:
        assert target.states[0].state_vector[0] < scenario["scenario_dimensions"][
            0
        ] / 2 and target.states[0].state_vector[0] > -(
            scenario["scenario_dimensions"][0] / 2
        )
        assert target.states[0].state_vector[2] < scenario["scenario_dimensions"][
            1
        ] / 2 and target.states[0].state_vector[2] > -(
            scenario["scenario_dimensions"][1] / 2
        )
