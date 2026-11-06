# SPDX-License-Identifier: MIT

import pytest

import integrated_node

sybil_guard = integrated_node.sybil_guard


@pytest.mark.parametrize("bad", [None, "N/A", float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("state", ["probation", "grandfathered", "trusted"])
def test_enrollment_weight_rejects_non_finite_and_garbage(bad, state):
    assert sybil_guard.enrollment_weight(bad, {"state": state}) == 0.0


def test_enrollment_weight_finite_unchanged():
    assert sybil_guard.enrollment_weight(1.5, {"state": "grandfathered"}) == 1.5


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf"), "nan", "inf", None])
def test_epoch_weight_to_units_non_finite_is_zero(bad):
    assert integrated_node.epoch_weight_to_units(bad) == 0


def test_epoch_weight_to_units_finite():
    assert integrated_node.epoch_weight_to_units(1.0) == integrated_node.EPOCH_WEIGHT_SCALE
