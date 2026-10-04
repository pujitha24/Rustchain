# SPDX-License-Identifier: MIT
"""
Tests for the documented `node status` / `epoch info` CLI invocations.
"""

import pytest
from click.testing import CliRunner

from rustchain_sdk import cli


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    async def fake_node(node, as_json):
        recorded.append(("node", node, as_json))

    async def fake_epoch(node, as_json):
        recorded.append(("epoch", node, as_json))

    monkeypatch.setattr(cli, "_node_status", fake_node)
    monkeypatch.setattr(cli, "_epoch_info", fake_epoch)
    return recorded


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["node", "status"], "node"),
        (["node"], "node"),
        (["epoch", "info"], "epoch"),
        (["epoch"], "epoch"),
    ],
)
def test_documented_commands_reach_callback(calls, argv, expected):
    result = CliRunner().invoke(cli.main, argv)
    assert result.exit_code == 0, result.output
    assert [c[0] for c in calls] == [expected]


def test_unknown_action_rejected(calls):
    result = CliRunner().invoke(cli.main, ["node", "bogus"])
    assert result.exit_code == 2
    assert not calls
