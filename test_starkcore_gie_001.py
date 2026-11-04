import pytest
from starkcore_gie_001 import (
    Verdict,
    Health,
    propagate,
    enforce
)

def test_three_level_rejection_propagation():
    nodes = {
        "crypto-lib": {"verdict": Verdict.REJECT, "health": Health.HEALTHY},
        "service-api": {"verdict": Verdict.ACCEPT, "health": Health.DEGRADED},
        "application": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY}
    }
    edges = [
        ("crypto-lib", "service-api"),
        ("service-api", "application")
    ]
    result = propagate(nodes, edges)

    assert result["crypto-lib"]["verdict"] == "REJECT"
    assert result["service-api"]["verdict"] == "REJECT"
    assert result["application"]["verdict"] == "REJECT"

    # Degradation remains independently observable.
    assert result["service-api"]["degraded"] is True
    assert result["application"]["degraded"] is True

def test_escalate_propagates():
    nodes = {
        "dependency": {"verdict": Verdict.ESCALATE, "health": Health.HEALTHY},
        "consumer": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY}
    }
    result = propagate(nodes, [("dependency", "consumer")])
    assert result["consumer"]["verdict"] == "ESCALATE"

def test_reject_dominates_escalate():
    nodes = {
        "a": {"verdict": Verdict.ESCALATE, "health": Health.HEALTHY},
        "b": {"verdict": Verdict.REJECT, "health": Health.HEALTHY},
        "c": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY}
    }
    result = propagate(nodes, [("a", "c"), ("b", "c")])
    assert result["c"]["verdict"] == "REJECT"

def test_degraded_does_not_mean_escalate():
    nodes = {
        "a": {"verdict": Verdict.ACCEPT, "health": Health.DEGRADED},
        "b": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY}
    }
    result = propagate(nodes, [("a", "b")])
    assert result["b"]["verdict"] == "ACCEPT"
    assert result["b"]["degraded"] is True

def test_cycle_is_rejected():
    nodes = {
        "a": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY},
        "b": {"verdict": Verdict.ACCEPT, "health": Health.HEALTHY}
    }
    with pytest.raises(ValueError, match="CYCLE_DETECTED"):
        propagate(nodes, [("a", "b"), ("b", "a")])

def test_enforcer_blocks_rejected_nodes():
    result = enforce({
        "crypto-lib": {"verdict": "REJECT", "degraded": False},
        "application": {"verdict": "ACCEPT", "degraded": False}
    })
    assert result["crypto-lib"]["decision"] == "REJECT"
    assert result["application"]["decision"] == "ACCEPT"
