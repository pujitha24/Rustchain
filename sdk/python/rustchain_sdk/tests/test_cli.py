# SPDX-License-Identifier: MIT
"""Tests for the `rustchain wallet balance` CLI output."""

from unittest.mock import AsyncMock, patch

from click.testing import CliRunner

from rustchain_sdk import cli


def _run(payload):
    client = AsyncMock()
    client.__aenter__.return_value = client
    client.get_balance.return_value = payload
    with patch.object(cli, "RustChainClient", return_value=client):
        return CliRunner().invoke(cli.main, ["wallet", "balance", "addr"])


def test_canonical_amount_rtc():
    result = _run({"amount_i64": 21000000, "amount_rtc": 21, "miner_id": "addr"})
    assert result.exit_code == 0
    assert "Balance:  21 RTC" in result.output


def test_zero_amount_rtc_is_not_unavailable():
    result = _run({"amount_rtc": 0})
    assert "Balance:  0 RTC" in result.output


def test_legacy_balance_alias_and_nonce():
    result = _run({"balance": 42, "nonce": 3})
    assert "Balance:  42 RTC" in result.output
    assert "Nonce:    3" in result.output


def test_missing_balance_is_unavailable_not_zero():
    result = _run({"miner_id": "addr"})
    assert "unavailable" in result.output
    assert "0 RTC" not in result.output
