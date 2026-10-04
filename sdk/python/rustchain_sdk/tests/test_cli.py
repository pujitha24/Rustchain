# SPDX-License-Identifier: MIT
"""
Tests for the RustChain CLI argument parsing.
"""

import pytest
from click.testing import CliRunner

from rustchain_sdk import cli


@pytest.fixture
def sent(monkeypatch):
    calls = []

    async def fake_send(*args):
        calls.append(args)

    monkeypatch.setattr(cli, "_wallet_send", fake_send)
    return calls


def _send(amount, *opts):
    return CliRunner().invoke(
        cli.main, ["wallet", "send", "--seed", "a b", *opts, "--", "from", "to", amount]
    )


class TestWalletSendAmounts:
    def test_fractional_amount(self, sent):
        result = _send("0.5")
        assert result.exit_code == 0, result.output
        assert sent[0][2] == 0.5 and sent[0][3] == 0

    def test_fractional_fee(self, sent):
        result = _send("10.5", "--fee", "0.01")
        assert result.exit_code == 0, result.output
        assert sent[0][2] == 10.5 and sent[0][3] == 0.01

    def test_integer_amount_and_fee(self, sent):
        assert _send("1", "--fee", "1").exit_code == 0
        assert sent[0][2] == 1 and sent[0][3] == 1

    @pytest.mark.parametrize("amount", ["0", "-1"])
    def test_non_positive_amount_rejected(self, sent, amount):
        assert _send(amount).exit_code == 2
        assert not sent

    def test_negative_fee_rejected(self, sent):
        assert _send("1", "--fee", "-0.1").exit_code == 2
        assert not sent

    @pytest.mark.parametrize("value", ["nan", "inf", "-inf", "1e999"])
    def test_non_finite_rejected(self, sent, value):
        assert _send(value).exit_code == 2
        assert _send("1", "--fee", value).exit_code == 2
        assert not sent
